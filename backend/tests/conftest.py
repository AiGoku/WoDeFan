import pytest
import pytest_asyncio
import aiosqlite
import sys
import os
from httpx import AsyncClient, ASGITransport

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app
from models.database import get_db

# 测试用内存数据库
TEST_DB_PATH = ":memory:"

# 测试菜品数据
TEST_DISHES = [
    {
        "name": "番茄炒蛋",
        "category": "hot_dish",
        "price": 18.0,
        "image_url": "/static/images/tomato_egg.jpg",
        "description": "经典家常菜",
        "season_tag": "spring"
    },
    {
        "name": "凉拌黄瓜",
        "category": "cold_dish",
        "price": 12.0,
        "image_url": "/static/images/cucumber.jpg",
        "description": "清爽开胃",
        "season_tag": "summer"
    },
    {
        "name": "酸辣汤",
        "category": "soup",
        "price": 15.0,
        "image_url": "/static/images/soup.jpg",
        "description": "酸辣可口",
        "season_tag": "winter"
    }
]

@pytest_asyncio.fixture
async def test_db():
    """创建测试用内存数据库"""
    db = await aiosqlite.connect(TEST_DB_PATH)
    db.row_factory = aiosqlite.Row

    # 创建表
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 0,
            image_url TEXT DEFAULT '',
            description TEXT DEFAULT '',
            season_tag TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            share_code TEXT UNIQUE NOT NULL,
            creator_openid TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            dish_id INTEGER NOT NULL,
            dish_name TEXT NOT NULL,
            dish_price REAL NOT NULL,
            dish_image TEXT DEFAULT '',
            added_by_openid TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        );

        CREATE INDEX IF NOT EXISTS idx_dishes_category ON dishes(category);
        CREATE INDEX IF NOT EXISTS idx_dishes_season ON dishes(season_tag);
        CREATE INDEX IF NOT EXISTS idx_orders_share_code ON orders(share_code);
        CREATE INDEX IF NOT EXISTS idx_orders_creator ON orders(creator_openid);
        CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
    """)

    # 插入测试数据
    for dish in TEST_DISHES:
        await db.execute(
            "INSERT INTO dishes (name, category, price, image_url, description, season_tag) VALUES (?, ?, ?, ?, ?, ?)",
            (dish["name"], dish["category"], dish["price"], dish["image_url"], dish["description"], dish["season_tag"])
        )
    await db.commit()

    yield db

    await db.close()

@pytest_asyncio.fixture
async def client(test_db):
    """创建测试客户端"""
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
