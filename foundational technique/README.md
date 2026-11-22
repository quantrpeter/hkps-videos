# 浪潮會過，基礎留低：點解基礎科技咁重要？

A Cantonese video (about 3¾ min) for 香港編程學會 on why fundamentals matter, to a programmer and to a
society. Over thirty years Hong Kong rushed after wave after wave (Java, Flash, .NET, mobile apps,
now AI); people who only learned the tool of the day were left with little when the wave passed,
while the foundations (maths, data structures and algorithms, computer architecture, operating
systems, networks, compilers) kept their value. The Hong Kong observations are the channel's own; no
person or company is named.

It is the first video in a new dark "documentary" style (`doc_cards.py`): near-black navy with a
faint grid, big white type with neon accents, kinetic wipes, and animated graphics: hype-cycle
waves over 1995 to today with the foundation line climbing underneath, a Flash timeline, a building
whose top-floor tool keeps being swapped (Flash, Web Forms, jQuery, React, AI tools) on the same
foundation, a Python iceberg, a typing IPython terminal with result bars, and a knowledge
"shelf life" chart.

Facts on screen:

- Flash: Macromedia Flash 1.0 in 1996; Steve Jobs' "Thoughts on Flash" in 2010; Adobe ended support
  at the end of 2020. Java applets: 1995, removed from the JDK in Java 11 (2018). Hash tables: H. P.
  Luhn's 1953 IBM memo. Boolean logic: Boole's *Laws of Thought*, 1854.
- Java and .NET are presented fairly: both are still widely used; what aged badly was knowing only
  the surface (drag-and-drop controls, memorised frameworks, certificates).
- The Python numbers are measured on an Apple Silicon Mac with Python 3.14 (the screen says so):
  `999_999 in nums` over 1,000,000 ints takes 4.82 ms with a list and 19 ns with a set (about
  250,000x); summing 10,000,000 ints takes 134 ms in a for loop and 0.99 ms with NumPy (about 136x);
  `0.1 + 0.2 == 0.3` is `False`, and `Decimal('0.1') + Decimal('0.2')` is `Decimal('0.3')`.

```sh
python3 foundations.py               # -> out/foundations.mp4 (narration is cached; reruns are quick)
python3 foundations.py --draft       # silent, estimated timing, fast encode: for checking layout and pace
python3 foundations.py --stills      # two PNGs per scene in build/foundations/stills/
python3 foundations.py --redo waves  # regenerate one scene's narration
```

`hkpsvid/` is the same renderer as the other videos; the new look lives entirely in `doc_cards.py`
(DocCard overrides the background and heading, each card animates in `draw_extra`), so other videos
can reuse it by copying that one file.
