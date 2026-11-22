"""A dark "documentary" look for HKPS videos: near-black navy with a faint grid, big white type,
neon accents (cyan, amber, pink, lime), kinetic wipes, and animated graphics: hype-cycle waves, a
building whose top floor keeps getting swapped, a Python iceberg, and a typing terminal.

Every card is a hkpsvid Card (so cues, sounds and the build work unchanged); the look comes from
DocCard.base() and the animation from draw_extra(). Times: None (from the start), seconds, a
[[cue]], (cue, offset), or False (never).
"""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw, ImageFilter

from hkpsvid import draw as D
from hkpsvid.style import H, MARGIN, W, font, mono
from hkpsvid.visuals import Card, ease

BG_TOP, BG_BOT = (16, 21, 38), (5, 7, 14)
CYAN, AMBER, PINK, LIME, VIOLET = (0, 214, 255), (255, 186, 8), (255, 77, 141), (132, 230, 80), (160, 120, 255)
WHITE, DIM, FAINT, PANEL, EDGE = (240, 244, 252), (134, 150, 180), (60, 72, 100), (20, 27, 46), (44, 56, 86)


def clamp(x):
    return min(1.0, max(0.0, x))


def tint(c, k):
    """Mix c towards the dark background (k = 0: c, k = 1: background)."""
    return tuple(int(a * (1 - k) + b * k) for a, b in zip(c, PANEL))


def fade(img, a):
    if a >= 1:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * max(0.0, a))))
    return img


def glow(img, color, radius=14, strength=1.2):
    """A soft halo of `color` behind the opaque parts of img."""
    pad = radius * 2
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad))
    mask = img.getchannel("A")
    halo = Image.new("RGBA", img.size, color + (255,))
    halo.putalpha(mask.point(lambda v: int(min(255, v * 0.6 * strength))))
    big = Image.new("RGBA", out.size)
    big.alpha_composite(halo, (pad, pad))
    out.alpha_composite(big.filter(ImageFilter.GaussianBlur(radius)))
    out.alpha_composite(img, (pad, pad))
    out.info["pad"] = pad
    return out


def rich(text: str, size: int, base=WHITE, accent=CYAN, weight="bold") -> Image.Image:
    """One line of text where **marked** words take the accent colour."""
    f = font(size, weight)
    parts, on = [], False
    for k, seg in enumerate(text.split("**")):
        if seg:
            parts.append((seg, accent if k % 2 else base))
    w = int(sum(f.getlength(s) for s, _ in parts)) + 6
    asc, desc = f.getmetrics()
    im = Image.new("RGBA", (w, asc + desc + 6))
    d = ImageDraw.Draw(im)
    x = 0
    for s, c in parts:
        d.text((x, 2), s, font=f, fill=c)
        x += f.getlength(s)
    return im


def dpill(text, color, size=40, fg=(8, 12, 22)):
    f = font(size, "bold")
    w = int(f.getlength(text)) + 64
    h = size + 34
    im = Image.new("RGBA", (w, h))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=color)
    ImageDraw.Draw(im).text((w / 2, h / 2), text, font=f, fill=fg, anchor="mm")
    return im


class DocCard(Card):
    """Dark background with a faint grid; heading in big white type with a cyan bar; optional
    chapter number. Subclasses animate in draw_extra with self.k(name, t)."""

    tail = 0.8

    def __init__(self, heading: str | None = None, chapter: str | None = None):
        super().__init__(heading)
        self.chapter = chapter
        self._marks: dict = {}
        self.T: dict = {}

    def mark(self, name, at):
        self._marks[name] = at

    def prepare_extra(self, timing):
        self.timing = timing
        self.T = {k: (math.inf if v is False else timing.at(v)) for k, v in self._marks.items()}
        self.setup(timing)
        return max([0.0, *[v for v in self.T.values() if v is not None and v != math.inf]]) + self.tail

    def setup(self, timing):
        pass

    def k(self, name, t, dur=0.6):
        t0 = self.T.get(name)
        return 1.0 if t0 is None else ease(clamp((t - t0) / dur))

    def extra_key(self, t):
        return tuple(round(self.k(n, t) * 40) for n in self._marks)

    def background(self):
        im = D.gradient(W, H, BG_TOP, BG_BOT)
        layer = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(layer)
        for x in range(0, W, 80):
            d.line((x, 0, x, H), fill=(255, 255, 255, 9))
        for y in range(0, H, 80):
            d.line((0, y, W, y), fill=(255, 255, 255, 9))
        im.alpha_composite(layer)
        return im

    def base(self):
        if self._base is None:
            im = self.background()
            d = ImageDraw.Draw(im)
            if self.tag and not self.big_logo:
                d.text((MARGIN, 44), self.tag.upper(), font=font(26, "bold"), fill=DIM)
            if self.heading:
                x = MARGIN
                if self.chapter:
                    d.text((x, 86), self.chapter, font=mono(70, True), fill=CYAN)
                    x += mono(70, True).getlength(self.chapter) + 30
                d.rectangle((MARGIN - 28, 100, MARGIN - 20, 164), fill=CYAN) if not self.chapter else None
                d.text((x, 88), self.heading, font=font(66, "bold"), fill=WHITE)
            self.decorate(im)
            self._base = im
        return self._base


