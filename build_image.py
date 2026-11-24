#!/usr/bin/env python3
"""Build the entry image for the make.fun news-image-20261123 bounty.

Draws a complete one-page newspaper -- "THE WORLD IN ONE DAY" for Monday
23 November 2026 -- with Pillow and saves it as entry.png (1024 x 1024)
next to this script. The page is drawn entirely at build time; the
shipped main.py never draws anything, it only copies entry.png.

Run:  python3 build_image.py
"""

import datetime
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 24
RIGHT = W - MARGIN
CONTENT_W = W - 2 * MARGIN

# --- palette -------------------------------------------------------------
PAPER = (247, 241, 227)        # cream newsprint
PAPER_DARK = (238, 228, 203)   # deeper cream for bands and boxes
CARD_BG = (253, 250, 242)
CARD_EDGE = (198, 186, 158)
INK = (26, 22, 17)
MUTED = (96, 86, 70)
RED = (179, 35, 27)
NAVY = (23, 58, 94)
TEAL = (14, 107, 105)
GOLD = (176, 124, 24)
GOLD_LIGHT = (243, 197, 92)
WHITE = (255, 253, 247)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_font_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


# --- text helpers ----------------------------------------------------------

def tw(draw, text, fnt):
    """Pixel width of text in the given font."""
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if tw(draw, trial, fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, pitch, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += pitch
    return y


def pill(draw, x, y, text, fnt, bg, fg, pad_x=8, pad_y=2):
    """Draw a rounded chip; returns the x just past it."""
    w = tw(draw, text, fnt) + 2 * pad_x
    h = fnt.size + 2 * pad_y + 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y), text, font=fnt, fill=fg)
    return x + w


def centered(draw, y, text, fnt, fill):
    draw.text(((W - tw(draw, text, fnt)) / 2, y), text, font=fnt, fill=fill)


# --- masthead --------------------------------------------------------------

def masthead(draw, doy):
    # furniture line
    f_furn = font(SANS, 13)
    draw.text((MARGIN, 12), f"VOL. I · NO. {doy}", font=f_furn, fill=MUTED)
    centered(draw, 12, "ALL THE DAY'S NEWS IN ONE PICTURE", f_furn, MUTED)
    right = "ONE IMAGE · ONE DAY"
    draw.text((RIGHT - tw(draw, right, f_furn), 12), right, font=f_furn, fill=MUTED)

    # the name of the paper
    centered(draw, 28, "THE WORLD IN ONE DAY", font(SERIF_BOLD, 58), INK)

    # double rule
    draw.line([MARGIN, 92, RIGHT, 92], fill=INK, width=3)
    draw.line([MARGIN, 97, RIGHT, 97], fill=INK, width=1)

    # giant date line, in red
    centered(draw, 102, "MONDAY 23 NOVEMBER 2026", font(SERIF_BOLD, 27), RED)

    # day-numbers strip: navy band, four numbered facts
    draw.rectangle([MARGIN, 136, RIGHT, 178], fill=NAVY)
    cells = [
        (str(doy), "DAY OF 2026", WHITE),
        ("14 DAYS", "COP31 · NO DEAL", WHITE),
        ("15+", "DEAD AROUND KYIV", WHITE),
        ("+30%", "NVIDIA IN ONE DAY", GOLD_LIGHT),
    ]
    cell_w = CONTENT_W / 4
    f_val = font(SANS_BOLD, 22)
    f_lab = font(SANS_BOLD, 12)
    for i, (value, label, colour) in enumerate(cells):
        cx = MARGIN + (i + 0.5) * cell_w
        draw.text((cx - tw(draw, value, f_val) / 2, 140), value, font=f_val, fill=colour)
        draw.text((cx - tw(draw, label, f_lab) / 2, 164), label,
                  font=f_lab, fill=(205, 218, 235))
        if i:
            x = MARGIN + i * cell_w
            draw.line([x, 143, x, 171], fill=(90, 120, 160), width=1)


# --- hero ------------------------------------------------------------------

