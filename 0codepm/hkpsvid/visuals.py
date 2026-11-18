"""What is on screen during a scene.

A Visual is told the scene's timing once (`prepare`), then asked for frames (`render`). `key(t)`
changes only when the picture changes, so static stretches are rendered once and reused.

Times inside a scene (`at=`) can be: None (there from the start), seconds, a cue name from the
narration (「…[[run]]…」), or (cue, offset seconds).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from PIL import Image, ImageDraw

from . import draw as D
from .text import CJK
from .style import (AMBER, BG_BOTTOM, BG_TOP, BLUE, CONTENT_BOTTOM, CONTENT_TOP, H, INK, LINE,
                    MARGIN, MUTED, NAVY, W, WHITE, font, mono)


class Timing:
    """Scene-local times: narration starts at `lead` and lasts `clip` seconds."""

    def __init__(self, lead: float, clip: float, shares: dict[str, float]):
        self.lead, self.clip = lead, clip
        self.speech_end = lead + clip
        self.cues = {k: lead + v * clip for k, v in shares.items()}

    def at(self, a) -> float | None:
        if a is None:
            return None
        if isinstance(a, (int, float)):
            return float(a)
        if isinstance(a, tuple):
            return self.at(a[0]) + a[1]
        if a == "start":
            return 0.0
        if a == "speech":
            return self.lead
        if a == "end":
            return self.speech_end
        if a not in self.cues:
            raise KeyError(f"no [[{a}]] cue in this scene's narration (have: {', '.join(self.cues) or 'none'})")
        return self.cues[a]


def ease(p: float) -> float:
    return 1 - (1 - p) ** 3


class Visual:
    dark = False       # dark background (the coding stage)
    big_logo = False   # shows the logo large itself, so no corner badge
    tag = ""           # top-left series line, set by the build

    def prepare(self, timing: Timing) -> float:
        """Resolves times; returns when the last action ends (scene-local seconds)."""
        return 0.0

    def key(self, t: float):
        return 0

    def render(self, t: float) -> Image.Image:
        raise NotImplementedError

    def sounds(self) -> list[tuple[float, str]]:
        return []


@dataclass
class Item:
    img: Image.Image
    x: float
    y: float
    at: object = None
    anim: str = "up"      # up, fade, pop
    dur: float = 0.45
    sound: str | None = None


class Card(Visual):
    """A light card: series tag, heading, and items that appear at their times."""

    def __init__(self, heading: str | None = None, items: list[Item] | None = None):
        self.heading = heading
        self.items: list[Item] = list(items or [])
        self._base = None
        self._times: list[float | None] = []

    def add(self, img, x, y, at=None, anim="up", dur=0.45, sound=None) -> Item:
        it = Item(img, x, y, at, anim, dur, sound)
        self.items.append(it)
        return it

    def add_center(self, img, y, at=None, **kw) -> Item:
        return self.add(img, (W - img.width + 2 * img.info.get("pad", 0)) / 2, y, at, **kw)

    def background(self) -> Image.Image:
        return D.gradient(W, H, BG_TOP, BG_BOTTOM)

    def decorate(self, im: Image.Image) -> None:
        """Static drawing on the background (under the items)."""

    def base(self) -> Image.Image:
        if self._base is None:
            im = self.background()
            d = ImageDraw.Draw(im)
            if self.tag and not self.big_logo:
                d.text((MARGIN, 44), self.tag, font=font(28, "medium"), fill=MUTED)
            if self.heading:
                d.text((MARGIN, 88), self.heading, font=font(66, "bold"), fill=NAVY)
                d.rounded_rectangle((MARGIN, 190, MARGIN + 96, 198), 4, fill=BLUE)
            self.decorate(im)
            self._base = im
        return self._base

    def prepare(self, timing: Timing) -> float:
        self._times = [timing.at(it.at) for it in self.items]
        ends = [t + it.dur for t, it in zip(self._times, self.items) if t is not None]
        return max([0.0, *ends, self.prepare_extra(timing)])

    def prepare_extra(self, timing: Timing) -> float:
        return 0.0

    def progress(self, i: int, t: float) -> float:
        t0 = self._times[i]
        if t0 is None:
            return 1.0
        return min(1.0, max(0.0, (t - t0) / self.items[i].dur))

    def key(self, t: float):
        return tuple(round(self.progress(i, t) * 30) for i in range(len(self.items))) + (self.extra_key(t),)

    def extra_key(self, t: float):
        return 0

    def render(self, t: float) -> Image.Image:
        im = self.base().copy()
        for i, it in enumerate(self.items):
            p = self.progress(i, t)
            if p > 0:
                self._draw_item(im, it, p)
        self.draw_extra(im, t)
        return im

    def draw_extra(self, im: Image.Image, t: float) -> None:
        pass

    @staticmethod
    def _draw_item(im: Image.Image, it: Item, p: float) -> None:
        img, x, y = it.img, it.x, it.y
        if p < 1:
            e = ease(p)
            pad = img.info.get("pad", 0)
            if it.anim == "pop":
                s = 0.86 + 0.14 * e
                cx, cy = x - pad + img.width / 2, y - pad + img.height / 2
                img = img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))))
                x, y, pad = cx - img.width / 2, cy - img.height / 2, 0
            elif it.anim == "up":
                y += 28 * (1 - e)
            img = img.copy()
            img.putalpha(img.getchannel("A").point(lambda a: int(a * e)))
            img.info["pad"] = pad
        D.paste(im, img, x, y)

    def sounds(self) -> list[tuple[float, str]]:
        return [(t, it.sound) for t, it in zip(self._times, self.items) if t is not None and it.sound]


# ---------------------------------------------------------------------------------------------


class TitleCard(Card):
    """Opening card: the logo at native size, the series, the title and the video number."""

    big_logo = True

    def __init__(self, series: str, ep_id: str, part: str, title: str, subtitle: str | None = None):
        super().__init__()
        lg = D.logo()
        self.add_center(lg, 112, at=0.05, anim="fade", dur=0.6)
        self.add_center(D.text_img(series, font(50, "bold"), BLUE), 340, at=0.2, anim="fade")
        px = 128                                   # long titles shrink to fit between the braces
        while px > 72 and font(px, "bold").getlength(title) > 1440:
            px -= 4
        t = D.text_img(title, font(px, "bold"), NAVY)
        self.add_center(t, 408 + (128 - px) * 0.5, at=0.35)
        self.add_center(D.pill(f"{ep_id}　{part}", font(40, "bold"), WHITE, BLUE, px=34, py=12), 618, at=0.55)
        if subtitle:
            self.add_center(D.text_img(subtitle, font(40), MUTED), 726, at=0.75)

    def decorate(self, im):
        layer = Image.new("RGBA", im.size)
        d = ImageDraw.Draw(layer)
        f = mono(560, bold=True)
        d.text((40, 120), "{", font=f, fill=(*BLUE, 20))
        d.text((W - 380, 120), "}", font=f, fill=(*BLUE, 20))
        im.alpha_composite(layer)


class BulletCard(Card):
    """Numbered points that appear one by one."""

    def __init__(self, heading: str, bullets: list[tuple[str, object]], numbered: bool = True,
                 size: int = 52, top: int = CONTENT_TOP + 20, color=BLUE, gap: int = 44):
        super().__init__(heading)
        y = top
        for i, (txt, at) in enumerate(bullets):
            t = D.text_img(txt, font(size, "medium"), INK, max_w=W - 2 * MARGIN - 120)
            d = 72
            row = Image.new("RGBA", (W - 2 * MARGIN, max(t.height, d)))
            if numbered:
                row.alpha_composite(D.circle_num(str(i + 1), d, color, size=36), (0, 0))
            else:
                ImageDraw.Draw(row).ellipse((22, 22, 50, 50), fill=color)
            row.alpha_composite(t, (100, max(0, int((d - size * 1.4) // 2))))
            self.add(row, MARGIN, y, at, sound="pop")
            y += row.height + gap


@dataclass
class Tile:
    icon: str
    title: str
    sub: str = ""
    at: object = None
    color: tuple = BLUE


class TileCard(Card):
    """A grid of tiles (emoji, title, one or two lines of detail)."""

    def __init__(self, heading: str, tiles: list[Tile], cols: int = 3, height: int | None = None,
                 footer: tuple[str, object] | None = None, top: int = CONTENT_TOP + 10, gap: int = 40):
        super().__init__(heading)
        rows = math.ceil(len(tiles) / cols)
        avail = CONTENT_BOTTOM - top - (120 if footer else 0)
        tw = (W - 2 * MARGIN - (cols - 1) * gap) // cols
        th = min(height or 10_000, (avail - (rows - 1) * gap) // rows)
        for i, tile in enumerate(tiles):
            r, c = divmod(i, cols)
            box = D.shadow_box(tw, th, 28, WHITE, outline=LINE)
            pad = box.info["pad"]
            d = ImageDraw.Draw(box)
            d.rounded_rectangle((pad, pad + 26, pad + 10, pad + th - 26), 5, fill=tile.color)
            ic = D.emoji(tile.icon, 84)
            box.alpha_composite(ic, (pad + 44, pad + 34))
            d.text((pad + 44, pad + 140), tile.title, font=font(46, "bold"), fill=NAVY)
            if tile.sub:
                s = D.text_img(tile.sub, font(31), MUTED, max_w=tw - 80, line_h=1.35)
                box.alpha_composite(s, (pad + 44, pad + 206))
            box.info["pad"] = pad
            self.add(box, MARGIN + c * (tw + gap), top + r * (th + gap), tile.at, anim="pop", sound="pop")
        if footer:
            txt, at = footer
            p = D.pill(txt, font(42, "bold"), WHITE, AMBER, px=40, py=14)
            self.add_center(p, top + rows * th + (rows - 1) * gap + 44, at=at, anim="pop", sound="pop")


@dataclass
class Event:
    year: str
    title: str
    sub: str = ""
    at: object = None
    color: tuple = BLUE


class TimelineCard(Card):
    """A horizontal timeline; labels alternate above and below the line."""

    LINE_Y = 540

    def __init__(self, heading: str, events: list[Event], callout: tuple[str, object] | None = None):
        super().__init__(heading)
        n = len(events)
        x0, x1 = MARGIN + 110, W - MARGIN - 110
        self._x0, self._x1 = x0 - 60, x1 + 60
        for i, ev in enumerate(events):
            x = x0 + i * (x1 - x0) / max(1, n - 1)
            above = i % 2 == 0
            parts = [D.text_img(ev.year, font(50, "bold"), ev.color),
                     D.text_img(ev.title, font(36, "bold"), NAVY, max_w=380, align="center")]
            if ev.sub:
                parts.append(D.text_img(ev.sub, font(28), MUTED, max_w=380, align="center"))
            bw = max(p.width for p in parts)
            bh = sum(p.height for p in parts) + 8 * (len(parts) - 1)
            block = Image.new("RGBA", (bw, bh))
            y = 0
            for p in parts:
                block.alpha_composite(p, ((bw - p.width) // 2, y))
                y += p.height + 8
            by = self.LINE_Y - 44 - bh if above else self.LINE_Y + 44
            stem = Image.new("RGBA", (40, 70))
            sd = ImageDraw.Draw(stem)
            sd.line((20, 0, 20, 70), fill=ev.color, width=4)
            dot = Image.new("RGBA", (40, 40))
            dd = ImageDraw.Draw(dot)
            dd.ellipse((2, 2, 38, 38), fill=WHITE, outline=ev.color, width=8)
            self.add(dot, x - 20, self.LINE_Y - 20, ev.at, anim="pop", sound="pop")
            self.add(block, x - bw / 2, by, ev.at)
        if callout:
            txt, at = callout
            self.add_center(D.pill(txt, font(44, "bold"), WHITE, AMBER, px=44, py=16), 812, at=at, anim="pop", sound="pop")

    def decorate(self, im):
        ImageDraw.Draw(im).rounded_rectangle((self._x0, self.LINE_Y - 4, self._x1, self.LINE_Y + 4), 4, fill=LINE)


@dataclass
class Node:
    title: str
    sub: str = ""
    at: object = None
    col: int | None = None


@dataclass
class Row:
    label: str
    sub: str
    color: tuple
    nodes: list[Node] = field(default_factory=list)
    note: str = ""
    note_at: object = None


class FlowCard(Card):
    """Rows of boxes joined by arrows, e.g. source -> compiler -> program."""

    NODE_W, NODE_H, COL0, COL_STEP = 290, 150, 400, 365

    def __init__(self, heading: str, rows: list[Row], top: int = 268, row_h: int = 300):
        super().__init__(heading)
        for r, row in enumerate(rows):
            y = top + r * row_h
            first = row.nodes[0].at if row.nodes else None
            lab = D.shadow_box(232, self.NODE_H, 26, row.color, blur=12, shadow=(20, 60, 120, 40))
            pad = lab.info["pad"]
            ld = ImageDraw.Draw(lab)
            ld.text((pad + 116, pad + 56), row.label, font=font(48, "bold"), fill=WHITE, anchor="mm")
            ld.text((pad + 116, pad + 108), row.sub, font=font(30, "medium"), fill=WHITE, anchor="mm")
            lab.info["pad"] = pad
            self.add(lab, MARGIN, y, first, anim="pop", sound="pop")
            prev_right = None
            for j, node in enumerate(row.nodes):
                col = node.col if node.col is not None else j
                x = self.COL0 + col * self.COL_STEP
                box = D.shadow_box(self.NODE_W, self.NODE_H, 24, WHITE, outline=row.color, outline_w=4)
                p = box.info["pad"]
                bd = ImageDraw.Draw(box)
                bd.text((p + self.NODE_W / 2, p + (52 if node.sub else self.NODE_H / 2)), node.title,
                        font=font(42, "bold"), fill=NAVY, anchor="mm")
                if node.sub:
                    s = D.text_img(node.sub, font(28), MUTED, max_w=self.NODE_W - 30, align="center", line_h=1.25)
                    box.alpha_composite(s, (p + (self.NODE_W - s.width) // 2, p + 84))
                box.info["pad"] = p
                if prev_right is not None:
                    a, ax, ay = D.arrow(prev_right + 10, y + self.NODE_H / 2, x - 12, y + self.NODE_H / 2, color=row.color)
                    self.add(a, ax, ay, node.at, anim="fade", dur=0.3)
                self.add(box, x, y, node.at, anim="pop", sound="pop")
                prev_right = x + self.NODE_W
            if row.note:
                t = D.text_img("「" + row.note + "」", font(34, "medium"), row.color)
                self.add(t, self.COL0, y + self.NODE_H + 26, row.note_at, anim="fade")


@dataclass
class Bar:
    label: str
    value: float
    text: str
    color: tuple


class BarCard(Card):
    """Horizontal bars that grow from zero, then a badge."""

    X0, MAX_LEN, BAR_H = 470, 1060, 100

    def __init__(self, heading: str, bars: list[Bar], at, badge: tuple[str, object] | None = None,
                 note: tuple[str, object] | None = None, top: int = 300, step: int = 170, stagger: float = 0.7):
        super().__init__(heading)
        self.bars, self.bars_at, self.top, self.step, self.stagger = bars, at, top, step, stagger
        self._t0 = 0.0
        vmax = max(b.value for b in bars) or 1
        self._len = [max(14, b.value / vmax * self.MAX_LEN) for b in bars]
        self._vals = [D.text_img(b.text, font(48, "bold"), b.color) for b in bars]
        for i, b in enumerate(bars):
            self.add(D.text_img(b.label, font(56, "bold"), NAVY), MARGIN, top + i * step + 14, at, anim="fade")
        if badge:
            txt, bat = badge
            self.add_center(D.pill(txt, font(64, "bold"), WHITE, AMBER, px=56, py=20), top + len(bars) * step + 40,
                            at=bat, anim="pop", sound="pop")
        if note:
            txt, nat = note
            self.add_center(D.text_img(txt, font(38, "medium"), MUTED), top + len(bars) * step + (200 if badge else 30),
                            at=nat, anim="fade")

    def prepare_extra(self, timing):
        self._t0 = timing.at(self.bars_at)
        return self._t0 + self.stagger * (len(self.bars) - 1) + 1.2

    def _grow(self, i, t):
        return ease(min(1.0, max(0.0, (t - self._t0 - i * self.stagger) / 1.0)))

    def extra_key(self, t):
        return tuple(round(self._grow(i, t) * 60) for i in range(len(self.bars)))

    def draw_extra(self, im, t):
        d = ImageDraw.Draw(im)
        for i, b in enumerate(self.bars):
            g = self._grow(i, t)
            if g <= 0:
                continue
            y = self.top + i * self.step
            L = self._len[i] * g
            d.rounded_rectangle((self.X0, y, self.X0 + max(L, 14), y + self.BAR_H), 16, fill=b.color)
            if g >= 0.98:
                v = self._vals[i]
                im.alpha_composite(v, (int(self.X0 + L + 26), int(y + (self.BAR_H - v.height) / 2)))


class RoadmapCard(Card):
    """The course parts as tiles; groups light up at their cues."""

    def __init__(self, heading: str, parts: list[tuple[int, str, str]],
                 groups: list[tuple[list[int], tuple, object]], cols: int = 7, top: int = 262):
        super().__init__(heading)
        gap = 26
        tw = (W - 2 * 112 - (cols - 1) * gap) // cols
        th = 300
        x0 = (W - (cols * tw + (cols - 1) * gap)) // 2
        group_of = {}
        for nums, color, at in groups:
            for k, n in enumerate(nums):
                group_of[n] = (color, (at, k * 0.08) if isinstance(at, str) else at)
        for i, (num, zh, en) in enumerate(parts):
            color, at = group_of.get(num, (MUTED, None))
            r, c = divmod(i, cols)
            box = D.shadow_box(tw, th, 24, WHITE, outline=LINE, blur=12)
            p = box.info["pad"]
            box.alpha_composite(D.circle_num(str(num), 76, color, size=36), (p + (tw - 76) // 2, p + 26))
            zf = font(33, "bold")
            z = D.text_img(D.balanced(zh, zf, tw - 28), zf, NAVY, align="center", line_h=1.25)
            box.alpha_composite(z, (p + (tw - z.width) // 2, p + 122))
            e = D.text_img(en, font(22), MUTED, max_w=tw - 28, align="center", line_h=1.25)
            box.alpha_composite(e, (p + (tw - e.width) // 2, p + 136 + z.height))
            box.info["pad"] = p
            self.add(box, x0 + c * (tw + gap), top + r * (th + 30), at, anim="pop", dur=0.35,
                     sound="pop" if i == 0 or (isinstance(at, tuple) and at[1] == 0) else None)


class EndCard(Card):
    """Closing card: the logo, 多謝收睇, the challenge and the next video."""

    big_logo = True

    def __init__(self, challenge: str, next_line: str, challenge_at=None, next_at=None):
        super().__init__()
        self.add_center(D.logo(), 70, at=None)
        self.add_center(D.text_img("多謝收睇", font(80, "bold"), NAVY), 276, at=None)
        bw = 1440
        t = D.text_img(challenge, font(44, "medium"), INK, max_w=bw - 120, line_h=1.45)
        bh = t.height + 150
        box = D.shadow_box(bw, bh, 30, WHITE, outline=AMBER, outline_w=4)
        p = box.info["pad"]
        box.alpha_composite(D.pill("小挑戰", font(36, "bold"), WHITE, AMBER, px=26, py=8), (p + 56, p + 34))
        box.alpha_composite(t, (p + 60, p + 110))
        box.info["pad"] = p
        self.add_center(box, 418, at=challenge_at, anim="pop", sound="pop")
        self.add_center(D.text_img(next_line, font(48, "bold"), BLUE), 418 + bh + 50, at=next_at)


@dataclass
class Step:
    text: str
    code: str = ""
    at: object = None


class StepsCard(Card):
    """Numbered how-to steps, each with an optional command in a dark box."""

    def __init__(self, heading: str, steps: list[Step], icon: str | None = None, color=BLUE,
                 start: int = 1, top: int = CONTENT_TOP + 10, gap: int = 30, size: int = 44):
        super().__init__(heading)
        self.icon = icon
        y = top
        for i, s in enumerate(steps):
            t = D.text_img(s.text, font(size, "medium"), INK, max_w=W - 2 * MARGIN - 110)
            code = D.code_chip(s.code) if s.code else None
            h = max(64, t.height + (code.height + 12 if code else 0))
            row = Image.new("RGBA", (W - 2 * MARGIN, h))
            row.alpha_composite(D.circle_num(str(start + i), 64, color, size=32), (0, 0))
            row.alpha_composite(t, (96, 2))
            if code:
                row.alpha_composite(code, (96, t.height + 10))
            self.add(row, MARGIN, y, s.at, sound="pop")
            y += h + gap

    def decorate(self, im):
        if self.icon and self.heading:
            x = MARGIN + int(font(66, "bold").getlength(self.heading)) + 28
            im.alpha_composite(D.emoji(self.icon, 72), (x, 104))


@dataclass
class Part:
    code: str
    label: str = ""
    color: tuple = BLUE
    at: object = None


class AnatomyCard(Card):
    """A line of code (or a command, or an error line) in big type; each part lights up with a label."""

    def __init__(self, heading: str, parts: list[Part], size: int = 60, y: int = 400,
                 note: tuple[str, object] | None = None):
        super().__init__(heading)
        n = sum(len(p.code) for p in parts)
        size = min(size, int((W - 2 * MARGIN) / (n * 0.602)))
        f = mono(size)
        adv = f.getlength("M")
        x = (W - n * adv) / 2
        self._grey = []
        ends = [-1e9, -1e9]
        line_y = y + size * 1.32
        for p in parts:
            lead = len(p.code) - len(p.code.lstrip(" "))
            trail = len(p.code) - len(p.code.rstrip(" "))
            xa, xb = x + lead * adv, x + (len(p.code) - trail) * adv
            core = p.code.strip()
            self._grey.append((xa, y, core, f))
            if core:
                canvas = Image.new("RGBA", (W, H))
                d = ImageDraw.Draw(canvas)
                d.text((xa, y), core, font=f, fill=p.color)
                d.rounded_rectangle((xa + 2, line_y, xb - 2, line_y + 8), 4, fill=p.color)
                if p.label:
                    lab = D.text_img(p.label, font(34, "bold"), p.color)
                    lx = (xa + xb) / 2 - lab.width / 2
                    row = 0 if lx > ends[0] + 24 else 1
                    ends[row] = lx + lab.width
                    ly = line_y + 34 + row * 66
                    if row:
                        d.line(((xa + xb) / 2, line_y + 12, (xa + xb) / 2, ly - 4), fill=p.color, width=3)
                    canvas.alpha_composite(lab, (int(lx), int(ly)))
                box = canvas.getbbox()
                self.add(canvas.crop(box), box[0], box[1], p.at, anim="fade", sound="pop")
            x += len(p.code) * adv
        if note:
            txt, at = note
            self.add_center(D.text_img(txt, font(40, "medium"), MUTED), line_y + 190, at=at, anim="fade")

    def decorate(self, im):
        d = ImageDraw.Draw(im)
        for xa, y, core, f in self._grey:
            d.text((xa, y), core, font=f, fill=(150, 164, 186))


@dataclass
class Pane:
    title: str
    code: str
    good: bool = True
    at: object = None
    name: str = "a.cpp"


class CodeCompareCard(Card):
    """Code side by side with ❌ / ✅ headers (style, naming, before and after)."""

    def __init__(self, heading: str, panes: list[Pane], size: int = 30, top: int = CONTENT_TOP + 10):
        super().__init__(heading)
        gap = 40
        pw = (W - 2 * MARGIN - (len(panes) - 1) * gap) // len(panes)
        for i, pn in enumerate(panes):
            x = MARGIN + i * (pw + gap)
            head = Image.new("RGBA", (pw, 70))
            head.alpha_composite(D.emoji("✅" if pn.good else "❌", 52), (0, 8))
            ImageDraw.Draw(head).text((70, 35), pn.title, font=font(44, "bold"),
                                       fill=(22, 163, 74) if pn.good else (220, 38, 38), anchor="lm")
            self.add(head, x, top, pn.at, sound="pop")
            self.add(D.code_panel(pn.code, pn.name, pw, size), x, top + 90, pn.at)


# -- memory boxes and tables ---------------------------------------------------------------------


@dataclass
class Box:
    name: str = ""          # above the box (a variable name, mono)
    value: object = ""      # inside: "5", or [("5", None), ("6", "inc")] for a value that changes at cues
    sub: str = ""           # below: the type, an address or an index
    at: object = None
    color: tuple = BLUE
    w: int = 0              # 0: wide enough for every value
    key: str = ""           # for arrows; defaults to the name


@dataclass
class BoxRow:
    boxes: list
    label: str = ""         # at the left, e.g. 「main 嘅變數」
    gap: int = 40           # 0 joins the boxes into one array
    at: object = None


def _tint(c, k: float = 0.88) -> tuple:
    return tuple(int(v + (255 - v) * k) for v in c)


class BoxesCard(Card):
    """Memory as boxes: name above, value inside, type (or address, or index) below. Values can
    change at cues, and arrows join boxes (a pointer, a reference, a copy)."""

    NAME_H, SUB_H = 54, 50

    def __init__(self, heading: str | None, rows: list[BoxRow], arrows: list[tuple] = (),
                 footer: tuple[str, object] | None = None, top: int = CONTENT_TOP + 60, row_h: int = 260,
                 box_h: int = 120, size: int = 48, notes: list[tuple[str, object]] = ()):
        super().__init__(heading)
        vf, nf, sf = mono(size), mono(max(34, round(size * 0.6)), bold=True), font(max(28, round(size * 0.45)), "medium")
        self.NAME_H, self.SUB_H = round(nf.size * 1.6), round(sf.size * 1.8)
        label_w = 300 if any(r.label for r in rows) else 0
        self.rects: dict[str, tuple] = {}
        y = top
        for row in rows:
            ws = []
            for b in row.boxes:
                vals = b.value if isinstance(b.value, list) else [(b.value, None)]
                need = max([(font(round(size * 0.8), "medium") if CJK.search(str(v)) else vf).getlength(str(v)) for v, _ in vals]
                           + [nf.getlength(b.name) - 20, sf.getlength(b.sub) - 20])
                ws.append(b.w or max(150, int(need) + 64))
            total = sum(ws) + row.gap * (len(ws) - 1)
            x0 = MARGIN + label_w + (W - 2 * MARGIN - label_w - total) / 2
            if row.label:
                lab = D.text_img(row.label, font(36, "bold"), MUTED, max_w=label_w - 30)
                self.add(lab, MARGIN, y + self.NAME_H + (box_h - lab.height) / 2, row.at, anim="fade")
            x = x0
            for b, w in zip(row.boxes, ws):
                fill = _tint(b.color)
                im = Image.new("RGBA", (w, self.NAME_H + box_h + self.SUB_H))
                d = ImageDraw.Draw(im)
                if b.name:
                    nf_ = font(nf.size, "bold") if CJK.search(b.name) else nf
                    d.text((w / 2, self.NAME_H / 2), b.name, font=nf_, fill=NAVY, anchor="mm")
                d.rounded_rectangle((0, self.NAME_H, w - 1, self.NAME_H + box_h - 1), 10 if row.gap else 2,
                                    fill=fill, outline=b.color, width=4)
                if b.sub:
                    d.text((w / 2, self.NAME_H + box_h + self.SUB_H / 2 + 2), b.sub, font=sf, fill=MUTED, anchor="mm")
                self.add(im, x, y, b.at, anim="pop", sound="pop")
                vals = b.value if isinstance(b.value, list) else [(b.value, None)]
                for k, (v, vat) in enumerate(vals):
                    if v == "" or v is None:
                        continue
                    vi = Image.new("RGBA", (w - 12, box_h - 12), (*fill, 255))
                    f_ = font(round(size * 0.8), "medium") if CJK.search(str(v)) else vf   # Menlo has no CJK
                    ImageDraw.Draw(vi).text(((w - 12) / 2, (box_h - 12) / 2), str(v), font=f_, fill=INK, anchor="mm")
                    when = b.at if (k == 0 and vat is None) else vat
                    self.add(vi, x + 6, y + self.NAME_H + 6, when, anim="fade" if k == 0 else "pop",
                             sound=None if k == 0 else "pop")
                self.rects[b.key or b.name] = (x, y + self.NAME_H, x + w, y + self.NAME_H + box_h)
                x += w + row.gap
            y += max(row_h, self.NAME_H + box_h + self.SUB_H + 24)
        for a in arrows:
            src, dst, at = a[0], a[1], a[2] if len(a) > 2 else None
            color = a[3] if len(a) > 3 else AMBER
            (sx0, sy0, sx1, sy1), (tx0, ty0, tx1, ty1) = self.rects[src], self.rects[dst]
            if abs(sy0 - ty0) < 1:
                if tx0 >= sx1:
                    p0, p1 = (sx1 + 6, (sy0 + sy1) / 2), (tx0 - 8, (ty0 + ty1) / 2)
                else:
                    p0, p1 = (sx0 - 6, (sy0 + sy1) / 2), (tx1 + 8, (ty0 + ty1) / 2)
            elif ty0 > sy0:
                p0, p1 = ((sx0 + sx1) / 2, sy1 + self.SUB_H), ((tx0 + tx1) / 2, ty0 - self.NAME_H)
            else:
                p0, p1 = ((sx0 + sx1) / 2, sy0 - self.NAME_H), ((tx0 + tx1) / 2, ty1 + self.SUB_H)
            img, ax, ay = D.arrow(*p0, *p1, color=color)
            self.add(img, ax, ay, at, anim="fade", dur=0.3)
        ny = y + 10
        for txt, at in notes:
            t = D.text_img(txt, font(38, "medium"), INK, max_w=W - 2 * MARGIN)
            self.add_center(t, ny, at=at, anim="fade")
            ny += t.height + 18
        if footer:
            txt, at = footer
            self.add_center(D.pill(txt, font(42, "bold"), WHITE, AMBER, px=40, py=14), max(ny, y) + 10, at=at,
                            anim="pop", sound="pop")


class TableCard(Card):
    """A table whose rows appear at their cues. rows: (cells, at) or (cells, at, colour)."""

    def __init__(self, heading: str | None, header: list[str], rows: list[tuple], widths: list[float] | None = None,
                 size: int = 40, code_cols: tuple = (0,), top: int = CONTENT_TOP + 20,
                 note: tuple[str, object] | None = None):
        super().__init__(heading)
        n = len(header)
        widths = widths or [1] * n
        tw = W - 2 * MARGIN
        cw = [int(tw * w / sum(widths)) for w in widths]
        hf = font(size - 4, "bold")
        hh = round(size * 1.9)
        head = Image.new("RGBA", (tw, hh))
        d = ImageDraw.Draw(head)
        d.rounded_rectangle((0, 0, tw - 1, hh - 1), 16, fill=NAVY)
        d.rectangle((0, hh - 16, tw - 1, hh - 1), fill=NAVY)
        x = 0
        for c, h in zip(cw, header):
            d.text((x + 28, hh / 2), h, font=hf, fill=WHITE, anchor="lm")
            x += c
        self.add(head, MARGIN, top, None)
        y = top + hh
        for i, r in enumerate(rows):
            cells, at = r[0], r[1]
            color = r[2] if len(r) > 2 else INK
            imgs = []
            for k, (c, txt) in enumerate(zip(cw, cells)):
                wide = any(ord(ch) > 0x2E7F for ch in str(txt))          # Menlo has no CJK or full-width forms
                f = mono(size - 4) if k in code_cols and not wide else font(size, "medium")
                imgs.append(D.text_img(str(txt), f, color if k else (color if color != INK else NAVY), max_w=c - 50, line_h=1.3))
            rh = max(im.height for im in imgs) + 34
            row = Image.new("RGBA", (tw, rh))
            rd = ImageDraw.Draw(row)
            rd.rectangle((0, 0, tw - 1, rh - 1), fill=WHITE if i % 2 == 0 else (243, 248, 255))
            rd.line((0, rh - 1, tw, rh - 1), fill=LINE, width=2)
            x = 0
            for c, im in zip(cw, imgs):
                row.alpha_composite(im, (x + 28, (rh - im.height) // 2))
                x += c
            self.add(row, MARGIN, y, at, sound="pop")
            y += rh
        if note:
            txt, at = note
            self.add_center(D.text_img(txt, font(38, "medium"), MUTED, max_w=tw), y + 36, at=at, anim="fade")


class CodeCard(Card):
    """A whole program on a dark panel. marks: ((first, last), label, at[, colour]) light up line
    ranges with a label beside the panel, e.g. ((5, 8), "輸入", "in")."""

    def __init__(self, heading: str | None, code: str, name: str = "main.cpp", marks: list[tuple] = (),
                 size: int = 30, width: int = 1160, top: int = CONTENT_TOP - 10):
        super().__init__(heading)
        lh = round(size * 1.45)
        self.add(D.code_panel(code, name, width, size), MARGIN, top, None)
        used: list[tuple[int, int]] = []          # label rows already taken (absolute y), so labels never overlap
        for m in marks:
            (first, last), label, at = m[0], m[1], m[2]
            color = m[3] if len(m) > 3 else AMBER
            y0, y1 = top + 30 + (first - 1) * lh - 6, top + 30 + last * lh - 4
            lab = D.pill(label, font(38, "bold"), WHITE, color, px=24, py=10)
            ly = (y0 + y1) // 2 - lab.height // 2
            for a, b in sorted(used):
                if ly < b + 8 and ly + lab.height > a - 8:
                    ly = b + 12
            used.append((ly, ly + lab.height))
            oy = min(y0 - 2, ly)
            ov = Image.new("RGBA", (W - MARGIN, max(y1, ly + lab.height) - oy + 8))
            d = ImageDraw.Draw(ov)
            d.rounded_rectangle((0, y0 - oy, width - 1, y1 - oy + 2), 10, outline=color, width=4)
            cy = ly + lab.height // 2 - oy
            d.line((width + 4, min(max(cy, y0 - oy + 8), y1 - oy - 4), width + 20, cy), fill=color, width=4)
            d.line((width + 20, cy, width + 40, cy), fill=color, width=4)
            ov.alpha_composite(lab, (width + 40, ly - oy))
            self.add(ov, MARGIN, oy, at, anim="fade", sound="pop")


# -- conversations and comparisons ---------------------------------------------------------------


@dataclass
class Msg:
    who: int            # index into ChatCard's people: 0 talks from the left, 1 from the right
    text: str
    at: object = None


class ChatCard(Card):
    """A conversation as speech bubbles that appear at their cues. people: (emoji, name, colour)
    for the left and the right speaker. footer: (text, at[, colour]) for the outcome."""

    AV = 104

    def __init__(self, heading: str | None, people: list[tuple[str, str, tuple]], msgs: list[Msg],
                 footer: tuple | None = None, size: int = 40, top: int = CONTENT_TOP - 30, gap: int = 14,
                 max_w: int = 1080):
        super().__init__(heading)
        f, nf = font(size, "medium"), font(26, "bold")
        y = top
        for m in msgs:
            emo, name, color = people[m.who]
            right = m.who == 1
            t = D.text_img(m.text, f, INK, max_w=max_w, line_h=1.38)
            bw, bh = t.width + 64, t.height + 28
            lab = D.text_img(name, nf, color)
            rh = max(self.AV, lab.height + 8 + bh)
            row = Image.new("RGBA", (W - 2 * MARGIN, rh))
            d = ImageDraw.Draw(row)
            ax = row.width - self.AV if right else 0
            d.ellipse((ax, 0, ax + self.AV - 1, self.AV - 1), fill=_tint(color, 0.8), outline=color, width=4)
            ic = D.emoji(emo, 60)
            row.alpha_composite(ic, (ax + (self.AV - ic.width) // 2, (self.AV - ic.height) // 2))
            bx = ax - 28 - bw if right else self.AV + 28
            row.alpha_composite(lab, ((bx + bw - lab.width) if right else bx, 0))
            by = lab.height + 8
            d.rounded_rectangle((bx, by, bx + bw - 1, by + bh - 1), 28,
                                fill=_tint(color, 0.86) if right else WHITE, outline=color if right else LINE, width=3)
            row.alpha_composite(t, (bx + 32, by + 12))
            self.add(row, MARGIN, y, m.at, sound="pop")
            y += rh + gap
        if footer:
            txt, at = footer[0], footer[1]
            color = footer[2] if len(footer) > 2 else AMBER
            p = D.pill(txt, font(42, "bold"), WHITE, color, px=40, py=14)
            y += 8
            self.add_center(p, y, at=at, anim="pop", sound="pop")
            y += p.height
        if y > CONTENT_BOTTOM + 10:
            raise SystemExit(f"hkpsvid: ChatCard {heading!r} runs {y - CONTENT_BOTTOM:.0f}px into the subtitles; "
                             "shorten the messages or drop one")


@dataclass
class Column:
    icon: str
    title: str
    lines: list[tuple[str, object]]   # (text, at)
    color: tuple = BLUE
    at: object = "first"              # when the panel appears; "first" = with its first line


class CompareCard(Card):
    """Panels side by side (bad vs good, boss vs staff), each a title and points appearing at cues."""

    def __init__(self, heading: str | None, cols: list[Column], footer: tuple | None = None, size: int = 46,
                 top: int = CONTENT_TOP + 10, gap: int = 48, line_gap: int = 40):
        super().__init__(heading)
        n = len(cols)
        pw = (W - 2 * MARGIN - (n - 1) * gap) // n
        f = font(size, "medium")
        texts = [[D.text_img(txt, f, INK, max_w=pw - 130, line_h=1.32) for txt, _ in c.lines] for c in cols]
        head_h = 150
        ph = max(head_h + sum(t.height for t in ts) + line_gap * max(0, len(ts) - 1) + 44 for ts in texts)
        for i, (c, ts) in enumerate(zip(cols, texts)):
            x = MARGIN + i * (pw + gap)
            box = D.shadow_box(pw, ph, 28, WHITE, outline=LINE)
            p = box.info["pad"]
            d = ImageDraw.Draw(box)
            d.rounded_rectangle((p, p, p + pw - 1, p + 18), 9, fill=c.color)
            d.rectangle((p, p + 9, p + pw - 1, p + 18), fill=WHITE)
            box.alpha_composite(D.emoji(c.icon, 64), (p + 40, p + 46))
            d.text((p + 124, p + 78), c.title, font=font(52, "bold"), fill=c.color, anchor="lm")
            box.info["pad"] = p
            at = c.lines[0][1] if c.at == "first" and c.lines else (None if c.at == "first" else c.at)
            self.add(box, x, top, at, anim="pop", sound="pop")
            y = top + head_h
            for (txt, lat), t in zip(c.lines, ts):
                row = Image.new("RGBA", (pw - 60, t.height))
                ImageDraw.Draw(row).ellipse((0, size * 0.45, 24, size * 0.45 + 24), fill=c.color)
                row.alpha_composite(t, (50, 0))
                self.add(row, x + 44, y, lat, sound=None if lat == at else "pop")
                y += t.height + line_gap
        if footer:
            txt, at = footer[0], footer[1]
            color = footer[2] if len(footer) > 2 else AMBER
            self.add_center(D.pill(txt, font(42, "bold"), WHITE, color, px=40, py=14), top + ph + 40, at=at,
                            anim="pop", sound="pop")
