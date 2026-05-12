"""Generate PNG food icons for each dish using Pillow."""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "miniprogram", "assets", "dishes")

CATEGORY_COLORS = {
    "cold_dish": ((200, 240, 200), (76, 175, 80)),
    "hot_dish": ((255, 215, 215), (244, 67, 54)),
    "soup": ((255, 245, 200), (255, 193, 7)),
    "staple": ((255, 230, 200), (255, 152, 0)),
    "dessert": ((255, 210, 230), (233, 30, 99)),
    "drink": ((200, 225, 255), (33, 150, 243)),
}

DISHES = [
    ("pat_huanggua", "拍黄瓜", "cold_dish"),
    ("liangban_muer", "凉拌木耳", "cold_dish"),
    ("pidan_doufu", "皮蛋豆腐", "cold_dish"),
    ("koushui_ji", "口水鸡", "cold_dish"),
    ("suanni_bairou", "蒜泥白肉", "cold_dish"),
    ("liangban_sanwen", "凉拌三丝", "cold_dish"),
    ("wuhua_routun", "五花肉冻", "cold_dish"),
    ("tangcu_lianou", "糖醋莲藕", "cold_dish"),
    ("fanqie_chaodan", "番茄炒蛋", "hot_dish"),
    ("gongbao_jiding", "宫保鸡丁", "hot_dish"),
    ("yuxiang_rousi", "鱼香肉丝", "hot_dish"),
    ("hongshao_rou", "红烧肉", "hot_dish"),
    ("mapo_doufu", "麻婆豆腐", "hot_dish"),
    ("qingzheng_luyu", "清蒸鲈鱼", "hot_dish"),
    ("tangcu_paigu", "糖醋排骨", "hot_dish"),
    ("shuizhu_niurou", "水煮牛肉", "hot_dish"),
    ("ganbian_sijidou", "干煸四季豆", "hot_dish"),
    ("huiguo_rou", "回锅肉", "hot_dish"),
    ("qingchao_xilan", "清炒西兰花", "hot_dish"),
    ("jidan_geng", "鸡蛋羹", "hot_dish"),
    ("hongshaorou_donggua", "红烧冬瓜", "hot_dish"),
    ("chaoniurou", "炒牛肉", "hot_dish"),
    ("zicai_danhuatang", "紫菜蛋花汤", "soup"),
    ("fanqie_dantang", "番茄蛋汤", "soup"),
    ("donggu_paigutang", "冬瓜排骨汤", "soup"),
    ("suanla_tang", "酸辣汤", "soup"),
    ("yumi_nongtang", "玉米浓汤", "soup"),
    ("luobo_tang", "萝卜排骨汤", "soup"),
    ("zidou_danhuatang", "冬瓜虾仁汤", "soup"),
    ("sanxian_tang", "三鲜汤", "soup"),
    ("dan_chaofan", "蛋炒饭", "staple"),
    ("yangchun_mian", "阳春面", "staple"),
    ("zhajiang_mian", "炸酱面", "staple"),
    ("yangzhou_chaofan", "扬州炒饭", "staple"),
    ("jiaozi", "水饺", "staple"),
    ("chao_mifen", "炒米粉", "staple"),
    ("doujiang_youtiao", "豆浆油条", "staple"),
    ("huntun", "馄饨", "staple"),
    ("mifan", "白米饭", "staple"),
    ("chao_mian", "炒面", "staple"),
    ("hongtang_ciba", "红糖糍粑", "dessert"),
    ("mangguo_buding", "芒果布丁", "dessert"),
    ("shuangpi_nai", "双皮奶", "dessert"),
    ("danta", "蛋挞", "dessert"),
    ("zhima_qiu", "芝麻球", "dessert"),
    ("tangyuan", "汤圆", "dessert"),
    ("yuebing", "月饼", "dessert"),
    ("bingqilin", "冰淇淋", "dessert"),
    ("ningmeng_shui", "柠檬水", "drink"),
    ("suanmei_tang", "酸梅汤", "drink"),
    ("doujiang", "豆浆", "drink"),
    ("naicha", "奶茶", "drink"),
    ("xigua_zhi", "西瓜汁", "drink"),
    ("chengzhi", "橙汁", "drink"),
    ("boluomei", "菠萝蜜汁", "drink"),
    ("lucha", "绿茶", "drink"),
]


def get_font(size):
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def generate_png(filename, name, category):
    bg_color, accent = CATEGORY_COLORS[category]
    size = 200

    img = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    # Center circle
    circle_r = 50
    cx, cy = size // 2, size // 2 - 15
    draw.ellipse(
        [cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r],
        fill=(255, 255, 255),
    )

    # Category icon
    icon_font = get_font(36)
    cat_icons = {
        "cold_dish": "凉",
        "hot_dish": "热",
        "soup": "汤",
        "staple": "主",
        "dessert": "甜",
        "drink": "饮",
    }
    icon = cat_icons.get(category, "")
    bbox = draw.textbbox((0, 0), icon, font=icon_font)
    iw = bbox[2] - bbox[0]
    ih = bbox[3] - bbox[1]
    draw.text((cx - iw // 2, cy - ih // 2 - 4), icon, fill=accent, font=icon_font)

    # Dish name
    name_font = get_font(22)
    bbox = draw.textbbox((0, 0), name, font=name_font)
    nw = bbox[2] - bbox[0]
    draw.text((size // 2 - nw // 2, 145), name, fill=(51, 51, 51), font=name_font)

    filepath = os.path.join(OUTPUT_DIR, f"{filename}.png")
    img.save(filepath, "PNG")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Remove old SVG files
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".svg"):
            os.remove(os.path.join(OUTPUT_DIR, f))
    for filename, name, category in DISHES:
        generate_png(filename, name, category)
    print(f"Generated {len(DISHES)} PNG files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