def hero_art(img, draw, x, y):
    """Fractured globe above a conference table of delegates."""
    # bunting: a string of small flags across the top of the scene
    draw.line([x + 6, y + 1, x + 294, y + 1], fill=MUTED, width=1)
    for fx, colour in [(x + 22, NAVY), (x + 50, RED),
                       (x + 236, TEAL), (x + 264, GOLD)]:
        draw.polygon([(fx, y + 1), (fx + 14, y + 1), (fx + 7, y + 12)],
                     fill=colour)
    cx, cy, r = x + 150, y + 48, 44
    # globe with meridians and a parallel
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - 17, cy - r, cx + 17, cy + r], outline=INK, width=2)
    draw.ellipse([cx - 33, cy - r, cx + 33, cy + r], outline=INK, width=2)
    draw.ellipse([cx - r, cy - 15, cx + r, cy + 15], outline=INK, width=2)
    # the crack
    crack = [(cx - 20, cy - r + 2), (cx - 8, cy - 28), (cx - 16, cy - 12),
             (cx - 2, cy + 2), (cx - 10, cy + 18), (cx + 2, cy + 32),
             (cx - 4, cy + r - 2)]
    draw.line(crack, fill=RED, width=3, joint="curve")
    # two flags behind the table
    draw.line([x + 52, y + 62, x + 52, y + 98], fill=INK, width=2)
    draw.rectangle([x + 52, y + 62, x + 70, y + 74], fill=NAVY)
    draw.line([x + 248, y + 62, x + 248, y + 98], fill=INK, width=2)
    draw.rectangle([x + 230, y + 62, x + 248, y + 74], fill=RED)
    # delegates seated behind the table: heads and shoulders, muted ink
    for i in range(7):
        dx = x + 48 + i * 34
        draw.ellipse([dx - 6, y + 92, dx + 6, y + 104], fill=MUTED)
        draw.polygon([(dx - 12, y + 111), (dx - 8, y + 102),
                      (dx + 8, y + 102), (dx + 12, y + 111)], fill=MUTED)
    # name plates along the table edge
    for i in range(5):
        px = x + 66 + i * 42
        draw.rectangle([px, y + 98, px + 24, y + 108], fill=WHITE, outline=INK)
    # the table itself
    draw.polygon([(x + 30, y + 108), (x + 270, y + 108),
                  (x + 248, y + 130), (x + 52, y + 130)],
                 fill=PAPER_DARK, outline=INK)
    # loose paper sheets scattered on the table surface
    for px, py in [(x + 72, y + 113), (x + 128, y + 118),
                   (x + 156, y + 111)]:
        draw.polygon([(px, py), (px + 17, py + 2), (px + 16, py + 9),
                      (px - 1, py + 7)], fill=WHITE, outline=MUTED)
    # fallen gavel: handle, head, and the block it slipped off
    draw.line([x + 196, y + 122, x + 230, y + 112], fill=INK, width=4)
    draw.polygon([(x + 226, y + 102), (x + 242, y + 107),
                  (x + 238, y + 118), (x + 222, y + 113)], fill=INK)
    draw.rectangle([x + 172, y + 125, x + 198, y + 131], outline=INK, width=2)
    # a red NO DEAL stamp slammed over the scene by the clerk
    f_stamp = font(SANS_BOLD, 14)
    label = "NO DEAL"
    sw = int(tw(draw, label, f_stamp)) + 20
    stamp = Image.new("RGBA", (sw, 30), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([1, 1, sw - 2, 28], outline=RED + (255,), width=3)
    sd.text(((sw - tw(draw, label, f_stamp)) / 2, 7), label,
            font=f_stamp, fill=RED + (255,))
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (x + 215 - stamp.width // 2,
                      y + 107 - stamp.height // 2), stamp)


HERO_SUMMARY = (
    "The longest UN climate summit in history closed in Antalya, Türkiye, "
    "with no agreement after the draft text omitted any mention of fossil "
    "fuels. The EU, Panama, the Marshall Islands and Norway rejected the "
    "text; Saudi Arabia and Russia blocked the wording — the first summit "
    "to collapse since Copenhagen 2009. Agreed instead: a just-transition "
    "package and an electrification push, said UN climate chief Simon "
    "Stiell. Monday's fallout: the EU will propose reforming the consensus "
    "rule, and Al Gore says the process needs reform."
)

LEGEND = [
    ("CONFIRMED", TEAL, "verified by officials or multiple wires"),
    ("REPORTED", GOLD, "single-source reporting"),
    ("CLAIM", RED, "asserted, not yet verified"),
]


def hero(img, draw, y):
    draw.rounded_rectangle([MARGIN, y, RIGHT, y + 246], radius=8,
                           fill=CARD_BG, outline=CARD_EDGE)
    # kicker band in navy, with the certainty chip on the right
    draw.rounded_rectangle([MARGIN + 2, y + 2, RIGHT - 2, y + 26], radius=6,
                           fill=NAVY)
    draw.text((MARGIN + 12, y + 6), "CLIMATE SUMMIT · ANTALYA, TÜRKIYE",
              font=font(SANS_BOLD, 13), fill=(240, 238, 230))
    chip = "CONFIRMED"
    f_chip = font(SANS_BOLD, 12)
    chip_w = tw(draw, chip, f_chip) + 16
    pill(draw, RIGHT - 12 - chip_w, y + 4, chip, f_chip, TEAL, WHITE)

    # headline
    draw.text((MARGIN + 14, y + 36), "COP31 ENDS WITHOUT A DEAL",
              font=font(SERIF_BOLD, 40), fill=INK)

    # summary on the left, illustration on the right
    text_block(draw, MARGIN + 14, y + 88, HERO_SUMMARY,
               font(SERIF, 15), INK, 632, 20)
    hero_art(img, draw, RIGHT - 314, y + 86)

    # certainty legend along the bottom of the hero
    lx = MARGIN + 14
    ly = y + 220
    f_lab = font(SANS_BOLD, 12)
    f_txt = font(SANS, 12)
    for label, colour, desc in LEGEND:
        draw.ellipse([lx, ly + 2, lx + 10, ly + 12], fill=colour)
        draw.text((lx + 16, ly), label, font=f_lab, fill=INK)
        lx += 16 + tw(draw, label, f_lab)
        rest = " — " + desc
        draw.text((lx, ly), rest, font=f_txt, fill=INK)
        lx += tw(draw, rest, f_txt) + 26


# --- card illustrations (48 x 48, drawn at x, y) -----------------------------

def icon_drone(draw, x, y):
    draw.ellipse([x + 18, y + 17, x + 30, y + 26], fill=INK)
    for rx, ry in [(4, 5), (35, 5), (4, 32), (35, 32)]:
        draw.line([x + 24, y + 21, x + rx + 4, y + ry + 2], fill=INK, width=2)
        draw.ellipse([x + rx, y + ry, x + rx + 9, y + ry + 4], outline=INK, width=2)
    draw.arc([x + 7, y + 34, x + 24, y + 46], 0, 180, fill=NAVY, width=2)
    draw.arc([x + 24, y + 34, x + 41, y + 46], 180, 360, fill=NAVY, width=2)


def icon_skyline(draw, x, y):
    draw.rectangle([x + 5, y + 24, x + 13, y + 44], fill=INK)
    draw.rectangle([x + 15, y + 14, x + 23, y + 44], fill=INK)
    draw.rectangle([x + 25, y + 20, x + 34, y + 44], fill=INK)
    draw.rectangle([x + 36, y + 10, x + 43, y + 44], fill=INK)
    smoke = (158, 150, 136)
    draw.ellipse([x + 15, y + 3, x + 24, y + 9], fill=smoke)
    draw.ellipse([x + 23, y + 0, x + 35, y + 8], fill=smoke)
    draw.ellipse([x + 32, y + 4, x + 40, y + 10], fill=smoke)


def icon_flame(draw, x, y):
    draw.rectangle([x + 6, y + 32, x + 42, y + 44], fill=INK)
    draw.rectangle([x + 10, y + 20, x + 16, y + 32], fill=INK)
    draw.polygon([(x + 28, y + 3), (x + 36, y + 17), (x + 33, y + 28),
                  (x + 23, y + 28), (x + 20, y + 17)], fill=(228, 116, 28))
    draw.polygon([(x + 28, y + 13), (x + 32, y + 20), (x + 30, y + 27),
                  (x + 26, y + 27), (x + 24, y + 20)], fill=(246, 196, 64))


def icon_market(draw, x, y):
    draw.line([x + 8, y + 6, x + 8, y + 40], fill=INK, width=2)
    draw.line([x + 8, y + 40, x + 42, y + 40], fill=INK, width=2)
    draw.line([(x + 12, y + 32), (x + 20, y + 25), (x + 27, y + 29),
               (x + 38, y + 13)], fill=TEAL, width=3)
    draw.polygon([(x + 38, y + 13), (x + 30, y + 12), (x + 36, y + 21)],
                 fill=TEAL)


def icon_proof(draw, x, y):
    draw.text((x + 24, y + 21), "ζ", font=font(SERIF_BOLD, 34), fill=TEAL,
              anchor="mm")
    for dx, dy in [(7, 7), (38, 5), (39, 37), (6, 38)]:
        draw.ellipse([x + dx, y + dy, x + dx + 3, y + dy + 3], fill=GOLD)


def icon_mercury(draw, x, y):
    draw.ellipse([x + 3, y + 17, x + 45, y + 31], outline=MUTED, width=2)
    draw.ellipse([x + 13, y + 9, x + 35, y + 33], fill=(196, 172, 138),
                 outline=INK, width=2)
    draw.ellipse([x + 18, y + 15, x + 24, y + 21], outline=(150, 128, 96),
                 width=2)
    draw.ellipse([x + 26, y + 23, x + 31, y + 28], outline=(150, 128, 96),
                 width=2)
    for dx, dy in [(6, 6), (40, 8), (42, 38), (5, 36)]:
        draw.ellipse([x + dx, y + dy, x + dx + 2, y + dy + 2], fill=GOLD)


ICONS = {
    "drone": icon_drone,
    "skyline": icon_skyline,
    "flame": icon_flame,
    "market": icon_market,
    "proof": icon_proof,
    "mercury": icon_mercury,
}


# --- the six cards -----------------------------------------------------------

CARD_W = (CONTENT_W - 2 * 12) // 3

CARDS_R1 = [
    dict(badge="WAR · LIBYA", colour=(146, 32, 26), chip=("CONFIRMED", TEAL, WHITE),
         icon="drone", headline="UKRAINE'S DRONES REACH LIBYA",
         text="Sea drones sank a Russian warship at Benghazi; Zelensky "
              "confirmed it. A Russian cargo ship was also hit in the Baltic."),
    dict(badge="UKRAINE", colour=(38, 84, 124), chip=("REPORTED", GOLD_LIGHT, INK),
         icon="skyline", headline="KYIV UNDER FIRE AGAIN",
         text="Russian strikes kill at least 15 people around the capital; "
              "a boy is pulled alive from the rubble in Dymer."),
    dict(badge="INDONESIA", colour=(166, 84, 20), chip=None,
         icon="flame", headline="FACTORY FIRE KILLS 24 IN INDONESIA",
         text="A confectionery plant in Cikande, Banten, burned on "
              "Saturday evening: 24 dead, about 30 still missing."),
]

CARDS_R2 = [
    dict(badge="TECH & MARKETS", colour=(94, 52, 140), chip=("REPORTED", GOLD_LIGHT, INK),
         icon="market", headline="NVIDIA BRINGS BACK ITS FOUNDER",
         text="Jensen Huang reinstated as chief executive; shares jump "
              "about 30%. US intelligence tracked alleged Alice Huang–China "
              "spy contacts (New York Times); senators demand tighter "
              "export controls."),
    dict(badge="SCIENCE", colour=TEAL, chip=None,
         icon="proof", headline="A PROOF FROM A MACHINE",
         text="Anthropic says its AI helped prove the Riemann hypothesis. "
              "Mathematicians debate whether a proof no human can fully "
              "check still counts."),
    dict(badge="SPACE", colour=NAVY, chip=None,
         icon="mercury", headline="MERCURY, AT LAST",
         text="BepiColombo enters orbit around Mercury after an eight-year "
              "journey — only the second craft ever to orbit it, after NASA's "
              "Messenger. ESA–JAXA will study its surface and magnetic "
              "field."),
]


def card(draw, x, y, h, spec, max_lines):
    draw.rounded_rectangle([x, y, x + CARD_W, y + h], radius=8,
                           fill=CARD_BG, outline=CARD_EDGE)
    draw.line([x + 10, y + 4, x + CARD_W - 10, y + 4],
              fill=spec["colour"], width=3)
    # section badge, plus an honesty chip where one fits
    bx = pill(draw, x + 10, y + 9, spec["badge"], font(SANS_BOLD, 12),
              spec["colour"], WHITE)
    if spec["chip"]:
        label, bg, fg = spec["chip"]
        pill(draw, bx + 6, y + 9, label, font(SANS_BOLD, 12), bg, fg)
    # illustration, top right
    ix = x + CARD_W - 58
    draw.rounded_rectangle([ix, y + 8, ix + 48, y + 56], radius=6,
                           fill=(240, 234, 216))
    ICONS[spec["icon"]](draw, ix, y + 8)
    # headline (kept clear of the illustration) and body text
    text_block(draw, x + 10, y + 30, spec["headline"],
               font(SERIF_BOLD, 19), INK, CARD_W - 76, 20, max_lines=2)
    text_block(draw, x + 10, y + 70, spec["text"],
               font(SERIF, 13), INK, CARD_W - 20, 16, max_lines=max_lines)


def cards(draw):
    xs = [MARGIN + i * (CARD_W + 12) for i in range(3)]
    for x, spec in zip(xs, CARDS_R1):
        card(draw, x, 440, 118, spec, max_lines=3)
    for x, spec in zip(xs, CARDS_R2):
        card(draw, x, 566, 140, spec, max_lines=5)


# --- numbered briefs ---------------------------------------------------------

BRIEFS = [
    "Drone strikes hit homes and a UN building in Khartoum.",
    "NHS EDITH trial invites nearly 700,000 women to test AI "
    "breast-cancer screening.",
    "Asian tech shares slide as AI sell-off deepens.",
    "Euro-area inflation reaches 4.0%.",
    "Trump warns of new strikes on Iran after the New Year; "
    "blockade runners will be sunk.",
    "JD Vance meets Qatar's prime minister over the stalled Iran talks.",
    "Houthis claim an attack on a Saudi oil refinery.",
    "Israeli opposition leader Eisenkot calls West Bank settler attacks "
    "‘Jewish terrorism’.",
    "Burnham defends the EU reset deal in the Commons; its "
    "£17bn-a-year-by-2040 figure is a CLAIM.",
    "FIFA: UK to host the 2035 Women's World Cup.",
    "GTA VI hacker Arion Kurtaj gets seven years at Woolwich Crown Court.",
    "Iranian singer Parastoo Ahmadi gets 74 lashes for an online concert "
    "without a hijab.",
    "Don Toliver concert in Manchester evacuated after unknown "
    "substance released.",
    "India announces an aid package for Nepal.",
    "Chinese espionage networks recruited ex-US officials via fake "
    "LinkedIn firms (CNN).",
    "UK voters name rising prices their top concern.",
    "China calls COP31 outcome a ‘deep disappointment’ (via Xinhua).",
    "President Erdoğan of Türkiye says the summit laid ‘a valuable "
    "foundation’ despite no deal.",
    "Caribbean leaders condemn COP31 failure; adaptation finance "
    "at risk.",
    "A major equal-pay tribunal involving Asda workers opens in the UK.",
    "A second-home sell-off costs UK councils £48m in lost council tax.",
    "Trump's Thanksgiving turkeys reach a Washington hotel; "
    "the public votes on names.",
]


def briefs(draw, y):
    # header band
    draw.rectangle([MARGIN, y, RIGHT, y + 24], fill=PAPER_DARK)
    draw.text((MARGIN + 10, y + 5), "THE REST OF THE DAY — IN BRIEF",
              font=font(SANS_BOLD, 13), fill=INK)
    note = "22 STORIES, NUMBERED"
    f_note = font(SANS, 12)
    draw.text((RIGHT - 10 - tw(draw, note, f_note), y + 6), note,
              font=f_note, fill=MUTED)

    col_gap = 14
    col_w = (CONTENT_W - 2 * col_gap) // 3
    f_txt = font(SANS, 12)
    f_num = font(SANS_BOLD, 12)
    wrapped = [wrap(draw, t, f_txt, col_w - 26) for t in BRIEFS]
    heights = [len(ls) * 16 + 1 for ls in wrapped]

    # choose the two split points that minimise the tallest column
    n = len(BRIEFS)
    best = None
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            cols = (sum(heights[:i]), sum(heights[i:j]), sum(heights[j:]))
            if best is None or max(cols) < best[0]:
                best = (max(cols), i, j)
    _, split_i, split_j = best
    groups = [(0, split_i), (split_i, split_j), (split_j, n)]

    top = y + 29
    for c, (a, b) in enumerate(groups):
        x = MARGIN + c * (col_w + col_gap)
        cy = top
        for k in range(a, b):
            draw.text((x, cy), f"{k + 1}.", font=f_num, fill=RED)
            for line in wrapped[k]:
                draw.text((x + 26, cy), line, font=f_txt, fill=INK)
                cy += 16
            cy += 1


# --- date check --------------------------------------------------------------

def date_check(draw, y, doy):
    draw.rounded_rectangle([MARGIN, y, RIGHT, y + 44], radius=6,
                           fill=(250, 244, 228), outline=RED, width=2)
    f_b = font(SANS_BOLD, 13)
    f = font(SANS, 13)
    x = MARGIN + 12
    draw.text((x, y + 7), "DATE CHECK", font=f_b, fill=RED)
    x += tw(draw, "DATE CHECK", f_b)
    draw.text((x, y + 7),
              f" · Monday 23 November 2026 — day {doy} of 2026 · COP31 ran "
              "10–23 November in Antalya", font=f, fill=INK)
    draw.text((MARGIN + 12, y + 25),
              "Copenhagen 2009: the last summit to end without a deal · "
              "BepiColombo launched 2018, arrived 2026", font=f, fill=INK)


# --- assembly ------------------------------------------------------------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    day = datetime.date(2026, 11, 23)
    doy = day.timetuple().tm_yday
    masthead(draw, doy)
    hero(img, draw, 186)
    cards(draw)
    briefs(draw, 714)
    date_check(draw, 968, doy)
    img.save(OUT)
    print(f"wrote {OUT} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
