#!/usr/bin/env python3
"""Arithmetic coding：將預測變成壓縮（資訊理論・第三集）

A Cantonese explainer of arithmetic coding and "compression is intelligence" for 香港編程學會,
rewritten from the ideas in 3Blue1Brown's "This algorithm changed how I think about compression |
Information theory, part 3" (credited on the title and end cards). The narration is original
Cantonese, not a translation; the screens are HKPS cards with their own animations.

The interval, bits and random-sample demos run on a real (tiny) model, arith_model.py: next-letter
probabilities counted from the system word list. "math" lands in 13 bits (14.03 bits of
information), "mathematics" in 18 bits (18.05). The preamble's ASCII size (2,616 bits) and a
Huffman code built for that very text (1,406 bits) are computed here too. The NanoGPT and Qwen
figures are quoted from the original video and say so on screen.

    python3 arithmetic_part3.py              # -> out/arithmetic_part3.mp4 (narration is cached)
    python3 arithmetic_part3.py --draft      # silent, estimated timing, fast: for checking layout
    python3 arithmetic_part3.py --stills     # two PNGs per scene in build/arithmetic_part3/stills/
    python3 arithmetic_part3.py --redo zoom  # regenerate one scene's narration
"""

import heapq
from collections import Counter
from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D
from hkpsvid.style import MARGIN, W

import arith_model as M
from arith_cards import BinaryCard, TargetCard, ZoomStackCard
from cross_cards import PredictCard
from entropy_cards import CueBarCard, EquationCard

VIDEO = Video(slug=Path(__file__).stem, title="Arithmetic coding", series="資訊理論")
opts = options(VIDEO)

CREDIT = "內容參考：3Blue1Brown〈This algorithm changed how I think about compression｜part 3〉· 廣東話重新編寫"
FROM_SOURCE = "數字來自原片"

SAY = {
    "AI": "A I",
    "GB": "G B",
    "ASCII": "ask key",
    "Huffman code": "Huffman code",
    "Qwen": "Q when",
    "ANS": "A N S",
    "Hutter Prize": "Hutter Prize",
    "k": "K",
    "p": "P",
    "x": "X",
    "a": "A",
    "m": "M",
    "s": "S",
    "q": "Q",
    "Δ": "delta",
    "math": "math",
    "We the People": "We the People",
}

PRE = ("We the People of the United States, in Order to form a more perfect Union, establish Justice, "
       "insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure "
       "the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution "
       "for the United States of America.")


def huffman_bits(text: str) -> int:
    """Total bits of an optimal Huffman code built for this very text (its own letter counts)."""
    c = Counter(text)
    heap = [(n, i) for i, n in enumerate(c.values())]
    groups = {i: [ch] for i, ch in enumerate(c)}
    depth = dict.fromkeys(c, 0)
    heapq.heapify(heap)
    nid = len(heap)
    while len(heap) > 1:
        n1, a = heapq.heappop(heap)
        n2, b = heapq.heappop(heap)
        for ch in groups[a] + groups[b]:
            depth[ch] += 1
        groups[nid] = groups.pop(a) + groups.pop(b)
        heapq.heappush(heap, (n1 + n2, nid))
        nid += 1
    return sum(c[ch] * depth[ch] for ch in c)


ASCII_BITS = 8 * len(PRE)
HUFF_BITS = huffman_bits(PRE)
MATH = M.interval("math")[-1]
MATH_BITS = M.shortest_bits(*MATH)
MATHS = M.interval("mathematics")[-1]
MATHS_BITS = M.shortest_bits(*MATHS)
FIRST_M = [round(M.p_next("math"[:i], "math"[i]), 3) for i in range(4)]
SAMPLES = M.samples(5, 7, seed=5)


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 44) -> Card:
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


def credit(card: Card, y: int) -> Card:
    card.add_center(D.text_img(CREDIT, font(28), MUTED), y, at=None)
    return card


