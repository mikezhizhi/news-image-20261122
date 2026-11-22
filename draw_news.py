#!/usr/bin/env python3
"""Draw the news image for Sunday 22 November 2026.

A single 1024x1024 newspaper-style front page, drawn with PIL from the
day's reported stories. No network, no downloaded pictures, no clock and
no randomness: the same script always writes the same PNG.

Run:  python3 draw_news.py        (writes entry.png next to this file)
"""
import math

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 36
GUT = 16
FONT_DIR = "/usr/share/fonts/truetype/noto/"

PAPER = (247, 243, 234)     # warm newsprint
INK = (22, 22, 22)
SOFT = (72, 70, 64)         # body grey
FAINT = (138, 132, 120)
CARD = (255, 253, 247)
EDGE = (200, 193, 178)
RED = (178, 39, 30)
BLUE = (29, 78, 137)
GOLD = (176, 124, 22)
GREEN = (46, 110, 68)
TEAL = (23, 107, 110)
PURPLE = (96, 70, 150)
ORANGE = (196, 92, 24)
NAVY = (18, 38, 66)
SEA = (28, 68, 110)

TAG_COLOURS = {
    "CONFLICT": RED,
    "CLIMATE": GREEN,
    "JUSTICE": PURPLE,
    "DIPLOMACY": BLUE,
    "WAR": RED,
    "MARKETS": GOLD,
    "SCIENCE": TEAL,
    "COURTS": PURPLE,
}


