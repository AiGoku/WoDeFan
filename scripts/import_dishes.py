"""
菜品数据导入脚本
将菜品数据导入到 SQLite 数据库
用法: python scripts/import_dishes.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "data", "wodefam.db")

DISHES = [
    # 凉菜
    {"name": "拍黄瓜", "category": "cold_dish", "price": 12, "image_url": "", "description": "清爽开胃的经典凉菜，夏日必备", "season_tag": "summer"},
    {"name": "凉拌木耳", "category": "cold_dish", "price": 15, "image_url": "", "description": "爽脆可口的凉拌菜，富含膳食纤维", "season_tag": ""},
    {"name": "皮蛋豆腐", "category": "cold_dish", "price": 18, "image_url": "", "description": "经典家常凉菜，口感细腻", "season_tag": "summer"},
    {"name": "口水鸡", "category": "cold_dish", "price": 28, "image_url": "", "description": "麻辣鲜香的川味凉菜，让人垂涎", "season_tag": ""},
    {"name": "蒜泥白肉", "category": "cold_dish", "price": 25, "image_url": "", "description": "蒜香浓郁的传统凉菜", "season_tag": ""},
    {"name": "凉拌三丝", "category": "cold_dish", "price": 16, "image_url": "", "description": "清脆爽口的多丝凉拌", "season_tag": "summer"},
    {"name": "五花肉冻", "category": "cold_dish", "price": 22, "image_url": "", "description": "Q弹爽滑的传统肉冻", "season_tag": "winter"},
    {"name": "糖醋莲藕", "category": "cold_dish", "price": 18, "image_url": "", "description": "酸甜脆爽的开胃小菜", "season_tag": "autumn"},
    # 热菜
    {"name": "番茄炒蛋", "category": "hot_dish", "price": 16, "image_url": "", "description": "国民家常菜，酸甜下饭", "season_tag": "spring"},
    {"name": "宫保鸡丁", "category": "hot_dish", "price": 28, "image_url": "", "description": "经典川菜，花生酥脆鸡肉嫩滑", "season_tag": ""},
    {"name": "鱼香肉丝", "category": "hot_dish", "price": 26, "image_url": "", "description": "酸甜微辣的下饭菜，没有鱼的鱼香", "season_tag": ""},
    {"name": "红烧肉", "category": "hot_dish", "price": 38, "image_url": "", "description": "肥而不腻的经典硬菜，入口即化", "season_tag": "spring"},
    {"name": "麻婆豆腐", "category": "hot_dish", "price": 22, "image_url": "", "description": "麻辣鲜香的川菜代表", "season_tag": ""},
    {"name": "清蒸鲈鱼", "category": "hot_dish", "price": 48, "image_url": "", "description": "鲜嫩可口的清蒸鱼，原汁原味", "season_tag": "spring"},
    {"name": "糖醋排骨", "category": "hot_dish", "price": 35, "image_url": "", "description": "酸甜可口的传统名菜", "season_tag": ""},
    {"name": "水煮牛肉", "category": "hot_dish", "price": 42, "image_url": "", "description": "麻辣鲜香的川味硬菜", "season_tag": ""},
    {"name": "干煸四季豆", "category": "hot_dish", "price": 20, "image_url": "", "description": "干香入味的家常菜", "season_tag": ""},
    {"name": "回锅肉", "category": "hot_dish", "price": 30, "image_url": "", "description": "川菜之首，肥而不腻", "season_tag": ""},
    {"name": "清炒西兰花", "category": "hot_dish", "price": 18, "image_url": "", "description": "清淡健康的快手菜", "season_tag": ""},
    {"name": "鸡蛋羹", "category": "hot_dish", "price": 12, "image_url": "", "description": "嫩滑如布丁的蒸蛋", "season_tag": ""},
    {"name": "红烧冬瓜", "category": "hot_dish", "price": 16, "image_url": "", "description": "软糯入味的素菜硬菜", "season_tag": "summer"},
    {"name": "炒牛肉", "category": "hot_dish", "price": 35, "image_url": "", "description": "嫩滑多汁的快炒牛肉", "season_tag": ""},
    # 汤羹
    {"name": "紫菜蛋花汤", "category": "soup", "price": 10, "image_url": "", "description": "简单清淡的家汤，百搭之选", "season_tag": ""},
    {"name": "番茄蛋汤", "category": "soup", "price": 12, "image_url": "", "description": "酸甜开胃的家常汤", "season_tag": "spring"},
    {"name": "冬瓜排骨汤", "category": "soup", "price": 32, "image_url": "", "description": "清热消暑的滋补汤", "season_tag": "summer"},
    {"name": "酸辣汤", "category": "soup", "price": 15, "image_url": "", "description": "酸辣开胃的经典汤品", "season_tag": "winter"},
    {"name": "玉米浓汤", "category": "soup", "price": 18, "image_url": "", "description": "香甜浓郁的西式汤品", "season_tag": ""},
    {"name": "萝卜排骨汤", "category": "soup", "price": 28, "image_url": "", "description": "清甜滋补的家常炖汤", "season_tag": "winter"},
    {"name": "冬瓜虾仁汤", "category": "soup", "price": 22, "image_url": "", "description": "鲜美清爽的虾仁汤", "season_tag": "summer"},
    {"name": "三鲜汤", "category": "soup", "price": 25, "image_url": "", "description": "鲜美可口的多料汤", "season_tag": ""},
    # 主食
    {"name": "蛋炒饭", "category": "staple", "price": 15, "image_url": "", "description": "粒粒分明的经典炒饭", "season_tag": ""},
    {"name": "阳春面", "category": "staple", "price": 12, "image_url": "", "description": "清淡鲜美的传统面食", "season_tag": ""},
    {"name": "炸酱面", "category": "staple", "price": 18, "image_url": "", "description": "浓郁酱香的北方面食", "season_tag": ""},
    {"name": "扬州炒饭", "category": "staple", "price": 22, "image_url": "", "description": "配料丰富的经典炒饭", "season_tag": ""},
    {"name": "饺子（猪肉白菜）", "category": "staple", "price": 25, "image_url": "", "description": "传统手工水饺，皮薄馅大", "season_tag": "winter"},
    {"name": "炒米粉", "category": "staple", "price": 16, "image_url": "", "description": "干香入味的南方米粉", "season_tag": ""},
    {"name": "豆浆油条", "category": "staple", "price": 10, "image_url": "", "description": "经典早餐搭配", "season_tag": ""},
    {"name": "馄饨", "category": "staple", "price": 15, "image_url": "", "description": "皮薄馅鲜的传统小吃", "season_tag": "winter"},
    {"name": "白米饭", "category": "staple", "price": 3, "image_url": "", "description": "粒粒分明的白米饭", "season_tag": ""},
    {"name": "炒面", "category": "staple", "price": 16, "image_url": "", "description": "香气扑鼻的家常炒面", "season_tag": ""},
    # 甜品
    {"name": "红糖糍粑", "category": "dessert", "price": 15, "image_url": "", "description": "软糯香甜的传统小吃", "season_tag": "winter"},
    {"name": "芒果布丁", "category": "dessert", "price": 18, "image_url": "", "description": "清凉爽口的甜品", "season_tag": "summer"},
    {"name": "双皮奶", "category": "dessert", "price": 16, "image_url": "", "description": "顺德经典甜品，奶香浓郁", "season_tag": ""},
    {"name": "蛋挞", "category": "dessert", "price": 8, "image_url": "", "description": "酥脆香甜的葡式蛋挞", "season_tag": ""},
    {"name": "芝麻球", "category": "dessert", "price": 12, "image_url": "", "description": "外酥里糯的传统点心", "season_tag": ""},
    {"name": "汤圆", "category": "dessert", "price": 10, "image_url": "", "description": "软糯甜蜜的传统甜品", "season_tag": "winter"},
    {"name": "月饼", "category": "dessert", "price": 15, "image_url": "", "description": "中秋佳节的传统糕点", "season_tag": "autumn"},
    {"name": "冰淇淋", "category": "dessert", "price": 12, "image_url": "", "description": "清凉解暑的夏日甜品", "season_tag": "summer"},
    # 饮品
    {"name": "柠檬水", "category": "drink", "price": 8, "image_url": "", "description": "清爽解渴的柠檬水", "season_tag": "summer"},
    {"name": "酸梅汤", "category": "drink", "price": 10, "image_url": "", "description": "消暑解腻的传统饮品", "season_tag": "summer"},
    {"name": "豆浆", "category": "drink", "price": 6, "image_url": "", "description": "营养丰富的传统饮品", "season_tag": ""},
    {"name": "奶茶", "category": "drink", "price": 15, "image_url": "", "description": "香浓丝滑的奶茶", "season_tag": ""},
    {"name": "西瓜汁", "category": "drink", "price": 12, "image_url": "", "description": "清凉解暑的鲜榨果汁", "season_tag": "summer"},
    {"name": "橙汁", "category": "drink", "price": 12, "image_url": "", "description": "维C满满的鲜榨橙汁", "season_tag": "winter"},
    {"name": "菠萝蜜汁", "category": "drink", "price": 15, "image_url": "", "description": "热带风味的鲜甜果汁", "season_tag": "summer"},
    {"name": "绿茶", "category": "drink", "price": 8, "image_url": "", "description": "清香回甘的传统绿茶", "season_tag": ""},
]


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
    """)

    cur.execute("SELECT COUNT(*) FROM dishes")
    count = cur.fetchone()[0]
    if count > 0:
        print(f"数据库已有 {count} 条菜品，跳过导入")
        conn.close()
        return

    for d in DISHES:
        cur.execute(
            "INSERT INTO dishes (name, category, price, image_url, description, season_tag) VALUES (?, ?, ?, ?, ?, ?)",
            (d["name"], d["category"], d["price"], d["image_url"], d["description"], d["season_tag"]),
        )

    conn.commit()
    print(f"成功导入 {len(DISHES)} 道菜品到 {DB_PATH}")
    conn.close()


if __name__ == "__main__":
    main()