def note(card: Card, txt: str = FROM_SOURCE) -> Card:
    card.add(D.text_img(txt, font(28), MUTED), W - MARGIN - D.width(txt, font(28)), 250, None)
    return card


END = EndCard("如果模型估 m、a、t、h 四個字母嘅機率分別係 ½、¼、½、¼，用 arithmetic coding，成個字大約要幾多個 bit？",
              "資訊理論三部曲・完", challenge_at="ch", next_at="next")
credit(END, 860)

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟資訊理論第三集，亦係最後一集。今集講一個好靚嘅演算法：arithmetic coding。"
          "佢可以將一段文字，壓到每個字母唔使一個 bit。",
          credit(TitleCard(VIDEO.series, "第三集", "Arithmetic coding", "將預測變成壓縮",
                           "一段文字 → 0 同 1 之間嘅一個數"), 830)),
    Scene("hutter",
          "有個比賽叫 Hutter Prize：[[a]]邊個可以將 1 GB 嘅維基百科壓得最細，就有獎金。"
          "[[b]]計分唔止睇壓縮檔，仲要計埋解壓程式嘅大小。[[c]]而歷屆得獎方法，骨幹都係今集講嘅呢個演算法。",
          TileCard("Hutter Prize", [
              Tile("📚", "1 GB 維基百科", "邊個壓得最細？", "a", BLUE),
              Tile("📦", "連解壓程式一齊計", "壓縮檔 + 解壓程式", "b", PURPLE),
              Tile("🏆", "得獎方法嘅骨幹", "arithmetic coding", "c", AMBER),
          ], cols=3, height=300)),
    Scene("setup",
          "任何壓縮都分兩邊：[[s]]發送者將文字變成 0 同 1，越少越好；[[r]]接收者將 0 同 1 還原，"
          "[[l]]而且要一模一樣，即係無損壓縮。",
          pill(FlowCard("壓縮：兩個程式", [
              Row("發送者", "編碼", BLUE, [Node("文字", "We the People…", "s"), Node("編碼器", "越少 bit 越好", ("s", 0.5)),
                                         Node("0110…", "傳出去", ("s", 1.0))]),
              Row("接收者", "解碼", PURPLE, [Node("0110…", "收到", "r"), Node("解碼器", "還原", ("r", 0.5)),
                                          Node("文字", "一模一樣", ("r", 1.0))]),
          ], top=290, row_h=260), "無損壓縮：還原出嚟要一模一樣", 820, "l", BLUE)),
    Scene("shannon",
          "上兩集講過，Shannon 話最好嘅壓縮，一段訊息用嘅 bit 數，大約等於負 log 二 p。"
          "[[half]]機率每減半，就多一個 bit。[[odd]]但認真諗，呢個結論有啲荒謬。",
          EquationCard("Shannon 嘅結論", [
              ("bits ≈ -log_2 P(訊息)", None, {"size": 72, "box": AMBER, "weight": "bold"}),
              ("機率減半 → 多 1 個 bit", "half", {"size": 54}),
          ], top=320, gap=60, pill=("認真諗：有啲荒謬？", "odd", RED))),
    Scene("preamble",
          "例如美國憲法序言：[[w]]一見到開頭 We the People，熟悉嘅人幾乎估到後面成段。"
          "[[half]]假設你有一半信心，後面成段就只有一個 bit 資訊；[[k]]就算只有千分之一信心，都只係十個 bit。",
          EquationCard("美國憲法序言", [
              ("We the People of the United States, in Order to form a more perfect Union, …", "w", {"size": 40}),
              ("有一半信心：P = ½ → 1 bit", "half", {"size": 54}),
              ("得千分之一信心：P = 1/1000 → 約 10 bits", "k", {"size": 54}),
          ], top=320, gap=60)),
    Scene("absurd",
          "但你試吓寫個程式：[[a]]用 ASCII 存呢段序言，要成二千六百個 bit；"
          "[[h]]就算用專為呢段度身訂造嘅 Huffman code，都仲要一千四百個 bit。"
          "[[q]]要將大半段文字塞入十個 bit，點可能？[[promise]]但今集完之前，你會親眼見到。",
          CueBarCard("憲法序言要幾多 bit？", [
              ("ASCII", ASCII_BITS, f"{ASCII_BITS:,} bits", MUTED, "a"),
              ("Huffman code", HUFF_BITS, f"{HUFF_BITS:,} bits", BLUE, "h"),
              ("Shannon 話", 45, "幾十 bits？", RED, "q"),
          ], top=300, step=150, pill=("今集完之前，你會親眼見到", "promise", AMBER))),
    Scene("context",
          "Huffman code 嘅問題係：[[h1]]每個字母永遠用同一個碼，冇理會前文。"
          "[[c]]但 Shannon 話，壓得幾細取決於估得幾準，而估得幾準，好視乎前文。"
          "[[llm]]今日最識睇前文估下一個字嘅工具，就係語言模型。",
          CompareCard("問題出喺前文", [
              Column("🔤", "Huffman code", [("每個字母一個固定碼", "h1"), ("冇理會前文", ("h1", 1.0))], MUTED),
              Column("🤖", "語言模型", [("睇前文估下一個字", "llm"), ("估得越準，壓得越細", ("llm", 1.2))], BLUE),
          ], footer=("可壓縮 ＝ 可預測", "c", AMBER))),
    Scene("shared",
          "所以關鍵設定係：[[both]]發送者同接收者，各有一個一模一樣嘅語言模型。"
          "[[slot]]呢個演算法好似一個插座，插咩模型都得，模型越好，壓縮越好。"
          "[[idea]]做法係：將一段文字，變成 0 同 1 之間一個好精確嘅數。",
          pill(FlowCard("兩邊有同一個模型", [
              Row("發送者", "編碼", BLUE, [Node("文字", "math", "both"), Node("語言模型", "同一個", ("both", 0.5)),
                                         Node("一個數", "0 同 1 之間", "idea")]),
              Row("接收者", "解碼", PURPLE, [Node("一個數", "0 同 1 之間", "idea"), Node("語言模型", "同一個", ("both", 0.5)),
                                          Node("文字", "math", ("idea", 0.6))]),
          ], top=290, row_h=260), "插咩模型都得：模型越好，壓縮越好", 820, "slot", AMBER)),
    Scene("toy",
          "為咗睇得清楚，我哋用一個好細嘅模型：[[d]]佢由一本英文字典數出嚟，"
          "[[l]]睇住前面嘅字母，估下一個字母，只有二十六個字母。例如 m 後面，多數係元音。"
          "[[note]]換成真正嘅語言模型同 token，方法完全一樣。",
          pill(PredictCard("示範用嘅細模型", "m", [(c, p) for p, c in sorted(zip(M.dist("m"), M.ALPHA), reverse=True)[:5]],
                           in_at="d", model_at="d", out_at="l"),
               "換成真正嘅語言模型，方法一樣", 830, "note", BLUE)),
    Scene("line",
          "唔用棒形圖，我哋將機率排成一條橫條：[[w]]每個字母嘅闊度就係佢嘅機率，"
          "[[u]]總闊度係一，所以可以當佢係 0 到 1 嘅數線。[[t]]常見嘅開頭字母佔得闊，罕見嘅好似 q 同 x，窄到幾乎睇唔到。",
          pill(ZoomStackCard("機率排成一條數線", "", ["w"], axis=True, pick=False, top=380, row_h=160),
               "總闊度 ＝ 1：0 到 1 嘅數線", 600, "u", BLUE)),
    Scene("zoom",
          "而家編碼 math 呢個字。[[m]]第一個字母 m，佔數線上面一段；[[a]]將 m 放大，下一層係 m 後面嘅字母，a 最闊；"
          "[[t]]再放大 a，揀 t；[[h]]再放大 t，揀 h。[[w]]最後呢一小段嘅闊度，就係模型覺得文字以 math 開頭嘅機率。",
          ZoomStackCard("逐個字母放大：math", "math", ["m", "a", "t", "h"], top=300, row_h=128, readout_at="w")),
    Scene("chain",
          "點解？[[c1]]由成條數線縮到 m，係乘咗 m 嘅機率；[[c2]]再縮到 a，係乘咗 m 後面出 a 嘅機率；"
          "[[c3]]全部乘埋，就係 math 嘅機率，即係第一集講嘅連鎖法則。",
          EquationCard("闊度 ＝ 機率乘埋", [
              ("P(math) = P(m) × P(a | m) × P(t | ma) × P(h | mat)", "c1", {"size": 46}),
              (f"= {FIRST_M[0]} × {FIRST_M[1]} × {FIRST_M[2]} × {FIRST_M[3]}", "c2", {"size": 52}),
              (f"≈ {MATH[1] - MATH[0]:.6f}", "c3", {"size": 64, "box": AMBER, "weight": "bold"}),
          ], top=320, gap=56)),
    Scene("unique",
          "所以每一段文字，都對應數線上一小段。[[any]]喺嗰段入面揀任何一個數，再講埋有幾多個字母，就可以還原成段文字。"
          "[[inf]]理論上，每一個無限長嘅字串，都對應 0 同 1 之間一個獨一無二嘅數。",
          EquationCard("每段文字，對應數線上一小段", [
              (f"math → [{MATH[0]:.7f}, {MATH[1]:.7f})", None, {"size": 54}),
              (f"揀一個入面嘅數 + 長度 4 → 還原得返 math", "any", {"size": 50}),
              ("每個無限長字串 → 一個獨一無二嘅數", "inf", {"size": 54, "box": BLUE, "weight": "bold"}),
          ], top=320, gap=56)),
    Scene("decode",
          "接收者點解碼？[[s1]]佢用同一個模型睇第一層：x 落喺 m 嗰段，所以第一個字母係 m；"
          "[[s2]]再將 m 放入模型，睇第二層：x 落喺 a；[[s3]]如此類推，[[s4]]做夠四次就停。[[same]]所以兩邊嘅模型，一定要一模一樣。",
          pill(ZoomStackCard("接收者：跟住 x 逐層解碼", "math", ["s1", "s2", "s3", "s4"], top=330, row_h=118,
                             marker=(MATH[0] + MATH[1]) / 2, marker_at="s1"),
               "兩邊嘅模型，一定要一模一樣", 820, "same", RED)),
    Scene("random",
          "Shannon 話完美壓縮嘅輸出似隨機雜訊。[[r]]試吓喺 0 同 1 之間隨機揀數，再解碼：[[look]]出嚟嘅字串，大部分都似英文。"
          "[[why]]因為模型覺得越似英文嘅字串，佔嘅數線越闊。呢個其實就係語言模型生成文字嘅方式。",
          pill(EquationCard("隨機揀一個數，再解碼", [
              (f"x = {x:.4f}  →  {s}", ("r", 0.6 * i) if i < 3 else ("look", 0.5 * (i - 3)), {"size": 44})
              for i, (x, s) in enumerate(SAMPLES)
          ], top=280, gap=4), "越似英文，佔嘅數線越闊", 840, "why", BLUE)),
    Scene("binary",
          "要傳送呢個數，就要寫成二進制。[[b1]]小數點後第一個 bit，話你知喺左半定右半；[[b2]]第二個 bit，再揀嗰一半嘅左定右；"
          "[[b3]]每多一個 bit，範圍就再切一半。[[stop]]停喺邊度，代表嘅數就係嗰段最左邊嘅點。",
          BinaryCard("二進制小數：每個 bit 切一半", "0111", ["b1", "b2", "b3", ("b3", 1.2)], stop_at="stop")),
    Scene("target",
          "返去 math：[[k1]]用十一個 bit，間隔太闊，冇一個數落喺目標入面；[[k2]]十二個 bit，都係唔得；"
          "[[k3]]十三個 bit，終於有一個數落喺入面。[[avg]]四個字母用十三個 bit，平均每個字母三點二五 bit。",
          pill(TargetCard("math 要幾多個 bit？", MATH[0], MATH[1], [11, 12, 13], ["k1", "k2", "k3"]),
               f"math → .{MATH_BITS}（{len(MATH_BITS)} bits，平均 {len(MATH_BITS) / 4:.2f} bits / 字母）", 830, "avg", GREEN,
               size=38)),
    Scene("long",
          "再試長啲嘅字：mathematics。[[e]]math 後面嘅 e、m、a、t、i、c，模型都估得好準，範圍幾乎冇點縮；"
          "[[s]]到最後個 s，先真係要做選擇。[[bits]]結果成個字得十八個 bit，平均每個字母一點六四 bit。",
          pill(ZoomStackCard("mathematics：越長越抵", "mathematics", [None] * 4 + [("e", 0.6 * k) for k in range(6)] + ["s"],
                             top=262, row_h=54, labels=False),
               f"mathematics → {len(MATHS_BITS)} bits（平均 {len(MATHS_BITS) / 11:.2f} bits / 字母）", 878, "bits", GREEN,
               size=34)),
    Scene("bound",
          "一般嚟講要幾多 bit？[[s]]用 k 個 bit 寫得出嘅數，每隔二嘅負 k 次方就有一個。"
          "[[g]]目標闊度係 p，要保證一定瞄中，就要二嘅負 k 次方細過 p，[[k]]即係 k 大過或等於負 log 二 p。"
          "[[shannon]]呢個正正就係 Shannon 嘅資訊量！",
          EquationCard("要幾多個 bit？", [
              ("k 個 bit：每隔 2^{-k} 有一個數", "s", {"size": 52}),
              ("保證瞄中：2^{-k} ≤ p", "g", {"size": 52}),
              ("k ≥ -log_2 p", "k", {"size": 72, "box": AMBER, "weight": "bold"}),
          ], top=300, gap=56, pill=("＝ Shannon 嘅資訊量！", "shannon", RED))),
    Scene("dream",
          "Shannon 只證明咗理論上可以接近極限；[[a]]arithmetic coding 就係一個做得到嘅方法：壓縮後嘅大小，同資訊量只差唔夠一個 bit。"
          "[[len]]當然仲要傳埋長度，但三十二個 bit 已經可以表示四十幾億個字母，相比之下好少。",
          pill(BulletCard("實現咗 Shannon 嘅夢想", [
              ("壓縮大小 ≈ 資訊量，最多差一個 bit", "a"),
              ("另外傳長度：32 bits 夠表示四十幾億個字母", "len"),
          ]), "一個寫得出嚟嘅方法，貼住 Shannon 極限", 640, ("len", 1.5), AMBER)),
    Scene("lucky",
          "有時仲會好彩：[[m]]math 嘅資訊量係十四點零三 bit，但十三個 bit 就瞄中咗。"
          "[[aa]]極端例子：成段都係 a，對應數線最左邊，零個 bit 就得。"
          "[[avg]]不過 Shannon 講嘅係平均：好彩嘅時候，會被要向上取整嘅時候抵銷。",
          CompareCard("好彩 vs 平均", [
              Column("🍀", "有時好彩", [("math：資訊量 14.03，用 13 bits", "m"), ("成段 a：最左邊，0 bits", "aa")], GREEN),
              Column("⚖️", "平均嚟講", [("好彩會被向上取整抵銷", "avg"), ("平均低唔過資訊量", ("avg", 1.2))], BLUE),
          ])),
    Scene("model",
          "但仲有一個更重要嘅位：[[p]]呢度嘅 p，係模型估嘅機率，唔係語言真正嘅機率。"
          "[[q]]所以壓縮得幾好，幾乎完全取決於模型估得幾準。",
          EquationCard("p 係邊個嘅機率？", [
              ("壓縮大小 ≈ -log_2 P_{模型}(文字)", "p", {"size": 62, "box": PURPLE, "weight": "bold"}),
          ], top=360, pill=("模型越準，壓得越細", "q", PURPLE))),
    Scene("pretrain",
          "呢度可以重新理解點樣訓練語言模型：[[sum]]負 log 模型機率，拆開就係每個 token 嘅負 log 加埋，平均落嚟就係上集嘅 cross-entropy loss。"
          "[[two]]所以訓練語言模型，除咗可以講成學估下一個字，[[comp]]亦可以講成：學做最好嘅文字壓縮器。",
          CompareCard("兩種講法，同一件事", [
              Column("🎯", "講法一", [("目標：估下一個 token", "two"), ("量度：cross-entropy loss", ("two", 0.8))], BLUE),
              Column("📦", "講法二", [("目標：最好嘅文字壓縮器", "comp"), ("量度：壓縮後幾多 bit", ("comp", 0.8))], AMBER),
          ], footer=("-log P(文字) = Σ 每個 token 嘅 -log p", "sum", MUTED))),
    Scene("models",
          "模型好唔好，差好遠。[[small]]原片用一個三百七十萬參數嘅細模型，壓一句講歐幾里得《幾何原本》嘅英文句子，"
          "要二百五十四個 bit，每個字母大約兩個 bit；[[big]]換成五億參數嘅 Qwen，每個字母唔使一個 bit。",
          note(CueBarCard("同一句，唔同模型", [
              ("細模型（3.7M）", 254, "254 bits", MUTED, "small"),
              ("Qwen（0.5B）", 115, "< 127 bits", BLUE, "big"),
          ], top=330, step=170, pill=("模型越好，壓得越細", ("big", 2.0), BLUE)))),
    Scene("result",
          "再試返憲法序言：[[first]]原片用 Qwen，開頭 We the People 嗰句大約用三十五個 bit，[[rest]]後面成段，加埋只係十個 bit 左右。"
          "[[cmp]]同度身訂造嘅 Huffman code 比，細咗三十幾倍。",
          note(CueBarCard("憲法序言：結果", [
              ("ASCII", ASCII_BITS, f"{ASCII_BITS:,} bits", MUTED, None),
              ("Huffman code", HUFF_BITS, f"{HUFF_BITS:,} bits", BLUE, None),
              ("Qwen + 算術編碼", 45, "≈ 45 bits", GREEN, "first"),
          ], top=300, step=150, pill=(f"細咗 {HUFF_BITS // 45} 倍", "cmp", GREEN)))),
    Scene("cheat",
          "你可能會問：咁係咪作弊？大模型可能早已背熟咗成段序言。[[yes]]問得好，記住呢個疑問，我哋好快會返嚟。",
          pill(EquationCard("咁係咪作弊？", [
              ("大模型可能背熟咗成段序言", None, {"size": 56}),
          ], top=380), "記住呢個疑問，好快返嚟", 560, "yes", PURPLE)),
    Scene("history",
          "仲有個實際問題：[[z]]一路放大落去，數字要越嚟越精確，電腦頂唔順。[[e]]呢個想法最早可以追溯到一九六零年左右，Peter Elias 未發表嘅研究；"
          "[[r]]到一九七六年，Rissanen 同 Pasco 各自整出實用版本：每一步將範圍重新拉返做一，唔使無限精度。",
          TimelineCard("由想法到實用", [
              Event("問題", "越放大越要精確", "電腦頂唔順", "z", RED),
              Event("約 1960", "Peter Elias", "未發表嘅想法", "e", MUTED),
              Event("1976", "Rissanen、Pasco", "每步將範圍拉返做 1", "r", BLUE),
          ])),
    Scene("ans",
          "呢個就係今日講嘅 arithmetic coding，幾乎完美咁將預測器變成壓縮器，[[h]]Hutter Prize 嘅得獎方法都係咁做，進步主要嚟自更好嘅預測模型。"
          "[[ans]]另外，Jarek Duda 提出嘅 ANS，用一個越嚟越大嘅整數代替實數，速度更快。",
          TileCard("將預測器變成壓縮器", [
              Tile("🧮", "Arithmetic coding", "幾乎完美咁將預測變成壓縮", None, BLUE),
              Tile("🏆", "Hutter Prize", "進步嚟自更好嘅預測模型", "h", AMBER),
              Tile("🔢", "ANS（Jarek Duda）", "用越嚟越大嘅整數，更快", "ans", PURPLE),
          ], cols=3, height=300)),

    # -- compression is intelligence? ---------------------------------------------------------------------
    Scene("claim",
          "三集嘅總題目係：壓縮就係智能？[[v]]智能好難定義，所以我會當佢係一個建議：如果要俾智能一個數學定義，壓縮夠唔夠？"
          "[[e]]就好似物理將能量定義成一個可以量度嘅數，冇齊日常用法嘅意思，但好有用。[[three]]我想講三點。",
          TileCard("壓縮就係智能？", [
              Tile("🔁", "一：預測 ＝ 壓縮", "一個銀幣嘅兩面", "three", BLUE),
              Tile("🪶", "二：越細越好", "少啲死記，多啲原理", ("three", 0.6), GREEN),
              Tile("⚡", "三：學得快", "即時學習，壓得更細", ("three", 1.2), AMBER),
          ], cols=3, height=300, footer=("當佢係一個「智能」嘅數學定義：夠唔夠？", "v"))),
    Scene("point1",
          "第一，預測同壓縮係一個銀幣嘅兩面。[[a]]arithmetic coding 將任何預測器變成壓縮器；"
          "[[b]]反過嚟，有個壓縮器，都可以估機率：加一段文字之後，壓縮檔大咗 Δ 個 bit，[[c]]嗰段文字嘅機率，大約就係二嘅負 Δ 次方。",
          EquationCard("一：預測 ＝ 壓縮", [
              ("預測器 → arithmetic coding → 壓縮器", "a", {"size": 52}),
              ("壓縮器：加一段文字，大咗 Δ 個 bit", "b", {"size": 52}),
              ("P(嗰段文字) ≈ 2^{-Δ}", "c", {"size": 66, "box": BLUE, "weight": "bold"}),
          ], top=310, gap=56)),
    Scene("brain",
          "腦科學亦有個理論，叫 predictive processing：[[a]]大腦不停預測感官會收到乜，"
          "[[b]]感官送返上去嘅，唔係全部資訊，而係預測同現實之間嘅誤差。[[c]]即係話，好多我哋叫做智能嘅嘢，可能都係預測同壓縮。",
          pill(FlowCard("Predictive processing", [
              Row("大腦", "由上而下", PURPLE, [Node("預測", "感官會收到乜", "a")]),
              Row("感官", "由下而上", TEAL, [Node("只送誤差", "唔送全部資訊", "b")]),
          ], top=290, row_h=250), "智能 ≈ 預測 ＋ 壓縮？", 800, "c", AMBER)),
    Scene("point2",
          "第二，我覺得明白一樣嘢，係佢喺腦入面變細咗：幾條簡單原理，就推得出一大堆結果。"
          "[[m]]兩個模型預測一樣準，一個要幾萬億參數，一個好細，細嗰個靠嘅死記應該少啲。[[h]]但如果唔計模型大小，佢哋壓縮出嚟一樣大。",
          CompareCard("二：越細越好", [
              Column("🐘", "大模型", [("預測一樣準", "m"), ("幾萬億參數：死記多", ("m", 0.8))], MUTED),
              Column("🪶", "細模型", [("預測一樣準", "m"), ("參數少：靠原理", ("m", 0.8))], GREEN),
          ], footer=("唔計模型大小：壓縮出嚟一樣大", "h", RED))),
    Scene("decoder",
          "所以 Hutter Prize 要計埋解壓程式，包括個模型。[[cheat]]否則你可以將成個維基百科抄入解壓程式，壓縮檔幾乎係零。"
          "[[back]]頭先大模型背熟序言嘅疑問，就係咁樣計返入去。[[rhyme]]咁計嘅話，同樣準，細模型就係更好嘅壓縮。",
          EquationCard("連解壓程式一齊計", [
              ("總大小 = 壓縮檔 + 解壓程式（連模型）", None, {"size": 54, "box": AMBER, "weight": "bold"}),
              ("唔計程式：抄晒維基入去 → 壓縮檔 ≈ 0", "cheat", {"size": 50}),
              ("背熟序言嘅大模型：要計返佢嘅大小", "back", {"size": 50}),
          ], top=310, gap=56, pill=("同樣準：細模型 ＝ 更好嘅壓縮", "rhyme", GREEN))),
    Scene("point3",
          "第三，學得快。[[a]]一般嚟講，壓縮比同模型訓練得幾快冇關。[[b]]但如果用維基百科訓練嘅模型，去壓莎士比亞，"
          "[[c]]可以一路壓縮，一路即時用 backpropagation 微調模型；[[d]]解壓嗰邊做一模一樣嘅更新，預測就保持一致。[[e]]咁樣，學得越快，壓得越細。",
          pill(FlowCard("三：一路壓縮，一路學", [
              Row("編碼", "發送者", BLUE, [Node("讀一個 token", "莎士比亞", "c"), Node("壓縮", "用而家嘅模型", ("c", 0.5)),
                                         Node("更新模型", "backpropagation", ("c", 1.0))]),
              Row("解碼", "接收者", PURPLE, [Node("解一個 token", "同一個模型", "d"), Node("還原", "預測一致", ("d", 0.5)),
                                          Node("同樣更新", "一模一樣", ("d", 1.0))]),
          ], top=290, row_h=260), "學得越快，壓得越細", 820, "e", AMBER), seed=12),
    Scene("trilogy",
          "睇返成個三部曲：[[p1]]第一集，Shannon 要估英文可以壓幾細，要靠人估字；[[p2]]第二集，今日訓練 AI 嘅數學工具，原本用嚟研究壓縮；"
          "[[p3]]第三集，最好嘅壓縮方法，要一個預測準、體積細、學得快嘅模型。",
          TimelineCard("三部曲", [
              Event("第一集", "Entropy", "估英文要靠人腦", "p1", BLUE),
              Event("第二集", "Cross-entropy", "AI 用壓縮嘅數學", "p2", PURPLE),
              Event("第三集", "Arithmetic coding", "準、細、學得快", "p3", AMBER),
          ])),
    Scene("answer",
          "咁壓縮係咪就等於智能？[[no]]穩陣嘅答案當然係唔係，就好似物理學嘅能量，唔等於日常講嘅能量。"
          "[[but]]但如果真係要俾智能一個數學定義，壓縮剔中嘅格，比我想像中多好多。",
          EquationCard("壓縮 ＝ 智能？", [
              ("穩陣答案：唔係", "no", {"size": 60}),
              ("但作為數學定義，壓縮剔中好多格", "but", {"size": 56, "box": AMBER, "weight": "bold"}),
          ], top=340, gap=70)),
    Scene("recap",
          "今集重點：[[r1]]arithmetic coding 將一段文字變成數線上一個數；[[r2]]用嘅 bit 數，大約係負 log 二模型機率；"
          "[[r3]]所以模型越準，壓得越細；[[r4]]而一個又準、又細、又學得快嘅模型，好似就係我哋講嘅智能。",
          TileCard("今集重點", [
              Tile("📏", "文字 → 一個數", "逐個字母放大數線", "r1", BLUE),
              Tile("🔢", "bits ≈ −log₂ P", "貼住 Shannon 極限", "r2", AMBER),
              Tile("🤖", "模型越準越細", "訓練 ＝ 學做壓縮器", "r3", PURPLE),
              Tile("🧠", "準、細、學得快", "壓縮好似智能", "r4", GREEN),
          ], cols=2, height=250)),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]如果模型估 m、a、t、h 四個字母嘅機率，分別係二分一、四分一、二分一、四分一，成個字大約要幾多個 bit？"
          "[[next]]多謝收睇資訊理論三部曲，下次見！",
          END),
]

build(VIDEO, scenes, opts, say=SAY)
