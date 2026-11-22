#!/usr/bin/env python3
"""浪潮會過，基礎留低：點解基礎科技咁重要？

A Cantonese video for 香港編程學會 in a new dark "documentary" style (doc_cards.py). Over thirty
years Hong Kong rushed after wave after wave (Java, Flash, .NET, mobile apps, now AI); people who
only learned the tool of the day were left with little when the wave passed, while fundamentals
(maths, data structures and algorithms, computer architecture, operating systems, networks,
compilers) kept their value. The Python examples are measured, not made up:

    1,000,000 ints, `999_999 in nums`: list 4.82 ms, set 19 ns   (about 250,000x)
    sum of 10,000,000 ints: Python for loop 134 ms, NumPy 0.99 ms (about 136x)
    0.1 + 0.2 == 0.3 -> False; Decimal('0.1') + Decimal('0.2') -> Decimal('0.3')

measured on an Apple Silicon Mac with Python 3.14 (the screen says so). The point about Java and
.NET is made fairly: both are still widely used; what aged badly was knowing only the surface.
The Hong Kong observations are the channel's own; no person or company is named.

    python3 foundations.py              # -> out/foundations.mp4 (narration is cached)
    python3 foundations.py --draft      # silent, estimated timing, fast: for checking layout
    python3 foundations.py --stills     # two PNGs per scene in build/foundations/stills/
    python3 foundations.py --redo waves # regenerate one scene's narration
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D
from hkpsvid.style import W

from doc_cards import (AMBER, CYAN, DIM, LIME, PINK, VIOLET, DocEnd, DocTitle, EventLine, FoundationCard, IcebergCard,
                       ShelfCard, StatementCard, TerminalCard, VersusCard, WaveCard)

VIDEO = Video(slug=Path(__file__).stem, title="浪潮會過，基礎留低", series="香港編程學會 · 基礎篇")
opts = options(VIDEO)

MEASURED = "實測：Apple Silicon Mac · Python 3.14"

SAY = {
    ".NET": "dot net",
    "AI": "A I",
    "app": "app",
    "jQuery": "J query",
    "CPython": "C Python",
    "NumPy": "Num Pie",
    "CPU": "C P U",
    "JDK": "J D K",
    "Java Applet": "Java applet",
    "Web Forms": "Web Forms",
    "hash table": "hash table",
    "dict": "dict",
    "prompt": "prompt",
}


def measured(card: Card) -> Card:
    card.add(D.text_img(MEASURED, font(26), DIM), W - 120 - D.width(MEASURED, font(26)), 200, None)
    return card


scenes = [
    Scene("title",
          "大家好！歡迎收睇香港編程學會。今集唔教寫 code，講一個更根本嘅問題：點解基礎科技，對一個人、對一個社會，都咁重要？",
          DocTitle(VIDEO.series, ["浪潮會過，", "基礎留低"], "點解基礎科技對一個社會咁重要？")),
    Scene("waves",
          "香港過去三十年，經歷過一浪接一浪嘅科技熱潮。[[java]]九十年代中，Java 面世；[[flash]]跟住 Flash 網站同動畫大行其道；"
          "[[net]]二千年代初 .NET 出世，又一大班人轉過去；[[mobile]]之後係手機 app；[[ai]]而家，輪到 AI。",
          WaveCard("三十年，一浪接一浪", [
              ("Java", 1994.5, 1999, 2010, 300, AMBER, "java"),
              ("Flash", 1997, 2003, 2013, 380, PINK, "flash"),
              (".NET", 2001, 2006, 2015, 260, VIOLET, "net"),
              ("手機 App", 2008, 2013, 2021, 330, LIME, "mobile"),
              ("AI", 2016, 2027, 2027, 430, CYAN, "ai"),
          ], chapter="01")),
    Scene("surf",
          "每一浪嚟嘅時候，都有好多人衝埋去：[[a]]報課程、考證書、轉工。[[b]]但係浪潮一過，[[c]]淨係識嗰樣工具嘅人，就好似乜都冇晒。",
          StatementCard(None, [
              ("每一浪，都有人**衝埋去**", None, {"size": 76}),
              ("報課程 · 考證書 · 轉工", "a", {"size": 56, "color": DIM}),
              ("**浪潮一過**，", "b", {"size": 76, "accent": PINK}),
              ("淨係識工具嘅人，**乜都冇晒**", "c", {"size": 76, "accent": PINK}),
          ], top=270, gap=46)),
    Scene("flash",
          "Flash 係最清楚嘅例子。[[a]]一九九六年面世，[[peak]]全盛時期，好多網站同遊戲都用 Flash 做，識 Flash 好搵食；"
          "[[jobs]]二零一零年，Steve Jobs 寫咗封公開信，講明 iPhone 唔會支援 Flash；[[eol]]二零二零年尾，Adobe 正式停止支援。"
          "[[gone]]淨係識 Flash 嘅技能，一夜之間冇晒用。",
          EventLine("Flash：最清楚嘅例子", [
              ("1996", "Flash 面世", "網頁動畫、遊戲", AMBER, "a"),
              ("2000s", "全盛時期", "識 Flash 好搵食", AMBER, "peak"),
              ("2010", "Steve Jobs 公開信", "iPhone 唔支援 Flash", PINK, "jobs"),
              ("2020", "Adobe 停止支援", "Flash 正式退役", PINK, "eol"),
          ], chapter="02")),
    Scene("fair",
          "不過要講公道：[[j]]Java 同 .NET 今日仲喺度，仲用得好廣。[[s1]]被淘汰嘅，係當年淨係識拖拉控件、背框架、考證書，"
          "[[s2]]唔明白背後點運作嘅人；[[d1]]明白底層嘅人，[[d2]]換咗框架，照樣好快上手。",
          VersusCard("Java 同 .NET 仲喺度", [
              ("淨係識表面", PINK, [("拖拉控件、背框架", "s1"), ("考證書、唔問點解", ("s1", 1.2)), ("框架一換，就跟唔上", "s2")]),
              ("明白底層", LIME, [("知道背後點運作", "d1"), ("換框架，照樣上手", "d2"), ("工具係**佢揀**，唔係揀佢", ("d2", 1.2))]),
          ], footer=("被淘汰嘅唔係語言，係淨係識表面嘅人", ("d2", 1.5), AMBER))),
    Scene("building",
          "我覺得科技好似起樓。[[base]]下面係地基：數學、數據結構同演算法、電腦結構、作業系統、網絡，幾十年都冇乜點變。"
          "[[t1]]上面嘅工具就成日換：Flash、[[t2]].NET Web Forms、[[t3]]jQuery、[[t4]]React、[[t5]]今日嘅 AI 工具。"
          "[[end]]換咗一代又一代，地基依然係嗰啲。",
          FoundationCard("工具成日換，地基唔會", [
              ("數學", VIOLET), ("數據結構 · 演算法", CYAN), ("電腦結構", AMBER), ("作業系統", LIME), ("網絡 · 編譯器", PINK),
          ], "base", [
              ("Flash", AMBER, "t1"), ("ASP.NET Web Forms", VIOLET, "t2"), ("jQuery", CYAN, "t3"), ("React", CYAN, "t4"),
              ("AI 工具", PINK, "t5"),
          ], chapter="03")),
    Scene("iceberg",
          "用 Python 做例子。[[code]]你寫一行 numbers 等於 1、2、3，好簡單；[[l1]]但喺水面下面，有 CPython 直譯器，"
          "[[l2]]佢用 C 寫成；[[l3]]再下面係作業系統，[[l4]]最底係 CPU 同記憶體。[[note]]你睇唔到佢哋，但佢哋決定咗你個程式快定慢、啱定錯。",
          IcebergCard("Python：水面下面有咩？", "numbers = [1, 2, 3]", [
              ("CPython 直譯器", "將 Python 變成 bytecode 再執行", CYAN, "l1"),
              ("C 語言", "list 其實係一排指標", VIOLET, "l2"),
              ("作業系統", "記憶體、檔案、執行緒", LIME, "l3"),
              ("CPU + 記憶體", "二進制、快取、指令", AMBER, "l4"),
          ], code_at="code", chapter="04", note=("睇唔到，但**決定快慢同對錯**", "note"))),
    Scene("lookup",
          "試吓：[[q]]喺一百萬個數字入面，搵一個數字有冇出現。[[list]]用 list，要四點八毫秒；[[set]]用 set，只要十九納秒，快咗二十幾萬倍。"
          "[[why]]因為 list 要逐個比，set 用 hash table，一步就搵到。唔識數據結構，你連慢喺邊都唔知。",
          measured(TerminalCard("數據結構：快二十幾萬倍", [
              ("nums = list(range(1_000_000))", "", "q"),
              ("nums_set = set(nums)", "", ("q", 1.6)),
              ("%timeit 999_999 in nums", "4.82 ms per loop", "list", AMBER),
              ("%timeit 999_999 in nums_set", "19 ns per loop", "set", LIME),
          ], bars=[
              ("list：逐個比", "4.82 ms", 1.0, PINK, "list"),
              ("set：hash table", "0.000019 ms", 0.004, LIME, "set"),
          ], chapter="05", foot=("**快咗二十幾萬倍**：分別唔喺 Python，喺數據結構", "why")))),
    Scene("numpy",
          "再嚟一個：[[loop]]用 Python for loop，將一千萬個數加埋，要零點一三秒；[[np]]用 NumPy，大約一毫秒，快咗一百幾十倍。"
          "[[why]]因為 NumPy 底層用 C 寫，一次過處理成條陣列。明白底層，先知道點樣揀工具。",
          measured(TerminalCard("揀工具，要明白底層", [
              ("def loop_sum(n):\n    s = 0\n    for i in range(n):\n        s += i\n    return s", "", "loop"),
              ("%timeit loop_sum(10_000_000)", "134 ms per loop", ("loop", 3.2), AMBER),
              ("import numpy as np", "", "np"),
              ("arr = np.arange(10_000_000)", "", ("np", 0.9)),
              ("%timeit arr.sum()", "0.99 ms per loop", ("np", 2.2), LIME),
          ], bars=[
              ("Python for loop", "134 ms", 1.0, PINK, ("loop", 3.2)),
              ("NumPy（底層係 C）", "0.99 ms", 0.0074, LIME, ("np", 2.2)),
          ], foot=("快咗**一百幾十倍**：因為底層係 C", "why")))),
    Scene("float",
          "最後一個：[[q]]零點一加零點二，係咪等於零點三？[[f]]Python 話：False。[[why]]唔係 Python 有 bug，而係電腦用二進制存小數，零點一根本存唔準。"
          "[[fix]]要計錢，就要用 Decimal 呢類工具。唔識呢點，寫銀行系統就會出事。",
          TerminalCard("0.1 + 0.2 = ？", [
              ("0.1 + 0.2", "0.30000000000000004", "q", AMBER),
              ("0.1 + 0.2 == 0.3", "False", "f", PINK),
              ("from decimal import Decimal", "", "fix"),
              ("Decimal('0.1') + Decimal('0.2')", "Decimal('0.3')", ("fix", 1.6), LIME),
          ], width=1200, foot=("二進制**存唔準 0.1**：唔係 bug，係底層", "why"))),
    Scene("you",
          "所以，淨係識用工具，你只係跟住浪潮行。明白底層，你先可以：[[a]]知道問題出喺邊；[[b]]學新工具學得快，因為底層都係嗰啲；"
          "[[c]]甚至自己整工具，自己造浪。",
          StatementCard("明白底層，你可以", [
              ("1.  知道**問題出喺邊**", "a"),
              ("2.  新工具**學得快**：底層都係嗰啲", "b"),
              ("3.  自己整工具，**自己造浪**", "c"),
          ], top=330, gap=60, chapter="06")),
    Scene("society",
          "放大到一個社會都一樣。[[a]]如果一個社會淨係追住用人哋整好嘅工具，浪潮一過，乜都冇留低；"
          "[[b]]肯投資喺基礎：教育、研究、晶片、作業系統、編譯器，[[c]]先可以由用家，變成造工具嘅人。",
          VersusCard("放大到一個社會", [
              ("追浪潮", PINK, [("用人哋整好嘅工具", "a"), ("浪一過，乜都冇留低", ("a", 1.6))]),
              ("打地基", LIME, [("投資教育同研究", "b"), ("晶片、作業系統、編譯器", ("b", 1.2)), ("由用家變成**造工具嘅人**", "c")]),
          ], footer=("基礎科技 ＝ 一個社會嘅地基", ("c", 1.8), CYAN))),
    Scene("ai",
          "今日嘅 AI 浪潮都一樣。[[a]]淨係識打 prompt，同當年淨係識 Flash 冇乜分別；"
          "[[b]]明白機率、線性代數、神經網絡點樣訓練，[[c]]先唔會被下一浪沖走。",
          StatementCard("今日嘅 AI 浪潮", [
              ("淨係識打 prompt", "a", {"size": 72}),
              ("≈ 當年淨係識 **Flash**", ("a", 1.4), {"size": 72, "accent": PINK}),
              ("明白**機率、線性代數、神經網絡**", "b", {"size": 64}),
              ("先唔會被**下一浪**沖走", "c", {"size": 72, "accent": AMBER}),
          ], top=300, gap=44, chapter="07")),
    Scene("shelf",
          "睇吓唔同知識嘅保質期：[[f]]Flash，一九九六年到二零二零年；[[j]]Java Applet，一九九五年面世，二零一八年喺 JDK 入面被移除；"
          "[[h]]但 hash table，一九五三年已經有人提出，今日 Python 嘅 dict 同 set 仲用緊；[[b]]布林邏輯，一八五四年，今日每部電腦都用緊。",
          ShelfCard("知識嘅保質期", [
              ("Flash", 1996, 2020, "2020 停止支援", AMBER, "f"),
              ("Java Applet", 1995, 2018, "2018 喺 JDK 移除", AMBER, "j"),
              ("Hash table", 1953, None, "Python dict / set 仲用緊", LIME, "h"),
              ("布林邏輯", 1854, None, "每部電腦都用緊", CYAN, "b"),
          ], footer=("工具有保質期，基礎冇", ("b", 2.0), CYAN))),
    Scene("end",
          "浪潮一定會嚟，亦一定會過。[[a]]衝浪，冇問題，[[b]]但記得先學識游水。[[c]]基礎，先係唔會過時嘅競爭力。",
          StatementCard(None, [
              ("浪潮一定會嚟，亦一定會過", None, {"size": 64, "color": DIM}),
              ("衝浪，冇問題", "a", {"size": 84}),
              ("但記得先學識**游水**", "b", {"size": 84}),
              ("基礎，先係**唔會過時**嘅競爭力", "c", {"size": 72, "accent": AMBER}),
          ], top=270, gap=50, center=True)),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]揀一個你成日用嘅 Python 功能，例如 dict，查吓佢底層點運作，再講俾朋友聽。[[next]]多謝收睇，下次見！",
          DocEnd("揀一個你成日用嘅 Python 功能，例如 dict：查吓佢底層點運作，點解搵嘢咁快？然後講俾一個朋友聽。",
                 "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
