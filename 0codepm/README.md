# 零 Code PM 點樣為禍香港

A Cantonese satire (about 2.5 min) for 香港編程學會's 「IT 職場講堂」, the follow-up to
`../why need to know technical/`. It mocks the 「零 Code PM」 (Hong Kong IT slang for a software
project manager with no software-development knowledge) through the for loop: the PM who thinks
emailing 1,000 customers means writing 1,000 lines. Then it teaches the for loop in 30 seconds.

Facts about the term (its meaning, its 2010s Hong Kong forum origin, the harms and causes) come
from the Wikipedia article 「零Code PM」 (https://zh.wikipedia.org/zh-tw/零Code_PM) and are credited on
screen. The characters and dialogue are made up; no real person, company or project is named.

```sh
python3 zero_code_pm.py               # -> out/zero_code_pm.mp4 (narration is cached; reruns are quick)
python3 zero_code_pm.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 zero_code_pm.py --stills      # two PNGs per scene in build/zero_code_pm/stills/ (add --draft to skip TTS)
python3 zero_code_pm.py --redo chat   # regenerate one scene's narration (e.g. after changing its seed)
```

The folder is self-contained, like the first video's: `hkpsvid/` is the same renderer (this copy
also exports the code cards `CodeCompareCard`, `AnatomyCard` and `CodeCard`), with `hkpsLogo.png` and
`voices/yue.wav` (not in git: copy it from the C++ project). See the first video's README for what a run does.
