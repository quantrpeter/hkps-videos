"""Animated cards for the entropy video, in the HKPS card style (light background, PingFang, the
logo blue). They build on hkpsvid.visuals.Card: items still appear at their cues, and each class
adds its own animation in draw_extra, with extra_key changing only while something moves.

Times (`at`) work as everywhere else: None, seconds, a [[cue]] name, or (cue, offset).
"""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

from hkpsvid import draw as D
from hkpsvid.style import (AMBER, BLUE, GREEN, INK, LINE, MARGIN, MUTED, NAVY, PURPLE, RED, TEAL, W, WHITE,
                           font, mono)
from hkpsvid.visuals import Card, ease

SYM_COLOR = {"↑": BLUE, "↓": TEAL, "←": AMBER, "→": PURPLE}
NAIVE = {"↑": "00", "↓": "01", "←": "10", "→": "11"}
CLEVER = {"↑": "0", "↓": "10", "←": "110", "→": "111"}
ROBOT_P = {"↑": 0.5, "↓": 0.25, "←": 0.125, "→": 0.125}
FRAC = {0.5: "½", 0.25: "¼", 0.125: "⅛"}
PALETTE = [BLUE, TEAL, AMBER, PURPLE, GREEN, RED]


def clamp(x: float) -> float:
    return min(1.0, max(0.0, x))


def tint(c, k: float = 0.85) -> tuple:
    return tuple(int(v + (255 - v) * k) for v in c[:3])


def fade(img: Image.Image, a: float) -> Image.Image:
    if a >= 1:
        return img
    img = img.copy()
    img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    return img


def math_img(s: str, size: int = 56, fill=NAVY, weight: str = "medium") -> Image.Image:
    """Text with ^ and _ for superscripts and subscripts (one character or a {group}); '-' prints
    as a minus sign. PingFang has no superscript n or subscript i, so they are drawn small."""
    f, fs = font(size, weight), font(int(size * 0.6), weight)
    parts, buf, i = [], "", 0
    while i < len(s):
        c = s[i]
        if c in "^_" and i + 1 < len(s):
            if buf:
                parts.append((buf, "base"))
                buf = ""
            if s[i + 1] == "{":
                j = s.index("}", i + 2)
                grp, i = s[i + 2:j], j + 1
            else:
                grp, i = s[i + 1], i + 2
            parts.append((grp, "sup" if c == "^" else "sub"))
            continue
        buf += c
        i += 1
    if buf:
        parts.append((buf, "base"))
    parts = [(t.replace("-", "−"), k) for t, k in parts]
    top = int(size * 0.3)
    asc, desc = f.getmetrics()
    wd = sum((f if k == "base" else fs).getlength(t) + (0 if k == "base" else 5) for t, k in parts)
    im = Image.new("RGBA", (int(wd) + 6, asc + desc + top + int(size * 0.2)))
    d = ImageDraw.Draw(im)
    x = 0.0
    for t, k in parts:
        if k == "base":
            d.text((x, top), t, font=f, fill=fill)
            x += f.getlength(t)
        elif k == "sup":
            d.text((x + 2, top - size * 0.2), t, font=fs, fill=fill)
            x += fs.getlength(t) + 5
        else:
            d.text((x + 2, top + size * 0.5), t, font=fs, fill=fill)
            x += fs.getlength(t) + 5
    return im


def boxed(img: Image.Image, color=BLUE, px: int = 36, py: int = 16) -> Image.Image:
    """An equation on a tinted rounded box (the line to remember)."""
    im = Image.new("RGBA", (img.width + 2 * px, img.height + 2 * py))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 24, fill=tint(color, 0.88),
                                         outline=color, width=4)
    im.alpha_composite(img, (px, py))
    return im


def arrow_tile(sym: str, size: int = 84, alpha: float = 1.0) -> Image.Image:
    c = SYM_COLOR.get(sym, NAVY)
    im = Image.new("RGBA", (size, size))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size - 1, size - 1), size // 5, fill=tint(c, 0.86), outline=c, width=3)
    d.text((size / 2, size / 2 + 2), sym, font=font(int(size * 0.62), "bold"), fill=c, anchor="mm")
    return fade(im, alpha)


def pie(p: float, r: int, color=BLUE, bg=LINE) -> Image.Image:
    im = Image.new("RGBA", (2 * r + 4, 2 * r + 4))
    d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 2 * r + 2, 2 * r + 2), fill=WHITE, outline=bg, width=3)
    if p >= 0.999:
        d.ellipse((2, 2, 2 * r + 2, 2 * r + 2), fill=color)
    elif p > 0.001:
        d.pieslice((2, 2, 2 * r + 2, 2 * r + 2), -90, -90 + 360 * p, fill=color)
    return im


class Anim(Card):
    """A Card with named times: mark(name, at) in __init__, then self.T[name] in draw_extra."""

    tail = 0.8

    def __init__(self, heading: str | None = None):
        super().__init__(heading)
        self._marks: dict[str, object] = {}
        self.T: dict[str, float | None] = {}

    def mark(self, name: str, at) -> None:
        self._marks[name] = at

    def prepare_extra(self, timing):
        self.timing = timing
        self.T = {k: timing.at(v) for k, v in self._marks.items()}
        self.setup(timing)
        return max([0.0, *[v for v in self.T.values() if v is not None]]) + self.tail

    def setup(self, timing) -> None:
        pass

    def k(self, name: str, t: float, dur: float = 0.6) -> float:
        t0 = self.T.get(name)
        return 1.0 if t0 is None else ease(clamp((t - t0) / dur))

    def extra_key(self, t):
        return tuple(round(self.k(n, t) * 40) for n in self._marks)


# -- bits per character ---------------------------------------------------------------------------

