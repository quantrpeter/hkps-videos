# HKPS videos

Cantonese explainer videos for 香港編程學會 (HKPS). One Python script per video; rerun it at any
time to rebuild that video. The renderer in `hkpsvid/` is adapted from `cpptut` in
`cantonese-cpp-video-tutorial` (same voice, cards, logo badge, subtitles and checks), without the
C++ syllabus, Docker runs and coding stage.

| Script | Video |
|---|---|
| `it_technical.py` | IT 團隊：上下級都要識 technical (about 3 min) |

```sh
python3 it_technical.py               # -> out/it_technical.mp4 (narration is cached; reruns are quick)
python3 it_technical.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 it_technical.py --stills      # two PNGs per scene in build/it_technical/stills/ (add --draft to skip TTS)
python3 it_technical.py --redo myth   # regenerate one scene's narration (e.g. after changing its seed)
```

Any `python3` works: the script switches itself to the video venv
(`newblock-server/skills/video/.venv`, or whatever `HKPSVID_PY` points to).

What a run does: narration with OmniVoice cloned from `voices/yue.wav` (not in git, as in the C++ project: copy it from there; one clip per scene, only
changed clips are regenerated), a Whisper check of every clip (`BAD` lines: reword the narration or
give the scene `seed=12`..`15`), scene timing from `[[cue]]` markers, frames drawn with Pillow
(logo badge and burned-in subtitles), 1080p30 H.264 at −16 LUFS, then a full decode check and
contact sheets in `build/<script>/sheet-*.jpg`.

## Writing a new video

Copy `it_technical.py`, change `VIDEO` and the scenes. A scene is an id, its narration (written
the way the subtitles should read, with `[[cue]]` markers) and a card from `hkpsvid/visuals.py`:
`TitleCard`, `BulletCard`, `TileCard`, `ChatCard` (a dialogue in speech bubbles), `CompareCard`
(panels side by side), `TableCard`, `StepsCard`, `TimelineCard`, `FlowCard`, `BarCard`, `EndCard`,
or a plain `Card`. Words the TTS misreads get a spelling in the script's `SAY` dict (`"API": "A P I"`).
