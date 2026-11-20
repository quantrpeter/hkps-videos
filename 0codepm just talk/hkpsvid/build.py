"""Builds one video: narration -> scene timing -> frames (logo + subtitles) -> out/<slug>.mp4.

Each scene waits for its narration (plus a short gap), and for its on-screen actions if those run
longer. Actions are cued to points in the narration with [[cue]] markers, so a clip that comes out
longer or shorter just shifts them; nothing needs re-editing.
"""

from __future__ import annotations

import argparse
import bisect
import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw

from . import voice
from . import draw as D
from .style import BADGE, BADGE_MARGIN, FPS, H, ROOT, W, WHITE, font
from .text import cue_shares, spoken, subtitle_chunks, weight
from .visuals import Timing, Visual

LEAD, FIRST_LEAD, GAP, HOLD, END_HOLD = 0.25, 0.8, 0.6, 0.5, 1.5
EST_RATE = 6.0  # spoken weight per second (measured on video 1), for --draft timings before any audio exists
SR = voice.SR


@dataclass(frozen=True)
class Video:
    slug: str                      # file name: out/<slug>.mp4, build/<slug>/
    title: str                     # on the title card and in the top-left tag
    series: str = "香港編程學會"     # the tag's first half


@dataclass
class Scene:
    id: str
    text: str           # narration as the subtitles show it, with [[cue]] markers
    visual: Visual
    seed: int = 11      # TTS seed; try 12-15 if Whisper flags the clip


def options(video: Video, argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog=f"{video.slug}.py", description=f"Builds out/{video.slug}.mp4 ({video.title}).")
    ap.add_argument("--draft", action="store_true", help=f"no TTS: estimated timing, silent, fast encode -> out/{video.slug}-draft.mp4")
    ap.add_argument("--timing", action="store_true", help="with --draft: print the estimated scene timings and stop")
    ap.add_argument("--stills", action="store_true", help=f"only write two PNG frames per scene to build/{video.slug}/stills/")
    ap.add_argument("--audio-only", action="store_true", help="make and check the narration, then stop")
    ap.add_argument("--no-asr", action="store_true", help="skip the Whisper check")
    ap.add_argument("--redo", default="", help="scene ids (comma-separated) whose narration to regenerate")
    return ap.parse_args(argv)


@lru_cache(None)
def _subtitle(text: str) -> Image.Image:
    t = D.text_img(text, font(44, "medium"), WHITE, max_w=1500, align="center", line_h=1.32)
    w, h = t.width + 72, t.height + 20
    im = Image.new("RGBA", (w, h))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), 20, fill=(10, 18, 34, 210))
    im.alpha_composite(t, (36, 8))
    return im


def _click(kind: str) -> np.ndarray:
    rng = np.random.default_rng(7 if kind == "key" else 8)
    if kind == "pop":
        n = int(0.07 * SR)
        k = np.arange(n) / n
        phase = np.cumsum(2 * np.pi * (900 - 650 * k) / SR)
        return (np.sin(phase) * np.exp(-k * 6) * np.minimum(1, np.arange(n) / 48) * 0.16).astype(np.float32)
    n = int((0.018 if kind == "enter" else 0.012) * SR)
    noise = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    noise = np.diff(noise, prepend=0)
    return (noise * (0.07 if kind == "enter" else 0.045)).astype(np.float32)


