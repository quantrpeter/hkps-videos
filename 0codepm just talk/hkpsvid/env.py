"""Makes `python3 <video>.py` work with any python: re-runs the script under the video venv.

The venv is the one from newblock-server/skills/video (it has OmniVoice, torch, transformers,
Pillow, numpy, soundfile, OpenCC, Pygments). Set HKPSVID_PY to use another interpreter.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

DEFAULT_PY = "/Users/peter/workspace/newblock-server/skills/video/.venv/bin/python"
NEEDED = ("PIL", "numpy", "soundfile", "pygments", "omnivoice", "transformers", "opencc")


def reexec() -> None:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")          # the model weights are already cached
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    missing = [m for m in NEEDED if importlib.util.find_spec(m) is None]
    if not missing:
        return
    py = Path(os.environ.get("HKPSVID_PY", DEFAULT_PY))
    if py.exists() and not os.environ.get("HKPSVID_REEXEC"):
        os.environ["HKPSVID_REEXEC"] = "1"   # never loop
        os.execv(str(py), [str(py), *sys.argv])
    raise SystemExit(f"hkpsvid: this python is missing {', '.join(missing)}. "
                     f"Set HKPSVID_PY to the video venv's python (default {DEFAULT_PY}).")