class CueBarCard(Anim):
    """Horizontal bars, each growing at its own cue. bars: (label, value, text, colour, at)."""

    X0, MAX_LEN, BAR_H = 600, 980, 92

    def __init__(self, heading: str, bars: list[tuple], top: int = 300, step: int = 150,
                 pill: tuple | None = None, note: str | None = None):
        super().__init__(heading)
        self.bars, self.top, self.step = bars, top, step
        vmax = max(b[1] for b in bars)
        self._len = [max(16, b[1] / vmax * self.MAX_LEN) for b in bars]
        for i, b in enumerate(bars):
            self.mark(f"b{i}", b[4])
            self.add(D.text_img(b[0], font(50, "bold"), NAVY), MARGIN, top + i * step + 14, b[4], anim="fade")
        if pill:
            txt, at, color = pill
            self.add_center(D.pill(txt, font(46, "bold"), WHITE, color, px=44, py=16), top + len(bars) * step + 20,
                            at=at, anim="pop", sound="pop")
        if note:
            self.add(D.text_img(note, font(28), MUTED), W - MARGIN - D.width(note, font(28)), 860, None)

    def extra_key(self, t):
        return tuple(round(self.k(f"b{i}", t, 1.0) * 60) for i in range(len(self.bars)))

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        for i, b in enumerate(self.bars):
            g = self.k(f"b{i}", t, 1.0)
            if g <= 0:
                continue
            y = self.top + i * self.step
            L = self._len[i] * g
            d.rounded_rectangle((self.X0, y, self.X0 + max(L, 16), y + self.BAR_H), 18, fill=b[3])
            if g > 0.9:
                v = fade(D.text_img(b[2], font(50, "bold"), b[3]), (g - 0.9) * 10)
                im.alpha_composite(v, (int(self.X0 + L + 28), int(y + (self.BAR_H - v.height) / 2)))


# -- the robot -----------------------------------------------------------------------------------

