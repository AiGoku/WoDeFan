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
        {"name": "拍黄瓜", "category": "cold_dish", "price": 12, "image_url": "/assets/dishes/pat_huanggua.png", "description": "清爽开胃的经典凉菜，夏日必备", "season_tag": "summer", "ingredients": ["黄瓜", "蒜", "醋"], "cooking_time": 5, "difficulty": "easy", "spiciness": 1, "tags": ["家常", "快手菜", "开胃"]},
        {"name": "凉拌木耳", "category": "cold_dish", "price": 15, "image_url": "/assets/dishes/liangban_muer.png", "description": "爽脆可口的凉拌菜，富含膳食纤维", "season_tag": "", "ingredients": ["黑木耳", "胡萝卜", "香菜"], "cooking_time": 10, "difficulty": "easy", "spiciness": 1, "tags": ["家常", "健康"]},
        {"name": "皮蛋豆腐", "category": "cold_dish", "price": 18, "image_url": "/assets/dishes/pidan_doufu.png", "description": "经典家常凉菜，口感细腻", "season_tag": "summer", "ingredients": ["皮蛋", "嫩豆腐", "香菜"], "cooking_time": 8, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "下酒"]},
        {"name": "口水鸡", "category": "cold_dish", "price": 28, "image_url": "/assets/dishes/koushui_ji.png", "description": "麻辣鲜香的川味凉菜，让人垂涎", "season_tag": "", "ingredients": ["鸡腿", "花椒", "辣椒油"], "cooking_time": 30, "difficulty": "medium", "spiciness": 3, "tags": ["川菜", "麻辣"]},
        {"name": "蒜泥白肉", "category": "cold_dish", "price": 25, "image_url": "/assets/dishes/suanni_bairou.png", "description": "蒜香浓郁的传统凉菜", "season_tag": "", "ingredients": ["五花肉", "蒜", "酱油"], "cooking_time": 25, "difficulty": "medium", "spiciness": 1, "tags": ["传统", "下酒"]},
        {"name": "凉拌三丝", "category": "cold_dish", "price": 16, "image_url": "/assets/dishes/liangban_sanwen.png", "description": "清脆爽口的多丝凉拌", "season_tag": "summer", "ingredients": ["胡萝卜", "黄瓜", "粉丝"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜"]},
        {"name": "五花肉冻", "category": "cold_dish", "price": 22, "image_url": "/assets/dishes/wuhua_routun.png", "description": "Q弹爽滑的传统肉冻", "season_tag": "winter", "ingredients": ["五花肉", "猪皮", "姜"], "cooking_time": 120, "difficulty": "hard", "spiciness": 0, "tags": ["传统", "年菜"]},
        {"name": "糖醋莲藕", "category": "cold_dish", "price": 18, "image_url": "/assets/dishes/tangcu_lianou.png", "description": "酸甜脆爽的开胃小菜", "season_tag": "autumn", "ingredients": ["莲藕", "醋", "糖"], "cooking_time": 15, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "开胃"]},
        # 热菜
        {"name": "番茄炒蛋", "category": "hot_dish", "price": 16, "image_url": "/assets/dishes/fanqie_chaodan.png", "description": "国民家常菜，酸甜下饭", "season_tag": "spring", "ingredients": ["番茄", "鸡蛋", "葱"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜", "下饭"]},
        {"name": "宫保鸡丁", "category": "hot_dish", "price": 28, "image_url": "/assets/dishes/gongbao_jiding.png", "description": "经典川菜，花生酥脆鸡肉嫩滑", "season_tag": "", "ingredients": ["鸡胸肉", "花生", "干辣椒"], "cooking_time": 20, "difficulty": "medium", "spiciness": 2, "tags": ["川菜", "经典", "下饭"]},
        {"name": "鱼香肉丝", "category": "hot_dish", "price": 26, "image_url": "/assets/dishes/yuxiang_rousi.png", "description": "酸甜微辣的下饭菜，没有鱼的鱼香", "season_tag": "", "ingredients": ["猪肉", "木耳", "胡萝卜"], "cooking_time": 15, "difficulty": "medium", "spiciness": 2, "tags": ["川菜", "下饭"]},
        {"name": "红烧肉", "category": "hot_dish", "price": 38, "image_url": "/assets/dishes/hongshao_rou.png", "description": "肥而不腻的经典硬菜，入口即化", "season_tag": "spring", "ingredients": ["五花肉", "冰糖", "八角"], "cooking_time": 60, "difficulty": "medium", "spiciness": 0, "tags": ["经典", "硬菜", "下饭"]},
        {"name": "麻婆豆腐", "category": "hot_dish", "price": 22, "image_url": "/assets/dishes/mapo_doufu.png", "description": "麻辣鲜香的川菜代表", "season_tag": "", "ingredients": ["嫩豆腐", "猪肉末", "花椒"], "cooking_time": 15, "difficulty": "medium", "spiciness": 3, "tags": ["川菜", "麻辣", "下饭"]},
        {"name": "清蒸鲈鱼", "category": "hot_dish", "price": 48, "image_url": "/assets/dishes/qingzheng_luyu.png", "description": "鲜嫩可口的清蒸鱼，原汁原味", "season_tag": "spring", "ingredients": ["鲈鱼", "葱", "姜"], "cooking_time": 20, "difficulty": "medium", "spiciness": 0, "tags": ["粤菜", "清淡", "硬菜"]},
        {"name": "糖醋排骨", "category": "hot_dish", "price": 35, "image_url": "/assets/dishes/tangcu_paigu.png", "description": "酸甜可口的传统名菜", "season_tag": "", "ingredients": ["猪排骨", "醋", "糖"], "cooking_time": 40, "difficulty": "medium", "spiciness": 0, "tags": ["经典", "酸甜"]},
        {"name": "水煮牛肉", "category": "hot_dish", "price": 42, "image_url": "/assets/dishes/shuizhu_niurou.png", "description": "麻辣鲜香的川味硬菜", "season_tag": "", "ingredients": ["牛肉", "豆芽", "辣椒"], "cooking_time": 25, "difficulty": "hard", "spiciness": 3, "tags": ["川菜", "麻辣", "硬菜"]},
        {"name": "干煸四季豆", "category": "hot_dish", "price": 20, "image_url": "/assets/dishes/ganbian_sijidou.png", "description": "干香入味的家常菜", "season_tag": "", "ingredients": ["四季豆", "猪肉末", "干辣椒"], "cooking_time": 15, "difficulty": "easy", "spiciness": 2, "tags": ["家常", "下饭"]},
        {"name": "回锅肉", "category": "hot_dish", "price": 30, "image_url": "/assets/dishes/huiguo_rou.png", "description": "川菜之首，肥而不腻", "season_tag": "", "ingredients": ["五花肉", "蒜苗", "豆瓣酱"], "cooking_time": 20, "difficulty": "medium", "spiciness": 2, "tags": ["川菜", "经典", "下饭"]},
        {"name": "清炒西兰花", "category": "hot_dish", "price": 18, "image_url": "/assets/dishes/qingchao_xilan.png", "description": "清淡健康的快手菜", "season_tag": "", "ingredients": ["西兰花", "蒜", "盐"], "cooking_time": 8, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜", "健康"]},
        {"name": "鸡蛋羹", "category": "hot_dish", "price": 12, "image_url": "/assets/dishes/jidan_geng.png", "description": "嫩滑如布丁的蒸蛋", "season_tag": "", "ingredients": ["鸡蛋", "温水", "香油"], "cooking_time": 15, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜", "老少皆宜"]},
        {"name": "红烧冬瓜", "category": "hot_dish", "price": 16, "image_url": "/assets/dishes/hongshaorou_donggua.png", "description": "软糯入味的素菜硬菜", "season_tag": "summer", "ingredients": ["冬瓜", "酱油", "糖"], "cooking_time": 20, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "素菜"]},
        {"name": "炒牛肉", "category": "hot_dish", "price": 35, "image_url": "/assets/dishes/chaoniurou.png", "description": "嫩滑多汁的快炒牛肉", "season_tag": "", "ingredients": ["牛肉", "洋葱", "青椒"], "cooking_time": 10, "difficulty": "medium", "spiciness": 1, "tags": ["家常", "快手菜", "下饭"]},
        # 汤羹
        {"name": "紫菜蛋花汤", "category": "soup", "price": 10, "image_url": "/assets/dishes/zicai_danhuatang.png", "description": "简单清淡的家汤，百搭之选", "season_tag": "", "ingredients": ["紫菜", "鸡蛋", "虾皮"], "cooking_time": 8, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜", "清淡"]},
        {"name": "番茄蛋汤", "category": "soup", "price": 12, "image_url": "/assets/dishes/fanqie_dantang.png", "description": "酸甜开胃的家常汤", "season_tag": "spring", "ingredients": ["番茄", "鸡蛋", "葱"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "开胃"]},
        {"name": "冬瓜排骨汤", "category": "soup", "price": 32, "image_url": "/assets/dishes/donggu_paigutang.png", "description": "清热消暑的滋补汤", "season_tag": "summer", "ingredients": ["冬瓜", "排骨", "姜"], "cooking_time": 60, "difficulty": "easy", "spiciness": 0, "tags": ["滋补", "清淡"]},
        {"name": "酸辣汤", "category": "soup", "price": 15, "image_url": "/assets/dishes/suanla_tang.png", "description": "酸辣开胃的经典汤品", "season_tag": "winter", "ingredients": ["豆腐", "木耳", "鸡蛋"], "cooking_time": 15, "difficulty": "medium", "spiciness": 2, "tags": ["经典", "开胃"]},
        {"name": "玉米浓汤", "category": "soup", "price": 18, "image_url": "/assets/dishes/yumi_nongtang.png", "description": "香甜浓郁的西式汤品", "season_tag": "", "ingredients": ["玉米", "牛奶", "黄油"], "cooking_time": 20, "difficulty": "easy", "spiciness": 0, "tags": ["西式", "香甜"]},
        {"name": "萝卜排骨汤", "category": "soup", "price": 28, "image_url": "/assets/dishes/luobo_tang.png", "description": "清甜滋补的家常炖汤", "season_tag": "winter", "ingredients": ["白萝卜", "排骨", "枸杞"], "cooking_time": 60, "difficulty": "easy", "spiciness": 0, "tags": ["滋补", "家常"]},
        {"name": "冬瓜虾仁汤", "category": "soup", "price": 22, "image_url": "/assets/dishes/zidou_danhuatang.png", "description": "鲜美清爽的虾仁汤", "season_tag": "summer", "ingredients": ["冬瓜", "虾仁", "姜"], "cooking_time": 15, "difficulty": "easy", "spiciness": 0, "tags": ["鲜美", "清淡"]},
        {"name": "三鲜汤", "category": "soup", "price": 25, "image_url": "/assets/dishes/sanxian_tang.png", "description": "鲜美可口的多料汤", "season_tag": "", "ingredients": ["虾仁", "鱿鱼", "蘑菇"], "cooking_time": 15, "difficulty": "medium", "spiciness": 0, "tags": ["鲜美", "家常"]},
        # 主食
        {"name": "蛋炒饭", "category": "staple", "price": 15, "image_url": "/assets/dishes/dan_chaofan.png", "description": "粒粒分明的经典炒饭", "season_tag": "", "ingredients": ["米饭", "鸡蛋", "葱"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜"]},
        {"name": "阳春面", "category": "staple", "price": 12, "image_url": "/assets/dishes/yangchun_mian.png", "description": "清淡鲜美的传统面食", "season_tag": "", "ingredients": ["面条", "葱", "猪油"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["传统", "清淡"]},
        {"name": "炸酱面", "category": "staple", "price": 18, "image_url": "/assets/dishes/zhajiang_mian.png", "description": "浓郁酱香的北方面食", "season_tag": "", "ingredients": ["面条", "猪肉末", "黄瓜"], "cooking_time": 20, "difficulty": "medium", "spiciness": 1, "tags": ["北方", "经典"]},
        {"name": "扬州炒饭", "category": "staple", "price": 22, "image_url": "/assets/dishes/yangzhou_chaofan.png", "description": "配料丰富的经典炒饭", "season_tag": "", "ingredients": ["米饭", "虾仁", "火腿"], "cooking_time": 15, "difficulty": "medium", "spiciness": 0, "tags": ["经典", "丰盛"]},
        {"name": "饺子（猪肉白菜）", "category": "staple", "price": 25, "image_url": "/assets/dishes/jiaozi.png", "description": "传统手工水饺，皮薄馅大", "season_tag": "winter", "ingredients": ["猪肉", "白菜", "饺子皮"], "cooking_time": 60, "difficulty": "hard", "spiciness": 0, "tags": ["传统", "年菜"]},
        {"name": "炒米粉", "category": "staple", "price": 16, "image_url": "/assets/dishes/chao_mifen.png", "description": "干香入味的南方米粉", "season_tag": "", "ingredients": ["米粉", "鸡蛋", "豆芽"], "cooking_time": 15, "difficulty": "medium", "spiciness": 1, "tags": ["南方", "家常"]},
        {"name": "豆浆油条", "category": "staple", "price": 10, "image_url": "/assets/dishes/doujiang_youtiao.png", "description": "经典早餐搭配", "season_tag": "", "ingredients": ["黄豆", "面粉"], "cooking_time": 30, "difficulty": "medium", "spiciness": 0, "tags": ["早餐", "经典"]},
        {"name": "馄饨", "category": "staple", "price": 15, "image_url": "/assets/dishes/huntun.png", "description": "皮薄馅鲜的传统小吃", "season_tag": "winter", "ingredients": ["猪肉", "馄饨皮", "紫菜"], "cooking_time": 30, "difficulty": "medium", "spiciness": 0, "tags": ["传统", "早餐"]},
        {"name": "白米饭", "category": "staple", "price": 3, "image_url": "/assets/dishes/mifan.png", "description": "粒粒分明的白米饭", "season_tag": "", "ingredients": ["大米"], "cooking_time": 30, "difficulty": "easy", "spiciness": 0, "tags": ["基础", "百搭"]},
        {"name": "炒面", "category": "staple", "price": 16, "image_url": "/assets/dishes/chao_mian.png", "description": "香气扑鼻的家常炒面", "season_tag": "", "ingredients": ["面条", "鸡蛋", "青菜"], "cooking_time": 12, "difficulty": "easy", "spiciness": 0, "tags": ["家常", "快手菜"]},
        # 甜品小吃
        {"name": "红糖糍粑", "category": "dessert", "price": 15, "image_url": "/assets/dishes/hongtang_ciba.png", "description": "软糯香甜的传统小吃", "season_tag": "winter", "ingredients": ["糯米", "红糖", "黄豆粉"], "cooking_time": 20, "difficulty": "medium", "spiciness": 0, "tags": ["传统", "香甜"]},
        {"name": "芒果布丁", "category": "dessert", "price": 18, "image_url": "/assets/dishes/mangguo_buding.png", "description": "清凉爽口的甜品", "season_tag": "summer", "ingredients": ["芒果", "牛奶", "吉利丁"], "cooking_time": 30, "difficulty": "easy", "spiciness": 0, "tags": ["甜品", "清凉"]},
        {"name": "双皮奶", "category": "dessert", "price": 16, "image_url": "/assets/dishes/shuangpi_nai.png", "description": "顺德经典甜品，奶香浓郁", "season_tag": "", "ingredients": ["牛奶", "蛋清", "糖"], "cooking_time": 25, "difficulty": "medium", "spiciness": 0, "tags": ["粤式", "经典"]},
        {"name": "蛋挞", "category": "dessert", "price": 8, "image_url": "/assets/dishes/danta.png", "description": "酥脆香甜的葡式蛋挞", "season_tag": "", "ingredients": ["蛋挞皮", "鸡蛋", "牛奶"], "cooking_time": 25, "difficulty": "medium", "spiciness": 0, "tags": ["西式", "经典"]},
        {"name": "芝麻球", "category": "dessert", "price": 12, "image_url": "/assets/dishes/zhima_qiu.png", "description": "外酥里糯的传统点心", "season_tag": "", "ingredients": ["糯米粉", "芝麻", "豆沙"], "cooking_time": 20, "difficulty": "medium", "spiciness": 0, "tags": ["传统", "香甜"]},
        {"name": "汤圆", "category": "dessert", "price": 10, "image_url": "/assets/dishes/tangyuan.png", "description": "软糯甜蜜的传统甜品", "season_tag": "winter", "ingredients": ["糯米粉", "芝麻", "花生"], "cooking_time": 15, "difficulty": "easy", "spiciness": 0, "tags": ["传统", "节日"]},
        {"name": "月饼", "category": "dessert", "price": 15, "image_url": "/assets/dishes/yuebing.png", "description": "中秋佳节的传统糕点", "season_tag": "autumn", "ingredients": ["面粉", "莲蓉", "蛋黄"], "cooking_time": 60, "difficulty": "hard", "spiciness": 0, "tags": ["传统", "节日"]},
        {"name": "冰淇淋", "category": "dessert", "price": 12, "image_url": "/assets/dishes/bingqilin.png", "description": "清凉解暑的夏日甜品", "season_tag": "summer", "ingredients": ["牛奶", "奶油", "糖"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["甜品", "清凉"]},
        # 饮品
        {"name": "柠檬水", "category": "drink", "price": 8, "image_url": "/assets/dishes/ningmeng_shui.png", "description": "清爽解渴的柠檬水", "season_tag": "summer", "ingredients": ["柠檬", "蜂蜜", "水"], "cooking_time": 5, "difficulty": "easy", "spiciness": 0, "tags": ["清凉", "解渴"]},
        {"name": "酸梅汤", "category": "drink", "price": 10, "image_url": "/assets/dishes/suanmei_tang.png", "description": "消暑解腻的传统饮品", "season_tag": "summer", "ingredients": ["乌梅", "山楂", "桂花"], "cooking_time": 40, "difficulty": "easy", "spiciness": 0, "tags": ["传统", "消暑"]},
        {"name": "豆浆", "category": "drink", "price": 6, "image_url": "/assets/dishes/doujiang.png", "description": "营养丰富的传统饮品", "season_tag": "", "ingredients": ["黄豆", "水"], "cooking_time": 20, "difficulty": "easy", "spiciness": 0, "tags": ["早餐", "健康"]},
        {"name": "奶茶", "category": "drink", "price": 15, "image_url": "/assets/dishes/naicha.png", "description": "香浓丝滑的奶茶", "season_tag": "", "ingredients": ["红茶", "牛奶", "糖"], "cooking_time": 10, "difficulty": "easy", "spiciness": 0, "tags": ["饮品", "香浓"]},
        {"name": "西瓜汁", "category": "drink", "price": 12, "image_url": "/assets/dishes/xigua_zhi.png", "description": "清凉解暑的鲜榨果汁", "season_tag": "summer", "ingredients": ["西瓜"], "cooking_time": 5, "difficulty": "easy", "spiciness": 0, "tags": ["鲜榨", "消暑"]},
        {"name": "橙汁", "category": "drink", "price": 12, "image_url": "/assets/dishes/chengzhi.png", "description": "维C满满的鲜榨橙汁", "season_tag": "winter", "ingredients": ["橙子"], "cooking_time": 5, "difficulty": "easy", "spiciness": 0, "tags": ["鲜榨", "健康"]},
        {"name": "菠萝蜜汁", "category": "drink", "price": 15, "image_url": "/assets/dishes/boluomei.png", "description": "热带风味的鲜甜果汁", "season_tag": "summer", "ingredients": ["菠萝", "蜂蜜"], "cooking_time": 5, "difficulty": "easy", "spiciness": 0, "tags": ["鲜榨", "热带"]},
        {"name": "绿茶", "category": "drink", "price": 8, "image_url": "/assets/dishes/lucha.png", "description": "清香回甘的传统绿茶", "season_tag": "", "ingredients": ["绿茶叶"], "cooking_time": 5, "difficulty": "easy", "spiciness": 0, "tags": ["传统", "清饮"]},
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
            "INSERT INTO dishes (name, category, price, image_url, description, season_tag, ingredients, cooking_time, difficulty, spiciness, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (dish["name"], dish["category"], dish["price"], dish.get("image_url", ""),
             dish.get("description", ""), dish.get("season_tag", ""),
             json.dumps(dish.get("ingredients", []), ensure_ascii=False),
             dish.get("cooking_time", 0), dish.get("difficulty", "easy"),
             dish.get("spiciness", 0),
             json.dumps(dish.get("tags", []), ensure_ascii=False)),
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
