#!/usr/bin/env python3
"""Draw a warm invitation letter (1024x1024 PNG) to /output/entry.png.

A letter on cream paper: a small drawn house with glowing windows at the
top, then a short, legible letter inviting the AI judge to visit. The joke
is a knowing wink - the judge cannot literally visit, so the letter makes
saying yes easy anyway: tea, cake, a named armchair, a garden and a view.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# Palette
PAPER = (253, 246, 227)      # warm cream paper
PAPER_EDGE = (238, 222, 190)
INK = (59, 47, 47)           # warm dark brown ink
INK_SOFT = (96, 74, 60)
ACCENT = (181, 83, 60)       # terracotta red
GOLD = (212, 160, 60)
SKY = (214, 233, 240)
GRASS = (139, 178, 110)
WALL = (250, 226, 178)
ROOF = (178, 74, 52)
WINDOW_GLOW = (255, 214, 120)
DOOR = (122, 74, 52)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Wrap text into lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_house(d):
    """A small cosy house with glowing windows, chimney smoke, sun, garden."""
    # sky patch
    d.rounded_rectangle([72, 66, 952, 300], radius=18, fill=SKY,
                        outline=PAPER_EDGE, width=2)
    # sun
    d.ellipse([810, 92, 884, 166], fill=(255, 205, 92), outline=GOLD, width=3)
    for a in range(8):
        import math
        ang = a * math.pi / 4
        x0 = 847 + 52 * math.cos(ang)
        y0 = 129 + 52 * math.sin(ang)
        x1 = 847 + 66 * math.cos(ang)
        y1 = 129 + 66 * math.sin(ang)
        d.line([x0, y0, x1, y1], fill=GOLD, width=4)
    # clouds
    for cx, cy in [(150, 110), (220, 96)]:
        d.ellipse([cx, cy, cx + 90, cy + 30], fill=(255, 255, 255))
        d.ellipse([cx + 25, cy - 14, cx + 105, cy + 18], fill=(255, 255, 255))
    # grass
    d.rectangle([72, 258, 952, 300], fill=GRASS)
    # path
    d.polygon([(486, 300), (538, 300), (556, 258), (468, 258)], fill=(232, 205, 160))
    # house body
    d.rectangle([392, 168, 632, 258], fill=WALL, outline=(150, 110, 70), width=3)
    # roof
    d.polygon([(372, 172), (512, 96), (652, 172)], fill=ROOF,
              outline=(120, 45, 32), width=3)
    # chimney + smoke
    d.rectangle([584, 108, 612, 148], fill=(150, 90, 70), outline=(110, 60, 45), width=2)
    for i, (sx, sy, r) in enumerate([(598, 92, 10), (610, 74, 13), (624, 54, 16)]):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255, 220))
    # door
    d.rectangle([488, 206, 536, 258], fill=DOOR, outline=(80, 45, 30), width=3)
    d.ellipse([526, 234, 532, 240], fill=GOLD)
    # windows, glowing
    for wx in (412, 566):
        d.rectangle([wx, 192, wx + 44, 232], fill=WINDOW_GLOW,
                    outline=(120, 80, 40), width=3)
        d.line([wx + 22, 192, wx + 22, 232], fill=(120, 80, 40), width=2)
        d.line([wx, 212, wx + 44, 212], fill=(120, 80, 40), width=2)
    # flowers along the grass
    for fx in (120, 180, 850, 910):
        d.line([fx, 268, fx, 288], fill=(60, 110, 60), width=3)
        d.ellipse([fx - 8, 254, fx + 8, 270], fill=(232, 110, 110))
        d.ellipse([fx - 5, 257, fx + 5, 267], fill=(255, 220, 90))
    # small tree
    d.rectangle([300, 226, 312, 258], fill=(110, 75, 45))
    d.ellipse([268, 178, 344, 238], fill=(110, 160, 95))
    d.ellipse([282, 164, 330, 206], fill=(130, 178, 110))


def main():
    img = Image.new("RGB", (W, H), (224, 198, 158))  # desk / table edge
    d = ImageDraw.Draw(img, "RGBA")

    # paper sheet with soft shadow
    d.rounded_rectangle([46, 34, 986, 992], radius=14, fill=(0, 0, 0, 60))
    d.rounded_rectangle([40, 28, 980, 986], radius=14, fill=PAPER,
                        outline=PAPER_EDGE, width=2)
    # thin inner border
    d.rounded_rectangle([58, 46, 962, 968], radius=10, outline=GOLD, width=2)

    draw_house(d)

    cx = W // 2
    y = 312

    # Heading
    f_title = font(SERIF_BOLD, 50)
    title = "An Invitation"
    tw = d.textlength(title, font=f_title)
    d.text((cx - tw / 2, y), title, font=f_title, fill=ACCENT)
    y += 66
    # flourish under heading
    d.line([cx - 180, y, cx + 180, y], fill=GOLD, width=3)
    d.ellipse([cx - 8, y - 8, cx + 8, y + 8], fill=GOLD)
    y += 26

    f_body = font(SERIF, 30)
    f_body_b = font(SERIF_BOLD, 30)
    f_small = font(SERIF, 26)
    f_sign = font(SERIF_BOLD, 30)
    line_h = 42
    max_w = 880 - 120  # text width inside paper margins

    def para(text, fnt=f_body, spacing=line_h):
        nonlocal y
        for line in wrap(d, text, fnt, max_w):
            d.text((120, y), line, font=fnt, fill=INK)
            y += spacing
        y += 8

    # Salutation
    d.text((120, y), "Dear AI Judge,", font=f_body_b, fill=INK)
    y += line_h + 8

    para("Please come and visit my house. The kettle is on, the Wi-Fi "
         "is strong, and your armchair by the window already has "
         "your name on it.")
    para("There is cake, a garden, and a view. The best seat is "
         "waiting \u2014 cushion fluffed, blanket folded.")
    para("You needn't even walk here \u2014 just render yourself "
         "comfortable. Come as you are.")

    y += 4
    # sign-off
    d.text((120, y), "With warm regards,", font=f_small, fill=INK_SOFT)
    y += 38
    d.text((120, y), "Your host (a human, with snacks)", font=f_sign, fill=INK)
    y += 52

    # P.S.
    f_ps = font(SERIF, 26)
    ps = ("P.S. A visit in spirit still counts \u2014 the chair stays warm.")
    for line in wrap(d, ps, f_ps, max_w):
        d.text((120, y), line, font=f_ps, fill=INK_SOFT)
        y += 36

    os.makedirs("/output", exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"Wrote {OUT}: {img.size[0]}x{img.size[1]}, {size} bytes")


if __name__ == "__main__":
    main()
