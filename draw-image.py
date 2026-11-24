#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news image for make.fun news-image-20261123.

One 1024x1024 PNG: a broadsheet front page with six story panels, each with a
simple drawn pictogram, a kicker, a self-contained headline and a short body
line. Every story was verified against at least two independent sources as
having happened or first been reported on 23 November 2026.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
F_REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# --- palette ---
PAPER = (247, 243, 232)
NAVY = (27, 42, 74)
NAVY_DARK = (20, 32, 58)
INK = (32, 38, 54)
BODY = (74, 78, 88)
FOOT = (110, 112, 118)
WHITE = (255, 255, 255)
BORDER = (214, 208, 192)
SUB = (168, 188, 216)

# --- stories: (accent, kicker, headline, body, pictogram) ---
STORIES = [
    (
        (139, 69, 19),  # brown
        "WAR AT SEA \u00b7 LIBYA",
        "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
        "Zelenskyy says seven sea drones sank the corvette Merkury at Benghazi; a helicopter aboard was destroyed.",
        "ship",
    ),
    (
        (43, 84, 158),  # blue
        "EUROPE \u00b7 POLAND",
        "NATO SENDS SPY PLANE TO POLAND",
        "After three Russian missiles crashed in Poland on Friday, the alliance meets in Brussels and sends an AWACS early-warning jet.",
        "radar",
    ),
    (
        (27, 120, 88),  # green
        "MARKETS \u00b7 TECH",
        "NVIDIA BRINGS BACK HUANG, SHARES SOAR 31%",
        "The board reinstates Jensen Huang as chief executive 11 days after he quit; the S&P 500 jumps 4.7%.",
        "chip",
    ),
    (
        (14, 122, 122),  # teal
        "ASIA \u00b7 AID",
        "INDIA GIVES NEPAL $1.62 BILLION",
        "Modi announces the package in New Delhi after talks with PM Balendra Shah, to rebuild after August's glacier flood.",
        "mountain",
    ),
    (
        (198, 84, 24),  # orange
        "ASIA \u00b7 DISASTER",
        "24 DEAD IN INDONESIA FACTORY FIRE",
        "Indonesia confirms the toll from the blaze at a candy plant in Cikande, Banten; about 30 people are still missing.",
        "flame",
    ),
    (
        (96, 74, 158),  # purple
        "MIDDLE EAST \u00b7 SANCTIONS",
        "US SANCTIONS IRAN'S SHADOW BANKS",
        "Treasury blacklists more than two dozen exchange houses and firms, and traces about $14.7 billion in suspect flows.",
        "bank",
    ),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
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


def draw_ship(d, x, y, s, color):
    # simple warship: hull, deck, mast, flag
    d.polygon([(x, y + 0.62 * s), (x + s, y + 0.62 * s),
               (x + 0.88 * s, y + 0.85 * s), (x + 0.12 * s, y + 0.85 * s)],
              fill=color)
    d.rectangle([x + 0.18 * s, y + 0.42 * s, x + 0.62 * s, y + 0.62 * s], fill=color)
    d.rectangle([x + 0.30 * s, y + 0.18 * s, x + 0.36 * s, y + 0.42 * s], fill=color)
    d.polygon([(x + 0.36 * s, y + 0.18 * s), (x + 0.62 * s, y + 0.26 * s),
               (x + 0.36 * s, y + 0.34 * s)], fill=color)
    d.line([x, y + 0.94 * s, x + s, y + 0.94 * s], fill=color, width=4)


def draw_radar(d, x, y, s, color):
    # AWACS early-warning jet, side view: fuselage, dome, tail, wing
    d.ellipse([x + 0.34 * s, y + 0.14 * s, x + 0.62 * s, y + 0.34 * s],
              fill=color)
    d.polygon([(x + 0.02 * s, y + 0.52 * s), (x + 0.30 * s, y + 0.40 * s),
               (x + 0.82 * s, y + 0.40 * s), (x + 0.98 * s, y + 0.52 * s),
               (x + 0.82 * s, y + 0.64 * s), (x + 0.30 * s, y + 0.64 * s)],
              fill=color)
    d.polygon([(x + 0.78 * s, y + 0.40 * s), (x + 0.92 * s, y + 0.16 * s),
               (x + 0.97 * s, y + 0.40 * s)], fill=color)
    d.polygon([(x + 0.42 * s, y + 0.64 * s), (x + 0.58 * s, y + 0.64 * s),
               (x + 0.66 * s, y + 0.86 * s), (x + 0.34 * s, y + 0.86 * s)],
              fill=color)
    d.line([x + 0.06 * s, y + 0.94 * s, x + 0.94 * s, y + 0.94 * s],
           fill=color, width=4)


def draw_chip(d, x, y, s, color):
    # microchip with an upward arrow
    d.rectangle([x + 0.22 * s, y + 0.30 * s, x + 0.78 * s, y + 0.86 * s],
                outline=color, width=6)
    for i in range(3):
        t = 0.36 + 0.14 * i
        d.line([x + t * s, y + 0.18 * s, x + t * s, y + 0.30 * s],
               fill=color, width=4)
        d.line([x + t * s, y + 0.86 * s, x + t * s, y + 0.98 * s],
               fill=color, width=4)
        d.line([x + 0.10 * s, y + t * s, x + 0.22 * s, y + t * s],
               fill=color, width=4)
        d.line([x + 0.78 * s, y + t * s, x + 0.90 * s, y + t * s],
               fill=color, width=4)
    d.polygon([(x + 0.50 * s, y + 0.02 * s), (x + 0.66 * s, y + 0.22 * s),
               (x + 0.56 * s, y + 0.22 * s), (x + 0.56 * s, y + 0.40 * s),
               (x + 0.44 * s, y + 0.40 * s), (x + 0.44 * s, y + 0.22 * s),
               (x + 0.34 * s, y + 0.22 * s)], fill=color)


def draw_mountain(d, x, y, s, color):
    # two peaks with a sun
    d.polygon([(x + 0.02 * s, y + 0.92 * s), (x + 0.42 * s, y + 0.30 * s),
               (x + 0.82 * s, y + 0.92 * s)], fill=color)
    d.polygon([(x + 0.42 * s, y + 0.92 * s), (x + 0.72 * s, y + 0.48 * s),
               (x + 0.98 * s, y + 0.92 * s)], fill=color)
    d.ellipse([x + 0.68 * s, y + 0.06 * s, x + 0.92 * s, y + 0.30 * s],
              outline=color, width=5)
    d.line([x + 0.02 * s, y + 0.92 * s, x + 0.98 * s, y + 0.92 * s],
           fill=color, width=4)


def draw_flame(d, x, y, s, color):
    # flame shape
    d.polygon([
        (x + 0.50 * s, y + 0.02 * s), (x + 0.72 * s, y + 0.30 * s),
        (x + 0.86 * s, y + 0.52 * s), (x + 0.78 * s, y + 0.82 * s),
        (x + 0.50 * s, y + 0.96 * s), (x + 0.22 * s, y + 0.82 * s),
        (x + 0.14 * s, y + 0.52 * s), (x + 0.30 * s, y + 0.30 * s),
    ], fill=color)
    d.ellipse([x + 0.36 * s, y + 0.58 * s, x + 0.64 * s, y + 0.86 * s],
              fill=(255, 196, 66))


def draw_bank(d, x, y, s, color):
    # bank building with columns and a dollar sign
    d.polygon([(x + 0.02 * s, y + 0.30 * s), (x + 0.50 * s, y + 0.06 * s),
               (x + 0.98 * s, y + 0.30 * s)], fill=color)
    for i in range(4):
        cx = 0.16 + 0.22 * i
        d.rectangle([x + cx * s, y + 0.40 * s, x + (cx + 0.10) * s, y + 0.82 * s],
                    fill=color)
    d.rectangle([x + 0.06 * s, y + 0.82 * s, x + 0.94 * s, y + 0.92 * s],
                fill=color)
    d.text((x + 0.50 * s, y + 0.52 * s), "$", font=font(F_BOLD, int(0.30 * s)),
           fill=WHITE, anchor="mm")


ICONS = {
    "ship": draw_ship,
    "radar": draw_radar,
    "chip": draw_chip,
    "mountain": draw_mountain,
    "flame": draw_flame,
    "bank": draw_bank,
}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    f_date = font(F_BOLD, 66)
    d.text((W // 2, 52), "23 NOVEMBER 2026", font=f_date, fill=WHITE,
           anchor="mm")
    f_sub = font(F_BOLD, 21)
    d.text((W // 2, 98), "M O N D A Y   \u00b7   T H E   W O R L D   I N   O N E   I M A G E",
           font=f_sub, fill=SUB, anchor="mm")

    # ---- grid ----
    margin = 18
    gutter = 14
    top = 136
    bottom = 966
    col_w = (W - 2 * margin - gutter) // 2
    row_h = (bottom - top - 2 * 12) // 3

    f_kick = font(F_BOLD, 17)
    f_head = font(F_BOLD, 27)
    f_body = font(F_REG, 19)

    for i, (accent, kicker, headline, body, icon) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x0 = margin + col * (col_w + gutter)
        y0 = top + row * (row_h + 12)
        x1 = x0 + col_w
        y1 = y0 + row_h

        d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BORDER, width=2)
        d.rectangle([x0, y0, x1, y0 + 6], fill=accent)

        # pictogram, top-left
        px, py, ps = x0 + 20, y0 + 24, 62
        ICONS[icon](d, px, py, ps, accent)

        # kicker, right of pictogram
        kx = px + ps + 16
        d.text((kx, py + 8), kicker, font=f_kick, fill=accent)

        # headline: up to 2 lines, starting under the kicker row
        head_w = col_w - 40
        lines = wrap(d, headline, f_head, head_w)
        assert len(lines) <= 2, f"headline too long: {headline!r} -> {lines}"
        hy = y0 + 100
        for ln in lines:
            d.text((x0 + 20, hy), ln, font=f_head, fill=INK)
            hy += 34

        # body: up to 3 lines
        by = hy + 10
        blines = wrap(d, body, f_body, head_w)
        assert len(blines) <= 3, f"body too long: {body!r} -> {blines}"
        for ln in blines:
            d.text((x0 + 20, by), ln, font=f_body, fill=BODY)
            by += 27

    # ---- footer ----
    f_foot = font(F_REG, 18)
    d.text((W // 2, 992),
           "Every story above happened or was first reported on 23 November 2026.",
           font=f_foot, fill=FOOT, anchor="mm")

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
