"""Narration: OmniVoice TTS cloned from voices/yue.wav, then a Whisper check of every clip.

Same settings as the SemiBlock series (skills/videoTutorial.md): CPU only (OmniVoice segfaults on
MPS), seed 11, speed 0.95, silence trimmed, 24 kHz. A clip is only regenerated when its spoken
text or seed changed; `<id>.txt` next to the wav records what it says.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from .style import ROOT

SR = 24000
REF = ROOT / "voices" / "yue.wav"
REF_TEXT = "大家好！準備好未呀？今日我哋一齊整一啲好好玩嘅嘢。"
MODEL = "k2-fsa/OmniVoice"
WHISPER = "openai/whisper-large-v3-turbo"


def _trim(w: np.ndarray) -> np.ndarray:
    idx = np.where(np.abs(w) > 0.01)[0]
    if not len(idx):
        return w
    return w[max(0, idx[0] - int(0.05 * SR)): idx[-1] + int(0.15 * SR)]


def _stamp(text: str, seed: int) -> str:
    return f"seed {seed}\n{text}"


def clips(items: list[tuple[str, str, int]], out: Path, redo: set[str] = frozenset()) -> dict[str, float]:
    """items: (scene id, spoken text, seed). Writes out/<id>.wav; returns id -> seconds."""
    out.mkdir(parents=True, exist_ok=True)
    need = [(i, t, s) for i, t, s in items
            if i in redo or not (out / f"{i}.wav").exists() or not (out / f"{i}.txt").exists()
            or (out / f"{i}.txt").read_text() != _stamp(t, s)]
    if need:
        import torch
        from omnivoice import OmniVoice

        print(f"[tts] {len(need)} of {len(items)} clips to make; loading {MODEL} on CPU…", flush=True)
        model = OmniVoice.from_pretrained(MODEL, device_map="cpu", dtype=torch.float32)
        for k, (i, text, seed) in enumerate(need, 1):
            t0 = time.time()
            torch.manual_seed(seed)
            audio = model.generate(text=text, language="yue", ref_audio=str(REF), ref_text=REF_TEXT,
                                   speed=0.95, num_step=32)
            w = _trim(np.asarray(audio[0] if isinstance(audio, list) else audio, dtype=np.float32))
            sf.write(out / f"{i}.wav", w, SR)
            (out / f"{i}.txt").write_text(_stamp(text, seed))
            (out / f"{i}.asr.json").unlink(missing_ok=True)
            print(f"[tts] {k}/{len(need)} {i}: {len(w) / SR:.1f}s audio in {time.time() - t0:.0f}s", flush=True)
        del model
    return {i: sf.info(str(out / f"{i}.wav")).duration for i, _, _ in items}


# -- Whisper check (scoring as in skills/video/threejs/asr.py) -------------------------------------

_COLLOQUIAL = "嘅喺哋咗嚟嘢啲咁佢係唔冇乜嗰呢啦喇㗎呀吓撳郁掂攞擘度咩嘩噹啱邊晒睇揀整佢哋"
_NUM = set("零一二三四五六七八九十百千萬")


def _letters(s: str) -> str:
    """'h k o i' -> 'hkoi', so spelled-out acronyms match either way."""
    return re.sub(r"\b(?:[a-z] )+[a-z]\b", lambda m: m.group(0).replace(" ", ""), s)


def score(want: str, got: str, t2s) -> float:
    want = _letters(t2s.convert(want).lower())
    got = t2s.convert(got).lower()
    got = got.replace("c++", " c plus plus ").replace("g++", " g plus plus ").replace("c#", " c sharp ")
    got = _letters(got.replace("加加", " plus plus "))
    colloquial = set(t2s.convert(_COLLOQUIAL))
    en_w = re.findall(r"[a-z]+", want)
    en_g = set(re.findall(r"[a-z]+", got))
    zh_w = [c for c in re.findall(r"[一-鿿]", want) if c not in colloquial and c not in _NUM]
    zh_g = set(re.findall(r"[一-鿿]", got))
    hits = sum(c in zh_g for c in zh_w) + sum(w in en_g for w in en_w)
    return hits / max(1, len(zh_w) + len(en_w))


def check(items: list[tuple[str, str, int]], out: Path, threshold: float = 0.6) -> list[str]:
    """Transcribes every clip with Whisper (cached) and prints the ones that may be misread."""
    todo = []
    for i, text, seed in items:
        c = out / f"{i}.asr.json"
        if c.exists() and json.loads(c.read_text()).get("stamp") == _stamp(text, seed):
            continue
        todo.append((i, text, seed))
    if todo:
        from opencc import OpenCC
        from transformers import pipeline

        dev = os.environ.get("ASR_DEVICE") or ("mps" if sys.platform == "darwin" else "cpu")
        print(f"[asr] checking {len(todo)} clip(s) with Whisper on {dev}…", flush=True)
        asr = pipeline("automatic-speech-recognition", model=WHISPER, device=dev)
        t2s = OpenCC("t2s")
        for i, text, seed in todo:
            w, sr = sf.read(str(out / f"{i}.wav"), dtype="float32")
            got = asr({"raw": w, "sampling_rate": sr}, return_timestamps=True,
                      generate_kwargs={"language": "yue", "no_repeat_ngram_size": 3, "num_beams": 3})["text"].strip()
            (out / f"{i}.asr.json").write_text(json.dumps(
                {"stamp": _stamp(text, seed), "got": got, "score": score(text, got, t2s)}, ensure_ascii=False))
    bad = []
    for i, text, seed in items:
        r = json.loads((out / f"{i}.asr.json").read_text())
        ok = r["score"] >= threshold
        if not ok:
            bad.append(i)
        print(f"[asr] {'ok ' if ok else 'BAD'} {i:<12} {r['score']:.2f}" + ("" if ok else f"\n      want: {text}\n      got:  {r['got']}"))
    return bad