# -- title and statements -------------------------------------------------------------------------

class DocTitle(DocCard):
    """Opening: logo, series, a giant title whose words rise in one by one, subtitle, and slow
    glowing waves along the bottom."""

    big_logo = True

    def __init__(self, series: str, title_words: list[str], subtitle: str, credit: str | None = None):
        super().__init__()
        lg = D.logo()
        s = 150 / lg.height
        lg = lg.resize((round(lg.width * s), 150))
        self.add_center(lg, 90, at=0.05, anim="fade", dur=0.6)
        self.add_center(D.text_img(series, font(40, "bold"), CYAN), 270, at=0.2, anim="fade")
        imgs = [glow(D.text_img(w, font(124, "bold"), WHITE), CYAN, 18, 0.6) for w in title_words]
        total = sum(i.width - 2 * i.info["pad"] for i in imgs) + 24 * (len(imgs) - 1)
        x = (W - total) / 2
        for k, img in enumerate(imgs):
            self.add(img, x, 340, at=0.35 + 0.22 * k, anim="up", dur=0.5)
            x += img.width - 2 * img.info["pad"] + 24
        self.add_center(D.text_img(subtitle, font(46, "medium"), DIM), 540, at=0.35 + 0.22 * len(imgs) + 0.2, anim="fade")
        if credit:
            self.add_center(D.text_img(credit, font(28), FAINT), 960, at=None)

    def extra_key(self, t):
        return round(t * 15)

    def draw_extra(self, im, t):
        layer = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(layer)
        for j, (col, amp, freq, sp) in enumerate(((CYAN, 34, 1.6, 0.5), (VIOLET, 24, 2.3, -0.35), (PINK, 16, 3.1, 0.8))):
            pts = [(x, 790 + j * 26 + amp * math.sin(freq * x / W * 2 * math.pi + t * sp + j)) for x in range(0, W + 20, 20)]
            d.line(pts, fill=col + (150,), width=4, joint="curve")
        im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1)))


class StatementCard(DocCard):
    """Big lines of text (with **accent** words) wiping in from the left at their cues."""

    def __init__(self, heading: str | None, lines: list[tuple], top: int = 320, gap: int = 40, size: int = 68,
                 chapter: str | None = None, center: bool = False):
        super().__init__(heading, chapter)
        self.imgs = []
        y = top
        for i, ln in enumerate(lines):
            txt, at = ln[0], ln[1]
            o = ln[2] if len(ln) > 2 else {}
            img = rich(txt, o.get("size", size), o.get("color", WHITE), o.get("accent", CYAN), o.get("weight", "bold"))
            x = (W - img.width) / 2 if center else MARGIN
            self.imgs.append((img, x, y))
            self.mark(f"l{i}", at)
            y += img.height + gap

    def extra_key(self, t):
        return tuple(round(self.k(f"l{i}", t, 0.8) * 40) for i in range(len(self.imgs)))

    def draw_extra(self, im, t):
        for i, (img, x, y) in enumerate(self.imgs):
            g = self.k(f"l{i}", t, 0.8)
            if g <= 0:
                continue
            w = max(1, int(img.width * g))
            im.alpha_composite(img.crop((0, 0, w, img.height)), (int(x), int(y)))
            if g < 1:
                ImageDraw.Draw(im).rectangle((x + w, y + 6, x + w + 6, y + img.height - 6), fill=CYAN)


