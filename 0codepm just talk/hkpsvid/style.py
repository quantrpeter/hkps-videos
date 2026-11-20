"""Canvas size, colours and fonts shared by every video."""

from __future__ import annotations

import glob
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOGO = ROOT / "hkpsLogo.png"

W, H = 1920, 1080
FPS = 30

# Light cards. BLUE is sampled from hkpsLogo.png.
BLUE = (0, 148, 255)
NAVY = (11, 27, 51)
INK = (33, 46, 70)
MUTED = (96, 112, 138)
LINE = (214, 226, 242)
BG_TOP = (249, 252, 255)
BG_BOTTOM = (226, 239, 255)
AMBER = (245, 158, 11)
GREEN = (22, 163, 74)
RED = (220, 38, 38)
PURPLE = (124, 92, 255)
TEAL = (13, 148, 136)
WHITE = (255, 255, 255)

# The dark coding stage (One Dark colours).
STAGE_TOP = (22, 28, 44)
STAGE_BOTTOM = (11, 15, 26)
ED_BG = (40, 44, 52)
ED_BAR = (33, 37, 43)
ED_TEXT = (171, 178, 191)
ED_GUTTER = (92, 99, 112)
ED_CURRENT = (49, 54, 63)
TERM_BG = (13, 17, 23)
TERM_TEXT = (230, 237, 243)
TERM_PROMPT = (63, 185, 80)
TERM_DIM = (139, 148, 158)

# Layout: the logo badge owns the top-right corner, subtitles own the bottom strip.
MARGIN = 120
BADGE = 132
BADGE_MARGIN = 32
CONTENT_TOP = 250
CONTENT_BOTTOM = 930
SUB_Y = 1004  # centre line of the subtitle pill


def _find(patterns: list[str]) -> str | None:
    for p in patterns:
        hits = sorted(glob.glob(p))
        if hits:
            return hits[0]
    return None


CJK_PATH = _find([
    "/System/Library/AssetsV2/*/*/AssetData/PingFang.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
])
MONO_PATH = _find(["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/SFNSMono.ttf"])
EMOJI_PATH = _find(["/System/Library/Fonts/Apple Color Emoji.ttc"])
if not CJK_PATH or not MONO_PATH:
    raise SystemExit("hkpsvid: needs the macOS PingFang (or STHeiti) and Menlo fonts")


@lru_cache(None)
def _faces(path: str) -> dict[tuple[str, str], int]:
    """(family, style) -> index inside a .ttc collection."""
    out = {}
    for i in range(64):
        try:
            fam, sty = ImageFont.truetype(path, 12, index=i).getname()
        except OSError:
            break
        out.setdefault((fam, sty), i)
    return out


def _cjk_index(weight: str) -> int:
    faces = _faces(CJK_PATH)
    style = {"regular": "Regular", "medium": "Medium", "bold": "Semibold"}[weight]
    for fam in ("PingFang HK", "PingFang TC", "PingFang SC"):
        if (fam, style) in faces:
            return faces[(fam, style)]
    return 0


@lru_cache(None)
def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    """PingFang HK: weight is regular, medium or bold. Latin text uses it too."""
    return ImageFont.truetype(CJK_PATH, size, index=_cjk_index(weight))


@lru_cache(None)
def mono(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    faces = _faces(MONO_PATH)
    idx = faces.get(("Menlo", "Bold" if bold else "Regular"), 0)
    return ImageFont.truetype(MONO_PATH, size, index=idx)
