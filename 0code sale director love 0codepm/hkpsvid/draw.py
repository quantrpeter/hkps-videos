"""Drawing primitives: text, panels, emoji, the logo, arrows. Every helper returns an RGBA image.

Images with a drop shadow carry `img.info["pad"]`, the shadow margin around the visible box, so
`Item` can place the box itself at the given position.
"""

from __future__ import annotations

import re
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .style import (BADGE, BLUE, ED_BG, ED_GUTTER, EMOJI_PATH, INK, LINE, LOGO, MUTED, NAVY, WHITE, font, mono)
from .syntax import colours

NO_LINE_START = set("，。！？、；：」』）)》,.!?;:")


def width(s: str, f: ImageFont.FreeTypeFont) -> float:
    return f.getlength(s)


def wrap(s: str, f: ImageFont.FreeTypeFont, max_w: float) -> list[str]:
    """Wraps Chinese anywhere and English between words; punctuation never starts a line."""
    lines: list[str] = []
    for para in s.split("\n"):
        tokens = []
        for tok in re.findall(r"[A-Za-z0-9_+#.\-/:'&]+ ?| |.", para):
            while width(tok, f) > max_w and len(tok) > 1:      # a token too long for a line: split it
                k = len(tok)
                while k > 1 and width(tok[:k], f) > max_w:
                    k -= 1
                tokens.append(tok[:k])
                tok = tok[k:]
            tokens.append(tok)
        cur = ""
        for tok in tokens:
            if not cur or width(cur + tok, f) <= max_w or tok[0] in NO_LINE_START:
                cur += tok
            else:
                lines.append(cur.rstrip())
                cur = tok.lstrip()
        lines.append(cur.rstrip())
    return lines


def balanced(s: str, f: ImageFont.FreeTypeFont, max_w: float) -> str:
    """Breaks a short label into two even lines at a natural point (after 、, before 同, at a space)."""
    if width(s, f) <= max_w:
        return s
    cuts = [i + 1 for i, c in enumerate(s) if c == "、"] + [i for i, c in enumerate(s) if c == "同" and i > 0]
    cuts += [i for i, c in enumerate(s) if c == " "]
    best = None
    for i in cuts:
        a, b = s[:i].strip(), s[i:].strip()
        w = max(width(a, f), width(b, f))
        if w <= max_w and (best is None or w < best[0]):
            best = (w, f"{a}\n{b}")
    return best[1] if best else "\n".join(wrap(s, f, max_w))


def text_img(s: str, f: ImageFont.FreeTypeFont, fill, max_w: float | None = None,
             align: str = "left", line_h: float = 1.3) -> Image.Image:
    """Renders (wrapped) text to a tight RGBA image. Line height is a multiple of the font size."""
    lines = wrap(s, f, max_w) if max_w else s.split("\n")
    lh = round(f.size * line_h)
    w = max(1, int(max(width(l, f) for l in lines)) + 4)
    asc, desc = f.getmetrics()
    h = lh * (len(lines) - 1) + asc + desc + 4
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        lw = width(l, f)
        x = {"left": 0, "center": (w - lw) / 2, "right": w - lw}[align]
        d.text((x, i * lh), l, font=f, fill=fill)
    return im


def shadow_box(w: int, h: int, r: int, fill, outline=None, outline_w: int = 2,
               blur: int = 18, dy: int = 8, shadow=(20, 60, 120, 46)) -> Image.Image:
    """A rounded box with a soft drop shadow. info['pad'] is the shadow margin."""
    pad = blur * 2
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2))
    if shadow:
        sh = Image.new("RGBA", im.size)
        ImageDraw.Draw(sh).rounded_rectangle((pad, pad + dy, pad + w, pad + h + dy), r, fill=shadow)
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(blur)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((pad, pad, pad + w - 1, pad + h - 1), r, fill=fill,
                        outline=outline, width=outline_w if outline else 0)
    im.info["pad"] = pad
    return im


def paste(dst: Image.Image, src: Image.Image, x: float, y: float) -> None:
    """Alpha-pastes src so that its padded box (not its shadow) lands at x, y."""
    pad = src.info.get("pad", 0)
    dst.alpha_composite(src, (int(round(x)) - pad, int(round(y)) - pad))


def pill(s: str, f: ImageFont.FreeTypeFont, fg, bg, px: int = 28, py: int = 12,
         outline=None) -> Image.Image:
    t = text_img(s, f, fg)
    asc, desc = f.getmetrics()
    h = asc + desc + py * 2
    im = Image.new("RGBA", (t.width + px * 2, h))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, h - 1), h // 2, fill=bg,
                                         outline=outline, width=3 if outline else 0)
    im.alpha_composite(t, (px, py))
    return im


def circle_num(n: str, d: int, bg, fg=WHITE, size: int | None = None) -> Image.Image:
    im = Image.new("RGBA", (d, d))
    dr = ImageDraw.Draw(im)
    dr.ellipse((0, 0, d - 1, d - 1), fill=bg)
    f = font(size or int(d * 0.5), "bold")
    dr.text((d / 2, d / 2), n, font=f, fill=fg, anchor="mm")
    return im


