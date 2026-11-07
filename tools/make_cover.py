# -*- coding: utf-8 -*-
"""生成 ElegantBook 封面与徽标（PNG）。仅依赖 Pillow。"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

FONT_DIR = r"C:\Windows\Fonts"
YAHEI_BD = os.path.join(FONT_DIR, "msyhbd.ttc")
YAHEI = os.path.join(FONT_DIR, "msyh.ttc")
CONSOLA = os.path.join(FONT_DIR, "consola.ttf")
CONSOLA_BD = os.path.join(FONT_DIR, "consolab.ttf")

W, H = 1654, 2339
NAVY_TOP = (7, 18, 33)
NAVY_BOT = (17, 46, 78)
TEAL = (64, 196, 210)
TEAL_DIM = (44, 130, 150)
ORANGE = (232, 138, 62)
WHITE = (244, 247, 250)


def gradient(w, h, top, bot):
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        # 轻微非线性，底部更亮
        t = t ** 0.85
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def add_grid(img, step=64, alpha=14):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, img.width, step):
        d.line([(x, 0), (x, img.height)], fill=(120, 200, 220, alpha), width=1)
    for y in range(0, img.height, step):
        d.line([(0, y), (img.width, y)], fill=(120, 200, 220, alpha), width=1)
    return Image.alpha_composite(img.convert("RGBA"), layer)


def add_rings(img, cx, cy, rmax=1500, rmin=90, n=22):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(n):
        r = rmin + (rmax - rmin) * (i / (n - 1)) ** 1.6
        a = int(58 * (1 - i / n) + 6)
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  outline=(70, 200, 215, a), width=2 if i < 6 else 1)
    # 十字准线
    d.line([(cx - 40, cy), (cx + 40, cy)], fill=(200, 240, 245, 90), width=2)
    d.line([(cx, cy - 40), (cx, cy + 40)], fill=(200, 240, 245, 90), width=2)
    return Image.alpha_composite(img.convert("RGBA"), layer)


def add_points(img, cx, cy, random_seed=7):
    random.seed(random_seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    # 环形无序点云
    for _ in range(2600):
        ang = random.uniform(0, 2 * math.pi)
        rr = random.gauss(0, 0.34)
        r = abs(rr) * 1500
        if r < 120:
            continue
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang) * 0.62 + random.gauss(0, 18)
        if 0 <= x < img.width and 0 <= y < img.height:
            s = random.choice([1, 1, 1, 2, 2, 3])
            a = random.randint(35, 135)
            col = (150, 225, 235, a) if random.random() > 0.18 else (240, 170, 90, a)
            d.ellipse([x - s, y - s, x + s, y + s], fill=col)
            pts.append((x, y))
    # 稀疏点连线，模拟扫描线
    for _ in range(140):
        if len(pts) < 2:
            break
        x1, y1 = random.choice(pts)
        x2 = x1 + random.uniform(-160, 160)
        y2 = y1 + random.uniform(-10, 10)
        d.line([(x1, y1), (x2, y2)], fill=(120, 210, 225, random.randint(8, 30)), width=1)
    return Image.alpha_composite(img.convert("RGBA"), layer)


def add_vignette(img, strength=110):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    for i in range(strength):
        a = int(255 * (i / strength) ** 2.2)
        d.rectangle([i, i, w - 1 - i, h - 1 - i], outline=0)
    # 用径向渐变代替：中心亮四周暗
    grad = Image.new("L", (w, h), 0)
    gd = ImageDraw.Draw(grad)
    cx, cy = w / 2, h * 0.42
    maxd = math.hypot(w / 2, h / 2)
    step = 8
    for y in range(0, h, step):
        for x in range(0, w, step):
            dd = math.hypot(x - cx, y - cy) / maxd
            v = int(max(0, min(255, 255 * (1 - 0.55 * dd ** 2))))
            gd.rectangle([x, y, x + step, y + step], fill=v)
    grad = grad.filter(ImageFilter.GaussianBlur(24))
    black = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    black.putalpha(Image.eval(grad, lambda v: 255 - v))
    return Image.alpha_composite(img.convert("RGBA"), black)


def fit_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def draw_center(d, text, font, y, fill, anchor="mm", x=W // 2):
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)


def make_cover():
    img = gradient(W, H, NAVY_TOP, NAVY_BOT)
    img = add_grid(img, 64, 12)
    img = add_rings(img, int(W * 0.70), int(H * 0.80), 1500, 90, 24)
    img = add_points(img, int(W * 0.70), int(H * 0.80))
    # 顶部/底部渐变压暗
    img = add_vignette(img)

    d = ImageDraw.Draw(img)
    f_title = fit_font(YAHEI_BD, 196)
    f_title2 = fit_font(YAHEI_BD, 196)
    f_sub = fit_font(YAHEI, 66)
    f_en = fit_font(CONSOLA_BD, 34)
    f_meta = fit_font(YAHEI, 40)
    f_small = fit_font(CONSOLA, 26)

    # 顶部细线 + 英文小标
    d.line([(140, 250), (W - 140, 250)], fill=(90, 200, 215, 120), width=2)
    d.text((140, 285), "LOCALIZATION  &  NAVIGATION  HANDBOOK",
           font=f_en, fill=(120, 200, 215, 220))

    # 主标题（两行）
    draw_center(d, "定位与导航", f_title, 760, WHITE)
    draw_center(d, "技术文档", f_title2, 980, (150, 220, 232))

    # 分隔短线
    d.line([(W // 2 - 90, 1092), (W // 2 + 90, 1092)], fill=ORANGE, width=6)

    # 副标题
    draw_center(d, "从里程计到 SLAM，从建图到自主导航", f_sub, 1178, (205, 225, 238))

    # 底部信息
    d.line([(140, H - 360), (W - 140, H - 360)], fill=(90, 200, 215, 70), width=1)
    d.text((140, H - 320), "算法组  ·  RoboMaster", font=f_meta, fill=(190, 215, 230))
    d.text((W - 140, H - 320), "2026.11", font=f_meta, fill=(190, 215, 230), anchor="ra")
    d.text((140, H - 250),
           "FAST-LIO2 / Point-LIO / Cartographer / Nav2 / Z-Localization",
           font=f_small, fill=(110, 165, 185, 220))

    img = img.convert("RGB")
    path = os.path.join(OUT, "cover.png")
    img.save(path, quality=95)
    print("saved", path, img.size)


def make_logo():
    S = 640
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = S // 2
    # 外环
    d.ellipse([c - 290, c - 290, c + 290, c + 290],
              outline=(60, 180, 200, 230), width=18)
    # 内环
    d.ellipse([c - 205, c - 205, c + 205, c + 205],
              outline=(60, 180, 200, 120), width=6)
    # 刻度
    for k in range(72):
        ang = 2 * math.pi * k / 72
        r1 = 290
        r2 = 255 if k % 6 else 230
        d.line([(c + r1 * math.cos(ang), c + r1 * math.sin(ang)),
                (c + r2 * math.cos(ang), c + r2 * math.sin(ang))],
               fill=(70, 190, 210, 190), width=3 if k % 6 == 0 else 2)
    # 十字准线
    d.line([(c - 150, c), (c + 150, c)], fill=(200, 240, 248, 160), width=4)
    d.line([(c, c - 150), (c, c + 150)], fill=(200, 240, 248, 160), width=4)
    # 指针（罗盘）
    d.polygon([(c, c - 175), (c + 34, c - 18), (c, c - 34), (c - 34, c - 18)],
              fill=(232, 138, 62, 245))
    d.polygon([(c, c + 175), (c + 30, c + 20), (c, c + 34), (c - 30, c + 20)],
              fill=(60, 180, 200, 200))
    # 中心点
    d.ellipse([c - 16, c - 16, c + 16, c + 16], fill=(235, 245, 250, 255))
    path = os.path.join(OUT, "logo.png")
    img.save(path)
    print("saved", path, img.size)


if __name__ == "__main__":
    make_cover()
    make_logo()
