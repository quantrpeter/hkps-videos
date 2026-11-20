"""Animated cards for the cross-entropy video (資訊理論・第二集), on top of entropy_cards.py:
the gzip trick, the cross-entropy area, the two-outcome curve, a language model's prediction,
gradient descent on a loss hill, per-token loss, loss-function shapes, the "My name is ___"
example and distillation targets.
"""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from entropy_cards import PALETTE, Anim, clamp, fade, math_img, pie, tint
from hkpsvid import draw as D
from hkpsvid.style import AMBER, BLUE, GREEN, INK, LINE, MARGIN, MUTED, NAVY, PURPLE, RED, TEAL, W, WHITE, font, mono
from hkpsvid.visuals import ease


def lg(x: float) -> float:
    return -math.log2(max(x, 1e-9))


def dashed_rect(d: ImageDraw.ImageDraw, box, color, width: int = 3, dash: int = 14) -> None:
    x0, y0, x1, y1 = box
    for (a, b, c, e) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x0, y1, x1, y1), (x0, y0, x0, y1)):
        L = math.hypot(c - a, e - b)
        n = max(1, int(L // dash))
        for k in range(0, n, 2):
            t0, t1 = k / n, min(1, (k + 1) / n)
            d.line((a + (c - a) * t0, b + (e - b) * t0, a + (c - a) * t1, b + (e - b) * t1), fill=color, width=width)


def glide(keys, T, t, dur: float = 1.8):
    """keys: [(name_in_T, value)] where value is a float or a list; eases from key to key."""
    cur = keys[0][1]
    for name, val in keys[1:]:
        t0 = T.get(name)
        if t0 is None or t < t0:
            break
        g = ease(clamp((t - t0) / dur))
        cur = [a + (b - a) * g for a, b in zip(cur, val)] if isinstance(cur, list) else cur + (val - cur) * g
    return cur


# -- the gzip trick ---------------------------------------------------------------------------------

class ZipCard(Anim):
    """gzip(A + a bit of B) against gzip(A): the extra length is what B costs under A's patterns.
    Then two pairs: a close language adds little, a distant one adds a lot."""

    def __init__(self, heading: str, docs_at=None, both_at=None, diff_at=None, pairs_at=False):
        super().__init__(heading)
        for n, at in (("docs", docs_at), ("both", both_at), ("diff", diff_at), ("pairs", pairs_at)):
            self.mark(n, at)

    def _doc(self, d, x, y, color, label, lines=7):
        d.rounded_rectangle((x, y, x + 180, y + 230), 18, fill=WHITE, outline=color, width=4)
        for k in range(lines):
            w = 120 if k % 3 == 2 else 140
            d.rounded_rectangle((x + 20, y + 22 + k * 28, x + 20 + w, y + 34 + k * 28), 6, fill=tint(color, 0.5))
        d.text((x + 90, y + 260), label, font=font(32, "bold"), fill=color, anchor="mm")

    def draw_extra(self, im, t):
        layer = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(layer)
        a = self.k("docs", t)
        if a > 0:
            self._doc(d, 140, 290, BLUE, "文件 A")
            d.rounded_rectangle((360, 290, 450, 380), 14, fill=WHITE, outline=GREEN, width=4)
            for k in range(2):
                d.rounded_rectangle((376, 312 + k * 28, 434, 324 + k * 28), 6, fill=tint(GREEN, 0.5))
            d.text((405, 410), "B 一小段", font=font(30, "bold"), fill=GREEN, anchor="mm")
            im.alpha_composite(fade(layer, a))
            layer = Image.new("RGBA", im.size)
            d = ImageDraw.Draw(layer)
        x0, unit = 640, 1.0
        rows = [("gzip(A + B 一小段)", 760, 140, "both"), ("gzip(A)", 760, 0, "both")]
        g = self.k("both", t, 0.9)
        if g > 0:
            for r, (lab, la, lb, _) in enumerate(rows):
                y = 300 + r * 130
                d.text((x0, y - 6), lab, font=font(32, "bold"), fill=NAVY, anchor="ls")
                d.rounded_rectangle((x0, y + 10, x0 + la * g, y + 80), 12, fill=BLUE)
                if lb:
                    d.rounded_rectangle((x0 + la * g - 12, y + 10, x0 + (la + lb) * g, y + 80), 12, fill=GREEN)
                    d.rectangle((x0 + la * g - 12, y + 10, x0 + la * g, y + 80), fill=BLUE)
            im.alpha_composite(layer)
            layer = Image.new("RGBA", im.size)
            d = ImageDraw.Draw(layer)
        g = self.k("diff", t)
        if g > 0:
            xa, xb = x0 + 760, x0 + 900
            d.line((xa, 430, xa, 520), fill=RED, width=3)
            d.line((xb, 300, xb, 520), fill=RED, width=3)
            d.line((xa, 500, xb, 500), fill=RED, width=5)
            d.text(((xa + xb) / 2, 540), "多出嚟", font=font(32, "bold"), fill=RED, anchor="mt")
            im.alpha_composite(fade(layer, g))
            layer = Image.new("RGBA", im.size)
            d = ImageDraw.Draw(layer)
        g = self.k("pairs", t, 0.9)
        if g > 0:
            for r, (lab, extra, col) in enumerate((("法文 + 意大利文", 60, GREEN), ("法文 + 芬蘭文", 230, RED))):
                y = 640 + r * 110
                d.text((140, y + 40), lab, font=font(36, "bold"), fill=NAVY, anchor="lm")
                d.rounded_rectangle((640, y + 8, 640 + 760, y + 72), 12, fill=tint(BLUE, 0.35))
                d.rounded_rectangle((640 + 748, y + 8, 640 + 760 + extra * g, y + 72), 12, fill=col)
                d.text((640 + 790 + extra, y + 40), "多出少少" if r == 0 else "多出好多", font=font(32, "bold"), fill=col,
                       anchor="lm")
            im.alpha_composite(fade(layer, min(1, g * 1.5)))


# -- cross-entropy as an area ---------------------------------------------------------------------------

class CrossCard(Anim):
    """Widths are the real probabilities p, heights are −log₂ q (the code lengths made for q). The
    area is the cross-entropy. `ref` draws dashed −log₂ p outlines (the right code), so the gap is
    the waste (KL). states: (at, p, q). value: "cross", "kl" or "both"."""

    def __init__(self, heading: str, states: list[tuple], labels: list[str] | None = None, strip_at=None,
                 blocks_at=None, value_at=False, ref_at=False, formula: str | None = "H(p, q) = Σ p_i × (-log_2 q_i)",
                 formula_at=None, value: str = "cross", digits: int = 2, show_nums: bool = True):
        super().__init__(heading)
        self.states = states
        for i, (at, _, _) in enumerate(states):
            self.mark(f"s{i}", at)
        for n, at in (("strip", strip_at), ("blocks", blocks_at), ("value", value_at), ("ref", ref_at)):
            self.mark(n, at)
        self.labels, self.value, self.digits, self.show_nums = labels, value, digits, show_nums
        self.x0, self.wd, self.yb, self.scale = 330, 1300, 760, 64
        if formula:
            self.add(math_img(formula, 46, NAVY, "bold"), MARGIN, 236, formula_at, anim="fade")

    def pq(self, t):
        p = glide([(None, list(self.states[0][1]))] + [(f"s{i}", list(s[1])) for i, s in enumerate(self.states)][1:],
                  self.T, t)
        q = glide([(None, list(self.states[0][2]))] + [(f"s{i}", list(s[2])) for i, s in enumerate(self.states)][1:],
                  self.T, t)
        return p, q

    def extra_key(self, t):
        p, q = self.pq(t)
        return (tuple(round(v * 400) for v in p + q),) + tuple(round(self.k(n, t) * 20) for n in ("strip", "blocks", "value", "ref"))

    def draw_extra(self, im, t):
        p, q = self.pq(t)
        d = ImageDraw.Draw(im)
        for b in range(0, 7):
            y = self.yb - b * self.scale
            d.line((self.x0, y, self.x0 + self.wd, y), fill=LINE, width=2)
            d.text((self.x0 - 16, y), str(b), font=font(28), fill=MUTED, anchor="rm")
        d.text((self.x0 - 16, self.yb - 6.7 * self.scale), "bits", font=font(28, "bold"), fill=MUTED, anchor="rm")
        gs, gb, gr = self.k("strip", t), self.k("blocks", t, 1.0), self.k("ref", t)
        layer = Image.new("RGBA", im.size)
        ld = ImageDraw.Draw(layer)
        x = self.x0
        for i, (pi, qi) in enumerate(zip(p, q)):
            w = self.wd * pi
            if w < 0.5:
                continue
            col = PALETTE[i % 4]
            if gs > 0:
                ld.rectangle((x, self.yb + 10, x + w - 2, self.yb + 64), fill=col + (int(255 * gs),))
                lab = self.labels[i] if self.labels and i < len(self.labels) else ""
                if w > 70:
                    ld.text((x + w / 2, self.yb + 37), lab, font=font(34, "bold"), fill=(255, 255, 255, int(255 * gs)),
                            anchor="mm")
                if self.show_nums and w > 110:
                    ld.text((x + w / 2, self.yb + 92), f"p = {pi:.0%}" if pi >= 0.1 else f"p = {pi:.1%}",
                            font=font(28, "medium"), fill=NAVY + (int(255 * gs),), anchor="mm")
            if gb > 0:
                h = min(lg(qi), 6.5) * self.scale * gb
                ld.rectangle((x, self.yb - h, x + w - 2, self.yb), fill=tint(col, 0.55) + (230,), outline=col + (255,),
                             width=2)
                if self.show_nums and w > 90 and gb > 0.95:
                    ld.text((x + w / 2, self.yb - h - 10), f"{lg(qi):.2f}".rstrip("0").rstrip("."), font=font(28, "bold"),
                            fill=col + (255,), anchor="mb")
            if gr > 0:
                h = min(lg(pi), 6.5) * self.scale
                dashed_rect(ld, (x + 2, self.yb - h, x + w - 4, self.yb), RED + (int(255 * gr),), width=4)
            x += w
        im.alpha_composite(layer)
        gv = self.k("value", t)
        if gv > 0:
            cross = sum(pi * lg(qi) for pi, qi in zip(p, q) if pi > 1e-6)
            ent = sum(pi * lg(pi) for pi in p if pi > 1e-6)
            f = f".{self.digits}f"
            txt = {"cross": f"H(p, q) = {cross:{f}} bits", "kl": f"KL = {cross - ent:{f}} bits",
                   "both": f"H(p, q) = {cross:{f}}　·　H(p) = {ent:{f}}"}[self.value]
            pl = fade(D.pill(txt, font(42, "bold"), WHITE, AMBER, px=32, py=12), gv)
            im.alpha_composite(pl, (W - MARGIN - pl.width, 226))


# -- the two-outcome curve ------------------------------------------------------------------------------

class CurveCard(Anim):
    """Cross-entropy of (q, 1−q) against (p, 1−p) as a function of q, for p gliding between key
    values; the minimum sits at q = p, and `trace` draws the path of the minimum: H(p)."""

    def __init__(self, heading: str, p_keys: list[tuple], curve_at=None, min_at=False, eq_at=False, trace_at=False):
        super().__init__(heading)
        self.p_keys = p_keys
        for i, (at, _) in enumerate(p_keys):
            self.mark(f"p{i}", at)
        for n, at in (("curve", curve_at), ("min", min_at), ("eq", eq_at), ("trace", trace_at)):
            self.mark(n, at)
        self.ax0, self.ax1, self.ay0, self.ay1, self.ymax = 250, 1080, 830, 300, 4.0
        self.add(math_img("H(p, q) = -p log_2 q - (1-p) log_2 (1-q)", 34, BLUE, "bold"), 1200, 700, None)

    def X(self, v):
        return self.ax0 + v * (self.ax1 - self.ax0)

    def Y(self, b):
        return self.ay0 - min(b, self.ymax + 0.3) / self.ymax * (self.ay0 - self.ay1)

    def p_at(self, t):
        return glide([(None, self.p_keys[0][1])] + [(f"p{i}", v) for i, (_, v) in enumerate(self.p_keys)][1:], self.T, t, 2.2)

    def extra_key(self, t):
        return round(self.p_at(t) * 500), tuple(round(self.k(n, t, 1.4) * 30) for n in ("curve", "min", "eq", "trace"))

    @staticmethod
    def ce(p, q):
        return p * lg(q) + (1 - p) * lg(1 - q)

    def draw_extra(self, im, t):
        p = self.p_at(t)
        d = ImageDraw.Draw(im)
        d.line((self.ax0, self.ay0, self.ax1 + 20, self.ay0), fill=MUTED, width=3)
        d.line((self.ax0, self.ay0, self.ax0, self.ay1 - 20), fill=MUTED, width=3)
        for b in range(1, 5):
            d.line((self.ax0, self.Y(b), self.ax1, self.Y(b)), fill=LINE, width=2)
            d.text((self.ax0 - 14, self.Y(b)), str(b), font=font(28), fill=MUTED, anchor="rm")
        d.text((self.ax0 - 14, self.ay1 - 40), "bits", font=font(28, "bold"), fill=MUTED, anchor="rm")
        for v in (0, 0.5, 1):
            d.text((self.X(v), self.ay0 + 14), f"{v:g}", font=font(30), fill=MUTED, anchor="mt")
        d.text((self.ax1 + 40, self.ay0), "q", font=font(36, "bold"), fill=MUTED, anchor="lm")
        # p marker on the axis
        px = self.X(p)
        d.polygon([(px, self.ay0 + 52), (px - 14, self.ay0 + 76), (px + 14, self.ay0 + 76)], fill=GREEN)
        d.text((px, self.ay0 + 80), "p", font=font(30, "bold"), fill=GREEN, anchor="mt")
        # the green trace of the minimum: H(p) over the range p has visited since `trace`
        gtr = self.k("trace", t, 0.6)
        t0 = self.T.get("trace")
        if gtr > 0 and t0 is not None:
            vis = [self.p_at(t0 + (t - t0) * k / 80) for k in range(81)]
            lo, hi = min(vis), max(vis)
            pts = [(self.X(v), self.Y(self.ce(v, v))) for v in [lo + (hi - lo) * k / 120 for k in range(121)]]
            if hi - lo > 0.002:
                d.line(pts, fill=GREEN, width=7, joint="curve")
        g = self.k("curve", t, 1.4)
        if g > 0:
            qs = [0.004 + 0.992 * k / 240 for k in range(241)]
            pts = [(self.X(qv), self.Y(self.ce(p, qv))) for qv in qs if (qv - 0.004) / 0.992 <= g]
            if len(pts) > 1:
                d.line(pts, fill=BLUE, width=6, joint="curve")
        gm = self.k("min", t)
        if gm > 0:
            mx, my = self.X(p), self.Y(self.ce(p, p))
            r = 14 * gm
            d.ellipse((mx - r, my - r, mx + r, my + r), fill=GREEN)
            d.text((mx, my + 26), "最低點", font=font(30, "bold"), fill=GREEN, anchor="mt")
        ge = self.k("eq", t)
        if ge > 0:
            for yy in range(int(self.ay1), int(self.ay0), 22):
                d.line((px, yy, px, yy + 11), fill=GREEN, width=3)
        # the readout on the right
        rx = 1220
        d.text((rx, 330), f"p = {p:.2f}", font=font(48, "bold"), fill=GREEN, anchor="lm")
        if gm > 0:
            d.text((rx, 420), f"最低點：q = {p:.2f}", font=font(40, "bold"), fill=NAVY, anchor="lm")
            d.text((rx, 490), f"最低值 = {self.ce(p, p):.2f} bits", font=font(40, "bold"), fill=NAVY, anchor="lm")
        if gtr > 0:
            d.text((rx, 580), "綠色曲線 = H(p)", font=font(40, "bold"), fill=GREEN, anchor="lm")


# -- language models --------------------------------------------------------------------------------------

class PredictCard(Anim):
    """Text in, a black box with many parameters, a distribution over the next token out."""

    def __init__(self, heading: str, text: str, tokens: list[tuple[str, float]], in_at=None, model_at=None,
                 out_at=None):
        super().__init__(heading)
        self.tokens = tokens
        for n, at in (("in", in_at), ("model", model_at), ("out", out_at)):
            self.mark(n, at)
        self.add(D.pill(text, font(46, "bold"), NAVY, WHITE, px=30, py=16, outline=LINE), MARGIN, 470, in_at, anim="pop",
                 sound="pop")
        box = D.shadow_box(330, 250, 30, NAVY, blur=16)
        p = box.info["pad"]
        bd = ImageDraw.Draw(box)
        bd.text((p + 165, p + 92), "語言模型", font=font(50, "bold"), fill=WHITE, anchor="mm")
        bd.text((p + 165, p + 160), "幾十億個參數", font=font(30, "medium"), fill=tint(BLUE, 0.4), anchor="mm")
        for k in range(14):
            bd.ellipse((p + 40 + k * 18, p + 200, p + 50 + k * 18, p + 210), fill=tint(BLUE, 0.2 + 0.05 * (k % 4)))
        box.info["pad"] = p
        self.add(box, 640, 380, model_at, anim="pop", sound="pop")
        a, ax, ay = D.arrow(560, 505, 625, 505, color=MUTED)
        self.add(a, ax, ay, model_at, anim="fade")
        a, ax, ay = D.arrow(990, 505, 1070, 505, color=MUTED)
        self.add(a, ax, ay, out_at, anim="fade")
        self.add(D.text_img("下一個 token 嘅機率", font(34, "bold"), MUTED), 1100, 270, out_at, anim="fade")

    def extra_key(self, t):
        return round(self.k("out", t, 1.2) * 40)

    def draw_extra(self, im, t):
        g = self.k("out", t, 1.2)
        if g <= 0:
            return
        d = ImageDraw.Draw(im)
        for i, (tok, pr) in enumerate(self.tokens):
            y = 340 + i * 82
            gi = clamp(g * 1.4 - i * 0.12)
            d.text((1100, y + 28), tok, font=font(40, "bold"), fill=NAVY, anchor="lm")
            L = 560 * pr * gi
            d.rounded_rectangle((1240, y + 6, 1240 + max(L, 8), y + 52), 10, fill=BLUE if i == 0 else tint(BLUE, 0.45))
            if gi > 0.9:
                d.text((1240 + L + 14, y + 28), f"{pr:.0%}", font=font(32, "bold"), fill=BLUE, anchor="lm")


class HillCard(Anim):
    """A one-parameter loss curve and a ball taking gradient-descent steps down it."""

    def __init__(self, heading: str, go, steps: int = 9, dt: float = 0.7, pill: tuple | None = None):
        super().__init__(heading)
        self.mark("go", go)
        self.steps, self.dt = steps, dt
        self.f = lambda w: 0.35 + 3.2 * (w - 0.68) ** 2 + 0.18 * math.sin(9 * w) * (1 - w)
        self.df = lambda w: (self.f(w + 1e-4) - self.f(w - 1e-4)) / 2e-4
        ws = [0.06]
        for _ in range(steps):
            ws.append(ws[-1] - 0.09 * self.df(ws[-1]))
        self.ws = ws
        self.ax0, self.ax1, self.ay0, self.ay1 = 220, 1300, 820, 300
        if pill:
            txt, at, color = pill
            self.add(D.pill(txt, font(42, "bold"), WHITE, color, px=36, py=14), 1360, 420, at, anim="pop", sound="pop")
        self.add(D.text_img("Gradient descent\n+ backpropagation", font(36, "bold"), MUTED, line_h=1.35), 1360, 280, go,
                 anim="fade")

    def X(self, w):
        return self.ax0 + w * (self.ax1 - self.ax0)

    def Y(self, v):
        return self.ay0 - v / 2.0 * (self.ay0 - self.ay1)

    def _pos(self, t):
        t0 = self.T["go"]
        if t0 is None or t < t0:
            return self.ws[0], 0
        f = (t - t0) / self.dt
        i = min(int(f), self.steps - 1)
        s = ease(clamp(f - int(f))) if f < self.steps else 1.0
        return self.ws[i] + (self.ws[i + 1] - self.ws[i]) * s, i

    def extra_key(self, t):
        w, _ = self._pos(t)
        return round(w * 600)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        d.line((self.ax0, self.ay0, self.ax1, self.ay0), fill=MUTED, width=3)
        d.line((self.ax0, self.ay0, self.ax0, self.ay1 - 20), fill=MUTED, width=3)
        d.text((self.ax0 - 14, self.ay1 - 10), "loss", font=font(32, "bold"), fill=RED, anchor="rm")
        d.text((self.ax1, self.ay0 + 18), "參數", font=font(32, "bold"), fill=MUTED, anchor="rt")
        pts = [(self.X(k / 200), self.Y(self.f(k / 200))) for k in range(201)]
        d.line(pts, fill=RED, width=6, joint="curve")
        w, i = self._pos(t)
        for k in range(0, i + 1):
            x, y = self.X(self.ws[k]), self.Y(self.f(self.ws[k]))
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=tint(NAVY, 0.5))
        x, y = self.X(w), self.Y(self.f(w))
        d.ellipse((x - 20, y - 40, x + 20, y), fill=NAVY)
        d.text((1360, 560), f"loss = {self.f(w):.2f}", font=font(44, "bold"), fill=RED, anchor="lm")


class TokenCard(Anim):
    """Training text token by token: under each, the probability the model gave the true token
    (pie); above, its −log₂ (the surprise). The average is the loss."""

    def __init__(self, heading: str, tokens: list[str], probs: list[float], start, end, avg_at=False, note: str = "示意數字"):
        super().__init__(heading)
        self.tokens, self.probs = tokens, probs
        for n, at in (("start", start), ("end", end), ("avg", avg_at)):
            self.mark(n, at)
        f = mono(46, True)
        self.ws = [int(f.getlength(tk)) + 50 for tk in tokens]
        gap = 18
        self.xs = []
        x = (W - (sum(self.ws) + gap * (len(tokens) - 1))) / 2
        for w in self.ws:
            self.xs.append(x)
            x += w + gap
        self.yb = 640
        if note:
            self.add(D.text_img(note, font(28), MUTED), W - MARGIN - D.width(note, font(28)), 250, None)
        avg = sum(lg(p) for p in probs) / len(probs)
        self.add(D.pill(f"平均 loss ≈ {avg:.2f} bits / token", font(40, "bold"), WHITE, RED, px=36, py=12), MARGIN, 250,
                 avg_at, anim="pop", sound="pop")

    def setup(self, timing):
        a, b = self.T["start"] or 0.0, self.T["end"]
        self.dt = ((b if b and b > a else a + 0.7 * len(self.tokens)) - a) / len(self.tokens)

    def _n(self, t):
        a = self.T["start"] or 0.0
        if t < a:
            return 0, 0.0
        f = (t - a) / self.dt
        return min(len(self.tokens), int(f) + 1), clamp(f - int(f))

    def extra_key(self, t):
        n, s = self._n(t)
        return n, round(min(1, s * 2) * 12)

    def draw_extra(self, im, t):
        n, s = self._n(t)
        d = ImageDraw.Draw(im)
        for i, tk in enumerate(self.tokens):
            x, w, y = self.xs[i], self.ws[i], self.yb
            on = i < n
            d.rounded_rectangle((x, y, x + w, y + 96), 18, fill=WHITE if on else None, outline=NAVY if on else LINE,
                                width=4 if on else 3)
            if not on:
                continue
            d.text((x + w / 2, y + 50), tk, font=mono(46, True), fill=NAVY, anchor="mm")
            g = 1.0 if i < n - 1 else ease(min(1, s * 2))
            info = lg(self.probs[i])
            h = min(info, 6.5) * 50 * g
            col = RED if info > 3 else (AMBER if info > 1 else GREEN)
            bw = min(70, w - 30)
            d.rounded_rectangle((x + (w - bw) / 2, y - 18 - max(h, 4), x + (w + bw) / 2, y - 18), 10, fill=col)
            if g > 0.9:
                d.text((x + w / 2, y - 30 - h), f"{info:.1f}", font=font(30, "bold"), fill=col, anchor="mb")
            im.alpha_composite(pie(self.probs[i], 30, GREEN), (int(x + w / 2 - 32), y + 116))
            d.text((x + w / 2, y + 196), f"{self.probs[i]:.0%}", font=font(26, "medium"), fill=MUTED, anchor="mt")
        d.text((self.xs[0] - 24, self.yb - 60), "−log₂ q\n(bits)", font=font(26, "bold"), fill=MUTED, anchor="rm", align="right")
        d.text((self.xs[0] - 24, self.yb + 148), "模型估\n正確答案", font=font(26, "bold"), fill=MUTED, anchor="rm", align="right")


class FuncGraphCard(Anim):
    """Decreasing functions of q on [0, 1], each traced at its cue; dots with labels on curves."""

    def __init__(self, heading: str, funcs: list[tuple], points: list[tuple] = (), ymax: float = 7.0,
                 pill: tuple | None = None, note: tuple | None = None):
        super().__init__(heading)
        self.funcs, self.points, self.ymax = funcs, points, ymax
        for i, fn in enumerate(funcs):
            self.mark(f"f{i}", fn[3])
        for i, pt in enumerate(points):
            self.mark(f"pt{i}", pt[3])
        self.ax0, self.ax1, self.ay0, self.ay1 = 250, 1150, 830, 300
        if pill:
            txt, at, color = pill
            self.add(D.pill(txt, font(44, "bold"), WHITE, color, px=36, py=14), 1260, 300, at, anim="pop", sound="pop")
        if note:
            txt, at = note
            self.add(math_img(txt, 38, MUTED), 1260, 700, at, anim="fade")

    def X(self, v):
        return self.ax0 + v * (self.ax1 - self.ax0)

    def Y(self, v):
        return self.ay0 - min(v, self.ymax + 0.2) / self.ymax * (self.ay0 - self.ay1)

    def extra_key(self, t):
        return tuple(round(self.k(n, t, 1.2) * 40) for n in self._marks)

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        d.line((self.ax0, self.ay0, self.ax1 + 20, self.ay0), fill=MUTED, width=3)
        d.line((self.ax0, self.ay0, self.ax0, self.ay1 - 20), fill=MUTED, width=3)
        for v in (0, 0.5, 1):
            d.text((self.X(v), self.ay0 + 14), f"{v:g}", font=font(30), fill=MUTED, anchor="mt")
        d.text((self.ax1 + 40, self.ay0), "q", font=font(36, "bold"), fill=MUTED, anchor="lm")
        d.text((self.ax0 - 14, self.ay1 - 10), "懲罰", font=font(30, "bold"), fill=MUTED, anchor="rm")
        for i, (fn, col, label, _) in enumerate(self.funcs):
            g = self.k(f"f{i}", t, 1.2)
            if g <= 0:
                continue
            qs = [1 - 0.995 * k / 300 for k in range(301)]
            pts = [(self.X(q), self.Y(fn(q))) for k, q in enumerate(qs) if k / 300 <= g and fn(q) <= self.ymax + 0.2]
            if len(pts) > 1:
                d.line(pts, fill=col, width=6, joint="curve")
            if g > 0.95:
                d.text((1260, 470 + i * 60), label, font=font(38, "bold"), fill=col, anchor="lm")
        for i, (x, fi, label, _) in enumerate(self.points):
            g = self.k(f"pt{i}", t)
            if g <= 0:
                continue
            fn, col = self.funcs[fi][0], self.funcs[fi][1]
            px, py = self.X(x), self.Y(fn(x))
            d.ellipse((px - 12, py - 12, px + 12, py + 12), fill=col)
            d.text((px + 20, py - 8), label, font=font(32, "bold"), fill=NAVY, anchor="lb")


class NameCard(Anim):
    """"My name is ___" in the training data (left), the data's proportions p and the model's
    probabilities q per name (right), and the live average loss Σ p·(−log₂ q)."""

    def __init__(self, heading: str, names: list[tuple[str, int]], q_keys: list[tuple], data_at=None, p_at=None,
                 q_at=None, loss_at=False, formula: tuple | None = None):
        super().__init__(heading)
        self.names = names
        total = sum(c for _, c in names)
        self.p = [c / total for _, c in names]
        self.q_keys = q_keys
        for i, (at, _) in enumerate(q_keys):
            self.mark(f"q{i}", at)
        for n, at in (("data", data_at), ("p", p_at), ("q", q_at), ("loss", loss_at)):
            self.mark(n, at)
        lines = [nm for nm, c in names for _ in range(c)]
        cols = {nm: PALETTE[i % 4] for i, (nm, _) in enumerate(names)}
        for k, nm in enumerate(lines):
            row = Image.new("RGBA", (560, 50))
            rd = ImageDraw.Draw(row)
            rd.text((0, 25), "My name is", font=mono(32), fill=MUTED, anchor="lm")
            rd.text((mono(32).getlength("My name is "), 25), nm, font=mono(32, True), fill=cols[nm], anchor="lm")
            at = (data_at, 0.12 * k) if isinstance(data_at, str) else data_at
            self.add(row, MARGIN, 270 + k * 52, at, anim="fade", dur=0.3)
        self.add(D.text_img("訓練資料", font(30, "bold"), MUTED), MARGIN, 232, data_at, anim="fade")
        if formula:
            txt, at = formula
            self.add(math_img(txt, 44, NAVY, "bold"), 760, 820, at, anim="pop", sound="pop")

    def q_now(self, t):
        return glide([(None, list(self.q_keys[0][1]))] + [(f"q{i}", list(v)) for i, (_, v) in enumerate(self.q_keys)][1:],
                     self.T, t, 2.0)

    def extra_key(self, t):
        return tuple(round(v * 400) for v in self.q_now(t)), tuple(round(self.k(n, t) * 20) for n in ("p", "q", "loss"))

    def draw_extra(self, im, t):
        q = self.q_now(t)
        d = ImageDraw.Draw(im)
        gp, gq, gl = self.k("p", t), self.k("q", t), self.k("loss", t)
        x0 = 760
        if gp > 0 or gq > 0:
            d.text((x0 + 230, 262), "資料比例 p", font=font(30, "bold"), fill=GREEN, anchor="lm")
            d.text((x0 + 620, 262), "模型估 q", font=font(30, "bold"), fill=BLUE, anchor="lm")
        for i, (nm, _) in enumerate(self.names):
            y = 310 + i * 110
            d.text((x0, y + 30), nm, font=font(40, "bold"), fill=PALETTE[i % 4], anchor="lm")
            if gp > 0:
                L = 330 * self.p[i] / 0.5 * gp
                d.rounded_rectangle((x0 + 230, y + 8, x0 + 230 + L, y + 52), 10, fill=GREEN)
                d.text((x0 + 240 + L, y + 30), f"{self.p[i]:.0%}", font=font(30, "bold"), fill=GREEN, anchor="lm")
            if gq > 0:
                L = 330 * q[i] / 0.5 * gq
                d.rounded_rectangle((x0 + 620, y + 8, x0 + 620 + L, y + 52), 10, fill=BLUE)
                d.text((x0 + 630 + L, y + 30), f"{q[i]:.0%}", font=font(30, "bold"), fill=BLUE, anchor="lm")
        if gl > 0:
            loss = sum(pi * lg(qi) for pi, qi in zip(self.p, q))
            ent = sum(pi * lg(pi) for pi in self.p)
            pl = fade(D.pill(f"平均 loss = {loss:.2f} bits　（最細 = H(p) = {ent:.2f}）", font(38, "bold"), WHITE, RED,
                             px=30, py=12), gl)
            im.alpha_composite(pl, (x0, 740))


class TargetsCard(Anim):
    """Two panels of next-token targets side by side: the one-hot target of ordinary training and
    the big model's full distribution used in distillation."""

    def __init__(self, heading: str, tokens: list[str], panels: list[tuple]):
        super().__init__(heading)
        self.tokens, self.panels = tokens, panels
        for i, (_, _, _, at) in enumerate(panels):
            self.mark(f"pn{i}", at)

    def extra_key(self, t):
        return tuple(round(self.k(f"pn{i}", t, 1.0) * 40) for i in range(len(self.panels)))

    def draw_extra(self, im, t):
        pw = 780
        for i, (title, col, vals, _) in enumerate(self.panels):
            g = self.k(f"pn{i}", t, 1.0)
            if g <= 0:
                continue
            x = MARGIN + i * (pw + 120)
            layer = Image.new("RGBA", im.size)
            d = ImageDraw.Draw(layer)
            d.rounded_rectangle((x, 270, x + pw, 860), 28, fill=WHITE, outline=col, width=4)
            d.text((x + 40, 320), title, font=font(42, "bold"), fill=col, anchor="lm")
            n = len(self.tokens)
            bw = (pw - 120) / n
            for k, (tk, v) in enumerate(zip(self.tokens, vals)):
                bx = x + 60 + k * bw
                h = 380 * v * g
                d.rounded_rectangle((bx + 14, 780 - max(h, 4), bx + bw - 14, 780), 10, fill=col if v > 0 else LINE)
                d.text((bx + bw / 2, 800), tk, font=font(30, "bold"), fill=NAVY, anchor="mt")
                if g > 0.9:
                    d.text((bx + bw / 2, 770 - h), f"{v:.0%}", font=font(28, "bold"), fill=col, anchor="mb")
            im.alpha_composite(fade(layer, min(1, g * 1.4)))
