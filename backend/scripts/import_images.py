"""
菜品图片导入脚本
将 crawler/images/ 中的图片复制到 backend/static/images/，
并初始化菜品数据库记录（含图片关联）。
"""
import os
import shutil
import sqlite3

# 路径配置
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CRAWLER_IMAGES = os.path.join(PROJECT_ROOT, "crawler", "images")
STATIC_IMAGES = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "images")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "wodefam.db")

# 菜品数据：(文件名, 名称, 分类, 价格, 描述, 季节标签)
DISHES = [
    # 凉菜
    ("pat_huanggua", "拍黄瓜", "cold_dish", 16, "爽脆开胃的经典凉菜，蒜香十足", "summer"),
    ("liangban_muer", "凉拌木耳", "cold_dish", 18, "口感脆嫩，酸辣开胃", ""),
    ("pidan_doufu", "皮蛋豆腐", "cold_dish", 18, "滑嫩豆腐配皮蛋，清凉爽口", "summer"),
    ("koushui_ji", "口水鸡", "cold_dish", 28, "麻辣鲜香，让人垂涎欲滴", ""),
    ("suanni_bairou", "蒜泥白肉", "cold_dish", 26, "蒜香浓郁，肉片薄而不腻", "summer"),
    ("liangban_sanwen", "凉拌三丝", "cold_dish", 16, "清爽解腻的素食凉菜", ""),
    ("wuhua_routun", "五花肉冻", "cold_dish", 22, "传统年菜，Q弹爽滑", "winter"),
    ("tangcu_lianou", "糖醋莲藕", "cold_dish", 18, "酸甜脆爽，老少皆宜", "autumn"),

    # 热菜
    ("fanqie_chaodan", "番茄炒蛋", "hot_dish", 18, "国民家常菜，酸甜下饭", ""),
    ("gongbao_jiding", "宫保鸡丁", "hot_dish", 28, "经典川菜，花生香脆，鸡丁嫩滑", ""),
    ("yuxiang_rousi", "鱼香肉丝", "hot_dish", 26, "酸甜微辣，下饭神器", ""),
    ("hongshao_rou", "红烧肉", "hot_dish", 38, "肥而不腻，入口即化", "winter"),
    ("mapo_doufu", "麻婆豆腐", "hot_dish", 22, "麻辣鲜香，豆腐嫩滑", ""),
    ("qingzheng_luyu", "清蒸鲈鱼", "hot_dish", 48, "鲜嫩多汁，原汁原味", ""),
    ("tangcu_paigu", "糖醋排骨", "hot_dish", 36, "外酥里嫩，酸甜可口", ""),
    ("shuizhu_niurou", "水煮牛肉", "hot_dish", 42, "麻辣鲜香，肉片嫩滑", "winter"),
    ("ganbian_sijidou", "干煸四季豆", "hot_dish", 22, "干香入味，越嚼越香", ""),
    ("huiguo_rou", "回锅肉", "hot_dish", 28, "川菜之首，肥而不腻", ""),
    ("qingchao_xilan", "清炒西兰花", "hot_dish", 18, "清淡健康，营养丰富", ""),
    ("jidan_geng", "鸡蛋羹", "hot_dish", 12, "滑嫩如丝，入口即化", ""),
    ("hongshaorou_donggua", "红烧肉冬瓜", "hot_dish", 28, "冬瓜吸满肉汁，软糯入味", "summer"),
    ("chaoniurou", "炒牛肉", "hot_dish", 35, "嫩滑多汁，洋葱提香", ""),

    # 汤羹
    ("zicai_danhuatang", "紫菜蛋花汤", "soup", 10, "清淡鲜美，经典汤品", ""),
    ("fanqie_dantang", "番茄蛋汤", "soup", 12, "酸甜开胃，营养丰富", ""),
    ("donggu_paigutang", "冬瓜排骨汤", "soup", 28, "清热解暑，鲜美滋补", "summer"),
    ("suanla_tang", "酸辣汤", "soup", 15, "酸辣开胃，暖身驱寒", "winter"),
    ("yumi_nongtang", "玉米浓汤", "soup", 14, "香甜浓郁，老少皆宜", ""),
    ("luobo_tang", "萝卜汤", "soup", 16, "清甜润肺，秋冬滋补", "autumn"),
    ("zidou_danhuatang", "虾皮蛋花汤", "soup", 12, "鲜美补钙，简单快手", ""),
    ("sanxian_tang", "三鲜汤", "soup", 22, "鲜美可口，食材丰富", ""),

    # 主食
    ("dan_chaofan", "蛋炒饭", "staple", 12, "粒粒分明，蛋香四溢", ""),
    ("yangchun_mian", "阳春面", "staple", 10, "清汤素面，简单美味", ""),
    ("zhajiang_mian", "炸酱面", "staple", 18, "酱香浓郁，老北京味道", ""),
    ("yangzhou_chaofan", "扬州炒饭", "staple", 18, "配料丰富，色香味俱全", ""),
    ("jiaozi", "饺子", "staple", 22, "皮薄馅大，蘸醋更香", "winter"),
    ("chao_mifen", "炒米粉", "staple", 16, "干香入味，南方经典", ""),
    ("doujiang_youtiao", "豆浆油条", "staple", 8, "经典早餐搭配", ""),
    ("huntun", "馄饨", "staple", 14, "皮薄馅鲜，汤清味美", "winter"),
    ("mifan", "米饭", "staple", 3, "粒粒分明的白米饭", ""),
    ("chao_mian", "炒面", "staple", 15, "干香入味，快手主食", ""),

    # 甜品小吃
    ("hongtang_ciba", "红糖糍粑", "dessert", 14, "软糯香甜，外酥里嫩", "winter"),
    ("mangguo_buding", "芒果布丁", "dessert", 16, "香甜丝滑，夏日甜品", "summer"),
    ("shuangpi_nai", "双皮奶", "dessert", 14, "嫩滑香甜，广东经典", ""),
    ("danta", "蛋挞", "dessert", 12, "酥脆外皮，嫩滑内馅", ""),
    ("zhima_qiu", "芝麻球", "dessert", 10, "外酥里糯，芝麻飘香", ""),
    ("tangyuan", "汤圆", "dessert", 12, "软糯香甜，团团圆圆", "winter"),
    ("yuebing", "月饼", "dessert", 18, "传统糕点，中秋必备", "autumn"),
    ("bingqilin", "冰淇淋", "dessert", 8, "清凉解暑，甜蜜享受", "summer"),

    # 饮品
    ("ningmeng_shui", "柠檬水", "drink", 8, "清爽解渴，维C满满", "summer"),
    ("suanmei_tang", "酸梅汤", "drink", 8, "酸甜解腻，消暑佳品", "summer"),
    ("doujiang", "豆浆", "drink", 6, "香浓顺滑，营养早餐", ""),
    ("naicha", "奶茶", "drink", 12, "香甜丝滑，年轻人最爱", ""),
    ("xigua_zhi", "西瓜汁", "drink", 10, "清甜解暑，夏日必备", "summer"),
    ("chengzhi", "橙汁", "drink", 10, "新鲜榨取，维C丰富", ""),
    ("boluomei", "菠萝汁", "drink", 10, "酸甜热带风味", "summer"),
    ("lucha", "绿茶", "drink", 6, "清香回甘，提神醒脑", ""),
]