# -- the hype cycles ---------------------------------------------------------------------------------

class WaveCard(DocCard):
    """Years along the bottom; each technology wave rises and falls as a glowing bump traced in at
    its cue; the foundation line climbs slowly underneath all of them."""

    def __init__(self, heading, waves: list[tuple], foundation_at=False, years=(1994, 2027), chapter=None,
                 now: int | None = 2026):
        super().__init__(heading, chapter)
        self.waves, self.years, self.now = waves, years, now
        for i, wv in enumerate(waves):
            self.mark(f"w{i}", wv[6])
        self.mark("found", foundation_at)
        self.x0, self.x1, self.yb, self.ytop = 170, W - 120, 840, 300

    def X(self, yr):
        a, b = self.years
        return self.x0 + (yr - a) / (b - a) * (self.x1 - self.x0)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 1.4) * 50) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        d.line((self.x0, self.yb, self.x1, self.yb), fill=DIM, width=3)
        for yr in range(1995, self.years[1] + 1, 5):
            x = self.X(yr)
            d.line((x, self.yb, x, self.yb + 12), fill=DIM, width=3)
            d.text((x, self.yb + 20), str(yr), font=font(28, "bold"), fill=DIM, anchor="mt")
        if self.now:
            x = self.X(self.now)
            for yy in range(self.ytop, self.yb, 20):
                d.line((x, yy, x, yy + 10), fill=FAINT, width=2)
            d.text((x, self.ytop - 12), "今日", font=font(26, "bold"), fill=DIM, anchor="mb")
        layer = Image.new("RGBA", im.size)
        ld = ImageDraw.Draw(layer)
        for i, (name, start, peak, end, height, col, _) in enumerate(self.waves):
            g = self.k(f"w{i}", t, 1.4)
            if g <= 0:
                continue
            pts = []
            n = 90
            for j in range(n + 1):
                yr = start + (end - start) * j / n
                if j / n > g:
                    break
                if yr <= peak:
                    u = (yr - start) / max(peak - start, 0.1)
                else:
                    u = 1 - (yr - peak) / max(end - peak, 0.1)
                y = self.yb - height * (math.sin(clamp(u) * math.pi / 2) ** 2)
                pts.append((self.X(yr), y))
            if len(pts) > 1:
                ld.polygon(pts + [(pts[-1][0], self.yb), (pts[0][0], self.yb)], fill=col + (38,))
                ld.line(pts, fill=col + (255,), width=5, joint="curve")
            if g > 0.55:
                px = self.X(peak)
                ld.text((px, self.yb - height - 16), name, font=font(34, "bold"), fill=col + (255,), anchor="mb")
        im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.6)))
        gf = self.k("found", t, 1.6)
        if gf > 0:
            a, b = self.years
            pts = []
            for j in range(101):
                if j / 100 > gf:
                    break
                yr = a + 0.5 + (b - a - 1) * j / 100
                pts.append((self.X(yr), self.yb - 30 - 150 * (j / 100) ** 1.3))
            if len(pts) > 1:
                gl = Image.new("RGBA", im.size)
                gd = ImageDraw.Draw(gl)
                gd.line(pts, fill=CYAN + (255,), width=16)
                im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
                ImageDraw.Draw(im).line(pts, fill=WHITE, width=6)
                if gf > 0.95:
                    ImageDraw.Draw(im).text((pts[-1][0] - 10, pts[-1][1] - 22), "基礎：一路累積", font=font(36, "bold"),
                                            fill=CYAN, anchor="rb")


