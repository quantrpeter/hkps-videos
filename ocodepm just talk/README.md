# 識講唔識做：IT 出身嘅零 Code PM 有幾禍害

A Cantonese satire (about 3 min 20 s) for 香港編程學會's 「IT 職場講堂」, the follow-up to
`../0codepm/` (零 Code PM) and `../0codepm no git/` (零 Git Manager). It mocks the PM who studied IT
at university and talks in cloud-native, microservice and AI-driven, but can't write a five-line
login check: a jargon chat, the PM's "code" next to the real one, a jargon-to-reality dictionary,
why this PM is worse than one who never studied IT, six harms to the team, a project story, a
self-test and a fair word on what a PM needs to know.

The archetype is the channel's own observation; there is no survey behind it. The characters,
dialogue and the project story are made up (the narration calls the story 「完全虛構」); no real
person, company or project is named.

```sh
python3 talk_only_pm.py               # -> out/talk_only_pm.mp4 (narration is cached; reruns are quick)
python3 talk_only_pm.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 talk_only_pm.py --stills      # two PNGs per scene in build/talk_only_pm/stills/ (add --draft to skip TTS)
python3 talk_only_pm.py --redo chat   # regenerate one scene's narration (e.g. after changing its seed)
```

The folder is self-contained, like the others: `hkpsvid/` is the same renderer as `../0codepm no git/`,
with `hkpsLogo.png` and `voices/yue.wav` (not in git: copy it from the C++ project). See the first
video's README for what a run does.
