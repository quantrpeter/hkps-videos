# 零 Code PM 講 OOP：滿口 inheritance、polymorphism，但唔知係乜

A Cantonese satire (about 3 min) for 香港編程學會's 「IT 職場講堂」, after `../0codepm just talk/`.
It mocks the 零 Code PM who talks object-oriented programming all day but has every term wrong
(inheritance is a handover when someone resigns, polymorphism is one person doing three jobs).
Scenes: the chat, a 「PM 以為 vs 真正意思」 table for object and the four pillars, OOP in one
13-line Python program with each concept marked, the PM's class design (Email inherits Payment
inherits Order inherits Customer) against is-a / has-a, six harms to the team, a self-test, a fair
word on what a PM needs to know, and a polymorphism challenge (Animal, Dog, Cat).

The archetype is the channel's own observation; there is no survey behind it. The characters and
dialogue are made up; no real person, company or project is named.

```sh
python3 oop_pm.py               # -> out/oop_pm.mp4 (narration is cached; reruns are quick)
python3 oop_pm.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 oop_pm.py --stills      # two PNGs per scene in build/oop_pm/stills/ (add --draft to skip TTS)
python3 oop_pm.py --redo chat   # regenerate one scene's narration (e.g. after changing its seed)
```

The folder is self-contained, like the others: `hkpsvid/` is the same renderer as `../0codepm just talk/`,
with `hkpsLogo.png` and `voices/yue.wav` (not in git: copy it from the C++ project). See the first
video's README for what a run does.
