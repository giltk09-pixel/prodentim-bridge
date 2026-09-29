# -*- coding: utf-8 -*-
"""Gera os assets da bridge page: product webp/png, favicon e og-image 1200x630."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SRC_PRODUCT = r"C:\PRODENTIM\PRODUCT PIC-LABEL\PICTURE 1.png"
ASSETS.mkdir(exist_ok=True)

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"


def build_product():
    im = Image.open(SRC_PRODUCT).convert("RGBA")
    im.thumbnail((900, 900), Image.LANCZOS)
    im.save(ASSETS / "product.webp", "WEBP", quality=88, method=6)
    im.save(ASSETS / "product.png", "PNG", optimize=True)
    print("product:", im.size)


def build_favicon():
    base = Image.open(SRC_PRODUCT).convert("RGBA")
    side = min(base.size)
    left = (base.width - side) // 2
    top = (base.height - side) // 2
    crop = base.crop((left, top, left + side, top + side)).resize((64, 64), Image.LANCZOS)
    canvas = Image.new("RGBA", (64, 64), (13, 110, 168, 255))
    crop.thumbnail((56, 56), Image.LANCZOS)
    canvas.paste(crop, ((64 - crop.width) // 2, (64 - crop.height) // 2), crop)
    canvas.save(ASSETS / "favicon.png", "PNG", optimize=True)
    print("favicon ok")


def wrap(draw, text, max_w, f):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    c1, c2 = (13, 110, 168), (10, 74, 118)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(c1, c2)))

    d.rectangle([0, 0, W, 78], fill=(255, 193, 7))
    f_eyebrow = ImageFont.truetype(FONT_BOLD, 34)
    eye = "THE 30-SECOND MORNING HABIT FOR ADULTS 45+"
    d.text(((W - d.textlength(eye, font=f_eyebrow)) // 2, 21), eye, font=f_eyebrow,
           fill=(20, 50, 75))

    f_h = ImageFont.truetype(FONT_BOLD, 62)
    lines = wrap(d, "Bleeding Gums Mean Your Mouth Is Full Of Tooth-Eating Bacteria",
                 700, f_h)
    y = 130
    for ln in lines:
        d.text((60, y), ln, font=f_h, fill=(255, 255, 255))
        y += f_h.size + 12

    f_s = ImageFont.truetype(FONT_REG, 30)
    for ln in wrap(d, "The simple habit thousands of adults add after brushing.",
                   700, f_s):
        d.text((60, y + 16), ln, font=f_s, fill=(214, 236, 250))
        y += 44

    prod = Image.open(SRC_PRODUCT).convert("RGBA")
    prod.thumbnail((430, 430), Image.LANCZOS)
    img.paste(prod, (W - prod.width - 55, (H - prod.height) // 2 + 30), prod)

    f_btn = ImageFont.truetype(FONT_BOLD, 34)
    btn_t = "SHOW ME THE 30-SECOND HABIT"
    bw = d.textlength(btn_t, font=f_btn) + 70
    bx, by = 60, H - 110
    d.rounded_rectangle([bx, by, bx + bw, by + 72], radius=36, fill=(255, 193, 7))
    d.text((bx + 35, by + 17), btn_t, font=f_btn, fill=(25, 45, 65))

    img.save(ASSETS / "og-image.jpg", "JPEG", quality=86, optimize=True)
    print("og-image ok", img.size)


if __name__ == "__main__":
    build_product()
    build_favicon()
    build_og()
