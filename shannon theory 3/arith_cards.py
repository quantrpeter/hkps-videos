"""Animated cards for the arithmetic-coding video (資訊理論・第三集): the zooming interval stack,
binary halving of [0, 1), and the search for the shortest k-bit number inside a target range.
All numbers come from arith_model.py."""

from __future__ import annotations

from PIL import Image, ImageDraw

import arith_model as M
from entropy_cards import Anim, clamp, fade, tint
from hkpsvid.style import AMBER, BLUE, GREEN, INK, LINE, MARGIN, MUTED, NAVY, PURPLE, RED, TEAL, W, WHITE, font, mono
from hkpsvid.visuals import ease


def fmt(x: float, n: int = 6) -> str:
    return f"{x:.{n}f}"


class ZoomStackCard(Anim):
    """One row per letter of `text`: row i is the model's distribution for the next letter after
    text[:i], drawn over the current interval stretched to full width; the chosen letter is
    highlighted and the zoom into it is drawn down to the next row. `marker` is an x to point at
    in every row (decoding)."""

    def __init__(self, heading: str, text: str, rows_at: list, row_h: int = 118, top: int = 300,
                 axis: bool = False, marker: float | None = None, marker_at=None, readout_at=False,
                 pick: bool = True, labels: bool = True):
        super().__init__(heading)
        self.text, self.row_h, self.top, self.axis, self.pick, self.labels = text, row_h, top, axis, pick, labels
        self.n = max(1, len(text)) if pick else 1
        self.ivs = M.interval(text)
        for i, at in enumerate(rows_at):
            self.mark(f"r{i}", at)
        self.rows = len(rows_at)
        self.marker = marker
        self.mark("marker", marker_at if marker is not None else False)
        self.mark("readout", readout_at)
        self.x0, self.x1 = 300, W - MARGIN
        self.bar_h = min(56, row_h - 34)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 0.7) * 30) for n in self._marks)

    def X(self, v, lo, hi):
        return self.x0 + (v - lo) / (hi - lo) * (self.x1 - self.x0)

    def draw_extra(self, im, t):
        for i in range(self.rows):
            g = self.k(f"r{i}", t, 0.7)
            if g <= 0:
                continue
            layer = Image.new("RGBA", im.size)
            d = ImageDraw.Draw(layer)
            y = self.top + i * self.row_h
            lo, hi = self.ivs[i] if i < len(self.ivs) else self.ivs[-1]
            dist = M.dist(self.text[:i])
            chosen = self.text[i] if self.pick and i < len(self.text) else None
            x = self.x0
            for k, (c, p) in enumerate(zip(M.ALPHA, dist)):
                w = p * (self.x1 - self.x0)
                on = c == chosen
                col = AMBER if on else (BLUE if k % 2 == 0 else TEAL)
                fill = col if on else tint(col, 0.55)
                d.rectangle((x, y, x + max(w, 1) - 1, y + self.bar_h), fill=fill)
                if self.labels and w > 20:
                    d.text((x + w / 2, y + self.bar_h / 2), c, font=font(min(30, self.bar_h - 10), "bold"),
                           fill=WHITE if on else NAVY, anchor="mm")
                x += w
            # prefix label on the left
            pre = self.text[:i] if self.pick else ""
            d.text((self.x0 - 24, y + self.bar_h / 2), f"「{pre}」後面" if pre else "第一個字母",
                   font=font(26, "bold"), fill=MUTED, anchor="rm")
            # zoom lines into the chosen letter, down to the next row
            if chosen and i + 1 < self.rows:
                g2 = self.k(f"r{i + 1}", t, 0.7)
                if g2 > 0:
                    k = M.ALPHA.index(chosen)
                    ca = self.x0 + sum(dist[:k]) * (self.x1 - self.x0)
                    cb = ca + dist[k] * (self.x1 - self.x0)
                    y2 = y + self.row_h
                    d.polygon([(ca, y + self.bar_h), (cb, y + self.bar_h), (self.x1, y2), (self.x0, y2)],
                              fill=tint(AMBER, 0.85) + (int(150 * g2),))
            if self.axis and i == 0:
                for v in (0, 0.25, 0.5, 0.75, 1):
                    xx = self.X(v, 0, 1)
                    d.line((xx, y - 14, xx, y - 2), fill=MUTED, width=3)
                    d.text((xx, y - 18), f"{v:g}", font=font(28), fill=MUTED, anchor="mb")
            im.alpha_composite(fade(layer, g))
        if self.marker is not None:
            gm = self.k("marker", t)
            if gm > 0:
                d = ImageDraw.Draw(im)
                for i in range(self.rows):
                    if self.k(f"r{i}", t, 0.7) <= 0:
                        continue
                    lo, hi = M.interval(M.decode(self.marker, i))[-1]
                    xx = self.X(self.marker, lo, hi)
                    y = self.top + i * self.row_h
                    d.line((xx, y - 10, xx, y + self.bar_h + 10), fill=RED, width=5)
                    d.polygon([(xx - 10, y - 22), (xx + 10, y - 22), (xx, y - 6)], fill=RED)
                d.text((self.x1, self.top - 40), f"x = {fmt(self.marker, 7)}", font=font(34, "bold"), fill=RED, anchor="rb")
        gr = self.k("readout", t)
        if gr > 0 and self.text:
            lo, hi = self.ivs[-1]
            txt = f"「{self.text}」→ [{fmt(lo, 7)}, {fmt(hi, 7)})　闊度 = P(「{self.text}」) ≈ {hi - lo:.2g}"
            lab = fade(_pill(txt, AMBER), gr)
            im.alpha_composite(lab, ((W - lab.width) // 2, self.top + self.rows * self.row_h + 6))


def _pill(txt, color, size=34):
    f = font(size, "bold")
    w = int(f.getlength(txt)) + 60
    h = size + 30
    im = Image.new("RGBA", (w, h))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=color)
    ImageDraw.Draw(im).text((w / 2, h / 2), txt, font=f, fill=WHITE, anchor="mm")
    return im


class BinaryCard(Anim):
    """[0, 1) halved bit by bit: each new bit keeps the left (0) or right (1) half."""

    def __init__(self, heading: str, bits: str, bits_at: list, stop_at=False):
        super().__init__(heading)
        self.bits = bits
        for i, at in enumerate(bits_at):
            self.mark(f"b{i}", at)
        self.mark("stop", stop_at)
        self.x0, self.x1, self.y = 220, W - 220, 560

    def X(self, v):
        return self.x0 + v * (self.x1 - self.x0)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 0.6) * 30) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        lo, hi = 0.0, 1.0
        shown = ""
        prev = (lo, hi)
        g_last = 1.0
        for i, b in enumerate(self.bits):
            g = self.k(f"b{i}", t, 0.6)
            if g <= 0:
                break
            prev = (lo, hi)
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if b == "0" else (mid, hi)
            shown += b
            g_last = g
        # the ticks of every halving so far
        n = len(shown)
        for k in range(0, 2 ** min(n, 6) + 1):
            v = k / 2 ** min(n, 6)
            d.line((self.X(v), self.y - 20, self.X(v), self.y + 20), fill=LINE, width=2)
        d.line((self.x0, self.y, self.x1, self.y), fill=MUTED, width=4)
        for v, s in ((0, "0"), (0.5, "½"), (1, "1")):
            d.text((self.X(v), self.y + 34), s, font=font(32), fill=MUTED, anchor="mt")
        if n:
            a = prev[0] + (lo - prev[0]) * g_last
            b2 = prev[1] + (hi - prev[1]) * g_last
            d.rounded_rectangle((self.X(a), self.y - 34, self.X(b2), self.y + 34), 10, fill=tint(AMBER, 0.4),
                                outline=AMBER, width=4)
            d.text((W / 2, 330), "." + shown, font=mono(96, True), fill=NAVY, anchor="mm")
            d.text((W / 2, 430), f"範圍：[{lo:g}, {hi:g})　闊度 = 1/{2 ** n}", font=font(40, "bold"), fill=AMBER, anchor="mm")
        gs = self.k("stop", t)
        if gs > 0 and n:
            x = self.X(lo)
            d.ellipse((x - 14, self.y - 14, x + 14, self.y + 14), fill=RED)
            d.text((x, self.y + 90), f"代表嘅數 = 最左邊 = {lo:g}", font=font(38, "bold"), fill=RED, anchor="mt")


