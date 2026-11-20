"""A tiny character-level "language model" for the arithmetic-coding demos: it predicts the next
letter of an English word by counting, in the system word list (/usr/share/dict/words, Webster's
2nd), which letters follow the prefix so far. 26 lowercase letters, add-α smoothing, no
end-of-word symbol (the message length is sent separately, as in the video).

Everything the video shows about intervals, bits and random samples is computed from this model,
so the numbers on screen are real for this model (not for a large language model).
"""

from __future__ import annotations

import bisect
import math
import random
from functools import lru_cache
from pathlib import Path

ALPHA = "abcdefghijklmnopqrstuvwxyz"
SMOOTH = 0.02
WORDS_PATH = Path("/usr/share/dict/words")


@lru_cache(None)
def _words() -> list[str]:
    ws = {w.strip().lower() for w in WORDS_PATH.read_text().split()}
    return sorted(w for w in ws if w.isalpha() and w.isascii())


@lru_cache(None)
def dist(prefix: str) -> tuple[float, ...]:
    """P(next letter | prefix) over a..z."""
    ws = _words()
    lo = bisect.bisect_left(ws, prefix)
    hi = bisect.bisect_left(ws, prefix + "{")          # '{' sorts after 'z'
    counts = dict.fromkeys(ALPHA, SMOOTH)
    n = len(prefix)
    for w in ws[lo:hi]:
        if len(w) > n:
            counts[w[n]] += 1
    total = sum(counts.values())
    return tuple(counts[c] / total for c in ALPHA)


def p_next(prefix: str, ch: str) -> float:
    return dist(prefix)[ALPHA.index(ch)]


def interval(text: str) -> list[tuple[float, float]]:
    """The nested intervals [lo, hi) after each letter (first entry is the whole line)."""
    lo, hi = 0.0, 1.0
    out = [(lo, hi)]
    for i, ch in enumerate(text):
        d = dist(text[:i])
        k = ALPHA.index(ch)
        w = hi - lo
        lo, hi = lo + w * sum(d[:k]), lo + w * sum(d[:k + 1])
        out.append((lo, hi))
    return out


def prob(text: str) -> float:
    lo, hi = interval(text)[-1]
    return hi - lo


def shortest_bits(lo: float, hi: float) -> str:
    """The fewest bits b1..bk such that the binary fraction .b1..bk lies in [lo, hi)."""
    if lo <= 0:
        return ""
    for k in range(1, 60):
        m = math.ceil(lo * 2 ** k)
        if m / 2 ** k < hi:
            return format(m, f"0{k}b")
    raise ValueError("interval too small")


def decode(x: float, n: int) -> str:
    out = ""
    lo, hi = 0.0, 1.0
    for _ in range(n):
        d = dist(out)
        w = hi - lo
        acc = lo
        for c, pc in zip(ALPHA, d):
            if x < acc + w * pc:
                out += c
                lo, hi = acc, acc + w * pc
                break
            acc += w * pc
        else:
            out += "z"
    return out


def samples(n: int = 6, length: int = 7, seed: int = 5) -> list[tuple[float, str]]:
    rng = random.Random(seed)
    return [(x, decode(x, length)) for x in (rng.random() for _ in range(n))]


if __name__ == "__main__":
    for word in ("math", "mathematics"):
        lo, hi = interval(word)[-1]
        b = shortest_bits(lo, hi)
        print(word, f"[{lo:.10f}, {hi:.10f})", f"p={hi - lo:.3g}", f"info={-math.log2(hi - lo):.2f}",
              f"bits={len(b)} .{b}", f"{len(b) / len(word):.2f} bits/char")
        for i in range(len(word)):
            print("   ", repr(word[:i]), word[i], f"{p_next(word[:i], word[i]):.3f}")
    print(samples())
    d = dist("")
    print("first letters:", sorted(zip(d, ALPHA), reverse=True)[:6], "q", d[16], "x", d[23])
    print("after m:", sorted(zip(dist("m"), ALPHA), reverse=True)[:6])
