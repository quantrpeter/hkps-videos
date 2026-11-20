# Arithmetic coding：將預測變成壓縮（資訊理論・第三集）

A Cantonese explainer (about 9 min) of arithmetic coding and "compression is intelligence" for
香港編程學會, the last of the trilogy after `../shannon theory 1/` and `../shannon theory 2/`. It is
made from the ideas in 3Blue1Brown's "This algorithm changed how I think about compression |
Information theory, part 3" (the `.webm` in this folder, not in git). The narration is original
Cantonese written for this video, not a translation, and the screens are HKPS cards with their own
animations. The title and end cards credit the source video.

What it covers, in order: the Hutter Prize; sender and receiver; Shannon's −log₂ p and why it looks
absurd for the US Constitution's preamble (ASCII 2,616 bits, a Huffman code built for that very
text 1,406 bits); context and language models; a shared model on both sides; probabilities as a
number line; zooming letter by letter into "math"; the chain rule; decoding by following x; random
numbers decode to English-looking strings; binary fractions; the shortest k-bit number inside the
target (13 bits for "math"); "mathematics" in 18 bits; k ≥ −log₂ p; luck and averages; the model's
probability, not the true one; pre-training as building a compressor; small vs large models and the
preamble result; Elias, Rissanen and Pasco; ANS; then three ways compression touches intelligence
(prediction = compression, small models, learning fast) and the trilogy's conclusion. The original's
sponsor segment is left out.

**The demo model is real.** `arith_model.py` is a tiny character-level predictor: the next-letter
probabilities are counted from the system word list (`/usr/share/dict/words`, Webster's 2nd, about
236,000 words) with light smoothing. Every interval, probability, bit string and random sample on
screen is computed from it, so they are true for this model (not for a large language model). The
NanoGPT (254 bits), Qwen (under 1 bit per letter) and preamble-with-Qwen (about 45 bits) figures are
quoted from the original video and marked 數字來自原片.

```sh
python3 arithmetic_part3.py              # -> out/arithmetic_part3.mp4 (narration is cached; reruns are quick)
python3 arithmetic_part3.py --draft      # silent, estimated timing, fast encode: for checking layout and pace
python3 arithmetic_part3.py --stills     # two PNGs per scene in build/arithmetic_part3/stills/
python3 arithmetic_part3.py --redo zoom  # regenerate one scene's narration
python3 arith_model.py                   # print the model's numbers for math / mathematics and samples
```

`arith_cards.py` adds the part 3 cards (the zooming interval stack, binary halving, the k-bit target
search) on top of `entropy_cards.py` and `cross_cards.py` from parts 1 and 2.