class EventLine(DocCard):
    """A horizontal timeline; events pop in at their cues. events: (year, title, sub, colour, at)."""

    def __init__(self, heading, events: list[tuple], chapter=None, y: int = 560):
        super().__init__(heading, chapter)
        self.events, self.y = events, y
        for i, ev in enumerate(events):
            self.mark(f"e{i}", ev[4])

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        n = len(self.events)
        xs = [MARGIN + 140 + i * (W - 2 * MARGIN - 280) / max(1, n - 1) for i in range(n)]
        shown = [self.k(f"e{i}", t) for i in range(n)]
        last = max([i for i in range(n) if shown[i] > 0], default=-1)
        if last >= 0:
            d.line((xs[0] - 100, self.y, xs[last] + (60 if last < n - 1 else 100), self.y), fill=DIM, width=4)
        for i, (yr, title, sub, col, _) in enumerate(self.events):
            g = shown[i]
            if g <= 0:
                continue
            layer = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(layer)
            x = xs[i]
            r = 16 + 8 * (1 - g)
            ld.ellipse((x - r, self.y - r, x + r, self.y + r), fill=col)
            up = i % 2 == 0
            ld.text((x, self.y - 40 if up else self.y + 40), yr, font=mono(52, True), fill=col, anchor="mb" if up else "mt")
            ty = self.y - 108 if up else self.y + 110
            ld.text((x, ty), title, font=font(38, "bold"), fill=WHITE, anchor="mb" if up else "mt")
            ld.text((x, ty - 52 if up else ty + 52), sub, font=font(28, "medium"), fill=DIM, anchor="mb" if up else "mt")
            im.alpha_composite(fade(layer, g))


# -- the building ----------------------------------------------------------------------------------------

class FoundationCard(DocCard):
    """Foundation layers stack up from the ground; above them the 'tool of the day' block is swapped
    at each cue: the old one falls away, the new one drops in."""

    def __init__(self, heading, layers: list[tuple], layers_at, tools: list[tuple], chapter=None):
        super().__init__(heading, chapter)
        self.layers, self.tools = layers, tools
        for i in range(len(layers)):
            self.mark(f"L{i}", (layers_at, 0.25 * i) if isinstance(layers_at, str) else layers_at)
        for i, tl in enumerate(tools):
            self.mark(f"T{i}", tl[2])
        self.cx, self.ground = W // 2 + 180, 900

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 0.7) * 40) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        d.line((MARGIN, self.ground, W - MARGIN, self.ground), fill=DIM, width=3)
        y = self.ground
        lh = 74
        for i, (name, col) in enumerate(self.layers):
            g = self.k(f"L{i}", t, 0.5)
            if g <= 0:
                break
            w = 1100 - i * 70
            yy = y - lh - 8
            off = (1 - g) * 40
            layer = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(layer)
            ld.rounded_rectangle((self.cx - w / 2, yy - off, self.cx + w / 2, yy + lh - off), 12, fill=tint(col, 0.55),
                                 outline=col, width=3)
            ld.text((self.cx, yy + lh / 2 - off), name, font=font(34, "bold"), fill=WHITE, anchor="mm")
            im.alpha_composite(fade(layer, g))
            y = yy
        top = y
        cur = -1
        for i in range(len(self.tools)):
            if self.k(f"T{i}", t, 0.01) > 0:
                cur = i
        if cur >= 0 and self.k(f"L{len(self.layers) - 1}", t) > 0:
            # the previous tool falling away
            if cur > 0:
                gp = self.k(f"T{cur}", t, 0.8)
                if gp < 1:
                    name, col, _ = self.tools[cur - 1]
                    self._tool(im, name, col, top - 120 + gp * 90, 1 - gp, rot=gp * 14)
            name, col, _ = self.tools[cur]
            g = self.k(f"T{cur}", t, 0.6)
            self._tool(im, name, col, top - 120 - (1 - g) * 160, g)
            d.text((MARGIN, top - 70), "今日嘅工具", font=font(30, "bold"), fill=DIM, anchor="lm")
            d.text((MARGIN, (top + self.ground) / 2), "地基", font=font(30, "bold"), fill=DIM, anchor="lm")

    def _tool(self, im, name, col, y, a, rot=0.0):
        box = Image.new("RGBA", (520, 104))
        bd = ImageDraw.Draw(box)
        bd.rounded_rectangle((0, 0, 519, 103), 18, fill=tint(col, 0.35), outline=col, width=4)
        bd.text((260, 52), name, font=font(42, "bold"), fill=WHITE, anchor="mm")
        if rot:
            box = box.rotate(-rot, expand=True, resample=Image.BICUBIC)
        box = glow(fade(box, a), col, 12, 0.8 * a)
        p = box.info["pad"]
        im.alpha_composite(box, (int(self.cx - box.width / 2), int(y - p)))


# -- the iceberg -------------------------------------------------------------------------------------------