@lru_cache(None)
def emoji(ch: str, size: int) -> Image.Image:
    """Apple Color Emoji, rendered at its native 160 px and scaled down."""
    if not EMOJI_PATH:
        return Image.new("RGBA", (size, size))
    f = ImageFont.truetype(EMOJI_PATH, 160)
    im = Image.new("RGBA", (220, 220))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    box = im.getbbox() or (0, 0, 1, 1)
    im = im.crop(box)
    s = size / max(im.size)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


@lru_cache(None)
def logo() -> Image.Image:
    """hkpsLogo.png cropped to its visible pixels, at native size (never upscaled)."""
    im = Image.open(LOGO).convert("RGBA")
    return im.crop(im.getchannel("A").getbbox())


@lru_cache(None)
def logo_badge() -> Image.Image:
    """The corner watermark: the logo on a white rounded square, with a soft shadow."""
    box = shadow_box(BADGE, BADGE, 28, WHITE, outline=LINE, outline_w=2, blur=12, dy=4,
                     shadow=(10, 30, 70, 70))
    lg = logo()
    s = (BADGE - 22) / max(lg.size)
    lg = lg.resize((round(lg.width * s), round(lg.height * s)), Image.LANCZOS)
    pad = box.info["pad"]
    box.alpha_composite(lg, (pad + (BADGE - lg.width) // 2, pad + (BADGE - lg.height) // 2))
    box.info["pad"] = pad
    return box


def arrow(x0: float, y0: float, x1: float, y1: float, color=MUTED, w: int = 6,
          head: int = 22) -> tuple[Image.Image, int, int]:
    """An arrow as an image, plus the position to paste it at."""
    m = head + w
    left, top = min(x0, x1) - m, min(y0, y1) - m
    im = Image.new("RGBA", (int(abs(x1 - x0) + 2 * m), int(abs(y1 - y0) + 2 * m)))
    d = ImageDraw.Draw(im)
    a = np.array([x0 - left, y0 - top])
    b = np.array([x1 - left, y1 - top])
    v = b - a
    n = v / (np.linalg.norm(v) or 1)
    p = np.array([-n[1], n[0]])
    tip = b
    base = b - n * head
    d.line([tuple(a), tuple(base + n * 2)], fill=color, width=w)
    d.polygon([tuple(tip), tuple(base + p * head * 0.6), tuple(base - p * head * 0.6)], fill=color)
    return im, int(left), int(top)


def code_chip(code: str, size: int = 34) -> Image.Image:
    """A command in a small dark box, e.g. `g++ --version`."""
    f = mono(size)
    h = round(size * 1.9)
    w = int(width(code, f)) + 56
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=(30, 41, 59))
    d.text((28, h / 2), code, font=f, fill=(226, 232, 240), anchor="lm")
    return im


def code_panel(code: str, name: str, w: int, size: int = 30, header: str | None = None) -> Image.Image:
    """Syntax-highlighted code on a dark panel (One Dark), wide characters handled."""
    f, fz = mono(size), font(size)
    adv = f.getlength("M")
    lh = round(size * 1.45)
    lines = code.rstrip("\n").split("\n")
    top = 70 if header else 30
    h = top + lh * len(lines) + 28
    box = shadow_box(w, h, 22, ED_BG, blur=16, shadow=(10, 30, 70, 70))
    p = box.info["pad"]
    d = ImageDraw.Draw(box)
    if header:
        d.text((p + 28, p + 22), header, font=font(26, "medium"), fill=ED_GUTTER)
    cols = colours(name, code.rstrip("\n"))
    k = 0
    for r, line in enumerate(lines):
        col = 0
        y = p + top + r * lh
        for ch in line:
            c = cols[k]
            k += 1
            x = p + 28 + col * adv
            if ord(ch) > 0x2E7F:
                d.text((x, y - 2), ch, font=fz, fill=c)
                col += 2
            else:
                if not ch.isspace():
                    d.text((x, y), ch, font=f, fill=c)
                col += 1
        k += 1  # the newline
    box.info["pad"] = p
    return box


def gradient(w: int, h: int, top, bottom) -> Image.Image:
    t = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - t) + np.array(bottom)[None, None, :] * t)
    arr = np.repeat(arr, w, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")


def panel(w: int, h: int, title: str | None = None, lines: tuple[str, ...] = (),
          numbered: bool = False, mono_lines: bool = False, dark: bool = False,
          accent=BLUE, size: int = 40, title_size: int = 44) -> Image.Image:
    """A white (or dark) rounded panel with a title and lines of text."""
    bg = (30, 41, 59) if dark else WHITE
    im = shadow_box(w, h, 26, bg, outline=None if dark else LINE)
    pad = im.info["pad"]
    d = ImageDraw.Draw(im)
    y = pad + 36
    if title:
        d.rounded_rectangle((pad + 36, y + 6, pad + 44, y + title_size + 2), 4, fill=accent)
        d.text((pad + 60, y), title, font=font(title_size, "bold"), fill=WHITE if dark else NAVY)
        y += title_size + 34
    for i, line in enumerate(lines):
        x = pad + 40
        if numbered:
            c = circle_num(str(i + 1), 52, accent, size=28)
            im.alpha_composite(c, (x, y + 2))
            x += 74
        f = mono(size) if mono_lines else font(size)
        fill = (134, 239, 172) if dark else INK
        d.text((x, y + (4 if numbered else 0)), line, font=f, fill=fill)
        y += round(size * 1.75)
    im.info["pad"] = pad
    return im
