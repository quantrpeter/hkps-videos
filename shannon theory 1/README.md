# 重新發明 Entropy：壓縮嘅極限（資訊理論・第一集）

A Cantonese explainer (about 9½ min) of Shannon's information and entropy for 香港編程學會, made
from the ideas in 3Blue1Brown's "Reinventing Entropy | Information theory, part 1" (the `.webm` in
this folder, not in git). The narration is original Cantonese written for this video, not a
translation of the original script, and the screens are HKPS cards with their own animations, not
the original's visuals. The title and end cards credit the source video.

What it covers, in order: how few bits text can use; a moon robot whose instructions are ↑½ ↓¼ ←⅛ →⅛;
a 2-bit code against 0/10/110/111 (1.75 bits); decoding and prefix-free codes on the code-space
diagram; "perfect compression looks like random noise"; why squeezing one message costs others
more; bits = −log₂ p; the information of an event; letters of language and the chain rule; Shannon's
n-gram counts, guessing game and 1951 paper; entropy as an area; von Neumann's (probably apocryphal)
naming story; how entropy moves with the distribution; the noiseless coding theorem; English at
about 1 bit per letter. The original's sponsor and career-page segment is left out.

The letter probabilities for INFORMATION and the TH table are illustrative and marked 示意數字 on
screen. The guessing-game sentence is made up.

```sh
python3 entropy_part1.py                # -> out/entropy_part1.mp4 (narration is cached; reruns are quick)
python3 entropy_part1.py --draft        # silent, estimated timing, fast encode: for checking layout and pace
python3 entropy_part1.py --stills       # two PNGs per scene in build/entropy_part1/stills/ (add --draft to skip TTS)
python3 entropy_part1.py --redo robot   # regenerate one scene's narration (e.g. after changing its seed)
```

`entropy_cards.py` holds the animated cards (robot, bit streams, decoder, code-space diagram,
coin-flip tree, −log₂ p graph, pie and bar, letters, entropy area, guessing game) on top of the
shared renderer in `hkpsvid/`, which is the same copy as the other videos. `hkpsLogo.png` and
`voices/yue.wav` (not in git) are as elsewhere.