class IcebergCard(DocCard):
    """A line of Python above a moving waterline; the layers underneath light up at their cues,
    each wider and deeper than the last."""

    def __init__(self, heading, code: str, layers: list[tuple], code_at=None, chapter=None, note: tuple | None = None):
        super().__init__(heading, chapter)
        self.code, self.layers = code, layers
        self.mark("code", code_at)
        for i, ly in enumerate(layers):
            self.mark(f"L{i}", ly[3])
        self.note = note
        if note:
            self.mark("note", note[1])
        self.water = 430

    def extra_key(self, t):
        return round(t * 12), tuple(round(self.k(n, t) * 30) for n in self._marks)

    def draw_extra(self, im, t):
        cx = W / 2 - 120
        # water
        layer = Image.new("RGBA", im.size)
        ld = ImageDraw.Draw(layer)
        pts = [(x, self.water + 8 * math.sin(x / 90 + t * 1.4)) for x in range(0, W + 30, 30)]
        ld.polygon(pts + [(W, H), (0, H)], fill=(0, 120, 200, 46))
        ld.line(pts, fill=CYAN + (200,), width=4, joint="curve")
        im.alpha_composite(layer)
        g = self.k("code", t)
        if g > 0:
            chip = D.code_chip(self.code, 46)
            chip = glow(fade(chip, g), CYAN, 14, 0.7)
            im.alpha_composite(chip, (int(cx - chip.width / 2), int(self.water - 150 - chip.info["pad"] + (1 - g) * 20)))
        y = self.water + 40
        for i, (name, sub, col, _) in enumerate(self.layers):
            g = self.k(f"L{i}", t)
            if g <= 0:
                continue
            w = 560 + i * 170
            h = 92
            lay = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle((cx - w / 2, y, cx + w / 2, y + h), 16, fill=tint(col, 0.6), outline=col, width=3)
            ld.text((cx, y + 32), name, font=font(38, "bold"), fill=WHITE, anchor="mm")
            ld.text((cx, y + 70), sub, font=font(26, "medium"), fill=DIM, anchor="mm")
            im.alpha_composite(fade(lay, g))
            y += h + 14
        if self.note:
            gn = self.k("note", t)
            if gn > 0:
                txt = rich(self.note[0], 40, WHITE, AMBER)
                im.alpha_composite(fade(txt, gn), (W - MARGIN - txt.width, 300))


# -- the terminal --------------------------------------------------------------------------------------

