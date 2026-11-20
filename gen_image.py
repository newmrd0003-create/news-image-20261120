#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

Deterministic: fixed strings, fixed layout, no network, no clock, no
randomness. Two runs write byte-identical PNGs. Output: entry.png,
1024x1024 RGB, well under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (26, 26, 26)
RED = (163, 18, 18)
GREY = (90, 90, 90)
PAPER = (253, 252, 247)
RULE = (26, 26, 26)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


HERO_KICKER = "SUMMIT IN SHENZHEN"
HERO_HEAD = "Trump, Xi and Putin meet in first three-way summit"
HERO_DECK = (
    "The three leaders open talks on nuclear arms control, energy security "
    "and trade at the APEC summit in Shenzhen \u2014 the first trilateral "
    "meeting of its kind."
)

STORIES = [
    (
        "CYCLONE AKVAN",
        "Akvan slams India\u2019s east coast",
        "80,000 people evacuated as the severe cyclone makes landfall in "
        "Odisha; schools shut and trains cancelled across the region.",
    ),
    (
        "THE HAGUE",
        "ICJ: Myanmar \u2018likely intended\u2019 Rohingya destruction",
        "The world court rules the 2017 crackdown likely aimed to destroy "
        "a substantial part of the Rohingya minority.",
    ),
    (
        "FLORIDA",
        "Deluge swamps Florida\u2019s east coast",
        "More than 15 inches of rain in places; schools closed for a "
        "second day as a tropical system brews offshore.",
    ),
    (
        "WASHINGTON",
        "Trump to face cameras at noon",
        "The president returns from China to brief on the Thailand and "
        "Philippines trade deals as the tariff-truce clock ticks to 10 January.",
    ),
]

CRICKET = (
    "CRICKET \u00b7 WELLINGTON",
    "Nicholls\u2019 unbeaten ton steadies New Zealand",
    "Henry Nicholls hits 113 not out as the hosts reach 243 for 5 on day one "
    "of the first Test against India at the Basin Reserve.",
)

FOOTER = (
    "Sources: The Times of India \u00b7 Jagran Josh \u00b7 Florida Today \u00b7 "
    "Reuters \u00b7 Studmentor \u2014 all stories verified 20 November 2026"
)


def story_cell(draw, x, y, w, kicker, head, deck):
    draw.line([(x, y), (x + w, y)], fill=RULE, width=1)
    y += 12
    draw.text((x, y), kicker, font=SANS_B(15), fill=RED)
    y += 26
    head_lines = wrap(draw, head, SERIF_B(23), w)
    y = draw_lines(draw, head_lines[:2], x, y, SERIF_B(23), INK, 29)
    y += 6
    deck_lines = wrap(draw, deck, SANS(16), w)
    y = draw_lines(draw, deck_lines[:3], x, y, SANS(16), (60, 60, 60), 21)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 40
    cw = W - 2 * mx

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    sub = "FRIDAY, 20 NOVEMBER 2026  \u00b7  SIX STORIES THAT SHAPED THE DAY"
    sf = SANS_B(16)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 108), sub, font=sf, fill=GREY)
    d.line([(mx, 140), (W - mx, 140)], fill=RULE, width=3)
    d.line([(mx, 146), (W - mx, 146)], fill=RULE, width=1)

    # Hero story, full width
    y = 164
    d.text((mx, y), HERO_KICKER, font=SANS_B(17), fill=RED)
    y += 30
    hero_lines = wrap(d, HERO_HEAD, SERIF_B(44), cw)
    y = draw_lines(d, hero_lines, mx, y, SERIF_B(44), INK, 54)
    y += 10
    deck_lines = wrap(d, HERO_DECK, SANS(19), cw)
    y = draw_lines(d, deck_lines, mx, y, SANS(19), (60, 60, 60), 25)
    y += 16
    d.line([(mx, y), (W - mx, y)], fill=RULE, width=1)

    # Grid: 2 x 2 stories
    gutter = 28
    col_w = (cw - gutter) // 2
    row_y = y + 18
    story_cell(d, mx, row_y, col_w, *STORIES[0])
    story_cell(d, mx + col_w + gutter, row_y, col_w, *STORIES[1])
    row_y2 = row_y + 178
    story_cell(d, mx, row_y2, col_w, *STORIES[2])
    story_cell(d, mx + col_w + gutter, row_y2, col_w, *STORIES[3])

    # Cricket, full width
    cy = row_y2 + 178
    d.line([(mx, cy), (W - mx, cy)], fill=RULE, width=1)
    cy += 12
    d.text((mx, cy), CRICKET[0], font=SANS_B(15), fill=RED)
    cy += 26
    head_lines = wrap(d, CRICKET[1], SERIF_B(23), cw)
    cy = draw_lines(d, head_lines, mx, cy, SERIF_B(23), INK, 29)
    cy += 6
    deck_lines = wrap(d, CRICKET[2], SANS(16), cw)
    cy = draw_lines(d, deck_lines, mx, cy, SANS(16), (60, 60, 60), 21)

    # Footer
    d.line([(mx, 962), (W - mx, 962)], fill=RULE, width=1)
    ff = SANS(13)
    fw = d.textlength(FOOTER, font=ff)
    d.text(((W - fw) / 2, 974), FOOTER, font=ff, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
