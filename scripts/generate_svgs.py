"""Generate SVG food icons for each dish."""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "miniprogram", "assets", "dishes")

CATEGORY_COLORS = {
    "cold_dish": ("#E8F5E9", "#4CAF50"),
    "hot_dish": ("#FFEBEE", "#F44336"),
    "soup": ("#FFF8E1", "#FFC107"),
    "staple": ("#FFF3E0", "#FF9800"),
    "dessert": ("#FCE4EC", "#E91E63"),
    "drink": ("#E3F2FD", "#2196F3"),
}

DISHES = [
    # cold_dish
    ("pat_huanggua", "拍黄瓜", "🥒", "cold_dish"),
    ("liangban_muer", "凉拌木耳", "🍄", "cold_dish"),
    ("pidan_doufu", "皮蛋豆腐", "🥚", "cold_dish"),
    ("koushui_ji", "口水鸡", "🍗", "cold_dish"),
    ("suanni_bairou", "蒜泥白肉", "🥩", "cold_dish"),
    ("liangban_sanwen", "凉拌三丝", "🥗", "cold_dish"),
    ("wuhua_routun", "五花肉冻", "🍖", "cold_dish"),
    ("tangcu_lianou", "糖醋莲藕", "🪷", "cold_dish"),
    # hot_dish
    ("fanqie_chaodan", "番茄炒蛋", "🍅", "hot_dish"),
    ("gongbao_jiding", "宫保鸡丁", "🌶", "hot_dish"),
    ("yuxiang_rousi", "鱼香肉丝", "🥕", "hot_dish"),
    ("hongshao_rou", "红烧肉", "🥩", "hot_dish"),
    ("mapo_doufu", "麻婆豆腐", "🫕", "hot_dish"),
    ("qingzheng_luyu", "清蒸鲈鱼", "🐟", "hot_dish"),
    ("tangcu_paigu", "糖醋排骨", "🍖", "hot_dish"),
    ("shuizhu_niurou", "水煮牛肉", "🌶", "hot_dish"),
    ("ganbian_sijidou", "干煸四季豆", "🫛", "hot_dish"),
    ("huiguo_rou", "回锅肉", "🥩", "hot_dish"),
    ("qingchao_xilan", "清炒西兰花", "🥦", "hot_dish"),
    ("jidan_geng", "鸡蛋羹", "🥚", "hot_dish"),
    ("hongshaorou_donggua", "红烧冬瓜", "🍈", "hot_dish"),
    ("chaoniurou", "炒牛肉", "🥩", "hot_dish"),
    # soup
    ("zicai_danhuatang", "紫菜蛋花汤", "🥚", "soup"),
    ("fanqie_dantang", "番茄蛋汤", "🍅", "soup"),
    ("donggu_paigutang", "冬瓜排骨汤", "🍖", "soup"),
    ("suanla_tang", "酸辣汤", "🌶", "soup"),
    ("yumi_nongtang", "玉米浓汤", "🌽", "soup"),
    ("luobo_tang", "萝卜排骨汤", "🥕", "soup"),
    ("zidou_danhuatang", "紫豆蛋花汤", "🫘", "soup"),
    ("sanxian_tang", "三鲜汤", "🦐", "soup"),
    # staple
    ("dan_chaofan", "蛋炒饭", "🍚", "staple"),
    ("yangchun_mian", "阳春面", "🍜", "staple"),
    ("zhajiang_mian", "炸酱面", "🍜", "staple"),
    ("yangzhou_chaofan", "扬州炒饭", "🍚", "staple"),
    ("jiaozi", "饺子（猪肉白菜）", "🥟", "staple"),
    ("chao_mifen", "炒米粉", "🍝", "staple"),
    ("doujiang_youtiao", "豆浆油条", "🥖", "staple"),
    ("huntun", "馄饨", "🥟", "staple"),
    ("mifan", "白米饭", "🍚", "staple"),
    ("chao_mian", "炒面", "🍜", "staple"),
    # dessert
    ("hongtang_ciba", "红糖糍粑", "🍡", "dessert"),
    ("mangguo_buding", "芒果布丁", "🍮", "dessert"),
    ("shuangpi_nai", "双皮奶", "🥛", "dessert"),
    ("danta", "蛋挞", "🥧", "dessert"),
    ("zhima_qiu", "芝麻球", "🟤", "dessert"),
    ("tangyuan", "汤圆", "⚪", "dessert"),
    ("yuebing", "月饼", "🌕", "dessert"),
    ("bingqilin", "冰淇淋", "🍦", "dessert"),
    # drink
    ("ningmeng_shui", "柠檬水", "🍋", "drink"),
    ("suanmei_tang", "酸梅汤", "🫙", "drink"),
    ("doujiang", "豆浆", "🥛", "drink"),
    ("naicha", "奶茶", "🧋", "drink"),
    ("xigua_zhi", "西瓜汁", "🍉", "drink"),
    ("chengzhi", "橙汁", "🍊", "drink"),
    ("boluomei", "菠萝蜜汁", "🍍", "drink"),
    ("lucha", "绿茶", "🍵", "drink"),
]


def generate_svg(filename, name, emoji, category):
    bg_color, accent = CATEGORY_COLORS[category]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:{accent};stop-opacity:0.15"/>
    </linearGradient>
  </defs>
  <rect width="200" height="200" rx="20" fill="url(#bg)"/>
  <circle cx="100" cy="85" r="50" fill="white" opacity="0.6"/>
  <text x="100" y="105" font-size="60" text-anchor="middle" dominant-baseline="middle">{emoji}</text>
  <text x="100" y="165" font-size="22" font-weight="600" text-anchor="middle" fill="#333" font-family="PingFang SC, Microsoft YaHei, sans-serif">{name}</text>
</svg>'''
    filepath = os.path.join(OUTPUT_DIR, f"{filename}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename, name, emoji, category in DISHES:
        generate_svg(filename, name, emoji, category)
    print(f"Generated {len(DISHES)} SVG files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