class TerminalCard(DocCard):
    """A Python REPL typing entries at their cues; each entry's output appears when its typing is
    done. Optional bars (label, value_text, length 0..1, colour, at) sit to the right."""

    CPS = 26

    def __init__(self, heading, entries: list[tuple], bars: list[tuple] = (), chapter=None, foot: tuple | None = None,
                 width: int = 1040):
        super().__init__(heading, chapter)
        self.entries, self.bars, self.width = entries, bars, width
        for i, en in enumerate(entries):
            self.mark(f"e{i}", en[2])
        for i, b in enumerate(bars):
            self.mark(f"b{i}", b[4])
        self.foot = foot
        if foot:
            self.mark("foot", foot[1])

    def extra_key(self, t):
        out = []
        for i, (code, _, _, *rest) in enumerate(self.entries):
            t0 = self.T.get(f"e{i}")
            n = 0 if t0 is None or t < t0 else min(len(code), int((t - t0) * self.CPS))
            out.append(n if t0 is not None else len(code))
        return tuple(out), round(t * 2) % 2, tuple(round(self.k(f"b{i}", t, 1.0) * 40) for i in range(len(self.bars))), \
            round(self.k("foot", t) * 20) if self.foot else 0

    def draw_extra(self, im, t):
        x0, y0, w = MARGIN, 270, self.width
        n_lines = sum(1 + c.count("\n") + (1 if o else 0) for c, o, _, *r in self.entries)
        h = 80 + n_lines * 50
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 22, fill=(9, 12, 20), outline=EDGE, width=2)
        for k, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
            d.ellipse((x0 + 26 + k * 30, y0 + 22, x0 + 42 + k * 30, y0 + 38), fill=c)
        d.text((x0 + w / 2, y0 + 30), "ipython", font=font(24, "bold"), fill=DIM, anchor="mm")
        f = mono(34, True)
        y = y0 + 70
        cursor_at = None
        for i, (code, outp, _, *rest) in enumerate(self.entries):
            col = rest[0] if rest else WHITE
            t0 = self.T.get(f"e{i}")
            if t0 is not None and t < t0:
                break
            n = len(code) if t0 is None else min(len(code), int((t - t0) * self.CPS))
            typed = code[:n]
            for j, ln in enumerate(typed.split("\n")):
                prompt = f"In [{i + 1}]: " if j == 0 else "   ...: "
                d.text((x0 + 30, y), prompt, font=f, fill=LIME)
                d.text((x0 + 30 + f.getlength(prompt), y), ln, font=f, fill=WHITE)
                cursor_at = (x0 + 30 + f.getlength(prompt + ln), y)
                y += 50
            if n < len(code):
                break
            if outp:
                d.text((x0 + 30, y), outp, font=f, fill=col)
                y += 50
                cursor_at = None
        if cursor_at and int(t * 2) % 2 == 0:
            d.rectangle((cursor_at[0] + 4, cursor_at[1] + 4, cursor_at[0] + 22, cursor_at[1] + 40), fill=WHITE)
        bx = x0 + w + 70
        bw = W - MARGIN - bx
        for i, (label, val, L, colr, _) in enumerate(self.bars):
            g = self.k(f"b{i}", t, 1.0)
            if g <= 0:
                continue
            by = 300 + i * 200
            d.text((bx, by), label, font=font(36, "bold"), fill=WHITE)
            length = max(6, bw * L * g)
            gl = Image.new("RGBA", im.size)
            ImageDraw.Draw(gl).rounded_rectangle((bx, by + 60, bx + length, by + 112), 12, fill=colr)
            im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(8)))
            d.rounded_rectangle((bx, by + 60, bx + length, by + 112), 12, fill=colr)
            if g > 0.9:
                d.text((bx + (length + 16 if L < 0.6 else 0), by + 130 if L >= 0.6 else by + 86), val, font=font(38, "bold"),
                       fill=colr, anchor="lt" if L >= 0.6 else "lm")
        if self.foot:
            gf = self.k("foot", t)
            if gf > 0:
                if y0 + h < 850 or not self.bars:
                    txt = rich(self.foot[0], 40, WHITE, AMBER)
                    im.alpha_composite(fade(txt, gf), (MARGIN, max(880, y0 + h + 30) if y0 + h < 850 else 880))
                else:
                    txt = D.text_img(self.foot[0].replace("**", ""), font(38, "bold"), AMBER, max_w=W - MARGIN - bx)
                    im.alpha_composite(fade(txt, gf), (int(bx), 720))


# -- comparisons and the end -------------------------------------------------------------------------------

