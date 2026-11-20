#!/usr/bin/env python3
"""Numbers XL front page - Friday 20 November 2026.

One image that sums up the day: 48 stories, 7 regions, led by the numbers.
Drawn from scratch with PIL: masthead, giant-figures band, region strip,
UTC timeline, three hero panels, thirteen pictured panels, a dot-matrix
world map, thirty-two briefs, a date check and sources. Writes entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1600
PAPER = (250, 246, 238)
INK = (20, 20, 20)
BODY = (52, 48, 42)
NAVY = (13, 24, 48)
RED = (178, 34, 34)
ORANGE = (214, 96, 20)
GOLD = (212, 172, 66)
TEAL = (18, 110, 110)
GREY = (96, 92, 84)
LIGHT = (232, 226, 214)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"


def _font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        pass
    plain = path.rsplit("/", 1)[-1]
    if plain != path:
        try:
            return ImageFont.truetype(plain, size)
        except OSError:
            pass
    return ImageFont.load_default()


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return _font(DJ + name, size)


def serif(size, bold=False):
    name = "LiberationSerif-Bold.ttf" if bold else "LiberationSerif-Regular.ttf"
    return _font(LB + name, size)


def wrap_text(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, width, fill, lh, max_lines=None):
    lines = wrap_text(d, text, fnt, width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "...", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "..."
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def sky(d, x, y, w, h, top, bottom):
    steps = 14
    for i in range(steps):
        t = i / float(steps - 1)
        col = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + i * h / steps, x + w, y + (i + 1) * h / steps + 1],
                    fill=col)


def sun(d, cx, cy, r, col=(255, 176, 32)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for k in range(8):
        ang = k * math.pi / 4.0
        x1 = cx + int(math.cos(ang) * (r + 4))
        y1 = cy + int(math.sin(ang) * (r + 4))
        x2 = cx + int(math.cos(ang) * (r + 16))
        y2 = cy + int(math.sin(ang) * (r + 16))
        d.line([x1, y1, x2, y2], fill=col, width=4)


def towers(d, x, y, w, h, base, tops):
    n = len(tops)
    bw = w / float(n)
    for i, th in enumerate(tops):
        bx = x + i * bw + 3
        d.rectangle([bx, y + h - th, bx + bw - 6, y + h], fill=base)
        for wy in range(int(y + h - th + 8), int(y + h - 6), 14):
            d.rectangle([bx + 4, wy, bx + bw - 10, wy + 5], fill=(255, 214, 90))


def waves(d, x, y, w, h, col=(20, 90, 120)):
    d.rectangle([x, y, x + w, y + h], fill=col)
    for row in range(3):
        yy = y + 8 + row * (h / 3.0)
        for k in range(6):
            xx = x + k * (w / 6.0)
            d.arc([xx, yy - 6, xx + w / 6.0, yy + 10], 180, 360,
                  fill=(255, 255, 255), width=3)


def scene(d, x, y, w, h, kind):
    """A flat, hand-drawn scene for one story. No photographs."""
    if kind == "cyclone":
        sky(d, x, y, w, h, (16, 60, 80), (60, 110, 130))
        for i in range(7):
            d.line([x + i * w / 7.0, y + 6, x + i * w / 7.0 - 14, y + h - 8],
                   fill=(200, 220, 230), width=2)
        cx, cy = x + w * 0.62, y + h * 0.45
        for r in (34, 24, 14):
            d.ellipse([cx - r, cy - r, cx + r, cy + r],
                      outline=(255, 255, 255), width=4)
        waves(d, x, y + h - 26, w, 26, (14, 70, 95))
    elif kind == "missile":
        sky(d, x, y, w, h, (70, 40, 60), (200, 110, 50))
        sun(d, x + w * 0.78, y + h * 0.42, 15, (255, 120, 20))
        towers(d, x, y + h - 62, w, 62, (40, 30, 44), (62, 44, 56, 38))
        d.line([x + w * 0.15, y + h - 10, x + w * 0.78, y + h * 0.42],
               fill=(255, 220, 150), width=3)
        for k in range(6):
            ang = k * math.pi / 3.0
            d.line([x + w * 0.78, y + h * 0.42,
                    x + w * 0.78 + int(math.cos(ang) * 26),
                    y + h * 0.42 + int(math.sin(ang) * 26)],
                   fill=(255, 140, 30), width=4)
    elif kind == "summit":
        sky(d, x, y, w, h, (30, 70, 130), (120, 170, 210))
        towers(d, x, y + h - 58, w, 58, (24, 34, 58), (58, 40, 52, 34))
        for i, col in enumerate(((200, 40, 40), (255, 210, 60), (30, 90, 180))):
            fx = x + w * (0.22 + 0.26 * i)
            d.line([fx, y + 12, fx, y + 52], fill=(240, 240, 240), width=3)
            d.rectangle([fx, y + 14, fx + 34, y + 34], fill=col)
    elif kind == "bridge":
        sky(d, x, y, w, h, (90, 140, 180), (190, 210, 220))
        waves(d, x, y + h - 44, w, 44, (30, 100, 140))
        d.line([x, y + h - 44, x + w, y + h - 44], fill=(40, 40, 40), width=5)
        d.arc([x + w * 0.15, y + h - 110, x + w * 0.85, y + h - 10],
              180, 360, fill=(40, 40, 40), width=5)
        d.line([x + w * 0.5, y + h - 110, x + w * 0.5, y + h - 44],
               fill=(40, 40, 40), width=4)
        d.ellipse([x + w * 0.68 - 12, y + h - 72, x + w * 0.68 + 12,
                   y + h - 48], fill=(255, 90, 20))
    elif kind == "apec":
        sky(d, x, y, w, h, (40, 80, 140), (140, 180, 215))
        towers(d, x, y + h - 56, w, 56, (28, 40, 66), (56, 38, 50, 30))
        for i, col in enumerate(((200, 40, 40), (255, 210, 60), (30, 90, 180))):
            fx = x + w * (0.25 + 0.24 * i)
            d.line([fx, y + 10, fx, y + 44], fill=(240, 240, 240), width=3)
            d.rectangle([fx, y + 12, fx + 30, y + 30], fill=col)
    elif kind == "cop":
        sky(d, x, y, w, h, (20, 110, 110), (120, 200, 180))
        d.ellipse([x + w * 0.68 - 26, y + 12, x + w * 0.68 + 26, y + 64],
                  fill=(40, 160, 120))
        d.ellipse([x + w * 0.68 - 26, y + 12, x + w * 0.68 + 26, y + 64],
                  outline=(255, 255, 255), width=3)
        d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.55),
                   (x + w * 0.6, y + h)], fill=(30, 110, 60))
        d.polygon([(x + w * 0.4, y + h), (x + w * 0.7, y + h * 0.6),
                   (x + w, y + h)], fill=(24, 90, 50))
    elif kind == "court":
        sky(d, x, y, w, h, (120, 140, 170), (200, 205, 210))
        d.rectangle([x + w * 0.12, y + h - 52, x + w * 0.88, y + h - 44],
                    fill=(90, 80, 70))
        for i in range(5):
            cx = x + w * (0.18 + 0.16 * i)
            d.rectangle([cx - 6, y + h - 96, cx + 6, y + h - 52],
                        fill=(230, 225, 210))
        d.polygon([(x + w * 0.08, y + h - 96), (x + w * 0.5, y + h - 122),
                   (x + w * 0.92, y + h - 96)], fill=(150, 130, 110))
    elif kind == "market":
        sky(d, x, y, w, h, (60, 30, 40), (140, 60, 60))
        for i, bh in enumerate((30, 48, 38, 62, 46)):
            bx = x + 14 + i * (w - 28) / 5.0
            d.rectangle([bx, y + h - 12 - bh, bx + (w - 28) / 5.0 - 8,
                         y + h - 12], fill=(200, 60, 50))
        pts = [(x + 10, y + 22), (x + w * 0.3, y + 40),
               (x + w * 0.55, y + 34), (x + w * 0.78, y + 62),
               (x + w - 10, y + h - 22)]
        d.line(pts, fill=(255, 220, 60), width=5, joint="curve")
        d.polygon([(x + w - 26, y + h - 34), (x + w - 8, y + h - 22),
                   (x + w - 30, y + h - 10)], fill=(255, 220, 60))
    elif kind == "game":
        sky(d, x, y, w, h, (90, 40, 110), (255, 140, 90))
        sun(d, x + w * 0.72, y + h * 0.34, 20)
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(30, 90, 60))
        for i in range(3):
            px = x + w * (0.16 + 0.3 * i)
            d.line([px, y + h - 30, px, y + h - 62], fill=(60, 40, 20),
                   width=4)
            d.arc([px - 22, y + h - 78, px + 22, y + h - 46], 180, 360,
                  fill=(40, 120, 60), width=4)
    elif kind == "space":
        d.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
        for sx, sy, sr in ((0.12, 0.2, 2), (0.3, 0.5, 2), (0.55, 0.15, 3),
                           (0.7, 0.6, 2), (0.85, 0.3, 2), (0.42, 0.75, 2),
                           (0.92, 0.7, 3), (0.2, 0.8, 2)):
            d.ellipse([x + sx * w - sr, y + sy * h - sr, x + sx * w + sr,
                       y + sy * h + sr], fill=(255, 255, 255))
        d.ellipse([x + w * 0.55 - 26, y + h * 0.3 - 26, x + w * 0.55 + 26,
                   y + h * 0.3 + 26], fill=(120, 160, 220))
        d.ellipse([x + w * 0.55 - 26, y + h * 0.3 - 26, x + w * 0.55 + 26,
                   y + h * 0.3 + 26], outline=(200, 220, 255), width=2)
        d.line([x + w * 0.15, y + h * 0.8, x + w * 0.5, y + h * 0.45],
               fill=(255, 200, 80), width=3)
    elif kind == "seoul":
        sky(d, x, y, w, h, (50, 90, 150), (170, 200, 225))
        towers(d, x, y + h - 56, w, 56, (30, 44, 70), (56, 42, 50, 34))
        d.ellipse([x + w * 0.7 - 18, y + 10, x + w * 0.7 + 18, y + 46],
                  fill=(255, 255, 255))
        d.ellipse([x + w * 0.7 - 18, y + 10, x + w * 0.7 + 18, y + 46],
                  outline=(200, 40, 40), width=3)
    elif kind == "fiji":
        sky(d, x, y, w, h, (60, 140, 200), (180, 220, 240))
        sun(d, x + w * 0.74, y + h * 0.3, 18)
        waves(d, x, y + h - 36, w, 36, (20, 110, 170))
        px = x + w * 0.2
        d.line([px, y + h - 36, px, y + h - 70], fill=(90, 60, 30), width=4)
        d.arc([px - 20, y + h - 84, px + 20, y + h - 56], 180, 360,
              fill=(40, 130, 70), width=4)
    elif kind == "vienna":
        sky(d, x, y, w, h, (110, 120, 130), (190, 195, 200))
        d.rectangle([x + w * 0.2, y + h - 50, x + w * 0.8, y + h - 12],
                    fill=(120, 110, 100))
        d.ellipse([x + w * 0.5 - 30, y + h - 88, x + w * 0.5 + 30,
                   y + h - 40], fill=(150, 140, 130))
        for k in range(3):
            d.ellipse([x + w * 0.5 - 40 - k * 4, y + h - 70 - k * 6,
                       x + w * 0.5 + 40 + k * 4, y + h - 30 + k * 6],
                      outline=(220, 60, 40), width=2)
    elif kind == "caracas":
        sky(d, x, y, w, h, (50, 100, 160), (170, 200, 225))
        for i, col in enumerate(((240, 200, 40), (30, 90, 180), (200, 40, 40))):
            fx = x + w * (0.2 + 0.28 * i)
            d.line([fx, y + 12, fx, y + 50], fill=(240, 240, 240), width=3)
            d.rectangle([fx, y + 14, fx + 32, y + 32], fill=col)
        towers(d, x, y + h - 46, w, 46, (40, 50, 70), (46, 34, 42, 28))
    elif kind == "hormuz":
        sky(d, x, y, w, h, (200, 130, 70), (240, 190, 120))
        waves(d, x, y + h - 40, w, 40, (30, 90, 130))
        d.rectangle([x + w * 0.2, y + h - 62, x + w * 0.78, y + h - 40],
                    fill=(60, 50, 40))
        d.rectangle([x + w * 0.42, y + h - 82, x + w * 0.58, y + h - 62],
                    fill=(90, 80, 70))
        for k in range(3):
            d.ellipse([x + w * 0.6 + k * 12, y + h - 100 - k * 8,
                       x + w * 0.6 + k * 12 + 18, y + h - 82 - k * 8],
                      fill=(120, 120, 120))
    else:  # cricket
        sky(d, x, y, w, h, (90, 150, 210), (190, 220, 240))
        d.rectangle([x, y + h - 34, x + w, y + h], fill=(50, 130, 70))
        d.rectangle([x + w * 0.42, y + h - 58, x + w * 0.58, y + h - 34],
                    fill=(220, 200, 160))
        for i in range(3):
            sx = x + w * (0.3 + 0.12 * i)
            d.line([sx, y + h - 66, sx, y + h - 44], fill=(255, 240, 180),
                   width=3)
        d.ellipse([x + w * 0.8 - 7, y + h * 0.3 - 7, x + w * 0.8 + 7,
                   y + h * 0.3 + 7], fill=(255, 255, 255),
                  outline=(200, 40, 40), width=2)


# ---------------------------------------------------------------- data ---

FIGURES = [
    ("300,000", "people evacuated ahead of Cyclone Akvan"),
    ("$1.84bn", "GTA VI's first-day sales, Sensor Tower estimates"),
    ("-1,084", "points the Dow lost in Friday's slide"),
    ("16bn mi", "Voyager 1 from Earth - one light-day out"),
    ("7.91m", "peak viewers watching GTA VI at once"),
    ("9-6", "the ICJ vote finding Myanmar guilty"),
]

REGIONS = [
    ("EUROPE", 11, (30, 80, 160)),
    ("THE AMERICAS", 7, (0, 140, 120)),
    ("ASIA-PACIFIC", 19, (178, 34, 34)),
    ("MIDEAST", 4, (214, 120, 20)),
    ("AFRICA", 3, (110, 70, 160)),
    ("OCEANIA", 2, (20, 140, 180)),
    ("WORLD", 2, (70, 70, 70)),
]

TIMELINE = [
    ("OVERNIGHT", "Crimean Bridge hit a third time"),
    ("~06:00", "APEC leaders meet in Shenzhen"),
    ("~10:00", "Trilateral declaration issued"),
    ("~12:00", "Akvan makes landfall in Odisha"),
    ("~14:00", "Houthi missile hits Riyadh KAFD"),
    ("LATE", "Wall Street slides; Dow -1,084"),
]

HEROES = [
    dict(n=1, key="300,000", scene="cyclone", kicker="1 · ODISHA · STORM",
         src="IMD · THE HINDU",
         head="Akvan comes ashore on the Odisha coast",
         dek="Cyclone Akvan crossed the coast near Gopalpur at noon, winds "
             "90-100 km/h gusting to 110. Three hundred thousand people are "
             "out of harm's way, 423 rescue teams deployed, red alerts in "
             "11 districts."),
    dict(n=2, key="1 TOWER", scene="missile", kicker="2 · RIYADH · ATTACK",
         src="ARAB NEWS · REUTERS",
         head="Houthi missile hits Riyadh's KAFD financial district",
         dek="A Houthi missile damaged a wealth-fund tower in the financial "
             "district, one of Riyadh's tallest. No casualties are reported, "
             "as air defences answered the strike."),
    dict(n=3, key="12/10", scene="summit", kicker="3 · SHENZHEN · DIPLOMACY",
         src="REUTERS · AP",
         head="Trump, Xi and Putin issue a joint declaration",
         dek="No big peace deal from the trilateral's second day. Trump says "
             "the Iran war call waits until 2027, rates the summit '12 out "
             "of 10', and Putin may attend December's G20 in Miami."),
]

PICTURED = [
    dict(n=4, key="3RD HIT", scene="bridge",
         kicker="4 · KERCH STRAIT · WAR", src="CLAIM · KYIV",
         head="Crimean Bridge hit a third time this week; rail halted",
         dek="A Ukrainian naval drone strike disrupted rail traffic on the "
             "bridge. Rail partly resumes; Putin vows retaliation, and Kyiv "
             "was hit by drones."),
    dict(n=5, key="21", scene="apec", kicker="5 · SHENZHEN · SUMMIT",
         src="AP", head="APEC leaders meet in Shenzhen",
         dek="Leaders gather in China for the APEC summit. Xi urges APEC "
             "economies to back open trade and new technology."),
    dict(n=6, key="0", scene="cop", kicker="6 · ANTALYA · CLIMATE", src="UNFCCC · AFP",
         head="COP31's final day: fossil fuels cut from the text",
         dek="A revised draft strips out every fossil-fuel phase-out pledge. "
             "Delegates push back as the final plenary meets today."),
    dict(n=7, key="9-6", scene="court", kicker="7 · THE HAGUE · LAW",
         src="AP · BBC", head="The world answers the genocide verdict",
         dek="Britain expels Myanmar's defence attache and seeks an urgent "
             "Security Council meeting. The Gambia hails a 'historic' verdict."),
    dict(n=8, key="-1,084", scene="market", kicker="8 · NEW YORK · MARKETS",
         src="BLOOMBERG", head="Anthropic's debut can't stop the slide",
         dek="The Dow fell 1,084 points, the S&P 2.02% and the Nasdaq 2.25%, "
             "as the AI selloff bit a day after Anthropic's record debut."),
    dict(n=9, key="$1.84bn", scene="game", kicker="9 · VICE CITY · GAMES",
         src="SENSOR TOWER", head="GTA VI passes The Odyssey's $1.84bn",
         dek="Launch-day sales top The Odyssey's $1.80bn global run, Sensor "
             "Tower estimates. Reviews land; Rockstar calls it the "
             "highest-rated game ever."),
    dict(n=10, key="16bn", scene="space", kicker="10 · SPACE · SCIENCE",
         src="NASA · JPL", head="NASA confirms Voyager 1's light-day milestone",
         dek="The probe is now a full light-day from Earth - 16 billion miles "
             "out, the farthest any human-made object has ever travelled."),
    dict(n=11, key="0", scene="seoul", kicker="11 · SEOUL · LAW",
         src="KOREA TIMES", head="South Korea clears ex-PM Han",
         dek="The Supreme Court overturns former prime minister Han Duck-soo's "
             "conviction, in the case tied to the 2024 martial-law declaration."),
    dict(n=12, key="1", scene="fiji", kicker="12 · SUVA · CLIMATE", src="AFP",
         head="Fiji declares a national disaster over drought",
         dek="Fiji declares a national disaster over drought and water "
             "shortages. El Nino leaves water short across the islands."),
    dict(n=13, key="1 SITE", scene="vienna", kicker="13 · VIENNA · SECURITY",
         src="IAEA", head="North Korea expands uranium enrichment at Yongbyon",
         dek="The UN watchdog reports growth at the nuclear site, in its "
             "latest assessment of the Yongbyon complex."),
    dict(n=14, key="2", scene="caracas", kicker="14 · CARACAS · DIPLOMACY",
         src="REUTERS", head="US and Venezuela restore military cooperation",
         dek="The two countries sign an agreement to work together again, "
             "restoring a military channel closed for years."),
    dict(n=15, key="1", scene="hormuz", kicker="15 · HORMUZ · CONFLICT",
         src="REUTERS", head="ADNOC vessel attacked in the Strait of Hormuz",
         dek="One crew member is missing after the strike on the ADNOC vessel "
             "in the strait."),
    dict(n=16, key="113", scene="cricket", kicker="16 · WELLINGTON · CRICKET",
         src="AP", head="Day two at the Basin: Nicholls' 113 anchors New Zealand",
         dek="New Zealand build on Henry Nicholls' unbeaten 113 as India hunt "
             "early wickets, in the first Test at the Basin Reserve."),
]

BRIEFS = [
    (17, "BRUSSELS", "EU-UK summit opens"),
    (18, "NEW DELHI", "Modi meets William and Kate"),
    (19, "DHAKA", "Fire at the Yunus home; arson feared"),
    (20, "MUMBAI", "Sensex +1.21%, Nifty +1.14% on the day"),
    (21, "TOKYO", "Hayabusa2 gives up landing; mission rewritten"),
    (22, "BERLIN", "Coalition of the Willing meets in Berlin"),
    (23, "BERLIN", "Merz hosts Qatar's emir in Berlin"),
    (24, "NEW DELHI", "Pakistan minister leads delegation to Delhi for SCO"),
    (25, "MANILA", "Philippines-Chile trade deal signed"),
    (26, "MANILA", "Musk plans Philippines projects"),
    (27, "HONG KONG", "India beats Malaysia, Asian Hockey Trophy opens"),
    (28, "IPOH", "Harimau Shakti exercise opens in Ipoh"),
    (29, "NEW DELHI", "India's electronics exports jump 44%"),
    (30, "NEW DELHI", "ICMR completes 100 tech transfers"),
    (31, "NEW DELHI", "India unveils its first bird-flu vaccine"),
    (32, "GENEVA", "World Children's Day marked worldwide"),
    (33, "EUROPE", "Youth anti-war protests across Europe"),
    (34, "BRUSSELS", "EU delays its methane rules by 24 months"),
    (35, "COLOGNE", "Bayern Munich beat Koln 3-0"),
    (36, "U17 CUP", "Argentina 0-2 Australia at the U17 Cup"),
    (37, "WASHINGTON", "Jobless claims come in at 203,000"),
    (38, "STRASBOURG", "NATO's assembly opens its 72nd session"),
    (39, "HANOI", "Azerbaijan's Aliyev visits Vietnam"),
    (40, "MARKETS", "Crude futures fall over 3%"),
    (41, "KHARTOUM", "Sudan army: two-year El Obeid siege broken"),
    (42, "MOGADISHU", "Somalia gives UAE ambassador 72 hours to leave"),
    (43, "SAN SALVADOR", "Migrant boat capsizes off El Salvador; dozens missing"),
    (44, "PORT-AU-PRINCE", "Haiti approves Salvadoran troop deal vs gangs"),
    (45, "ARABIAN SEA", "Amur falcons cross the Arabian Sea"),
    (46, "NEW YORK", "Al-Saadi appears in a New York court over a UK plot"),
    (47, "KYIV", "Witkoff and Kushner brief Zelenskyy"),
    (48, "BEIJING", "Xi urges APEC to back open trade, new tech"),
]

# Rough land boxes in (lon_min, lat_min, lon_max, lat_max).
LAND = [
    (-168, 58, -140, 71), (-168, 48, -125, 60), (-125, 30, -66, 50),
    (-100, 15, -80, 32), (-105, 8, -78, 20), (-60, 60, -20, 83),
    (-80, 8, -35, -5), (-75, -35, -40, -5), (-70, -55, -53, -35),
    (-10, 36, 30, 60), (-6, 50, 2, 59), (5, 55, 31, 71),
    (30, 36, 45, 70), (-18, 15, 35, 35), (-10, -35, 40, 15),
    (43, -25, 50, -12), (35, 12, 60, 42), (40, 50, 180, 75),
    (60, 25, 140, 50), (75, 8, 105, 30), (95, 5, 110, 28),
    (100, -10, 150, 10), (113, -12, 154, -38), (166, -34, 178, -47),
]

PINS = {
    4: (36, 45), 5: (114, 22), 6: (30, 36), 7: (4, 52), 8: (-74, 40),
    9: (-80, 26), 10: (165, 72), 11: (127, 37), 12: (178, -18),
    13: (16, 48), 14: (-67, 10), 15: (56, 26), 16: (175, -41),
}

DATE_CHECK = (
    "Left out - they broke before Friday: the ICJ genocide ruling on Myanmar "
    "itself (Thursday 19 Nov) - Friday's news is the world's answer to it - "
    "Denmark's Greenland-US pact (19 Nov) - Anthropic's $81.34bn IPO (19 Nov); "
    "its first trading day was Thursday - Germany's electricity-tax cut "
    "(18 Nov) - the Crimean Bridge span collapse (17-18 Nov). Not yet: the "
    "trilateral's first meeting was 19 Nov; the joint declaration is Friday's."
)


# -------------------------------------------------------------- panels ---

def hero_panel(d, x, y, w, h, item):
    scene(d, x, y, w, 108, item["scene"])
    chip = item["key"]
    tw = d.textlength(chip, font=sans(24, True)) + 18
    d.rectangle([x, y, x + tw, y + 32], fill=RED)
    d.text((x + 9, y + 3), chip, font=sans(24, True), fill=(255, 255, 255))
    yy = y + 118
    d.text((x, yy), item["kicker"], font=sans(19, True), fill=RED)
    sw = d.textlength(item["src"], font=sans(15, True))
    d.text((x + w - sw, yy + 2), item["src"], font=sans(15, True), fill=GREY)
    yy += 26
    yy = para(d, x, yy, item["head"], serif(28, True), w, INK, 31,
              max_lines=2)
    para(d, x, yy + 4, item["dek"], sans(16), w, BODY, 19, max_lines=3)


def pic_panel(d, x, y, w, h, item):
    scene(d, x, y, w, 74, item["scene"])
    chip = item["key"]
    tw = d.textlength(chip, font=sans(16, True)) + 12
    d.rectangle([x, y, x + tw, y + 22], fill=RED)
    d.text((x + 6, y + 2), chip, font=sans(16, True), fill=(255, 255, 255))
    yy = y + 82
    d.text((x, yy), item["kicker"], font=sans(14, True), fill=RED)
    sw = d.textlength(item["src"], font=sans(11, True))
    d.text((x + w - sw, yy + 1), item["src"], font=sans(11, True), fill=GREY)
    yy += 20
    yy = para(d, x, yy, item["head"], serif(18, True), w, INK, 21,
              max_lines=2)
    para(d, x, yy + 2, item["dek"], sans(13), w, BODY, 16, max_lines=2)


def world_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 84.0, -58.0

    def px(lon):
        return x0 + (lon - lon0) / (lon1 - lon0) * (x1 - x0)

    def py(lat):
        return y0 + (lat0 - lat) / (lat0 - lat1) * (y1 - y0)

    lon = -177.0
    while lon <= 180.0:
        lat = 82.0
        while lat >= -56.0:
            inside = any(a <= lon <= c and b <= lat <= dd
                         for a, b, c, dd in LAND)
            if inside:
                d.ellipse([px(lon) - 2, py(lat) - 2, px(lon) + 2,
                           py(lat) + 2], fill=(210, 215, 225))
            lat -= 2.6
        lon += 3.0
    for n, (lon, lat) in sorted(PINS.items()):
        cx, cy = px(lon), py(lat)
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED,
                  outline=(255, 255, 255), width=2)
        num = str(n)
        tw = d.textlength(num, font=sans(13, True))
        d.text((cx - tw / 2, cy - 7), num, font=sans(13, True),
               fill=(255, 255, 255))


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    M = 36
    CW = W - 2 * M

    # Navy masthead band.
    d.rectangle([0, 0, W, 196], fill=NAVY)
    d.text((M, 26), "THE DAY IN WORLD NEWS - BY THE NUMBERS",
           font=sans(24, True), fill=GOLD)
    right = "48 STORIES - ONE PAGE"
    d.text((W - M - d.textlength(right, font=sans(24, True)), 26), right,
           font=sans(24, True), fill=(255, 255, 255))
    d.text((M, 66), "Friday 20 November 2026", font=serif(104, True),
           fill=(255, 255, 255))

    # Giant-figures band.
    y = 206
    colw = CW / 6.0
    for i, (big, lab) in enumerate(FIGURES):
        cx = M + i * colw
        d.text((cx, y), big, font=sans(42, True), fill=RED)
        para(d, cx, y + 52, lab, sans(17), colw - 16, BODY, 21,
             max_lines=2)
        if i:
            d.line([cx - 8, y + 4, cx - 8, y + 92], fill=LIGHT, width=2)
    d.line([M, 302, W - M, 302], fill=INK, width=2)

    # Region strip.
    y = 310
    total = sum(c for _, c, _ in REGIONS)
    rx = M
    for label, count, col in REGIONS:
        seg = CW * count / float(total)
        d.rectangle([rx, y, rx + seg, y + 32], fill=col)
        txt = "%s %d" % (label, count)
        tw = d.textlength(txt, font=sans(16, True))
        if tw > seg - 6:
            txt = str(count)
            tw = d.textlength(txt, font=sans(16, True))
        d.text((rx + (seg - tw) / 2, y + 7), txt, font=sans(16, True),
               fill=(255, 255, 255))
        rx += seg

    # UTC timeline strip.
    y = 352
    d.text((M, y), "THE DAY IN UTC", font=sans(18, True), fill=RED)
    items = "   |   ".join("%s %s" % (t, s) for t, s in TIMELINE)
    para(d, M + 190, y, items, sans(17), CW - 190, INK, 21, max_lines=2)
    d.line([M, 396, W - M, 396], fill=INK, width=2)

    # Heroes.
    y = 406
    hw = (CW - 2 * 14) / 3.0
    for i, item in enumerate(HEROES):
        hero_panel(d, M + i * (hw + 14), y, hw, 268, item)
    d.line([M, 684, W - M, 684], fill=INK, width=2)

    # Pictured rows: 5, then 4, then 4.
    rows = [PICTURED[0:5], PICTURED[5:9], PICTURED[9:13]]
    y = 694
    for row in rows:
        n = len(row)
        pw = (CW - (n - 1) * 14) / float(n)
        for i, item in enumerate(row):
            pic_panel(d, M + i * (pw + 14), y, pw, 190, item)
        y += 200

    # Bottom: map + briefs.
    y = 1294
    d.text((M, y), "WHERE IT HAPPENED", font=sans(20, True), fill=RED)
    d.text((640, y), "ALSO ON FRIDAY 20 NOVEMBER - 32 MORE STORIES",
           font=sans(20, True), fill=RED)
    world_map(d, M, y + 30, 620, y + 208)
    for col_i in range(2):
        bx = 640 + col_i * 470
        for j, (num, place, text) in enumerate(BRIEFS[col_i * 16:(col_i + 1) * 16]):
            yy = y + 32 + j * 12
            d.ellipse([bx, yy + 2, bx + 7, yy + 9], fill=RED)
            line = "%d %s - %s" % (num, place, text)
            para(d, bx + 12, yy - 2, line, sans(12), 452, INK, 12,
                 max_lines=1)

    # Date check box.
    y = 1508
    d.rectangle([M, y, W - M, y + 44], outline=RED, width=3)
    d.rectangle([M, y, M + 150, y + 44], fill=RED)
    d.text((M + 12, y + 11), "DATE CHECK", font=sans(19, True),
           fill=(255, 255, 255))
    para(d, M + 164, y + 4, DATE_CHECK, sans(14), CW - 178, INK, 17,
         max_lines=2)

    # Footer.
    d.text((M, 1560),
           "Every story here happened, or was first reported, on Friday 20 "
           "November 2026, in some time zone. Disputed claims are attributed, "
           "not stated as fact.",
           font=sans(14), fill=BODY)
    d.text((M, 1578),
           "Sources: Reuters - AP - AFP - BBC - Bloomberg - IMD - NASA - IAEA "
           "- The Hindu - Arab News - Sensor Tower. Original drawings, drawn "
           "for this page.",
           font=sans(14), fill=BODY)

    out = im.resize((1024, 1024), Image.LANCZOS)
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append(".")
    candidates.append(os.path.dirname(os.path.abspath(__file__)))
    last_err = None
    saved = None
    for cand in candidates:
        try:
            target = os.path.join(cand, "entry.png")
            out.save(target)
            saved = target
            break
        except OSError as err:
            last_err = err
    if saved is None:
        raise last_err
    print("wrote %s 1024x1024" % saved)


if __name__ == "__main__":
    main()
