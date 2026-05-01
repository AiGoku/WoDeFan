import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "wodefam.db")

async def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
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
        await db.commit()