def build(video: Video, scenes: list[Scene], opts: argparse.Namespace, say: dict[str, str] | None = None) -> Path | None:
    ids = [s.id for s in scenes]
    if len(set(ids)) != len(ids):
        raise SystemExit("hkpsvid: scene ids must be unique")
    work = ROOT / "build" / video.slug
    audio_dir = work / "audio"
    work.mkdir(parents=True, exist_ok=True)
    tag = f"{video.series} · {video.title}"
    for s in scenes:
        s.visual.tag = tag

    items = [(s.id, spoken(s.text, say), s.seed) for s in scenes]
    if opts.draft:
        clip = {i: weight(t) / EST_RATE + 0.3 for i, t, _ in items}
    else:
        clip = voice.clips(items, audio_dir, redo={x for x in opts.redo.split(",") if x})
        if not opts.no_asr:
            bad = voice.check(items, audio_dir)
            if bad:
                print(f"[asr] {len(bad)} clip(s) may be misread: {', '.join(bad)}. Listen to them; reword the "
                      "narration or set seed=12..15 on the scene, then rerun.", flush=True)
        if opts.audio_only:
            return None

    # Timing ---------------------------------------------------------------------------------
    starts, timings, durs = [], [], []
    t = 0.0
    print(f"\n{video.slug}: {video.title}")
    for k, s in enumerate(scenes):
        lead = FIRST_LEAD if k == 0 else LEAD
        tm = Timing(lead, clip[s.id], cue_shares(s.text, say))
        end = s.visual.prepare(tm)
        dur = max(lead + clip[s.id] + GAP, end + HOLD) + (END_HOLD if k == len(scenes) - 1 else 0)
        over = end - (lead + clip[s.id] * (0.9 if opts.draft else 1))   # real speech runs up to ~15% under the estimate
        note = f"  ! actions outlast the narration by {over:.1f}s" if over > 2 else ""
        print(f"  {s.id:<14} speech {clip[s.id]:5.1f}s  scene {dur:5.1f}s{note}")
        starts.append(t)
        timings.append(tm)
        durs.append(dur)
        t += dur
    total = t
    print(f"  total {total // 60:.0f}:{total % 60:04.1f}\n", flush=True)
    if opts.timing:
        return None

    subs: list[tuple[float, float, str]] = []
    for s, st, tm in zip(scenes, starts, timings):
        chunks = subtitle_chunks(s.text, say)
        for j, (a, b, txt) in enumerate(chunks):
            t0 = st + tm.lead + a * tm.clip
            t1 = st + tm.lead + (chunks[j + 1][0] if j + 1 < len(chunks) else b) * tm.clip + (0.35 if j + 1 == len(chunks) else 0)
            subs.append((t0, t1, txt))
    sub_starts = [x[0] for x in subs]
    (work / "timeline.json").write_text(json.dumps({
        "total": total,
        "scenes": [{"id": s.id, "start": st, "dur": d, "speech": [st + tm.lead, st + tm.speech_end],
                    "cues": {k: st + v for k, v in tm.cues.items()}} for s, st, d, tm in zip(scenes, starts, durs, timings)],
        "subtitles": subs}, ensure_ascii=False, indent=1))

    badge = D.logo_badge()

    def compose(gt: float):
        si = max(0, bisect.bisect_right(starts, gt) - 1)
        lt = gt - starts[si]
        v = scenes[si].visual
        j = bisect.bisect_right(sub_starts, gt) - 1
        sub = j if j >= 0 and gt < subs[j][1] else -1
        key = (si, v.key(lt), sub)

        def image() -> Image.Image:
            im = v.render(lt)
            if not v.big_logo:
                D.paste(im, badge, W - BADGE_MARGIN - BADGE, BADGE_MARGIN)
            if sub >= 0:
                si_ = _subtitle(subs[sub][2])
                im.alpha_composite(si_, ((W - si_.width) // 2, H - 26 - si_.height))
            return im.convert("RGB")

        return key, image

    if opts.stills:
        d = work / "stills"
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        for k, (s, st, du) in enumerate(zip(scenes, starts, durs)):
            for tag_, gt in (("a", st + du * 0.45), ("b", st + du - 0.12)):
                compose(gt)[1]().save(d / f"{k + 1:02d}-{s.id}-{tag_}.png")
        print(f"stills -> {d}")
        return d

    # Audio ----------------------------------------------------------------------------------
    pcm = np.zeros(int((total + 1) * SR), np.float32)
    if not opts.draft:
        for s, st, tm in zip(scenes, starts, timings):
            w, _ = sf.read(str(audio_dir / f"{s.id}.wav"), dtype="float32")
            i0 = int((st + tm.lead) * SR)
            pcm[i0: i0 + len(w)] += w[: len(pcm) - i0]
    for s, st in zip(scenes, starts):
        for at, kind in s.visual.sounds():
            c = _click(kind)
            i0 = int((st + at) * SR)
            if 0 <= i0 < len(pcm) - len(c):
                pcm[i0: i0 + len(c)] += c
    mix = work / "mix.wav"
    sf.write(str(mix), np.clip(pcm, -1, 1), SR)

    # Video ----------------------------------------------------------------------------------
    out_dir = ROOT / "out"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / (f"{video.slug}-draft.mp4" if opts.draft else f"{video.slug}.mp4")
    afilter = "anull" if opts.draft else "loudnorm=I=-16:TP=-1.5:LRA=11"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(mix), "-filter_complex",
           f"[0:v]format=yuv420p,fade=t=in:st=0:d=0.5,fade=t=out:st={total - 0.8:.2f}:d=0.8[v];"
           f"[1:a]{afilter},aresample=48000,afade=t=out:st={total - 1:.2f}:d=1[a]",
           "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast" if opts.draft else "medium",
           "-crf", "23" if opts.draft else "18", "-c:a", "aac", "-b:a", "160k", "-ac", "2",
           "-movflags", "+faststart", "-t", f"{total:.3f}", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = int(round(total * FPS))
    last_key, last = None, b""
    t0 = time.time()
    try:
        for fi in range(frames):
            key, image = compose(fi / FPS)
            if key != last_key:
                last, last_key = image().tobytes(), key
            proc.stdin.write(last)
            if fi % (FPS * 30) == 0:
                print(f"[render] {fi / FPS:5.0f}s / {total:.0f}s", flush=True)
    finally:
        proc.stdin.close()
        rc = proc.wait()
    if rc:
        raise SystemExit(f"ffmpeg failed ({rc})")
    print(f"[render] done in {time.time() - t0:.0f}s")

    # Checks ---------------------------------------------------------------------------------
    err = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"], capture_output=True, text=True).stderr.strip()
    for old in work.glob("sheet-*.jpg"):
        old.unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-vf", "fps=1/6,scale=480:-1,tile=4x4",
                    str(work / "sheet-%d.jpg")], check=False)
    print(f"\nwrote {out}  ({total // 60:.0f}:{total % 60:04.1f})")
    print("decode check: " + ("ok" if not err else f"{len(err.splitlines())} error line(s)\n{err[:800]}"))
    print(f"contact sheets: {work}/sheet-*.jpg")
    if err:
        sys.exit(1)
    return out
