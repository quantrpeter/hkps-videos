# Cross-entropy 係乜？（資訊理論・第二集）

A Cantonese explainer (about 8 min) of cross-entropy for 香港編程學會, following
`../shannon theory 1/`. It is made from the ideas in 3Blue1Brown's "But what is cross-entropy? |
Information theory, part 2" (the `.webm` in this folder, not in git). The narration is original
Cantonese written for this video, not a translation, and the screens are HKPS cards with their own
animations, not the original's visuals. The title and end cards credit the source video.

What it covers, in order: the 2002 "Language Trees and Zipping" gzip trick; the robot's new plan
(↑⅛ ↓⅛ ←¼ →½) under the old code, 2.625 bits; the formula Σ p·(−log₂ q) and its area (widths p,
heights −log₂ q); two-outcome examples (1 bit, then 1.74 bits: not symmetric); the curve over q with
its minimum at q = p, whose path traces H(p); gzip as a rough cross-entropy; language models, loss
and gradient descent; loss as the average surprise per token; why the loss has to be a log
("My name is ___" and the Lagrange argument); one-hot targets; distillation and a chess analogy;
the bridge back to compression (part 3); KL divergence (0.875 bits for the robot) and three puzzles.
The original's sponsor and career-page segment is left out.

The per-token probabilities, the next-token bars, the language pairs in the gzip picture and the
big model's distribution in the distillation picture are illustrative (marked 示意數字 where they
are numbers).

```sh
python3 cross_entropy_part2.py              # -> out/cross_entropy_part2.mp4 (narration is cached; reruns are quick)
python3 cross_entropy_part2.py --draft      # silent, estimated timing, fast encode: for checking layout and pace
python3 cross_entropy_part2.py --stills     # two PNGs per scene in build/cross_entropy_part2/stills/
python3 cross_entropy_part2.py --redo zip   # regenerate one scene's narration
```

`entropy_cards.py` is part 1's card module (this copy adds `False` as "never" for a cue, so optional
overlays stay off). `cross_cards.py` adds the part 2 cards: the gzip comparison, the cross-entropy
area with dashed KL outlines, the two-outcome curve with its H(p) trace, the language model box,
the gradient-descent hill, per-token loss, loss-shape graphs, "My name is ___" and distillation targets.
