"""Narration text: what the TTS says, where the [[cues]] fall, how subtitles split, Chinese numerals.

Scripts are written the way the subtitles should read (「C++」, 「IT」). `spoken()` swaps in
spellings the TTS pronounces well (「C plus plus」, 「I T」); a video adds its own with `build(say=…)`. Cue markers like `[[run]]` mark the moment an
action should happen; they are stripped before TTS and subtitles.
"""

from __future__ import annotations

import re

# Display form -> what the TTS is given. Longest keys are replaced first; keys that start or end
# with a letter only match whole words. Check new entries with the Whisper report.
SAY = {
    "C++": "C plus plus",
    "HKOI": "H K O I",
    "IT": "I T",
    "VS Code": "V S Code",
    "Ctrl": "control",
    "Cmd": "command",
}

CUE = re.compile(r"\[\[([\w-]+)\]\]")
CJK = re.compile(r"[㐀-鿿豈-﫿]")


def strip_cues(text: str) -> str:
    return CUE.sub("", text)


def spoken(text: str, say: dict[str, str] | None = None) -> str:
    say = {**SAY, **(say or {})}
    s = strip_cues(text)
    for k in sorted(say, key=len, reverse=True):
        pat = re.escape(k)
        if k[0].isalnum():
            pat = r"(?<![A-Za-z0-9_])" + pat
        if k[-1].isalnum():
            pat = pat + r"(?![A-Za-z0-9_])"
        s = re.sub(pat, lambda m, v=say[k]: f" {v} ", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r" ?([，。！？、；：「」]) ?", r"\1", s)
    return s.strip()


def weight(s: str) -> float:
    """Rough speaking time of spoken text, in Chinese-character units (pauses included)."""
    w = 0.0
    for ch in s:
        if CJK.match(ch):
            w += 1
        elif ch.isascii() and ch.isalpha():
            w += 0.35
        elif ch.isdigit():
            w += 0.6
        elif ch in "，、；：":
            w += 1.0
        elif ch in "。！？…":
            w += 1.5
    return w


def cue_shares(text: str, say: dict[str, str] | None = None) -> dict[str, float]:
    """Each cue's position as a share (0..1) of the spoken length."""
    parts = CUE.split(text)  # text, name, text, name, ...
    total = weight(spoken(text, say)) or 1
    out, acc = {}, 0.0
    for i, p in enumerate(parts):
        if i % 2:
            out[p] = acc / total
        else:
            acc += weight(spoken(p, say))
    return out


def _display_len(s: str) -> float:
    return sum(1 if CJK.match(c) else 0.55 for c in s if not c.isspace())


def subtitle_chunks(text: str, say: dict[str, str] | None = None,
                    max_len: float = 20) -> list[tuple[float, float, str]]:
    """Splits narration into subtitle lines: (start share, end share, display text)."""
    plain = strip_cues(text).strip()
    sentences = [s for s in re.split(r"(?<=[。！？])", plain) if s.strip()]
    chunks: list[str] = []
    for s in sentences:
        if _display_len(s) <= max_len:
            chunks.append(s)
            continue
        parts = [p for p in re.split(r"(?<=[，；：])", s) if p]
        cur = ""
        for p in parts:
            if cur and _display_len(cur + p) > max_len:
                chunks.append(cur)
                cur = p
            else:
                cur += p
        if cur:
            chunks.append(cur)
    total = sum(weight(spoken(c, say)) for c in chunks) or 1
    out, acc = [], 0.0
    for c in chunks:
        w = weight(spoken(c, say))
        disp = re.sub(r"[，、；：。]+$", "", c.strip())
        disp = re.sub(r"[，、；：]", "　", disp).replace("。", "　")
        out.append((acc / total, (acc + w) / total, disp.strip()))
        acc += w
    return out


DIGITS = "零一二三四五六七八九"


def _four(n: int) -> str:
    s, zero = "", False
    for unit, name in ((1000, "千"), (100, "百"), (10, "十"), (1, "")):
        d = n // unit % 10
        if d == 0:
            zero = bool(s)
            continue
        if zero:
            s += "零"
            zero = False
        s += DIGITS[d] + name
    return s


def zh_int(n: int) -> str:
    """Cantonese reading of an integer: 17984 -> 一萬七千九百八十四, 12 -> 十二."""
    if n == 0:
        return "零"
    if n < 0:
        return "負" + zh_int(-n)
    high, low = divmod(n, 10000)
    if high:
        s = zh_int(high) + "萬"
        if low:
            s += ("零" if low < 1000 else "") + _four(low)
    else:
        s = _four(low)
    if 10 <= n < 20:
        s = s[1:]  # 一十二 -> 十二
    return s


def zh_num(x: float, places: int = 0) -> str:
    """zh_num(0.031, 2) -> 零點零三, zh_num(1.24, 1) -> 一點二."""
    if places == 0:
        return zh_int(round(x))
    whole, frac = f"{x:.{places}f}".split(".")
    frac = frac.rstrip("0")
    s = zh_int(int(whole))
    return s + ("點" + "".join(DIGITS[int(c)] for c in frac) if frac else "")


def zh_seconds(t: float) -> str:
    """How a timing reads aloud: 零點零三秒, 一點二秒, 唔使零點零一秒."""
    if t < 0.01:
        return "唔使零點零一秒"
    s = zh_num(t, 2 if t < 1 else 1)
    if s.startswith("二") and not s.startswith("二十"):
        s = "兩" + s[1:]  # 兩秒, 兩點五秒 (not 二秒)
    return s + "秒"


def about(x: float) -> int:
    """Rounds a ratio for saying 「大約 N 倍」: 7 stays 7, 43 -> 45, 137 -> 140."""
    if x < 10:
        return max(1, round(x))
    if x < 100:
        return int(round(x / 5) * 5)
    return int(round(x / 10) * 10)
