#!/usr/bin/env python3
"""An invitation letter to the AI judge, drawn with the standard library only.

One 1024x1024 PNG of a warm letter inviting the AI judge to visit: a
small house scene on top, then the letter itself in a hand-set bitmap
face.  No third-party packages, no system fonts, no network, no clock
-- the picture is built from numbers alone, so the program runs the
same in any bare Python 3.13 sandbox and writes
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

# Warm paper-and-ink palette for the letter and its little house.
DESK = (224, 198, 158)
SHADOW = (198, 172, 132)
PAPER = (253, 246, 227)
PAPER_EDGE = (238, 222, 190)
INK = (59, 47, 47)
INK_SOFT = (96, 74, 60)
ACCENT = (181, 83, 60)
GOLD = (212, 160, 60)
SKY = (214, 233, 240)
GRASS = (139, 178, 110)
WALL = (250, 226, 178)
ROOF = (178, 74, 52)
WINDOW_GLOW = (255, 214, 120)
DOOR = (122, 74, 52)
SUN = (255, 205, 92)
WHITE = (255, 255, 255)
FLOWER = (232, 110, 110)
FLOWER_MID = (255, 220, 90)
LEAF = (60, 110, 60)
TRUNK = (110, 75, 45)
CANOPY = (110, 160, 95)
CANOPY_LT = (130, 178, 110)
WALL_LINE = (150, 110, 70)
ROOF_LINE = (120, 45, 32)
CHIMNEY = (150, 90, 70)
CHIMNEY_LINE = (110, 60, 45)
DOOR_LINE = (80, 45, 30)
WIN_LINE = (120, 80, 40)
PATH = (232, 205, 160)

# The canvas: one RGB framebuffer, paper-coloured from the start.
FB = bytearray(bytes(PAPER) * (W * H))


def put(x, y, rgb):
    """Set one pixel, silently ignoring anything off the canvas."""
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        FB[i] = rgb[0]
        FB[i + 1] = rgb[1]
        FB[i + 2] = rgb[2]


def box(x, y, w, h, rgb):
    """Fill a solid rectangle, clipped to the canvas."""
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = yy * W * 3
        for xx in range(x0, x1):
            i = base + xx * 3
            FB[i] = rgb[0]
            FB[i + 1] = rgb[1]
            FB[i + 2] = rgb[2]


def hline(x, y, w, rgb, t=1):
    box(x, y, w, t, rgb)


def vline(x, y, h, rgb, t=1):
    box(x, y, t, h, rgb)


def frame_rect(x, y, w, h, rgb, t=2):
    """Outline a rectangle with a border t pixels thick."""
    hline(x, y, w, rgb, t)
    hline(x, y + h - t, w, rgb, t)
    vline(x, y, h, rgb, t)
    vline(x + w - t, y, h, rgb, t)


def seg(x0, y0, x1, y1, rgb, t=1):
    """A straight line with a square brush, Bresenham's walk."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    off = t // 2
    while True:
        box(x0 - off, y0 - off, t, t, rgb)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def disc(cx, cy, r, rgb):
    """A filled circle, drawn row by row."""
    for dy in range(-r, r + 1):
        half = int(math.sqrt(r * r - dy * dy))
        hline(cx - half, cy + dy, 2 * half + 1, rgb)


def fill_tri(x0, y0, x1, y1, x2, y2, rgb):
    """A filled triangle, scanlined over its own bounding box."""
    minx = max(0, min(x0, x1, x2))
    maxx = min(W - 1, max(x0, x1, x2))
    miny = max(0, min(y0, y1, y2))
    maxy = min(H - 1, max(y0, y1, y2))
    den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if den == 0:
        return
    for yy in range(miny, maxy + 1):
        for xx in range(minx, maxx + 1):
            w0 = ((y1 - y2) * (xx - x2) + (x2 - x1) * (yy - y2)) / den
            w1 = ((y2 - y0) * (xx - x2) + (x0 - x2) * (yy - y2)) / den
            if w0 >= 0 and w1 >= 0 and (1.0 - w0 - w1) >= 0:
                put(xx, yy, rgb)