class VersusCard(DocCard):
    """Two dark panels; each line slides in at its cue. cols: (title, colour, [(text, at)])."""

    def __init__(self, heading, cols: list[tuple], chapter=None, footer: tuple | None = None):
        super().__init__(heading, chapter)
        self.cols = cols
        for c, (_, _, lines) in enumerate(cols):
            for j, (_, at) in enumerate(lines):
                self.mark(f"c{c}_{j}", at)
        self.footer = footer
        if footer:
            self.mark("foot", footer[1])

    def draw_extra(self, im, t):
        pw = (W - 2 * MARGIN - 60) / 2
        for c, (title, col, lines) in enumerate(self.cols):
            g0 = self.k(f"c{c}_0", t)
            if g0 <= 0:
                continue
            x = MARGIN + c * (pw + 60)
            lay = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(lay)
            ld.rounded_rectangle((x, 280, x + pw, 780), 26, fill=PANEL, outline=col, width=3)
            ld.rectangle((x + 30, 318, x + 38, 370), fill=col)
            ld.text((x + 58, 344), title, font=font(48, "bold"), fill=col, anchor="lm")
            im.alpha_composite(fade(lay, g0))
            for j, (txt, _) in enumerate(lines):
                g = self.k(f"c{c}_{j}", t)
                if g <= 0:
                    continue
                img = rich(txt, 40, WHITE, col, "medium")
                im.alpha_composite(fade(img, g), (int(x + 40 + (1 - g) * 30), 420 + j * 100))
        if self.footer:
            g = self.k("foot", t)
            if g > 0:
                p = fade(dpill(self.footer[0], self.footer[2] if len(self.footer) > 2 else AMBER, 40), g)
                im.alpha_composite(p, ((W - p.width) // 2, 830))


class ShelfCard(DocCard):
    """'Shelf life' rows: name, born, status, with a bar from the year it appeared to its end (or
    to today, glowing, if it is still in use). rows: (name, start, end_or_None, status, colour, at)."""

    def __init__(self, heading, rows: list[tuple], years=(1840, 2026), chapter=None, footer: tuple | None = None):
        super().__init__(heading, chapter)
        self.rows, self.years = rows, years
        for i, r in enumerate(rows):
            self.mark(f"r{i}", r[5])
        self.footer = footer
        if footer:
            self.mark("foot", footer[1])
        self.x0, self.x1 = 620, W - MARGIN

    def X(self, yr):
        a, b = self.years
        return self.x0 + (yr - a) / (b - a) * (self.x1 - self.x0)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 1.0) * 40) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        for yr in range(self.years[0], self.years[1] + 1, 40 if self.years[1] - self.years[0] > 100 else 10):
            x = self.X(yr)
            d.line((x, 290, x, 800), fill=(255, 255, 255, 18), width=1)
            d.text((x, 810), str(yr), font=font(26, "bold"), fill=DIM, anchor="mt")
        for i, (name, a, b, status, col, _) in enumerate(self.rows):
            g = self.k(f"r{i}", t, 1.0)
            if g <= 0:
                continue
            y = 300 + i * 120
            d.text((MARGIN, y + 26), name, font=font(40, "bold"), fill=WHITE, anchor="lm")
            d.text((MARGIN, y + 72), status, font=font(28, "medium"), fill=col, anchor="lm")
            end = b if b else self.years[1]
            xa, xb = self.X(a), self.X(a + (end - a) * g)
            if not b:
                gl = Image.new("RGBA", im.size)
                ImageDraw.Draw(gl).rounded_rectangle((xa, y + 10, xb, y + 50), 10, fill=col)
                im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(9)))
            d.rounded_rectangle((xa, y + 10, max(xb, xa + 8), y + 50), 10, fill=col if not b else tint(col, 0.35),
                                outline=col, width=2)
            d.text((xa, y + 64), str(a), font=font(24, "bold"), fill=DIM, anchor="lt")
            if b and g > 0.95:
                d.text((xb + 12, y + 30), f"{b} 完", font=font(28, "bold"), fill=PINK, anchor="lm")
        if self.footer:
            gf = self.k("foot", t)
            if gf > 0:
                p = fade(dpill(self.footer[0], self.footer[2] if len(self.footer) > 2 else CYAN, 40), gf)
                im.alpha_composite(p, ((W - p.width) // 2, 870))


class DocEnd(DocCard):
    """Closing: logo, 多謝收睇, the challenge box with a glowing edge, a line about what is next."""

    big_logo = True

    def __init__(self, challenge: str, next_line: str, challenge_at=None, next_at=None, credit: str | None = None):
        super().__init__()
        lg = D.logo()
        s = 130 / lg.height
        self.add_center(lg.resize((round(lg.width * s), 130)), 70, at=None)
        self.add_center(D.text_img("多謝收睇", font(84, "bold"), WHITE), 240, at=None)
        bw = 1440
        txt = D.text_img(challenge, font(44, "medium"), WHITE, max_w=bw - 120, line_h=1.45)
        bh = txt.height + 150
        box = Image.new("RGBA", (bw, bh))
        bd = ImageDraw.Draw(box)
        bd.rounded_rectangle((0, 0, bw - 1, bh - 1), 28, fill=PANEL, outline=AMBER, width=4)
        box.alpha_composite(dpill("小挑戰", AMBER, 34), (56, 32))
        box.alpha_composite(txt, (60, 116))
        self.add_center(glow(box, AMBER, 16, 0.5), 400, at=challenge_at, anim="pop", sound="pop")
        self.add_center(D.text_img(next_line, font(48, "bold"), CYAN), 400 + bh + 60, at=next_at)
        if credit:
            self.add_center(D.text_img(credit, font(28), FAINT), 960, at=None)
