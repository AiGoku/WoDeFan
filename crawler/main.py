"""
菜谱数据采集器
从美食网站采集菜谱数据，导出为JSON，供后端导入数据库
"""
import json
import os
import sys

# 分类映射
CATEGORY_MAP = {
    "凉菜": "cold_dish",
    "热菜": "hot_dish",
    "汤羹": "soup",
    "主食": "staple",
    "甜品": "dessert",
    "小吃": "dessert",
    "饮品": "drink",
    "饮料": "drink",
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def classify_dish(name: str, tags: list[str] = None) -> str:
    """根据菜名和标签推断分类"""
    keywords = {
        "cold_dish": ["拌", "凉", "卤", "腌", "泡", "沙拉", "刺身"],
        "soup": ["汤", "羹", "煲", "炖"],
        "staple": ["饭", "面", "粥", "饼", "馒头", "饺子", "包子", "馄饨", "粉"],
        "dessert": ["糕", "酥", "饼", "糖", "冰淇淋", "蛋糕", "布丁", "慕斯"],
        "drink": ["茶", "汁", "奶", "咖啡", "酒", "饮"],
    }
    for category, words in keywords.items():
        if any(w in name for w in words):
            return category
    return "hot_dish"


def generate_sample_data() -> list[dict]:
    """生成示例菜谱数据（用于开发测试）"""
    dishes = [
        # 凉菜
        {"name": "拍黄瓜", "category": "cold_dish", "price": 12, "image_url": "", "description": "清爽开胃的经典凉菜"},
        {"name": "凉拌木耳", "category": "cold_dish", "price": 15, "image_url": "", "description": "爽脆可口的凉拌菜"},
        {"name": "皮蛋豆腐", "category": "cold_dish", "price": 18, "image_url": "", "description": "经典家常凉菜"},
        {"name": "口水鸡", "category": "cold_dish", "price": 28, "image_url": "", "description": "麻辣鲜香的川味凉菜"},
        {"name": "蒜泥白肉", "category": "cold_dish", "price": 25, "image_url": "", "description": "蒜香浓郁的传统凉菜"},
        # 热菜
        {"name": "番茄炒蛋", "category": "hot_dish", "price": 16, "image_url": "", "description": "国民家常菜"},
        {"name": "宫保鸡丁", "category": "hot_dish", "price": 28, "image_url": "", "description": "经典川菜"},
        {"name": "鱼香肉丝", "category": "hot_dish", "price": 26, "image_url": "", "description": "酸甜微辣的下饭菜"},
        {"name": "红烧肉", "category": "hot_dish", "price": 38, "image_url": "", "description": "肥而不腻的经典硬菜"},
        {"name": "麻婆豆腐", "category": "hot_dish", "price": 22, "image_url": "", "description": "麻辣鲜香的川菜代表"},
        {"name": "清蒸鲈鱼", "category": "hot_dish", "price": 48, "image_url": "", "description": "鲜嫩可口的清蒸鱼"},
        {"name": "糖醋排骨", "category": "hot_dish", "price": 35, "image_url": "", "description": "酸甜可口的传统名菜"},
        {"name": "水煮牛肉", "category": "hot_dish", "price": 42, "image_url": "", "description": "麻辣鲜香的川味硬菜"},
        {"name": "干煸四季豆", "category": "hot_dish", "price": 20, "image_url": "", "description": "干香入味的家常菜"},
        {"name": "回锅肉", "category": "hot_dish", "price": 30, "image_url": "", "description": "川菜之首"},
        # 汤羹
        {"name": "紫菜蛋花汤", "category": "soup", "price": 10, "image_url": "", "description": "简单清淡的家常汤"},
        {"name": "番茄蛋汤", "category": "soup", "price": 12, "image_url": "", "description": "酸甜开胃的家常汤"},
        {"name": "冬瓜排骨汤", "category": "soup", "price": 32, "image_url": "", "description": "清热消暑的滋补汤"},
        {"name": "酸辣汤", "category": "soup", "price": 15, "image_url": "", "description": "酸辣开胃的经典汤品"},
        {"name": "玉米浓汤", "category": "soup", "price": 18, "image_url": "", "description": "香甜浓郁的西式汤品"},
        # 主食
        {"name": "蛋炒饭", "category": "staple", "price": 15, "image_url": "", "description": "粒粒分明的经典炒饭"},
        {"name": "阳春面", "category": "staple", "price": 12, "image_url": "", "description": "清淡鲜美的传统面食"},
        {"name": "炸酱面", "category": "staple", "price": 18, "image_url": "", "description": "浓郁酱香的北方面食"},
        {"name": "扬州炒饭", "category": "staple", "price": 22, "image_url": "", "description": "配料丰富的经典炒饭"},
        {"name": "饺子（猪肉白菜）", "category": "staple", "price": 25, "image_url": "", "description": "传统手工水饺"},
        # 甜品小吃
        {"name": "红糖糍粑", "category": "dessert", "price": 15, "image_url": "", "description": "软糯香甜的传统小吃"},
        {"name": "芒果布丁", "category": "dessert", "price": 18, "image_url": "", "description": "清凉爽口的甜品"},
        {"name": "双皮奶", "category": "dessert", "price": 16, "image_url": "", "description": "顺德经典甜品"},
        {"name": "蛋挞", "category": "dessert", "price": 8, "image_url": "", "description": "酥脆香甜的葡式蛋挞"},
        {"name": "芝麻球", "category": "dessert", "price": 12, "image_url": "", "description": "外酥里糯的传统点心"},
        # 饮品
        {"name": "柠檬水", "category": "drink", "price": 8, "image_url": "", "description": "清爽解渴的柠檬水"},
        {"name": "酸梅汤", "category": "drink", "price": 10, "image_url": "", "description": "消暑解腻的传统饮品"},
        {"name": "豆浆", "category": "drink", "price": 6, "image_url": "", "description": "营养丰富的传统饮品"},
        {"name": "奶茶", "category": "drink", "price": 15, "image_url": "", "description": "香浓丝滑的奶茶"},
        {"name": "西瓜汁", "category": "drink", "price": 12, "image_url": "", "description": "清凉解暑的鲜榨果汁"},
    ]
    return dishes


def export_to_json(dishes: list[dict], filename: str = "dishes.json"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dishes, f, ensure_ascii=False, indent=2)
    print(f"已导出 {len(dishes)} 道菜到 {filepath}")
    return filepath


def import_to_db(json_path: str, db_path: str):
    """将JSON数据导入SQLite数据库"""
    import sqlite3

    with open(json_path, "r", encoding="utf-8") as f:
        dishes = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for dish in dishes:
        cursor.execute(
            "INSERT INTO dishes (name, category, price, image_url, description, season_tag) VALUES (?, ?, ?, ?, ?, ?)",
            (dish["name"], dish["category"], dish["price"], dish.get("image_url", ""),
             dish.get("description", ""), dish.get("season_tag", "")),
        )

    conn.commit()
    conn.close()
    print(f"已导入 {len(dishes)} 道菜到数据库 {db_path}")


if __name__ == "__main__":
    dishes = generate_sample_data()

    if len(sys.argv) > 1 and sys.argv[1] == "--import":
        db_path = sys.argv[2] if len(sys.argv) > 2 else "../backend/data/wodefam.db"
        json_path = export_to_json(dishes)
        import_to_db(json_path, db_path)
    else:
        export_to_json(dishes)
        print("使用 --import 参数可直接导入数据库")
