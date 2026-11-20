"""Colours for code (Pygments, One Dark palette) and for terminal output (ANSI SGR codes)."""

from __future__ import annotations

import re
from functools import lru_cache

from pygments.lexers import get_lexer_for_filename
from pygments.token import Comment, Keyword, Name, Number, Operator, String

from .style import ED_TEXT, TERM_TEXT


def _colour(tt) -> tuple:
    if tt in Comment.PreprocFile:
        return (152, 195, 121)
    if tt in Comment.Preproc:
        return (198, 120, 221)
    if tt in Comment:
        return (127, 132, 142)
    if tt in Keyword.Type:
        return (229, 192, 123)
    if tt in Keyword.Constant:
        return (209, 154, 102)
    if tt in Keyword:
        return (198, 120, 221)
    if tt in Name.Builtin:
        return (86, 182, 194)
    if tt in Name.Function:
        return (97, 175, 239)
    if tt in String:
        return (152, 195, 121)
    if tt in Number:
        return (209, 154, 102)
    if tt in Operator:
        return (86, 182, 194)
    return ED_TEXT


@lru_cache(maxsize=4096)
def colours(name: str, code: str) -> tuple:
    """One colour per character of `code`, chosen by the file name's language."""
    out = [ED_TEXT] * len(code)
    try:
        lexer = get_lexer_for_filename(name)
    except Exception:
        return tuple(out)
    for i, tt, val in lexer.get_tokens_unprocessed(code):
        c = _colour(tt)
        for k in range(i, min(len(code), i + len(val))):
            out[k] = c
    return tuple(out)


# -- terminal ----------------------------------------------------------------------------------

ANSI = {30: (110, 118, 129), 31: (255, 123, 114), 32: (126, 231, 135), 33: (227, 179, 65),
        34: (121, 192, 255), 35: (210, 168, 255), 36: (86, 212, 221), 37: TERM_TEXT}
_SEQ = re.compile(r"\x1b\[([0-9;]*)([A-Za-z])|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")


@lru_cache(maxsize=4096)
def ansi(text: str) -> tuple:
    """Splits a line with SGR codes into ((text, colour, bold), ...); other escapes are dropped."""
    out, fg, bold, pos = [], TERM_TEXT, False, 0
    for m in _SEQ.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], fg, bold))
        pos = m.end()
        if m.group(2) != "m":
            continue
        codes = [int(c) for c in (m.group(1) or "0").split(";") if c.isdigit()] or [0]
        for c in codes:
            if c == 0:
                fg, bold = TERM_TEXT, False
            elif c == 1:
                bold = True
            elif c == 22:
                bold = False
            elif c == 39:
                fg = TERM_TEXT
            elif c in ANSI:
                fg = ANSI[c]
            elif 90 <= c <= 97:
                fg = ANSI[c - 60]
    if pos < len(text):
        out.append((text[pos:], fg, bold))
    return tuple(s for s in out if s[0])


def visible(text: str) -> str:
    return _SEQ.sub("", text)
