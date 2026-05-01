"""生成小程序所需的图标素材"""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "miniprogram", "assets")
ICONS_DIR = os.path.join(OUTPUT_DIR, "icons")
os.makedirs(ICONS_DIR, exist_ok=True)

GRAY = "#999999"
ORANGE = "#FF6B35"
LIGHT_BG = "#F5F5F5"
WHITE = "#FFFFFF"


def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2*radius, y0 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2*radius, y0, x1, y0 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2*radius, x0 + 2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2*radius, y1 - 2*radius, x1, y1], 0, 90, fill=fill)


def draw_menu_icon(size, color):
    """画一个餐盘+筷子的图标"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # 餐盘 - 椭圆
    plate_w, plate_h = int(size * 0.6), int(size * 0.3)
    plate_y = cy + int(size * 0.05)
    draw.ellipse(
        [cx - plate_w, plate_y - plate_h, cx + plate_w, plate_y + plate_h],
        fill=None, outline=color, width=max(2, size // 20)
    )

    # 餐盘底部弧线
    plate_bottom_h = int(size * 0.12)
    draw.arc(
        [cx - plate_w + 5, plate_y + plate_h - plate_bottom_h,
         cx + plate_w - 5, plate_y + plate_h + plate_bottom_h],
        0, 180, fill=color, width=max(2, size // 20)
    )

    # 筷子1
    chopstick_len = int(size * 0.45)
    x1_start = cx - int(size * 0.15)
    y1_start = cy - int(size * 0.35)
    x1_end = x1_start + int(chopstick_len * 0.3)
    y1_end = y1_start + chopstick_len
    draw.line([(x1_start, y1_start), (x1_end, y1_end)], fill=color, width=max(2, size // 22))

    # 筷子2
    x2_start = cx + int(size * 0.05)
    y2_start = cy - int(size * 0.35)
    x2_end = x2_start + int(chopstick_len * 0.3)
    y2_end = y2_start + chopstick_len
    draw.line([(x2_start, y2_start), (x2_end, y2_end)], fill=color, width=max(2, size // 22))

    return img


def draw_cart_icon(size, color):
    """画一个清单/列表图标"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    margin = int(size * 0.2)
    line_h = int(size * 0.12)
    gap = int(size * 0.16)
    start_y = cy - int(size * 0.22)

    lw = max(2, size // 20)
    dot_r = max(2, size // 24)

    for i in range(3):
        y = start_y + i * gap
        # 左侧圆点
        draw.ellipse(
            [margin, y - dot_r, margin + 2*dot_r, y + dot_r],
            fill=color
        )
        # 横线
        line_start_x = margin + 2 * dot_r + int(size * 0.08)
        line_end_x = size - margin
        draw.line([(line_start_x, y), (line_end_x, y)], fill=color, width=lw)

    return img


def draw_default_dish(size):
    """生成默认菜品占位图"""
    img = Image.new("RGB", (size, size), LIGHT_BG)
    draw = ImageDraw.Draw(img)

    # 浅色圆角背景
    draw_rounded_rect(draw, [0, 0, size-1, size-1], size // 10, "#EDEDED")

    # 餐具图标（简化）
    cx, cy = size // 2, size // 2

    # 盘子
    plate_r = int(size * 0.3)
    draw.ellipse(
        [cx - plate_r, cy - plate_r + int(size*0.05),
         cx + plate_r, cy + plate_r + int(size*0.05)],
        fill=None, outline="#CCCCCC", width=max(3, size // 30)
    )

    # 餐叉（左侧）
    fork_x = cx - int(size * 0.12)
    fork_top = cy - int(size * 0.3)
    fork_bottom = cy + int(size * 0.25)
    fork_w = max(2, size // 30)
    draw.line([(fork_x, fork_top), (fork_x, fork_bottom)], fill="#CCCCCC", width=fork_w)
    draw.line([(fork_x - int(size*0.06), fork_top), (fork_x - int(size*0.06), fork_top + int(size*0.15))], fill="#CCCCCC", width=fork_w)
    draw.line([(fork_x + int(size*0.06), fork_top), (fork_x + int(size*0.06), fork_top + int(size*0.15))], fill="#CCCCCC", width=fork_w)

    # 餐刀（右侧）
    knife_x = cx + int(size * 0.12)
    draw.line([(knife_x, fork_top + int(size*0.05)), (knife_x, fork_bottom)], fill="#CCCCCC", width=fork_w)

    return img


# 生成 tabbar 图标（81x81）
ICON_SIZE = 81

menu_normal = draw_menu_icon(ICON_SIZE, GRAY)
menu_active = draw_menu_icon(ICON_SIZE, ORANGE)
cart_normal = draw_cart_icon(ICON_SIZE, GRAY)
cart_active = draw_cart_icon(ICON_SIZE, ORANGE)

menu_normal.save(os.path.join(ICONS_DIR, "menu.png"))
menu_active.save(os.path.join(ICONS_DIR, "menu-active.png"))
cart_normal.save(os.path.join(ICONS_DIR, "cart.png"))
cart_active.save(os.path.join(ICONS_DIR, "cart-active.png"))

# 生成默认菜品占位图（400x400）
default_dish = draw_default_dish(400)
default_dish.save(os.path.join(OUTPUT_DIR, "default-dish.png"))

print(f"图标已生成到 {OUTPUT_DIR}")
print("  icons/menu.png")
print("  icons/menu-active.png")
print("  icons/cart.png")
print("  icons/cart-active.png")
print("  default-dish.png")
