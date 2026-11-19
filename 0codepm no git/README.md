# 零 Git Manager：IT Manager 唔識 Git 有幾禍害

A Cantonese satire (about 2 min 50 s) for 香港編程學會's 「IT 職場講堂」, the follow-up to
`../0codepm/` (零 Code PM). It mocks the IT manager who never learned Git, so the team passes code
around as zip files, email and USB sticks: a Desktop of `project_final_最終版_真係最後.zip`, a chat,
what Git is, six harms, a Friday-night production story, the five commands a manager needs
(`clone`, `log`, `diff`, `blame`, `revert`), a self-test and a fair word on how much a manager needs to know.

The claim that most Hong Kong IT managers can't use Git is the channel's own observation, and the
narration says so (「喺我哋見過嘅香港 IT 公司入面」); there is no survey behind it. The characters,
dialogue and the Friday-night story are made up; no real person, company or project is named.

```sh
python3 zero_git_manager.py               # -> out/zero_git_manager.mp4 (narration is cached; reruns are quick)
python3 zero_git_manager.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 zero_git_manager.py --stills      # two PNGs per scene in build/zero_git_manager/stills/ (add --draft to skip TTS)
python3 zero_git_manager.py --redo chat   # regenerate one scene's narration (e.g. after changing its seed)
```

The folder is self-contained, like the first two: `hkpsvid/` is the same renderer as `../0codepm/`,
with `hkpsLogo.png` and `voices/yue.wav` (not in git: copy it from the C++ project). See the first
video's README for what a run does.
