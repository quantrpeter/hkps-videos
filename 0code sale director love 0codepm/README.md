# 點解零 Code Sales Director 愛請零 Code PM

A Cantonese satire (about 2 min 50 s) for 香港編程學會's 「IT 職場講堂」, after `../0codepm oop/`.
It asks why the 零 Code PM keeps getting hired, and points at the non-technical Sales Director
behind them. Scenes: an interview (the technical PM says three months, the 零 Code PM says no
problem), six reasons the Director prefers the 零 Code PM, what a non-technical interviewer can and
can't judge, the PM's "strengths" as the Director sees them, how one deal turns into a disaster
(Sales gets the commission, the programmers get the mess), a self-test, a fair word, and a
challenge that calls back to the first 零 Code PM video's for-loop question.

The archetype is the channel's own observation; there is no survey behind it, and the narration
says not every Sales Director is like this. The characters and dialogue are made up; no real
person, company or project is named.

```sh
python3 sales_loves_pm.py               # -> out/sales_loves_pm.mp4 (narration is cached; reruns are quick)
python3 sales_loves_pm.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 sales_loves_pm.py --stills      # two PNGs per scene in build/sales_loves_pm/stills/ (add --draft to skip TTS)
python3 sales_loves_pm.py --redo chat   # regenerate one scene's narration (e.g. after changing its seed)
```

The folder is self-contained, like the others: `hkpsvid/` is the same renderer as `../0codepm oop/`,
with `hkpsLogo.png` and `voices/yue.wav` (not in git: copy it from the C++ project). See the first
video's README for what a run does.
