"""
菜品图片下载器
从 Pexels API 下载真实菜品图片，供上传到微信云存储
需要设置环境变量 PEXELS_API_KEY（免费注册: https://www.pexels.com/api/）
"""
import os
import json
import urllib.request
import urllib.parse
import ssl
import time

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

# Pexels API Key（从环境变量读取，或直接填写在引号内）
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "ov266eIlIgbMdsdBuUbOmNz7ZKlZnZtdnIvqOEHUBEzHQDUEJiTHf2He")

# 菜品文件名 → Pexels 搜索关键词
DISH_KEYWORDS = {
    # 凉菜
    "pat_huanggua": "smashed cucumber salad",
    "liangban_muer": "wood ear mushroom salad",
    "pidan_doufu": "tofu century egg",
    "koushui_ji": "mouthwatering chicken sichuan",
    "suanni_bairou": "garlic pork belly slices",
    "liangban_sanwen": "mixed vegetable salad",
    "wuhua_routun": "pork aspic jelly",
    "tangcu_lianou": "sweet sour lotus root",
    # 热菜
    "fanqie_chaodan": "tomato egg stir fry chinese",
    "gongbao_jiding": "kung pao chicken",
    "yuxiang_rousi": "yu xiang shredded pork",
    "hongshao_rou": "braised pork belly chinese",
    "mapo_doufu": "mapo tofu",
    "qingzheng_luyu": "steamed sea bass fish",
    "tangcu_paigu": "sweet sour ribs chinese",
    "shuizhu_niurou": "sichuan boiled beef spicy",
    "ganbian_sijidou": "dry fried green beans",
    "huiguo_rou": "twice cooked pork belly",
    "qingchao_xilan": "steamed broccoli",
    "jidan_geng": "steamed egg custard",
    "hongshaorou_donggua": "braised winter melon",
    "chaoniurou": "stir fried beef onion",
    # 汤羹
    "zicai_danhuatang": "seaweed egg soup",
    "fanqie_dantang": "tomato egg soup",
    "donggu_paigutang": "winter melon pork rib soup",
    "suanla_tang": "hot sour soup chinese",
    "yumi_nongtang": "corn cream soup",
    "luobo_tang": "radish pork soup",
    "zidou_danhuatang": "shrimp egg soup",
    "sanxian_tang": "seafood soup chinese",
    # 主食
    "dan_chaofan": "egg fried rice",
    "yangchun_mian": "plain noodles chinese",
    "zhajiang_mian": "zhajiang noodles beijing",
    "yangzhou_chaofan": "yangzhou fried rice",
    "jiaozi": "chinese dumplings jiaozi",
    "chao_mifen": "stir fried rice noodles",
    "doujiang_youtiao": "soy milk chinese donut",
    "huntun": "wonton soup chinese",
    "mifan": "steamed rice bowl",
    "chao_mian": "stir fried noodles chinese",
    # 甜品
    "hongtang_ciba": "glutinous rice cake chinese",
    "mangguo_buding": "mango pudding dessert",
    "shuangpi_nai": "double skin milk pudding",
    "danta": "egg tart portuguese",
    "zhima_qiu": "sesame ball fried",
    "tangyuan": "tangyuan glutinous rice ball",
    "yuebing": "mooncake chinese",
    "bingqilin": "ice cream scoops",
    # 饮品
    "ningmeng_shui": "lemon water drink",
    "suanmei_tang": "sour plum drink chinese",
    "doujiang": "soy milk drink",
    "naicha": "milk tea bubble tea",
    "xigua_zhi": "watermelon juice",
    "chengzhi": "orange juice fresh",
    "boluomei": "pineapple juice",
    "lucha": "green tea chinese",
}


def search_pexels(keyword):
    """通过 Pexels API 搜索图片，返回第一张图片的下载 URL"""
    if not PEXELS_API_KEY:
        print("  ERROR: 请设置 PEXELS_API_KEY 环境变量或在脚本中填写")
        return None

    url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(keyword)}&per_page=1&orientation=landscape"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Mozilla/5.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            photos = data.get("photos", [])
            if photos:
                # 使用 medium 尺寸（约 400px 宽），适合小程序展示
                return photos[0]["src"]["medium"]
    except Exception as e:
        print(f"  search error: {e}")
    return None


def download_image(filename, keyword):
    filepath = os.path.join(IMAGES_DIR, f"{filename}.jpg")
    if os.path.exists(filepath):
        print(f"  skip {filename} (exists)")
        return True

    image_url = search_pexels(keyword)
    if not image_url:
        print(f"  fail {filename} (no result for '{keyword}')")
        return False

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"  ok {filename} ({len(data)} bytes)")
                return True
            else:
                print(f"  fail {filename} (too small)")
                return False
    except Exception as e:
        print(f"  fail {filename}: {e}")
        return False


def main():
    if not PEXELS_API_KEY:
        print("ERROR: 请先设置 PEXELS_API_KEY")
        print("  方式1: 设置环境变量  set PEXELS_API_KEY=你的key")
        print("  方式2: 在脚本中填写  PEXELS_API_KEY = '你的key'")
        print("  免费注册: https://www.pexels.com/api/")
        return

    os.makedirs(IMAGES_DIR, exist_ok=True)
    total = len(DISH_KEYWORDS)
    success = 0
    failed = []

    print(f"Downloading {total} images from Pexels...")
    for filename, keyword in DISH_KEYWORDS.items():
        print(f"[{success + len(failed) + 1}/{total}] {keyword}")
        if download_image(filename, keyword):
            success += 1
        else:
            failed.append(filename)
        time.sleep(0.5)  # Pexels API 限速

    print(f"\nDone: {success} ok, {len(failed)} failed")
    if failed:
        print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