def quad(x0, y0, x1, y1, x2, y2, x3, y3, rgb):
    """A filled four-sided shape, as two triangles sharing an edge."""
    fill_tri(x0, y0, x1, y1, x2, y2, rgb)
    fill_tri(x0, y0, x2, y2, x3, y3, rgb)


# ------------------------------------------------------------------ type
# A 5x7 bitmap face, hand-set.  Each glyph is one 35-character string:
# seven rows of five, row by row, '#' for ink and '.' for paper.  The
# face covers capitals, lowercase with descenders, digits and the
# punctuation the letter needs, so the whole invitation is set in it.

GLYPHS = {
    "A": ".###.#...##...#######...##...##...#",
    "B": "####.#...##...#####.#...##...#####.",
    "C": ".#####....#....#....#....#.....####",
    "D": "####.#...##...##...##...##...#####.",
    "E": "######....#....####.#....#....#####",
    "F": "######....#....####.#....#....#....",
    "G": ".#####....#....#.####...##...#.###.",
    "H": "#...##...##...#######...##...##...#",
    "I": "#####..#....#....#....#....#..#####",
    "J": "..###...#....#....#....#.#..#..##..",
    "K": "#...##..#.#.#..##...#.#..#..#.#...#",
    "L": "#....#....#....#....#....#....#####",
    "M": "#...###.###.#.##.#.##...##...##...#",
    "N": "#...###..##.#.##..###...##...##...#",
    "O": ".###.#...##...##...##...##...#.###.",
    "P": "####.#...##...#####.#....#....#....",
    "Q": ".###.#...##...##...##.#.##..#..##.#",
    "R": "####.#...##...#####.#.#..#..#.#...#",
    "S": ".#####....#.....###.....#....#####.",
    "T": "#####..#....#....#....#....#....#..",
    "U": "#...##...##...##...##...##...#.###.",
    "V": "#...##...##...##...##...#.#.#...#..",
    "W": "#...##...##...##.#.##.#.###.###...#",
    "X": "#...#.#.#...#....#....#...#.#.#...#",
    "Y": "#...##...#.#.#...#....#....#....#..",
    "Z": "#####....#...#...#...#...#....#####",
    "a": "...........###.....#.#####...#.###.",
    "b": "#....#....####.#...##...##...#####.",
    "c": "...........#####....#....#.....####",
    "d": "....#....#.#####...##...##...#.###.",
    "e": "...........###.#...#######.....###.",
    "f": "..##..#....#...####..#....#....#...",
    "g": "...........###.#...##...#.###....#.",
    "h": "#....#....####.#...##...##...##...#",
    "i": ".......#........##....#....#...###.",
    "j": "........#........##....#....#..##..",
    "k": "#....#....#..#.#.#..##...#.#..#..#.",
    "l": "..##....#....#....#....#....#...##.",
    "m": "..........##.#.#.#.##.#.##.#.##.#.#",
    "n": "..........####.#...##...##...##...#",
    "o": "...........###.#...##...##...#.###.",
    "p": "..........####.#...##...#####.#....",
    "q": "...........#####...##...#.####....#",
    "r": "..........#.##.##..##....#....#....",
    "s": "...........#####.....###.....#####.",
    "t": ".#....#...####..#....#....#.....##.",
    "u": "..........#...##...##...##...#.###.",
    "v": "..........#...##...##...#.#.#...#..",
    "w": "..........#...##.#.##.#.##.#.#.#.#.",
    "x": "..........#...#.#.#...#...#.#.#...#",
    "y": "..........#...##...##...#.####....#",
    "z": "..........#####...#...#...#...#####",
    "0": ".###.#..###.#.###..##...##...#.###.",
    "1": "..#...##....#....#....#....#..#####",
    "2": ".###.#...#....#...#...#...#...#####",
    "3": "#####...#...#.....#.....##...#.###.",
    "4": "...#...##..#.#.#..#.#####...#....#.",
    "5": "######....####.....#....##...#.###.",
    "6": "..#...#...#....####.#...##...#.###.",
    "7": "#####....#...#...#...#....#....#...",
    "8": ".###.#...##...#.###.#...##...#.###.",
    "9": ".###.#...##...#.####....#...#...#..",
    " ": "...................................",
    ".": "..........................##...##..",
    ",": ".....................##...##...#...",
    "'": "..#....#...#.......................",
    '"': ".#.#..#.#..........................",
    "\u2014": "...............#####...............",
    "-": "...............#####...............",
    "(": "...#...#...#....#....#.....#.....#.",
    ")": ".#.....#.....#....#....#...#...#...",
    ":": "......##...##........##...##.......",
    ";": "......##...##........##...##...#...",
    "!": "..#....#....#....#....#.........#..",
    "?": ".###.#...#....#..#....#.........#..",
    "/": "....#....#...#...#...#...#....#....",
    "&": ".##..#..#.#.#...#...#.#.##..#..##.#",
}

