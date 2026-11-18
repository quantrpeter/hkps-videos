"""hkpsvid: builds HKPS Cantonese explainer videos from Python scripts.

Adapted from cpptut in cantonese-cpp-video-tutorial, without the C++ syllabus, Docker runs and
coding stage. A video script describes itself with `Video`, lists its scenes (narration + what is
on screen) and calls `build`. Shared here: narration (OmniVoice + Whisper check), the logo on every
frame, subtitles, cards and the MP4 assembly.
"""

from . import env

env.reexec()  # first: switches to the video venv before anything imports Pillow, numpy or torch

from .build import Scene, Video, build, options  # noqa: E402
from .style import AMBER, BLUE, GREEN, MUTED, NAVY, PURPLE, RED, TEAL  # noqa: E402
from .text import about, zh_int, zh_num, zh_seconds  # noqa: E402
from .visuals import (Bar, BarCard, BulletCard, Card, ChatCard, Column, CompareCard, EndCard, Event,  # noqa: E402
                      FlowCard, Msg, Node, Row, Step, StepsCard, TableCard, Tile, TileCard, TimelineCard,
                      TitleCard)

__all__ = [
    "Scene", "Video", "build", "options",
    "AMBER", "BLUE", "GREEN", "MUTED", "NAVY", "PURPLE", "RED", "TEAL",
    "about", "zh_int", "zh_num", "zh_seconds",
    "Bar", "BarCard", "BulletCard", "Card", "ChatCard", "Column", "CompareCard", "EndCard", "Event",
    "FlowCard", "Msg", "Node", "Row", "Step", "StepsCard", "TableCard", "Tile", "TileCard", "TimelineCard",
    "TitleCard",
]