class TargetCard(Anim):
    """A window around a target range [lo, hi); one row per k shows the k-bit numbers (spaced 2⁻ᵏ)
    in the window, green when inside the target. The first k with a hit is the code length."""

    def __init__(self, heading: str, lo: float, hi: float, ks: list[int], rows_at: list, top: int = 330):
        super().__init__(heading)
        self.lo, self.hi, self.ks, self.top = lo, hi, ks, top
        for i, at in enumerate(rows_at):
            self.mark(f"r{i}", at)
        c = (lo + hi) / 2
        span = 2 ** -(max(ks) - 3)
        self.a, self.b = c - span / 2, c + span / 2
        self.x0, self.x1 = 360, W - MARGIN

    def X(self, v):
        return self.x0 + (v - self.a) / (self.b - self.a) * (self.x1 - self.x0)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 0.6) * 30) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        for i, k in enumerate(self.ks):
            g = self.k(f"r{i}", t, 0.6)
            if g <= 0:
                continue
            layer = Image.new("RGBA", im.size)
            ld = ImageDraw.Draw(layer)
            y = self.top + i * 170
            ld.rounded_rectangle((self.X(self.lo), y - 30, self.X(self.hi), y + 30), 8, fill=tint(AMBER, 0.6),
                                 outline=AMBER, width=3)
            ld.line((self.x0, y, self.x1, y), fill=MUTED, width=3)
            ld.text((self.x0 - 30, y), f"{k} 個 bit", font=font(40, "bold"), fill=NAVY, anchor="rm")
            step = 2 ** -k
            m0 = int(self.a / step) + 1
            hit = None
            m = m0
            while m * step < self.b:
                v = m * step
                inside = self.lo <= v < self.hi
                col = GREEN if inside else MUTED
                ld.line((self.X(v), y - 22, self.X(v), y + 22), fill=col, width=6 if inside else 4)
                if inside and hit is None:
                    hit = m
                m += 1
            if hit is not None:
                bits = format(hit, f"0{k}b")
                ld.text((self.X(hit * step), y + 40), "." + bits, font=mono(30, True), fill=GREEN, anchor="mt")
                ld.text((self.x1, y - 40), "瞄中！", font=font(36, "bold"), fill=GREEN, anchor="rb")
            else:
                ld.text((self.x1, y - 40), "冇數落喺入面", font=font(36, "bold"), fill=RED, anchor="rb")
            im.alpha_composite(fade(layer, g))
        d.text((self.X((self.lo + self.hi) / 2), self.top - 70), "目標範圍", font=font(32, "bold"), fill=AMBER, anchor="mb")