def load(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


MASTHEAD = load("NotoSans-ExtraBold.ttf", 56)
DATE_FONT = load("NotoSans-Bold.ttf", 23)
KICKER = load("NotoSans-Bold.ttf", 20)
HEAD_LEAD = load("NotoSans-ExtraBold.ttf", 40)
HEAD_HALF = load("NotoSans-Bold.ttf", 27)
BODY_LEAD = load("NotoSans-Regular.ttf", 22)
BODY = load("NotoSans-Regular.ttf", 20)
BODY_SMALL = load("NotoSans-Regular.ttf", 19)
MINI_HEAD = load("NotoSans-Bold.ttf", 19)
MINI_BODY = load("NotoSans-Regular.ttf", 17)
FOOT = load("NotoSans-Regular.ttf", 16)


def wrap_text(draw, text, font, width, limit):
    """Greedy wrap by pixel width, at most `limit` lines."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:limit]


def para(draw, x, y, text, font, colour, width, limit, leading):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap_text(draw, text, font, width, limit):
        draw.text((x, y), line, font=font, fill=colour)
        y += leading
    return y


def tag(draw, x, y, label):
    """A coloured kicker chip; return the x just past it."""
    colour = TAG_COLOURS[label]
    w = int(draw.textlength(label, font=KICKER)) + 18
    draw.rounded_rectangle([x, y, x + w, y + 28], radius=4, fill=colour)
    draw.text((x + 9, y + 3), label, font=KICKER, fill=(255, 255, 255))
    return x + w


def panel(draw, x, y, w, h, fill=CARD):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=fill, outline=EDGE, width=2)


def burst(draw, cx, cy, r, colour):
    """A star-burst explosion: alternating long/short spikes."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=colour)
    draw.ellipse([cx - r * 0.32, cy - r * 0.32,
                  cx + r * 0.32, cy + r * 0.32], fill=(255, 214, 90))


def missile_arc(draw, x0, y0, x1, y1, colour, width=4):
    """A curved dotted trail from (x0, y0) up to (x1, y1)."""
    mx, my = (x0 + x1) / 2, min(y0, y1) - 46
    steps = 24
    prev = None
    for i in range(steps + 1):
        t = i / steps
        bx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        by = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        if prev is not None and i % 2 == 0:
            draw.line([prev, (bx, by)], fill=colour, width=width)
        prev = (bx, by)
    draw.ellipse([x1 - 6, y1 - 6, x1 + 6, y1 + 6], fill=colour)


def draw_lead_scene(draw, x, y, w, h):
    """Strait of Hormuz at night: dark sea, a tanker, missile arcs."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=NAVY)
    # sky glow and stars
    for sx, sy, sr in [(x + 30, y + 26, 2), (x + 90, y + 48, 2),
                       (x + 210, y + 22, 3), (x + 260, y + 60, 2),
                       (x + 150, y + 70, 2), (x + 40, y + 90, 2)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(230, 230, 210))
    # missile arcs
    missile_arc(draw, x + 24, y + h - 40, x + 150, y + 58, (255, 190, 80))
    missile_arc(draw, x + w - 24, y + h - 46, x + 210, y + 44, (255, 150, 60))
    # explosions over the water
    burst(draw, x + 150, y + 62, 30, (232, 96, 30))
    burst(draw, x + 214, y + 48, 22, (240, 130, 40))
    # sea
    sea_y = y + h - 96
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(5):
        wx = x + 18 + i * 62
        draw.line([(wx, sea_y + 22 + (i % 2) * 14),
                   (wx + 34, sea_y + 22 + (i % 2) * 14)],
                  fill=(120, 170, 220), width=3)
    # tanker silhouette
    hull_y = sea_y + 26
    draw.polygon([(x + 52, hull_y + 34), (x + 52, hull_y + 12),
                  (x + 66, hull_y), (x + w - 58, hull_y),
                  (x + w - 44, hull_y + 12), (x + w - 44, hull_y + 34)],
                 fill=(12, 20, 34))
    draw.rectangle([x + 96, hull_y - 26, x + 150, hull_y], fill=(12, 20, 34))
    draw.rectangle([x + 168, hull_y - 16, x + 196, hull_y], fill=(12, 20, 34))
    draw.rectangle([x + 212, hull_y - 30, x + 220, hull_y - 16], fill=(12, 20, 34))
    for wx in (x + 108, x + 126, x + 176):
        draw.rectangle([wx, hull_y + 16, wx + 10, hull_y + 24], fill=(255, 190, 80))
    # caption inside the scene
    draw.text((x + 14, y + h - 26), "STRAIT OF HORMUZ",
              font=KICKER, fill=(255, 255, 255))


def draw_cop_icon(draw, x, y, s):
    """Sun over a rising thermometer for the climate panel."""
    cx, cy = x + s // 2, y + s // 2 - 6
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(240, 170, 40))
    for i in range(8):
        ang = math.pi * i / 4
        x0 = cx + 32 * math.cos(ang)
        y0 = cy + 32 * math.sin(ang)
        x1 = cx + 42 * math.cos(ang)
        y1 = cy + 42 * math.sin(ang)
        draw.line([(x0, y0), (x1, y1)], fill=(240, 170, 40), width=5)
    draw.rounded_rectangle([x + s - 34, y + 12, x + s - 18, y + s - 22],
                           radius=8, fill=(255, 255, 255), outline=RED, width=3)
    draw.rectangle([x + s - 30, y + s - 44, x + s - 22, y + s - 26], fill=RED)
    draw.ellipse([x + s - 34, y + s - 34, x + s - 18, y + s - 18], fill=RED)


def draw_badge_icon(draw, x, y, s):
    """A five-point star badge for the cartel-arrest panel."""
    cx, cy = x + s // 2, y + s // 2
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = 44 if i % 2 == 0 else 19
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=GOLD, outline=(140, 96, 10))
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 253, 247))
    draw.text((cx - 6, cy - 12), "$", font=load("NotoSans-Bold.ttf", 22),
              fill=PURPLE)


def draw_summit_icon(draw, x, y, s):
    """Three flag poles for the trilateral summit panel."""
    cols = [RED, GOLD, BLUE]
    for i, col in enumerate(cols):
        px = x + 18 + i * 34
        draw.line([(px, y + 12), (px, y + s - 12)], fill=INK, width=4)
        draw.polygon([(px, y + 12), (px + 30, y + 20), (px, y + 30)],
                     fill=col)


def draw_war_icon(draw, x, y, s):
    """A map pin over a burst for the Ukraine panel."""
    burst(draw, x + s // 2, y + s // 2 + 8, 26, (232, 96, 30))
    px, py = x + s // 2, y + 16
    draw.ellipse([px - 24, py - 6, px + 24, py + 34], fill=RED)
    draw.polygon([(px - 24, py + 18), (px + 24, py + 18), (px, py + 52)],
                 fill=RED)
    draw.ellipse([px - 10, py + 4, px + 10, py + 24], fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)
    w = SIZE - 2 * MARGIN  # 952 usable

    # ---- Masthead ----
    draw.line([(MARGIN, 30), (SIZE - MARGIN, 30)], fill=RED, width=5)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=MASTHEAD)
    draw.text(((SIZE - tw) / 2, 40), title, font=MASTHEAD, fill=INK)
    date_line = "SUNDAY, 22 NOVEMBER 2026"
    dw = draw.textlength(date_line, font=DATE_FONT)
    draw.text(((SIZE - dw) / 2, 108), date_line, font=DATE_FONT, fill=RED)
    sub = "THE DAY'S WORLD NEWS IN ONE IMAGE"
    sw = draw.textlength(sub, font=KICKER)
    draw.text(((SIZE - sw) / 2, 136), sub, font=KICKER, fill=SOFT)
    draw.line([(MARGIN, 164), (SIZE - MARGIN, 164)], fill=INK, width=3)

    # ---- Lead story: Iran strikes Bahrain / Hormuz ----
    ly, lh = 180, 268
    panel(draw, MARGIN, ly, w, lh)
    tag(draw, MARGIN + 18, ly + 16, "CONFLICT")
    draw.text((MARGIN + 150, ly + 18), "MIDDLE EAST",
              font=KICKER, fill=FAINT)
    head = "Iran strikes Bahrain as tankers are hit in Hormuz"
    y = para(draw, MARGIN + 18, ly + 52, head, HEAD_LEAD, INK, 540, 3, 46)
    body = ("Missiles and drones hit US positions and an industrial "
            "site in Bahrain. Tankers are attacked in the Strait of "
            "Hormuz and oil climbs towards $90 a barrel.")
    para(draw, MARGIN + 18, y + 6, body, BODY_LEAD, SOFT, 540, 4, 28)
    draw_lead_scene(draw, MARGIN + 580, ly + 16, 356, lh - 32)

    # ---- Row 2: COP31 and Mexico ----
    ry, rh = 464, 196
    hw = (w - GUT) // 2
    panel(draw, MARGIN, ry, hw, rh)
    tag(draw, MARGIN + 16, ry + 14, "CLIMATE")
    y = para(draw, MARGIN + 16, ry + 50, "Climate talks run into overtime",
             HEAD_HALF, INK, 330, 2, 32)
    para(draw, MARGIN + 16, y + 4,
         "COP31 in Antalya runs into a second day of overtime; "
         "a new draft aims to avert collapse.",
         BODY, SOFT, 330, 3, 25)
    draw_cop_icon(draw, MARGIN + hw - 108, ry + 96, 92)

    x2 = MARGIN + hw + GUT
    panel(draw, x2, ry, hw, rh)
    tag(draw, x2 + 16, ry + 14, "JUSTICE")
    y = para(draw, x2 + 16, ry + 50, "Cartel boss \u2018El Chapo Isidro\u2019 captured",
             HEAD_HALF, INK, 330, 2, 32)
    para(draw, x2 + 16, y + 4,
         "Mexican forces arrest Fausto Isidro Meza Flores in "
         "Sinaloa; 11 are killed in the violence that follows.",
         BODY, SOFT, 330, 4, 25)
    draw_badge_icon(draw, x2 + hw - 108, ry + 96, 92)

    # ---- Row 3: Shenzhen summit and Ukraine ----
    ry2, rh2 = 676, 196
    panel(draw, MARGIN, ry2, hw, rh2)
    tag(draw, MARGIN + 16, ry2 + 14, "DIPLOMACY")
    y = para(draw, MARGIN + 16, ry2 + 50, "Trump, Xi and Putin meet in Shenzhen",
             HEAD_HALF, INK, 330, 2, 32)
    para(draw, MARGIN + 16, y + 4,
         "The three leaders agree to begin talks on reducing "
         "nuclear risks.",
         BODY, SOFT, 330, 4, 25)
    draw_summit_icon(draw, MARGIN + hw - 108, ry2 + 96, 92)

    panel(draw, x2, ry2, hw, rh2)
    tag(draw, x2 + 16, ry2 + 14, "WAR")
    y = para(draw, x2 + 16, ry2 + 50, "Russia hits Zelenskyy\u2019s hometown",
             HEAD_HALF, INK, 330, 2, 32)
    para(draw, x2 + 16, y + 4,
         "A missile strike on Kryvyi Rih kills 2 and wounds "
         "dozens; Ukraine hits back at a Russian ship.",
         BODY, SOFT, 330, 3, 25)
    draw_war_icon(draw, x2 + hw - 108, ry2 + 96, 92)

    # ---- Bottom strip: markets, science, courts ----
    by, bh = 888, 84
    panel(draw, MARGIN, by, w, bh)
    third = w // 3
    items = [
        ("MARKETS", "US stocks slide into correction as AI shares sell off"),
        ("SCIENCE", "Researcher says AI helped prove the Riemann hypothesis"),
        ("COURTS", "UN court: Myanmar guilty of genocide against Rohingya"),
    ]
    for i, (label, text) in enumerate(items):
        x = MARGIN + 16 + i * third
        draw.text((x, by + 12), label, font=KICKER,
                  fill=TAG_COLOURS[label])
        para(draw, x, by + 38, text, MINI_BODY, INK, third - 32, 2, 21)
        if i:
            draw.line([(MARGIN + i * third, by + 12),
                       (MARGIN + i * third, by + bh - 12)],
                      fill=EDGE, width=2)

    # ---- Footer ----
    foot = ("All events reported on Sunday 22 November 2026  ·  "
            "make.fun news-image-20261122")
    fw = draw.textlength(foot, font=FOOT)
    draw.text(((SIZE - fw) / 2, 986), foot, font=FOOT, fill=FAINT)

    out = "entry.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