class RobotCard(Anim):
    """The robot on a moon grid, stepping through random instructions, with the instruction feed
    and the probability strip on the right."""

    GRID, CELL = 9, 70

    def __init__(self, heading: str, go, probs_at=None, step: float = 0.9, seed: int = 4):
        super().__init__(heading)
        self.mark("go", go)
        self.mark("probs", probs_at)
        self.step, self.seed = step, seed
        self.gx, self.gy = MARGIN, 272
        size = self.GRID * self.CELL
        moon = D.shadow_box(size, size, 28, (236, 241, 249), outline=LINE, blur=14)
        p = moon.info["pad"]
        md = ImageDraw.Draw(moon)
        for k in range(1, self.GRID):
            md.line((p + k * self.CELL, p + 10, p + k * self.CELL, p + size - 10), fill=(222, 230, 242), width=2)
            md.line((p + 10, p + k * self.CELL, p + size - 10, p + k * self.CELL), fill=(222, 230, 242), width=2)
        rng = random.Random(9)
        for _ in range(7):
            cx, cy, r = rng.randint(40, size - 40), rng.randint(40, size - 40), rng.randint(14, 34)
            md.ellipse((p + cx - r, p + cy - r, p + cx + r, p + cy + r), outline=(208, 218, 234), width=4)
        moon.info["pad"] = p
        self.add(moon, self.gx, self.gy, None)
        self.add(D.text_img("🌕 遙遠嘅月球", font(30, "medium"), MUTED), self.gx, self.gy + size + 14, None)
        rx = 900
        self.add(D.text_img("地球發出嘅指令", font(40, "bold"), NAVY), rx, 290, go, anim="fade")
        self.add(D.text_img("每個指令嘅機率", font(40, "bold"), NAVY), rx, 560, probs_at, anim="fade")
        self.robot = D.emoji("🤖", 60)

    def setup(self, timing):
        rng = random.Random(self.seed)
        n = int((timing.speech_end + 3 - (self.T["go"] or 0)) / self.step) + 2
        syms, wts = list(ROBOT_P), list(ROBOT_P.values())
        self.moves = rng.choices(syms, wts, k=max(n, 4))
        pos, self.path = [self.GRID // 2, self.GRID // 2], []
        for m in self.moves:
            dx, dy = {"↑": (0, -1), "↓": (0, 1), "←": (-1, 0), "→": (1, 0)}[m]
            pos = [(pos[0] + dx) % self.GRID, (pos[1] + dy) % self.GRID]
            self.path.append(tuple(pos))

    def _state(self, t):
        t0 = self.T["go"]
        if t0 is None or t < t0:
            return -1, 0.0
        f = (t - t0) / self.step
        return min(int(f), len(self.moves) - 1), clamp((f - int(f)) / 0.45)

    def extra_key(self, t):
        i, s = self._state(t)
        return i, round(s * 12), round(self.k("probs", t, 0.8) * 30)

    def draw_extra(self, im, t):
        i, s = self._state(t)
        c = self.CELL
        start = (self.GRID // 2, self.GRID // 2)
        if i < 0:
            pos = start
        else:
            a = self.path[i - 1] if i > 0 else start
            b = self.path[i]
            jump = abs(a[0] - b[0]) > 1 or abs(a[1] - b[1]) > 1     # wrapped round the edge
            e = ease(s)
            pos = b if jump else (a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e)
        d = ImageDraw.Draw(im)
        for k in range(max(0, i - 6), max(0, i)):
            px, py = self.path[k]
            d.ellipse((self.gx + px * c + c / 2 - 6, self.gy + py * c + c / 2 - 6,
                       self.gx + px * c + c / 2 + 6, self.gy + py * c + c / 2 + 6), fill=tint(BLUE, 0.55))
        r = self.robot
        im.alpha_composite(r, (int(self.gx + pos[0] * c + (c - r.width) / 2), int(self.gy + pos[1] * c + (c - r.height) / 2)))
        # the feed: the latest instructions, newest on the right
        if i >= 0:
            shown = self.moves[max(0, i - 8): i + 1]
            for j, m in enumerate(shown):
                a = 1.0 if j < len(shown) - 1 else ease(s)
                im.alpha_composite(arrow_tile(m, 84, a), (900 + j * 96, 370))
        # the probability strip
        g = self.k("probs", t, 0.8)
        if g > 0:
            x, wd, y = 900, 880, 640
            for sym, p in ROBOT_P.items():
                w = wd * p * g
                col = SYM_COLOR[sym]
                d.rounded_rectangle((x, y, x + w - 6, y + 110), 16, fill=tint(col, 0.8), outline=col, width=3)
                if g > 0.95:
                    d.text((x + (w - 6) / 2, y + 40), sym, font=font(46, "bold"), fill=col, anchor="mm")
                    d.text((x + (w - 6) / 2, y + 86), FRAC[p], font=font(36, "bold"), fill=NAVY, anchor="mm")
                x += w


# -- encoding a stream of instructions ------------------------------------------------------------

class StreamCard(Anim):
    """A row of instructions revealed one by one; under it, each code's bit string grows with a
    running count. codes: (name, mapping, colour)."""

    TILE, GAP = 80, 12

    def __init__(self, heading: str, seq: str, codes: list[tuple], start, end, book_at=None,
                 pill: tuple | None = None, top: int = 270):
        super().__init__(heading)
        self.seq, self.codes, self.top = seq, codes, top
        self.mark("start", start)
        self.mark("end", end)
        self.mark("book", book_at)
        n = len(seq)
        self.x0 = (W - (n * (self.TILE + self.GAP) - self.GAP)) // 2
        # the code books, one row per code
        for r, (name, mp, color) in enumerate(codes):
            row = Image.new("RGBA", (1680, 74))
            rd = ImageDraw.Draw(row)
            rd.text((0, 37), name, font=font(36, "bold"), fill=color, anchor="lm")
            x = 330
            for sym, bits in mp.items():
                row.alpha_composite(arrow_tile(sym, 62), (int(x), 6))
                rd.text((x + 76, 37), bits, font=mono(40, True), fill=NAVY, anchor="lm")
                x += 76 + mono(40).getlength(bits) + 70
            self.add(row, MARGIN, top + r * 84, book_at if r == 0 else (book_at if isinstance(book_at, (int, float)) or book_at is None else (book_at, 0.4 * r)), anim="fade")
        if pill:
            txt, at, color = pill
            self.add_center(D.pill(txt, font(44, "bold"), WHITE, color, px=40, py=14), 820, at=at, anim="pop", sound="pop")

    def setup(self, timing):
        a, b = self.T["start"] or 0.0, self.T["end"]
        if b is None or b <= a:
            b = a + 0.5 * len(self.seq)
        self.dt = (b - a) / len(self.seq)

    def _count(self, t):
        a = self.T["start"] or 0.0
        if t < a:
            return 0, 0.0
        f = (t - a) / self.dt
        return min(len(self.seq), int(f) + 1), clamp((f - int(f)) / 0.4)

    def extra_key(self, t):
        n, s = self._count(t)
        return n, round(s * 10), round(self.k("book", t) * 30)

    def draw_extra(self, im, t):
        n, s = self._count(t)
        d = ImageDraw.Draw(im)
        y = self.top + len(self.codes) * 84 + 40
        for i, sym in enumerate(self.seq):
            x = self.x0 + i * (self.TILE + self.GAP)
            if i < n:
                a = 1.0 if i < n - 1 else ease(s)
                im.alpha_composite(arrow_tile(sym, self.TILE, a), (x, y))
            else:
                d.rounded_rectangle((x, y, x + self.TILE - 1, y + self.TILE - 1), 16, outline=LINE, width=3)
        f = mono(34, True)
        adv = f.getlength("0")
        for r, (name, mp, color) in enumerate(self.codes):
            yy = y + self.TILE + 50 + r * 110
            d.text((MARGIN, yy + 20), name, font=font(30, "bold"), fill=color, anchor="lm")
            x = MARGIN + 250
            total = 0
            for i, sym in enumerate(self.seq[:n]):
                bits = mp[sym]
                col = SYM_COLOR[sym] if i % 2 == 0 else NAVY
                d.text((x, yy + 20), bits, font=f, fill=col, anchor="lm")
                x += adv * len(bits) + 4
                total += len(bits)
            d.text((W - MARGIN, yy + 20), f"{total} bits", font=font(40, "bold"), fill=color, anchor="rm")


class DecodeCard(Anim):
    """The robot reading bits one at a time: the open buffer is outlined, and each completed code
    word drops its instruction into the output row."""

    BOX, GAP = 76, 10

    def __init__(self, heading: str, words: list[str], book: dict, start, end, top: int = 280):
        super().__init__(heading)
        self.words, self.book, self.top = words, {v: k for k, v in book.items()}, top
        self.bits = "".join(words)
        self.mark("start", start)
        self.mark("end", end)
        row = Image.new("RGBA", (1680, 74))
        rd = ImageDraw.Draw(row)
        rd.text((0, 37), "碼表", font=font(36, "bold"), fill=MUTED, anchor="lm")
        x = 150
        for sym, bits in book.items():
            row.alpha_composite(arrow_tile(sym, 62), (int(x), 6))
            rd.text((x + 76, 37), bits, font=mono(40, True), fill=NAVY, anchor="lm")
            x += 76 + mono(40).getlength(bits) + 70
        self.add(row, MARGIN, top, None)
        self.x0 = (W - (len(self.bits) * (self.BOX + self.GAP) - self.GAP)) // 2
        self.ends = []
        k = 0
        for w in words:
            k += len(w)
            self.ends.append(k)

    def setup(self, timing):
        a, b = self.T["start"] or 0.0, self.T["end"]
        if b is None or b <= a:
            b = a + 0.7 * len(self.bits)
        self.dt = (b - a) / len(self.bits)

    def _read(self, t):
        a = self.T["start"] or 0.0
        return 0 if t < a else min(len(self.bits), int((t - a) / self.dt) + 1)

    def extra_key(self, t):
        return self._read(t)

    def draw_extra(self, im, t):
        n = self._read(t)
        d = ImageDraw.Draw(im)
        y = self.top + 150
        done = [e for e in self.ends if e <= n]
        open_from = done[-1] if done else 0
        for i, b in enumerate(self.bits):
            x = self.x0 + i * (self.BOX + self.GAP)
            if i < n:
                w = next(j for j, e in enumerate(self.ends) if e > i)
                sym = self.book[self.words[w]]
                complete = self.ends[w] <= n
                col = SYM_COLOR[sym] if complete else AMBER
                d.rounded_rectangle((x, y, x + self.BOX, y + self.BOX), 14, fill=tint(col, 0.85) if complete else WHITE,
                                    outline=col, width=4 if not complete else 3)
                d.text((x + self.BOX / 2, y + self.BOX / 2 + 2), b, font=mono(40, True), fill=NAVY, anchor="mm")
            else:
                d.rounded_rectangle((x, y, x + self.BOX, y + self.BOX), 14, outline=LINE, width=3)
                d.text((x + self.BOX / 2, y + self.BOX / 2 + 2), b, font=mono(40, True), fill=LINE, anchor="mm")
        # brackets and decoded instructions under the completed words
        start = 0
        for w, e in enumerate(self.ends):
            if e <= n:
                xa = self.x0 + start * (self.BOX + self.GAP)
                xb = self.x0 + e * (self.BOX + self.GAP) - self.GAP
                sym = self.book[self.words[w]]
                col = SYM_COLOR[sym]
                d.line((xa + 4, y + self.BOX + 18, xb - 4, y + self.BOX + 18), fill=col, width=5)
                tile = arrow_tile(sym, 70)
                im.alpha_composite(tile, (int((xa + xb) / 2 - 35), y + self.BOX + 40))
            start = e
        if n < len(self.bits) and n > open_from:
            buf = self.bits[open_from:n]
            msg = f"讀咗「{buf}」：仲未係完整嘅碼，繼續讀"
            d.text((W / 2, y + self.BOX + 190), msg, font=font(38, "medium"), fill=AMBER, anchor="mm")
        elif n > 0:
            sym = self.book[self.words[len(done) - 1]] if done else ""
            msg = f"「{self.words[len(done) - 1]}」係完整嘅碼 → {sym}" if done else ""
            d.text((W / 2, y + self.BOX + 190), msg, font=font(38, "medium"), fill=GREEN, anchor="mm")


# -- the space of all code words ---------------------------------------------------------------------

class Claim:
    def __init__(self, bits: str, label: str = "", color=BLUE, at=None, until=None):
        self.bits, self.label, self.color, self.at, self.until = bits, label, color, at, until


class CodeSpaceCard(Anim):
    """Every bit string, one row per length (1 bit at the top). Each cell sits under its prefix,
    so claiming a code word uses up the whole column under it."""

    def __init__(self, heading: str, depth: int = 4, rows_at=None, claims: list[Claim] = (),
                 fracs: tuple | None = None, top: int = 262, row_h: int = 96, gap: int = 10,
                 pill: tuple | None = None):
        super().__init__(heading)
        self.depth, self.top, self.row_h, self.gap = depth, top, row_h, gap
        self.claims = list(claims)
        rows_at = rows_at if isinstance(rows_at, list) else [rows_at] * depth
        for r, at in enumerate(rows_at):
            self.mark(f"row{r}", at)
        for i, c in enumerate(self.claims):
            self.mark(f"c{i}", c.at)
            self.mark(f"u{i}", c.until)
        self.fracs = fracs
        if fracs:
            self.mark("fracs", fracs[1])
        self.x0, self.wd = MARGIN, W - 2 * MARGIN
        self.bottom = top + depth * (row_h + gap)
        if pill:
            txt, at, color = pill
            self.add_center(D.pill(txt, font(44, "bold"), WHITE, color, px=40, py=14), self.bottom + 96, at=at,
                            anim="pop", sound="pop")

    def span(self, bits: str):
        cw = self.wd / 2 ** len(bits)
        x = self.x0 + int(bits, 2) * cw
        return x, x + cw

    def row_y(self, r: int) -> int:
        return self.top + r * (self.row_h + self.gap)

    def _alpha(self, i, t):
        a = self.k(f"c{i}", t, 0.5)
        if self.T.get(f"u{i}") is not None:
            a *= 1 - self.k(f"u{i}", t, 0.5)
        return a

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        for r in range(self.depth):
            a = self.k(f"row{r}", t, 0.5)
            if a <= 0:
                continue
            n = 2 ** (r + 1)
            cw = self.wd / n
            y = self.row_y(r)
            f = mono(max(18, min(34, int(cw / (r + 1) / 0.75))), True)
            show = cw > (r + 1) * f.getlength("0") + 12
            for j in range(n):
                x = self.x0 + j * cw
                fill = tint(BLUE, 0.94 + 0.06 * (1 - a))
                d.rounded_rectangle((x + 3, y, x + cw - 3, y + self.row_h), 10, fill=fill,
                                    outline=tint(LINE, 0.3 * (1 - a)), width=2)
                if show:
                    d.text((x + cw / 2, y + self.row_h / 2), format(j, f"0{r + 1}b"), font=f,
                           fill=tint(MUTED, 1 - a), anchor="mm")
        # claimed code words: their own cell, and the column under it shaded (no longer usable)
        for i, c in enumerate(self.claims):
            a = self._alpha(i, t)
            if a <= 0:
                continue
            xa, xb = self.span(c.bits)
            r = len(c.bits) - 1
            layer = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(layer)
            for rr in range(r + 1, self.depth):
                y = self.row_y(rr)
                ld.rounded_rectangle((xa + 3, y, xb - 3, y + self.row_h), 10, fill=tint(c.color, 0.72) + (150,))
                ld.line((xa + 12, y + self.row_h - 12, xb - 12, y + 12), fill=tint(c.color, 0.45) + (120,), width=3)
            y = self.row_y(r)
            ld.rounded_rectangle((xa + 3, y, xb - 3, y + self.row_h), 12, fill=c.color + (255,))
            lab = f"{c.label}  {c.bits}" if c.label and (xb - xa) > 150 else (c.label or c.bits)
            fz = 40 if (xb - xa) > 200 else 30
            ld.text(((xa + xb) / 2, y + self.row_h / 2), lab, font=font(fz, "bold"), fill=WHITE, anchor="mm")
            im.alpha_composite(fade(layer, a))
        if self.fracs:
            g = self.k("fracs", t)
            if g > 0:
                for bits, txt in self.fracs[0]:
                    xa, xb = self.span(bits)
                    lab = fade(D.text_img(txt, font(44, "bold"), NAVY), g)
                    im.alpha_composite(lab, (int((xa + xb - lab.width) / 2), self.bottom + 4))


# -- the coin-flip tree -------------------------------------------------------------------------

class TreeCard(Anim):
    """The clever code as a tree read left to right: every branch is a fair coin flip."""

    def __init__(self, heading: str, levels_at: list, pill: tuple | None = None):
        super().__init__(heading)
        for i, at in enumerate(levels_at):
            self.mark(f"l{i}", at)
        X = [330, 760, 1190, 1620]
        self.nodes = {"": (X[0], 470), "0": (X[1], 330), "1": (X[1], 620), "10": (X[2], 500), "11": (X[2], 740),
                      "110": (X[3], 640), "111": (X[3], 830)}
        self.leaf = {"0": "↑", "10": "↓", "110": "←", "111": "→"}
        if pill:
            txt, at, color = pill
            self.add(D.pill(txt, font(42, "bold"), WHITE, color, px=36, py=14), 1080, 300, at, anim="pop", sound="pop")

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        for parent in ("", "1", "11"):
            lvl = len(parent)
            g = self.k(f"l{lvl}", t, 0.7)
            if g <= 0:
                continue
            px, py = self.nodes[parent]
            for b in "01":
                cx, cy = self.nodes[parent + b]
                ex, ey = px + (cx - px) * g, py + (cy - py) * g
                d.line((px, py, ex, ey), fill=NAVY, width=6)
                if g > 0.6:
                    mx, my = (px + cx) / 2, (py + cy) / 2
                    lab = f"{b}  50%"
                    d.rounded_rectangle((mx - 78, my - 28, mx + 78, my + 28), 28, fill=WHITE, outline=LINE, width=2)
                    d.text((mx, my), lab, font=font(32, "bold"), fill=BLUE if b == "0" else NAVY, anchor="mm")
        for key, (x, y) in self.nodes.items():
            lvl = len(key)
            g = 1.0 if key == "" else self.k(f"l{lvl - 1}", t, 0.7)
            if g < 0.7:
                continue
            if key in self.leaf:
                sym = self.leaf[key]
                im.alpha_composite(arrow_tile(sym, 96), (x - 48, y - 48))
                p = ROBOT_P[sym]
                d.text((x + 66, y), FRAC[p], font=font(40, "bold"), fill=SYM_COLOR[sym], anchor="lm")
            else:
                d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=NAVY)


# -- information: the curve and the pie ------------------------------------------------------------

class GraphCard(Anim):
    """−log₂ p on axes, with points at p = 1/2, 1/4, 1/8, 1/16 (each with its halved square) and the
    whole curve traced at `curve`."""

    def __init__(self, heading: str, points_at: list, curve_at, top: int = 270):
        super().__init__(heading)
        for i, at in enumerate(points_at):
            self.mark(f"p{i}", at)
        self.mark("curve", curve_at)
        self.ax0, self.ax1, self.ay0, self.ay1 = 250, 1040, 840, 300
        self.ymax = 5.0
        self.add(math_img("-log_2 p", 46, BLUE, "bold"), 600, 250, None)

    def X(self, p):
        return self.ax0 + p * (self.ax1 - self.ax0)

    def Y(self, b):
        return self.ay0 - min(b, self.ymax) / self.ymax * (self.ay0 - self.ay1)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 1.6 if n == "curve" else 0.6) * 60) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        # axes
        d.line((self.ax0, self.ay0, self.ax1 + 20, self.ay0), fill=MUTED, width=3)
        d.line((self.ax0, self.ay0, self.ax0, self.ay1 - 30), fill=MUTED, width=3)
        for b in range(1, 6):
            y = self.Y(b)
            d.line((self.ax0, y, self.ax1, y), fill=LINE, width=2)
            d.text((self.ax0 - 16, y), f"{b}", font=font(28), fill=MUTED, anchor="rm")
        d.text((self.ax0 - 16, self.ay1 - 50), "bits", font=font(28, "bold"), fill=MUTED, anchor="rm")
        for p, s in ((0, "0"), (0.5, "½"), (1, "1")):
            d.text((self.X(p), self.ay0 + 16), s, font=font(32), fill=MUTED, anchor="mt")
        d.text((self.ax1 + 40, self.ay0), "p", font=font(36, "bold"), fill=MUTED, anchor="lm")
        # the curve
        g = self.k("curve", t, 1.6)
        if g > 0:
            p_min = 1 / 2 ** self.ymax
            pts = []
            steps = 160
            for k in range(steps + 1):
                p = 1 - (1 - p_min) * (k / steps)       # traced from p = 1 down towards 0
                if k / steps > g:
                    break
                pts.append((self.X(p), self.Y(-math.log2(p))))
            if len(pts) > 1:
                d.line(pts, fill=BLUE, width=6, joint="curve")
        # points with their bars and halved squares
        for i in range(4):
            a = self.k(f"p{i}", t)
            if a <= 0:
                continue
            n = i + 1
            p = 1 / 2 ** n
            x, y = self.X(p), self.Y(n)
            layer = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(layer)
            ld.rectangle((x - 9, y, x + 9, self.ay0), fill=tint(BLUE, 0.4))
            ld.ellipse((x - 12, y - 12, x + 12, y + 12), fill=BLUE)
            ld.text((x + 18, y - 6), f"{n} bit", font=font(30, "bold"), fill=NAVY, anchor="lb")
            # the halved square on the right
            sx, sy, s = 1180, 280 + i * 150, 120
            cols, rows = 2 ** ((n + 1) // 2), 2 ** (n // 2)
            cw, ch = s / cols, s / rows
            for r in range(rows):
                for c in range(cols):
                    on = r == 0 and c == 0
                    ld.rectangle((sx + c * cw, sy + r * ch, sx + (c + 1) * cw, sy + (r + 1) * ch),
                                 fill=BLUE if on else WHITE, outline=NAVY, width=2)
            frac = {1: "½", 2: "¼", 3: "⅛", 4: "1/16"}[n]
            ld.text((sx + s + 40, sy + s / 2), f"p = {frac}：切 {n} 次 → {n} bit", font=font(38, "bold"),
                    fill=NAVY, anchor="lm")
            im.alpha_composite(fade(layer, a))


class PieBarCard(Anim):
    """A probability as a pie and its information as a bar; p glides between key values."""

    def __init__(self, heading: str, keys: list[tuple], formula_at=None):
        super().__init__(heading)
        self.keys = keys                    # (at, p); the first is the starting value
        for i, (at, _) in enumerate(keys):
            self.mark(f"k{i}", at)
        self.add(boxed(math_img("資訊量 = -log_2 p", 50, NAVY, "bold")), 1060, 262, formula_at, anim="pop", sound="pop")

    def p_at(self, t):
        p = self.keys[0][1]
        for i in range(1, len(self.keys)):
            t0 = self.T[f"k{i}"]
            if t0 is None or t < t0:
                break
            g = ease(clamp((t - t0) / 1.8))
            p = p + (self.keys[i][1] - p) * g
        return p

    def extra_key(self, t):
        return round(self.p_at(t) * 600)

    def draw_extra(self, im, t):
        p = self.p_at(t)
        info = -math.log2(max(p, 1e-6))
        d = ImageDraw.Draw(im)
        cx, cy, r = 520, 560, 200
        im.alpha_composite(pie(p, r, BLUE), (cx - r - 2, cy - r - 2))
        d.text((cx, cy + r + 50), f"機率 p = {p * 100:.0f}%" if p >= 0.1 else f"機率 p = {p * 100:.1f}%",
               font=font(46, "bold"), fill=BLUE, anchor="mm")
        bx, base, scale = 1180, 840, 70
        h = min(info, 7.5) * scale
        d.line((bx - 60, base, bx + 260, base), fill=MUTED, width=3)
        d.rounded_rectangle((bx, base - max(h, 6), bx + 140, base), 16, fill=AMBER)
        d.text((bx + 170, base - h / 2), f"{info:.2f} bits", font=font(48, "bold"), fill=AMBER, anchor="lm")
        d.text((bx + 70, base + 40), "資訊量", font=font(36, "bold"), fill=NAVY, anchor="mm")


class LetterCard(Anim):
    """A word letter by letter: each letter's probability (pie) and information (bar), as a
    language model might give them."""

    def __init__(self, heading: str, word: str, probs: list[float], start, end, total_at=None,
                 note: str = "示意數字"):
        super().__init__(heading)
        self.word, self.probs = word, probs
        self.mark("start", start)
        self.mark("end", end)
        self.mark("total", total_at)
        n = len(word)
        self.bw, self.gap = 112, 16
        self.x0 = (W - (n * (self.bw + self.gap) - self.gap)) // 2
        self.y_base = 640
        if note:
            self.add(D.text_img(note, font(28), MUTED), W - MARGIN - D.width(note, font(28)), 250, None)
        if total_at is not None:
            total = sum(-math.log2(p) for p in probs)
            self.add(D.pill(f"成個字：{total:.1f} bits", font(40, "bold"), WHITE, AMBER, px=36, py=12), MARGIN, 250,
                     at=total_at, anim="pop", sound="pop")

    def setup(self, timing):
        a, b = self.T["start"] or 0.0, self.T["end"]
        if b is None or b <= a:
            b = a + 0.6 * len(self.word)
        self.dt = (b - a) / len(self.word)

    def _n(self, t):
        a = self.T["start"] or 0.0
        if t < a:
            return 0, 0.0
        f = (t - a) / self.dt
        return min(len(self.word), int(f) + 1), clamp(f - int(f))

    def extra_key(self, t):
        n, s = self._n(t)
        return n, round(min(1, s * 2) * 12)

    def draw_extra(self, im, t):
        n, s = self._n(t)
        d = ImageDraw.Draw(im)
        for i, ch in enumerate(self.word):
            x = self.x0 + i * (self.bw + self.gap)
            y = self.y_base
            on = i < n
            d.rounded_rectangle((x, y, x + self.bw, y + self.bw), 18, fill=WHITE if on else None,
                                outline=NAVY if on else LINE, width=4 if on else 3)
            if not on:
                continue
            g = 1.0 if i < n - 1 else ease(min(1, s * 2))
            d.text((x + self.bw / 2, y + self.bw / 2 + 4), ch, font=mono(64, True), fill=NAVY, anchor="mm")
            p = self.probs[i]
            info = -math.log2(p)
            h = min(info, 7) * 52 * g
            col = RED if info > 3 else (AMBER if info > 1 else GREEN)
            d.rounded_rectangle((x + 20, y - 18 - max(h, 4), x + self.bw - 20, y - 18), 10, fill=col)
            if g > 0.9:
                d.text((x + self.bw / 2, y - 30 - h), f"{info:.1f}", font=font(30, "bold"), fill=col, anchor="mb")
            im.alpha_composite(pie(p, 30, GREEN), (int(x + self.bw / 2 - 32), y + self.bw + 18))
            d.text((x + self.bw / 2, y + self.bw + 98), f"{p * 100:.0f}%", font=font(26, "medium"), fill=MUTED, anchor="mt")
        d.text((self.x0 - 30, self.y_base - 60), "資訊量\n(bits)", font=font(26, "bold"), fill=MUTED, anchor="rm", align="right")
        d.text((self.x0 - 30, self.y_base + self.bw + 50), "機率", font=font(26, "bold"), fill=MUTED, anchor="rm")


# -- entropy as an area ---------------------------------------------------------------------------

class EntropyCard(Anim):
    """A distribution as a strip of widths p; above each slot a block of height −log₂ p. The total
    area is the entropy. states: (at, probs, labels or None); probs are padded to one length and
    glide from state to state."""

    def __init__(self, heading: str, states: list[tuple], strip_at=None, blocks_at=None, value_at=None,
                 formula_at=None):
        super().__init__(heading)
        n = max(len(s[1]) for s in states)
        self.states = [(at, list(p) + [0.0] * (n - len(p)), labels) for at, p, labels in states]
        for i, (at, _, _) in enumerate(self.states):
            self.mark(f"s{i}", at)
        self.mark("strip", strip_at)
        self.mark("blocks", blocks_at)
        self.mark("value", value_at)
        self.x0, self.wd, self.y_base, self.scale = 330, 1300, 780, 64
        self.add(math_img("H = Σ p_i × (-log_2 p_i)", 48, NAVY, "bold"), MARGIN, 236, formula_at, anim="fade")

    def probs_at(self, t):
        cur = self.states[0][1]
        idx = 0
        for i in range(1, len(self.states)):
            t0 = self.T[f"s{i}"]
            if t0 is None or t < t0:
                break
            g = ease(clamp((t - t0) / 1.8))
            cur = [a + (b - a) * g for a, b in zip(cur, self.states[i][1])]
            idx = i if g > 0.5 else idx
        return cur, idx

    def extra_key(self, t):
        ps, _ = self.probs_at(t)
        return (tuple(round(p * 300) for p in ps), round(self.k("strip", t) * 20), round(self.k("blocks", t, 1.0) * 30),
                round(self.k("value", t) * 20))

    def draw_extra(self, im, t):
        ps, idx = self.probs_at(t)
        labels = self.states[idx][2]
        d = ImageDraw.Draw(im)
        # y axis
        for b in range(0, 7):
            y = self.y_base - b * self.scale
            d.line((self.x0, y, self.x0 + self.wd, y), fill=LINE, width=2)
            d.text((self.x0 - 16, y), str(b), font=font(28), fill=MUTED, anchor="rm")
        d.text((self.x0 - 16, self.y_base - 6.6 * self.scale), "bits", font=font(28, "bold"), fill=MUTED, anchor="rm")
        gs, gb = self.k("strip", t), self.k("blocks", t, 1.0)
        x = self.x0
        H = 0.0
        layer = Image.new("RGBA", im.size)
        ld = ImageDraw.Draw(layer)
        for i, p in enumerate(ps):
            w = self.wd * p
            if w < 0.5:
                continue
            col = PALETTE[i % 4]
            info = -math.log2(p)
            H += p * info
            if gs > 0:
                ld.rectangle((x, self.y_base + 10, x + w - 2, self.y_base + 64), fill=col + (int(255 * gs),))
                if labels and i < len(labels) and w > 60:
                    ld.text((x + w / 2, self.y_base + 37), labels[i], font=font(36, "bold"), fill=(255, 255, 255, int(255 * gs)),
                            anchor="mm")
            if gb > 0:
                h = min(info, 6.5) * self.scale * gb
                ld.rectangle((x, self.y_base - h, x + w - 2, self.y_base), fill=tint(col, 0.55) + (230,),
                             outline=col + (255,), width=2)
            x += w
        im.alpha_composite(layer)
        gv = self.k("value", t)
        if gv > 0:
            pl = fade(D.pill(f"H = {H:.2f} bits", font(46, "bold"), WHITE, AMBER, px=36, py=12), gv)
            im.alpha_composite(pl, (W - MARGIN - pl.width, 226))


# -- Shannon's guessing game ------------------------------------------------------------------------

class GuessCard(Anim):
    """A sentence letter by letter; under it Shannon's record: a dash where the guess was right,
    the letter where it was wrong."""

    def __init__(self, heading: str, text: str, right: str, start, end, result_at=None):
        super().__init__(heading)
        assert len(text) == len(right)
        self.text, self.right = text, right
        self.mark("start", start)
        self.mark("end", end)
        self.gap = 6
        self.cw = min(58, int((W - 2 * MARGIN + self.gap) / len(text)) - self.gap)
        self.x0 = (W - (len(text) * (self.cw + self.gap) - self.gap)) // 2
        self.add(D.text_img("原文", font(36, "bold"), MUTED), self.x0, 300, None)
        self.add(D.text_img("Shannon 嘅記錄（估中就寫「–」）", font(36, "bold"), MUTED), self.x0, 500, start, anim="fade")
        kept = sum(1 for c, r in zip(text, right) if c != " " and r == "x")
        letters = sum(1 for c in text if c != " ")
        self.add_center(D.pill(f"{letters} 個字母，只需要記低 {kept} 個", font(42, "bold"), WHITE, BLUE, px=40, py=14),
                        720, at=result_at, anim="pop", sound="pop")

    def setup(self, timing):
        a, b = self.T["start"] or 0.0, self.T["end"]
        self.dt = ((b if b and b > a else a + 0.4 * len(self.text)) - a) / len(self.text)

    def _n(self, t):
        a = self.T["start"] or 0.0
        return 0 if t < a else min(len(self.text), int((t - a) / self.dt) + 1)

    def extra_key(self, t):
        return self._n(t)

    def draw_extra(self, im, t):
        n = self._n(t)
        d = ImageDraw.Draw(im)
        for i, ch in enumerate(self.text):
            x = self.x0 + i * (self.cw + self.gap)
            if ch == " ":
                continue
            for y, row in ((360, "orig"), (560, "rec")):
                shown = i < n
                d.rounded_rectangle((x, y, x + self.cw, y + 76), 10, fill=WHITE if shown else None,
                                    outline=NAVY if shown and row == "orig" else LINE, width=3)
                if not shown:
                    continue
                if row == "orig":
                    d.text((x + self.cw / 2, y + 40), ch, font=mono(44, True), fill=NAVY, anchor="mm")
                elif self.right[i] == "x":
                    d.rounded_rectangle((x, y, x + self.cw, y + 76), 10, fill=tint(RED, 0.85), outline=RED, width=3)
                    d.text((x + self.cw / 2, y + 40), ch, font=mono(44, True), fill=RED, anchor="mm")
                else:
                    d.text((x + self.cw / 2, y + 38), "–", font=font(44, "bold"), fill=MUTED, anchor="mm")


# -- plain helpers built from Card --------------------------------------------------------------------

class EquationCard(Card):
    """Lines of maths (math_img markup) that appear at their cues, centred. lines: (text, at) or
    (text, at, {"size":…, "color":…, "box": colour})."""

    def __init__(self, heading: str, lines: list[tuple], top: int = 300, gap: int = 36,
                 pill: tuple | None = None):
        super().__init__(heading)
        y = top
        for ln in lines:
            txt, at = ln[0], ln[1]
            o = ln[2] if len(ln) > 2 else {}
            img = math_img(txt, o.get("size", 60), o.get("color", NAVY), o.get("weight", "medium"))
            if o.get("box"):
                img = boxed(img, o["box"])
            self.add_center(img, y, at=at, anim="pop" if o.get("box") else "up", sound="pop" if o.get("box") else None)
            y += img.height + gap
        if pill:
            txt, at, color = pill
            self.add_center(D.pill(txt, font(44, "bold"), WHITE, color, px=40, py=14), max(y + 10, 760), at=at,
                            anim="pop", sound="pop")


class NoiseCard(Anim):
    """Rows of random bits typing in: what a perfect compressor's output should look like."""

    def __init__(self, heading: str, at, rows: int = 6, cols: int = 40, pill: tuple | None = None, top: int = 300):
        super().__init__(heading)
        self.mark("go", at)
        rng = random.Random(11)
        self.rows = ["".join(rng.choice("01") for _ in range(cols)) for _ in range(rows)]
        self.top = top
        f = mono(40, True)
        self.adv = f.getlength("0") + 8
        self.x0 = (W - self.adv * cols) / 2
        if pill:
            txt, at2, color = pill
            self.add_center(D.pill(txt, font(44, "bold"), WHITE, color, px=40, py=14), top + rows * 62 + 50, at=at2,
                            anim="pop", sound="pop")

    def _n(self, t):
        t0 = self.T["go"]
        if t0 is None:
            return 10 ** 6
        return max(0, int((t - t0) * 90))

    def extra_key(self, t):
        return min(self._n(t), sum(map(len, self.rows)))

    def draw_extra(self, im, t):
        n = self._n(t)
        d = ImageDraw.Draw(im)
        f = mono(40, True)
        k = 0
        for r, row in enumerate(self.rows):
            for c, b in enumerate(row):
                if k >= n:
                    return
                d.text((self.x0 + c * self.adv, self.top + r * 62), b, font=f, fill=BLUE if b == "0" else NAVY)
                k += 1


class TermsCard(Card):
    """One equation built term by term on a row (terms: (text, at, colour)), with optional lines
    under it (lines: (text, at, colour, size))."""

    def __init__(self, heading: str, terms: list[tuple], y: int = 380, size: int = 72, lines: list[tuple] = (),
                 pill: tuple | None = None):
        super().__init__(heading)
        imgs = [math_img(txt, size, col, "bold") for txt, _, col in terms]
        gap = 18
        x = (W - (sum(i.width for i in imgs) + gap * (len(imgs) - 1))) / 2
        for img, (_, at, _) in zip(imgs, terms):
            self.add(img, x, y, at, anim="pop", sound="pop")
            x += img.width + gap
        yy = y + max(i.height for i in imgs) + 60
        for txt, at, col, sz in lines:
            img = math_img(txt, sz, col)
            self.add_center(img, yy, at=at)
            yy += img.height + 24
        if pill:
            txt, at, color = pill
            self.add_center(D.pill(txt, font(44, "bold"), WHITE, color, px=40, py=14), max(yy + 20, 700), at=at,
                            anim="pop", sound="pop")