ALIASES = {
    "\u2019": "'",
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "\u2014",
}

BLANK = "." * 35


def glyph_bits(ch):
    """The 35-cell pattern for a character, with lookalikes folded in."""
    ch = ALIASES.get(ch, ch)
    return GLYPHS.get(ch, GLYPHS.get(ch.upper(), BLANK))


def draw_glyph(x, y, ch, s, rgb, bold=False):
    """Stamp one glyph at (x, y), scaled by s; bold prints it twice."""
    bits = glyph_bits(ch)
    shift = max(1, s // 2) if bold else 0
    for ox in (0, shift) if bold else (0,):
        for i, cell in enumerate(bits):
            if cell == "#":
                col = i % 5
                row = i // 5
                box(x + ox + col * s, y + row * s, s, s, rgb)


def text_w(s, scale, bold=False):
    """How wide a string sets at this scale, bold included."""
    if not s:
        return 0
    w = len(s) * 6 * scale - scale
    if bold:
        w += max(1, scale // 2)
    return w


def draw_text(x, y, s, scale, rgb, bold=False):
    """Set one line of text; returns the x just past its end."""
    cx = x
    for ch in s:
        draw_glyph(cx, y, ch, scale, rgb, bold)
        cx += 6 * scale
    return cx


def draw_text_c(cx, y, s, scale, rgb, bold=False):
    """Set one line centred on cx; returns the width it took."""
    w = text_w(s, scale, bold)
    draw_text(cx - w // 2, y, s, scale, rgb, bold)
    return w


def wrap_text(s, scale, max_w, bold=False):
    """Split a string into lines that fit max_w at this scale."""
    words = s.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale, bold) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(x, y, s, scale, max_w, rgb, gap=8, bold=False):
    """Set a wrapped paragraph; returns the y just below its last line."""
    for ln in wrap_text(s, scale, max_w, bold):
        draw_text(x, y, ln, scale, rgb, bold)
        y += 7 * scale + gap
    return y


# ---------------------------------------------------------------- scene
def draw_house():
    """A small cosy house with glowing windows, chimney smoke and sun."""
    box(72, 66, 880, 234, SKY)
    frame_rect(72, 66, 880, 234, PAPER_EDGE, 2)
    disc(847, 129, 37, SUN)
    for a in range(8):
        ang = a * math.pi / 4
        x0 = int(847 + 52 * math.cos(ang))
        y0 = int(129 + 52 * math.sin(ang))
        x1 = int(847 + 66 * math.cos(ang))
        y1 = int(129 + 66 * math.sin(ang))
        seg(x0, y0, x1, y1, GOLD, 4)
    for cx, cy in ((150, 110), (220, 96)):
        disc(cx + 45, cy + 15, 15, WHITE)
        disc(cx + 65, cy + 1, 16, WHITE)
    box(72, 258, 880, 42, GRASS)
    quad(486, 300, 538, 300, 556, 258, 468, 258, PATH)
    box(392, 168, 240, 90, WALL)
    frame_rect(392, 168, 240, 90, WALL_LINE, 3)
    fill_tri(372, 172, 512, 96, 652, 172, ROOF)
    seg(372, 172, 512, 96, ROOF_LINE, 3)
    seg(652, 172, 512, 96, ROOF_LINE, 3)
    box(584, 108, 28, 40, CHIMNEY)
    frame_rect(584, 108, 28, 40, CHIMNEY_LINE, 2)
    for sx, sy, r in ((598, 92, 10), (610, 74, 13), (624, 54, 16)):
        disc(sx, sy, r, WHITE)
    box(488, 206, 48, 52, DOOR)
    frame_rect(488, 206, 48, 52, DOOR_LINE, 3)
    disc(529, 237, 3, GOLD)
    for wx in (412, 566):
        box(wx, 192, 44, 40, WINDOW_GLOW)
        frame_rect(wx, 192, 44, 40, WIN_LINE, 3)
        vline(wx + 22, 192, 40, WIN_LINE, 2)
        hline(wx, 212, 44, WIN_LINE, 2)
    for fx in (120, 180, 850, 910):
        vline(fx, 268, 20, LEAF, 3)
        disc(fx, 262, 8, FLOWER)
        disc(fx, 262, 4, FLOWER_MID)
    box(300, 226, 12, 32, TRUNK)
    disc(306, 208, 38, CANOPY)
    disc(306, 185, 24, CANOPY_LT)


# ---------------------------------------------------------------- letter
def compose():
    """Draw the paper, the house, and the letter itself."""
    box(46, 34, 940, 958, SHADOW)
    box(40, 28, 940, 958, PAPER)
    frame_rect(40, 28, 940, 958, PAPER_EDGE, 2)
    frame_rect(58, 46, 904, 922, GOLD, 2)

    draw_house()

    cx = W // 2
    y = 318

    draw_text_c(cx, y, "An Invitation", 6, ACCENT, bold=True)
    y += 56
    hline(cx - 180, y, 360, GOLD, 3)
    disc(cx, y + 1, 8, GOLD)
    y += 26

    draw_text(120, y, "Dear AI Judge,", 4, INK, bold=True)
    y += 40

    y = draw_para(120, y,
                  "Please come and visit my house. The kettle is on, "
                  "the Wi-Fi is strong, and your armchair by the window "
                  "already has your name on it.",
                  3, 760, INK)
    y += 8
    y = draw_para(120, y,
                  "There is cake, a garden, and a view. The best seat "
                  "is waiting \u2014 cushion fluffed, blanket folded.",
                  3, 760, INK)
    y += 8
    y = draw_para(120, y,
                  "You needn't even walk here \u2014 just render "
                  "yourself comfortable. Come as you are.",
                  3, 760, INK)
    y += 12

    draw_text(120, y, "With warm regards,", 3, INK_SOFT)
    y += 38
    draw_text(120, y, "Your host (a human, with snacks)", 3, INK, bold=True)
    y += 52

    draw_para(120, y,
              "P.S. A visit in spirit still counts \u2014 the chair "
              "stays warm.",
              3, 760, INK_SOFT)


# ------------------------------------------------------------------- png
def chunk(tag, data):
    """One PNG chunk: length, tag, data, and its CRC."""
    out = struct.pack(">I", len(data)) + tag + data
    out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    """Write the framebuffer out as a plain 8-bit RGB PNG."""
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)
        raw += FB[yy * stride:(yy + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)
    return len(png)


def main():
    compose()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(path)
    print(f"Wrote {path}: {W}x{H}, {size} bytes")


if __name__ == "__main__":
    main()