def copy_images():
    """复制图片到 static 目录"""
    os.makedirs(STATIC_IMAGES, exist_ok=True)
    copied = 0
    for filename, *_ in DISHES:
        src = os.path.join(CRAWLER_IMAGES, f"{filename}.jpg")
        dst = os.path.join(STATIC_IMAGES, f"{filename}.jpg")
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied += 1
        else:
            print(f"  [WARN] 图片不存在: {src}")
    return copied


def init_dishes():
    """初始化菜品数据并关联图片"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)

    # 检查是否已有数据
    count = db.execute("SELECT COUNT(*) FROM dishes").fetchone()[0]
    if count > 0:
        print(f"  数据库已有 {count} 条菜品记录，跳过初始化")
        # 只更新图片链接
        for filename, name, *_ in DISHES:
            image_url = f"/static/images/{filename}.jpg"
            db.execute("UPDATE dishes SET image_url = ? WHERE name = ?", (image_url, name))
        db.commit()
        print("  已更新图片链接")
        db.close()
        return len(DISHES)

    # 插入菜品数据
    inserted = 0
    for filename, name, category, price, description, season_tag in DISHES:
        image_url = f"/static/images/{filename}.jpg"
        try:
            db.execute(
                "INSERT INTO dishes (name, category, price, image_url, description, season_tag) VALUES (?, ?, ?, ?, ?, ?)",
                (name, category, price, image_url, description, season_tag),
            )
            inserted += 1
        except Exception as e:
            print(f"  [ERROR] 插入失败 {name}: {e}")

    db.commit()
    db.close()
    return inserted


def main():
    print("=== 菜品图片导入 ===\n")

    print("1. 复制图片到 static 目录...")
    copied = copy_images()
    print(f"   复制了 {copied} 张图片到 {STATIC_IMAGES}\n")

    print("2. 初始化菜品数据库...")
    inserted = init_dishes()
    print(f"   处理了 {inserted} 道菜品\n")

    print("=== 完成 ===")
    print(f"图片目录: {STATIC_IMAGES}")
    print(f"数据库: {DB_PATH}")


if __name__ == "__main__":
    main()
