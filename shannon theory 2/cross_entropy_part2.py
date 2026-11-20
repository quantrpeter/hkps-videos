#!/usr/bin/env python3
"""Cross-entropy 係乜？（資訊理論・第二集）

A Cantonese explainer of cross-entropy for 香港編程學會, rewritten from the ideas in 3Blue1Brown's
"But what is cross-entropy? | Information theory, part 2" (credited on the title and end cards).
The narration is original Cantonese, not a translation; the screens are HKPS cards with their own
animations (entropy_cards.py from part 1, and cross_cards.py), not the original's visuals.

The path: the 2002 "Language Trees and Zipping" gzip trick; the robot's rotated distribution under
the old code (2.625 bits); the formula Σ p·(−log₂ q) as an area; two-outcome examples (1 bit, then
1.74 bits: not symmetric); the curve over q with its minimum at q = p tracing H(p); gzip as rough
cross-entropy; language models, loss and gradient descent; loss as average surprise per token; why
the loss must be a log ("My name is ___" and the Lagrange argument); one-hot targets; distillation;
the bridge back to compression; KL divergence and three puzzles.

Token probabilities, the next-token bars and the language pairs are illustrative (示意數字).

    python3 cross_entropy_part2.py              # -> out/cross_entropy_part2.mp4 (narration is cached)
    python3 cross_entropy_part2.py --draft      # silent, estimated timing, fast: for checking layout
    python3 cross_entropy_part2.py --stills     # two PNGs per scene in build/cross_entropy_part2/stills/
    python3 cross_entropy_part2.py --redo zip   # regenerate one scene's narration
"""

import math
from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D

from cross_cards import CrossCard, CurveCard, FuncGraphCard, HillCard, NameCard, PredictCard, TargetsCard, TokenCard, ZipCard
from entropy_cards import EquationCard, TermsCard

VIDEO = Video(slug=Path(__file__).stem, title="Cross-entropy 係乜？", series="資訊理論")
opts = options(VIDEO)

CREDIT = "內容參考：3Blue1Brown〈But what is cross-entropy?｜Information theory, part 2〉· 廣東話重新編寫"

SAY = {
    "gzip": "G zip",
    "AI": "A I",
    "p": "P",
    "q": "Q",
    "KL divergence": "K L divergence",
    "KL": "K L",
    "token": "token",
    "π": "pi",
    "Language Trees and Zipping": "Language Trees and Zipping",
}


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 44) -> Card:
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


def credit(card: Card, y: int) -> Card:
    card.add_center(D.text_img(CREDIT, font(28), MUTED), y, at=None)
    return card


ARROWS = ["↑", "↓", "←", "→"]
OLD = [0.5, 0.25, 0.125, 0.125]          # the distribution the code was built for (q)
NEW = [0.125, 0.125, 0.25, 0.5]          # the new plan (p)
SIX_P = [0.30, 0.22, 0.18, 0.14, 0.10, 0.06]

END = EndCard("如果機械人嘅四個指令變成機率一樣，但仲用緊舊碼表（0、10、110、111），cross-entropy 同 KL divergence 各係幾多？",
              "第三集：語言模型變壓縮器", challenge_at="ch", next_at="next")
credit(END, 860)

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟資訊理論第二集。上集我哋重新發明咗 entropy，今集講佢嘅兄弟：cross-entropy，交叉熵。"
          "佢一邊同壓縮有關，另一邊，就係訓練大型語言模型嘅 loss。",
          credit(TitleCard(VIDEO.series, "第二集", "Cross-entropy 交叉熵", "Cross-entropy 係乜？",
                           "用錯碼表，要多付幾多 bit？"), 830)),
    Scene("paper",
          "先講一篇二零零二年嘅論文，叫 Language Trees and Zipping。[[a]]佢只用 gzip 呢種普通嘅壓縮工具，"
          "[[b]]就可以將唔同語言嘅文件分類，[[c]]甚至畫得出語言嘅族譜。[[d]]完全唔使語言學知識，亦冇任何 AI 模型。",
          pill(FlowCard("2002：Language Trees and Zipping", [
              Row("輸入", "文件", BLUE, [
                  Node("一堆文件", "唔同語言", "a"),
                  Node("gzip", "普通壓縮工具", ("a", 0.6)),
                  Node("分類", "邊份係咩語言", "b"),
              ]),
              Row("輸出", "族譜", PURPLE, [
                  Node("語言族譜", "邊啲語言似", "c"),
              ]),
          ], top=290, row_h=250), "唔使語言學，唔使 AI", 800, "d", AMBER)),
    Scene("zip",
          "做法好簡單：[[a]]將文件 B 嘅一小段，駁喺文件 A 後面，[[both]]一齊壓縮，再同淨係壓縮 A 嘅大小比較。"
          "[[diff]]多出嚟嗰截，就係用 A 嘅規律去壓 B，要幾多額外 bit。[[pairs]]B 同 A 越似，多出嚟嘅就越少。",
          ZipCard("gzip 點樣量語言有幾似？", docs_at="a", both_at="both", diff_at="diff", pairs_at="pairs")),
    Scene("plan",
          "呢個技巧背後嘅概念，就係 cross-entropy。今集分兩半：[[p1]]上半講 cross-entropy 點樣喺壓縮入面自然出現；"
          "[[p2]]下半講訓練同蒸餾語言模型，[[p3]]睇吓佢點解又喺嗰度出現；[[p4]]最後再講 KL divergence。",
          BulletCard("今集路線", [
              ("上半：cross-entropy 點樣喺壓縮入面出現", "p1"),
              ("下半：訓練同蒸餾語言模型", "p2"),
              ("兩邊點樣連埋一齊", "p3"),
              ("補充：KL divergence", "p4"),
          ])),

    # -- cross-entropy from compression ---------------------------------------------------------------
    Scene("recap",
          "先溫一溫上集：[[r1]]機械人收四種指令，上一半、下四分一、左右各八分一；"
          "[[r2]]最好嘅編碼係 0、10、110、111，[[r3]]每個碼長都等於負 log 二 p，即係資訊量。[[r4]]平均一點七五 bit，就係 entropy。",
          TableCard("上集重溫：機械人", ["指令", "機率", "碼", "碼長 = −log₂ p"], [
              (["↑", "½", "0", "1"], "r1"),
              (["↓", "¼", "10", "2"], ("r1", 0.5)),
              (["←、→", "⅛", "110、111", "3"], ("r1", 1.0)),
          ], widths=[0.7, 0.7, 1, 1.4], code_cols=(2,), size=46, note=("平均 1.75 bits：就係 entropy", "r4"))),
    Scene("change",
          "而家太空總署改咗計劃，想機械人多啲向右行：[[n1]]上同下各八分一，[[n2]]左四分一，[[n3]]右一半。"
          "[[q]]但機械人嘅編碼已經寫死咗，仲用緊舊碼表。咁會嘥幾多？",
          pill(TableCard("新計劃：多啲向右", ["指令", "舊機率", "新機率", "舊碼"], [
              (["↑", "½", "⅛", "0"], "n1"),
              (["↓", "¼", "⅛", "10"], ("n1", 0.5)),
              (["←", "⅛", "¼", "110"], "n2"),
              (["→", "⅛", "½", "111"], "n3"),
          ], widths=[0.7, 1, 1, 1], code_cols=(3,), size=46), "碼表冇變：會嘥幾多？", 760, "q", RED)),
    Scene("compute",
          "計吓：[[t1]]一個 bit 嘅上，而家只有八分一機會；[[t2]]兩個 bit 嘅下，都係八分一；"
          "[[t3]]三個 bit 嘅左同右，[[t4]]加埋有四分三機會。[[sum]]平均變成二點六二五 bit。"
          "[[name]]呢個數，就叫 cross-entropy。",
          TermsCard("舊碼表 + 新分佈：平均幾多 bit？", [
              ("⅛ × 1", "t1", BLUE),
              ("+ ⅛ × 2", "t2", TEAL),
              ("+ ¼ × 3", "t3", AMBER),
              ("+ ½ × 3", "t4", PURPLE),
              ("= 2.625", "sum", RED),
          ], y=400, lines=[("用啱碼表：1.75 bits", "sum", MUTED, 44)],
              pill=("呢個就係 cross-entropy", "name", RED))),
    Scene("formula",
          "推廣一下：舊分佈叫 q，新分佈叫 p。[[e1]]為 q 設計嘅編碼，每個符號用負 log 二 q 個 bit；"
          "[[e2]]如果現實真係 q，平均就係 q 嘅 entropy。[[e3]]但如果現實係 p，就要用 p 做權重：p 乘負 log 二 q，全部加埋。",
          EquationCard("Cross-entropy 嘅公式", [
              ("為 q 設計嘅碼：每個符號 -log_2 q_i bits", "e1", {"size": 50}),
              ("現實係 q：H(q) = Σ q_i × (-log_2 q_i)", "e2", {"size": 50}),
              ("現實係 p：H(p, q) = Σ p_i × (-log_2 q_i)", "e3", {"size": 58, "box": RED, "weight": "bold"}),
          ], top=300, gap=56, pill=("寫法唔統一，記住條式就得", ("e3", 2.5), MUTED))),
    Scene("area",
          "畫出嚟：[[w]]每段嘅闊度係實際機率 p，[[h]]每格嘅高度係舊碼表嘅碼長，負 log 二 q。"
          "[[val]]總面積，就係 cross-entropy：二點六二五。[[cmp]]最常見嘅右，偏偏用緊三個 bit 嘅長碼，所以嘥咗。",
          pill(CrossCard("Cross-entropy：闊度 p，高度 −log₂ q", [(None, NEW, OLD)], labels=ARROWS, strip_at="w",
                         blocks_at=("h", 0.3), value_at="val", digits=3),
               "最常見嘅「右」用緊 3 bits 長碼", 880, "cmp", RED, size=38)),
    Scene("two1",
          "用最簡單嘅例子建立直覺：只有兩個結果。[[a]]q 係五五分，所以每個結果都係一個 bit。"
          "[[b]]就算現實 p 變成九一分，[[c]]因為每個結果都係一個 bit，平均都係一個 bit。",
          CrossCard("兩個結果：q = 50 / 50", [(None, [0.5, 0.5], [0.5, 0.5]), ("b", [0.9, 0.1], [0.5, 0.5])],
                    labels=["A", "B"], value_at="a")),
    Scene("two2",
          "反轉過嚟：[[a]]q 係九一分，常見嗰個好平，零點一五 bit，罕見嗰個要三點三 bit。"
          "[[b]]但如果現實係五五分，[[c]]罕見嗰個成日出現，平均變成一點七四 bit。[[d]]所以 p 同 q 唔可以調轉：cross-entropy 唔對稱。",
          pill(CrossCard("兩個結果：q = 90 / 10", [(None, [0.9, 0.1], [0.9, 0.1]), ("b", [0.5, 0.5], [0.9, 0.1])],
                         labels=["A", "B"], value_at="a"), "H(p, q) ≠ H(q, p)", 880, "d", RED, size=40)),
    Scene("curve",
          "兩個結果嘅時候，p 同 q 各自得一個數，可以畫圖。[[fix]]固定 p，將 cross-entropy 畫成 q 嘅函數，"
          "[[min]]會見到一個好清楚嘅最低點，[[eq]]就喺 q 等於 p 嗰度。[[why]]好合理：碼表同現實一致，壓縮先最有效率。",
          CurveCard("固定 p，改變 q", [(None, 0.3)], curve_at="fix", min_at="min", eq_at="eq")),
    Scene("trace",
          "而家郁吓 p，[[move]]成條曲線跟住變，最低點亦跟住走。[[back]]將最低點行過嘅路畫出嚟，就係呢條綠色曲線。"
          "[[what]]佢係乜？最低點代表現實係 p 嘅時候，最好嘅壓縮，即係 p 嘅 entropy。",
          CurveCard("郁吓 p：最低點去咗邊？", [(None, 0.3), ("move", 0.75), ("back", 0.12), ("what", 0.5)],
                    min_at=None, trace_at="move")),
    Scene("fact",
          "所以 cross-entropy 最重要嘅性質係：[[k1]]固定 p，佢喺 q 等於 p 嘅時候最細；[[k2]]而最細嗰個值，就係 p 嘅 entropy。"
          "[[k3]]多過兩個結果都一樣：用錯碼表，只會嘥 bit，唔會賺。",
          pill(CrossCard("多個結果：q 越似 p，面積越細", [
              (None, SIX_P, [0.05, 0.10, 0.15, 0.20, 0.25, 0.25]),
              ("k1", SIX_P, SIX_P),
          ], value="both", value_at=None, ref_at="k2"), "用錯碼表：只會嘥，唔會賺", 880, "k3", RED, size=38)),
    Scene("gzipce",
          "返去 gzip 嘅例子：[[a]]先壓 A，壓縮器就熟咗 A 嘅規律；[[b]]再壓 B 嘅一小段，量嘅就係為 A 優化嘅壓縮，應付 B 有幾差。"
          "[[c]]呢個正正就係 cross-entropy 問嘅問題。[[d]]當然只係粗略估計，因為 gzip 只係搵重複片段，遠遠未去到 Shannon 極限。",
          TableCard("gzip 技巧 ≈ cross-entropy", ["gzip 技巧", "Cross-entropy"], [
              (["為 A 優化嘅壓縮", "為 q 設計嘅碼表"], "a"),
              (["B 嘅一小段", "現實分佈 p"], "b"),
              (["多出嚟嘅大小", "H(p, q)"], "c"),
          ], code_cols=(), size=46, note=("粗略估計：gzip 只係搵重複片段", "d"))),

    # -- training language models --------------------------------------------------------------------------
    Scene("lm",
          "下半場：語言模型。[[tok]]模型將文字切成 token，即係字或者字嘅一部分；[[fn]]佢係一個函數，輸入一段文字，"
          "[[out]]輸出下一個 token 嘅機率分佈。",
          PredictCard("語言模型：一個函數", "香港編程", [("學", 0.55), ("比", 0.12), ("課", 0.08), ("嘅", 0.06), ("…", 0.04)],
                      in_at="tok", model_at="fn", out_at="out")),
    Scene("hill",
          "訓練模型，要有一個 loss function，量度佢估得好唔好。[[go]]訓練就好似落山：用 gradient descent 同 backpropagation，"
          "一步步調校幾十億個參數，令 loss 越嚟越細。[[key]]所以最重要嘅設計，就係揀邊條 loss。",
          HillCard("訓練 ＝ 將 loss 推到最低", go="go", pill=("關鍵：揀邊條 loss？", "key", RED))),
    Scene("tokens",
          "語言模型用嘅 loss 可以咁理解：[[go]]睇住訓練資料每一個 token，問模型：你估真正嗰個 token 有幾大機率？"
          "[[log]]再取負 log，即係模型覺得有幾意外。[[avg]]所有 token 平均落嚟，就係 loss：模型角度嘅平均資訊量。",
          TokenCard("Loss ＝ 模型角度嘅平均資訊量", ["It", "was", "the", "best", "of", "times"],
                    [0.02, 0.30, 0.55, 0.22, 0.85, 0.62], start="go", end=("log", 1.0), avg_at="avg")),
    Scene("steep",
          "[[smart]]聰明嘅模型好少覺得意外，真正答案機率高，loss 就低；[[dumb]]亂估嘅模型乜都覺得意外，loss 就高。"
          "[[steep]]負 log 嘅形狀亦好合理：真正答案你只估百分之一，就會罰得好重。",
          FuncGraphCard("估得越離譜，罰得越重", [(lambda q: -math.log2(q), BLUE, "−log₂ q", None)], points=[
              (0.9, 0, "估 90%：罰 0.15", "smart"), (0.25, 0, "估 25%：罰 2", "dumb"), (0.01, 0, "估 1%：罰 6.6", "steep")])),
    Scene("whylog",
          "不過，同樣形狀嘅函數多的是：[[f1]]例如一減 q，[[f2]]或者一除 q 減一。[[q]]點解偏偏要用 log？"
          "[[ln]]順帶一提，機器學習通常用自然對數，同 log 二只差一個常數倍，冇本質分別。",
          FuncGraphCard("咁多形狀差唔多嘅函數", [
              (lambda q: -math.log2(q), BLUE, "−log₂ q", None),
              (lambda q: 3 * (1 - q), TEAL, "3 × (1 − q)", "f1"),
              (lambda q: 1 / q - 1, AMBER, "1/q − 1", "f2"),
          ], pill=("點解係 log？", "q", RED), note=("ln q = log_2 q × ln 2", "ln"))),
    Scene("names",
          "睇一個例子：My name is 空格。[[data]]訓練資料入面會出現好多次，常見嘅名多啲，罕見嘅少啲。"
          "[[p]]用 p 代表每個名喺資料入面嘅比例，[[q]]用 q 代表模型估每個名嘅機率。[[avg]]平均 loss，就係用 p 做權重嘅加權平均。",
          NameCard("My name is ___", [("Alice", 4), ("Bob", 3), ("Charlie", 2), ("Dora", 1)],
                   [(None, [0.25, 0.25, 0.25, 0.25])], data_at="data", p_at="p", q_at="q",
                   formula=("平均 loss = Σ p_i × f(q_i)", "avg"))),
    Scene("names2",
          "如果 f 係負 log，[[ce]]呢條式就正正係 cross-entropy：模型 q 相對資料 p 嘅 cross-entropy。"
          "[[move]]而佢喺 q 等於 p 嘅時候最細。[[done]]即係話，loss 最低嘅時候，模型估嘅機率，正正就係資料入面嘅比例。",
          NameCard("f ＝ −log：平均 loss 就係 cross-entropy", [("Alice", 4), ("Bob", 3), ("Charlie", 2), ("Dora", 1)],
                   [(None, [0.25, 0.25, 0.25, 0.25]), ("move", [0.4, 0.3, 0.2, 0.1])], loss_at="ce",
                   formula=("Σ p_i × (-log_2 q_i) = H(p, q)", "ce"))),
    Scene("forced",
          "更妙嘅係反過嚟都成立：[[want]]如果你要求 loss 只喺模型同資料一致嘅時候最細，"
          "[[lag]]用 Lagrange multiplier 一計，條件會變成 f 嘅導數等於常數除 q，[[only]]而只有 log 有呢個性質。"
          "[[forced]]所以用 log 唔係揀出嚟，係被迫出嚟。",
          EquationCard("點解一定係 log？", [
              ("要求：Σ p_i × f(q_i) 只喺 q = p 最細", "want", {"size": 50}),
              ("Lagrange multiplier → f'(q) = c / q", "lag", {"size": 50}),
              ("f(q) = -log q", "only", {"size": 72, "box": AMBER, "weight": "bold"}),
          ], top=300, gap=56, pill=("唔係揀出嚟，係被迫出嚟", "forced", AMBER))),
    Scene("onehot",
          "咁點解叫 cross-entropy loss？[[usual]]常見講法係：將正確答案當成一個分佈，正確 token 佔百分之一百，其他全部係零；"
          "[[gone]]代入條式，零全部消失，只剩負 log q。[[real]]但真正原因係頭先嗰個：平均落所有例子，loss 本身就係 cross-entropy。",
          EquationCard("點解叫 cross-entropy loss？", [
              ("p = (0, …, 0, 1, 0, …, 0)", "usual", {"size": 54}),
              ("Σ p_i × (-log q_i) = -log q_{正確}", "gone", {"size": 54}),
          ], top=310, gap=60, pill=("真正原因：平均落所有例子 ＝ cross-entropy", "real", BLUE))),
    Scene("distill",
          "Cross-entropy 用得最直接嘅地方，係 distillation，蒸餾。[[goal]]目標係訓練一個細模型，模仿一個大模型。"
          "[[one]]普通訓練，每個位置只得一個正確答案；[[soft]]蒸餾就同大模型成個分佈比，loss 係細模型相對大模型嘅 cross-entropy。",
          TargetsCard("蒸餾：同大模型成個分佈比", ["Alice", "Bob", "Charlie", "Dora"], [
              ("普通訓練：一個答案", MUTED, [1.0, 0, 0, 0], "one"),
              ("蒸餾：大模型嘅分佈", BLUE, [0.42, 0.28, 0.19, 0.11], "soft"),
          ])),
    Scene("chess",
          "就好似學捉棋：[[a]]普通訓練，似淨係睇人落棋，每步只見到一個答案；"
          "[[b]]蒸餾就似有個高手喺隔籬，話你知每步有邊啲好棋，各有幾好。[[c]]所以細模型唔使睇幾百萬次 My name is，一次就學到成個分佈。",
          CompareCard("好似學捉棋", [
              Column("👀", "普通訓練", [("淨係睇人落棋", "a"), ("每步只見到一個答案", ("a", 1.2))], MUTED),
              Column("🧑‍🏫", "蒸餾", [("有高手喺隔籬講解", "b"), ("每步有邊啲好棋、各有幾好", ("b", 1.5))], BLUE),
          ], footer=("一個例子，就學到成個分佈", "c", BLUE))),

    # -- tying it together -----------------------------------------------------------------------------
    Scene("halves",
          "總結兩半：[[a]]上半，cross-entropy 嚟自壓縮：為一個情況優化嘅編碼，用喺另一個情況有幾好。"
          "[[b]]下半，佢喺訓練語言模型出現，原因係一個最佳化嘅論證。",
          FlowCard("兩次出現，同一條式", [
              Row("上半", "壓縮", BLUE, [Node("碼表 q", "為 q 優化", "a"), Node("現實 p", "平均幾多 bit", ("a", 0.8)),
                                       Node("H(p, q)", "cross-entropy", ("a", 1.6))]),
              Row("下半", "訓練", PURPLE, [Node("模型 q", "估下一個 token", "b"), Node("資料 p", "真實比例", ("b", 0.8)),
                                         Node("Loss", "cross-entropy", ("b", 1.6))]),
          ], top=290, row_h=270)),
    Scene("bridge",
          "就好似 π 出現嘅地方，總會同圓有關，[[c]]cross-entropy 出現嘅地方，總會同壓縮有關。"
          "[[d]]第三集會講點樣將語言模型變成壓縮器，到時就會見到：訓練語言模型，其實就係訓練一個最好嘅文字壓縮器。",
          EquationCard("π 同圓，cross-entropy 同壓縮", [
              ("π 出現 → 背後總有圓", None, {"size": 56}),
              ("cross-entropy 出現 → 背後總有壓縮", "c", {"size": 56}),
              ("訓練語言模型 = 訓練最好嘅文字壓縮器", "d", {"size": 56, "box": AMBER, "weight": "bold"}),
          ], top=310, gap=60, pill=("第三集：語言模型點樣變壓縮器", ("d", 2.0), BLUE))),
    Scene("kl",
          "最後補充一個常見概念：KL divergence。[[d]]cross-entropy 最細係 p 嘅 entropy，兩者嘅差，就叫 KL divergence。"
          "[[waste]]用壓縮嘅講法，就係用錯碼表，每個符號嘥咗幾多 bit。[[robot]]機械人例子：二點六二五減一點七五，每個指令嘥零點八七五 bit。",
          EquationCard("KL divergence：嘥咗幾多 bit", [
              ("D_{KL}(p || q) = H(p, q) - H(p)", "d", {"size": 60, "box": PURPLE, "weight": "bold"}),
              ("用錯碼表，每個符號嘥咗幾多 bit", "waste", {"size": 50}),
              ("機械人：2.625 - 1.75 = 0.875 bits", "robot", {"size": 54}),
          ], top=300, gap=56)),
    Scene("klpic",
          "畫出嚟：[[ref]]紅色虛線係用啱碼表嘅高度，負 log 二 p；[[gap]]實際面積比虛線多出嚟嘅部分，就係 KL divergence。"
          "[[asym]]佢好似一種距離：兩個分佈一樣就係零，越唔同越大；但佢唔對稱，p 對 q 同 q 對 p 唔一樣。",
          pill(CrossCard("KL：實際面積 − 啱碼表嘅面積", [(None, NEW, OLD)], labels=ARROWS, ref_at="ref", value="kl",
                         value_at="gap", digits=3), "似距離，但唔對稱", 880, "asym", PURPLE, size=38)),
    Scene("puzzles",
          "留三條問題俾你諗：[[q1]]第一，KL 常見嘅寫法係 p 乘 log p 除 q 加埋，點解同兩者相減一樣？"
          "[[q2]]第二，喺頭先個圖入面，KL 對應邊一部分？[[q3]]第三，蒸餾嘅時候，用 KL 代替 cross-entropy 做 loss，會有咩分別？",
          BulletCard("三條問題俾你諗", [
              ("KL = Σ p × log(p / q)：點解同 H(p, q) − H(p) 一樣？", "q1"),
              ("喺面積圖入面，KL 對應邊一部分？", "q2"),
              ("蒸餾用 KL 代替 cross-entropy，會有咩分別？", "q3"),
          ])),
    Scene("recap2",
          "今集重點：[[r1]]cross-entropy 係用為 q 而設嘅編碼，應付現實 p 嘅平均 bit 數；"
          "[[r2]]佢喺 q 等於 p 嘅時候最細，最細就係 p 嘅 entropy；[[r3]]訓練語言模型嘅 loss，平均落嚟就係 cross-entropy；"
          "[[r4]]多出嚟嘅部分，就係 KL divergence。",
          TileCard("今集重點", [
              Tile("📦", "Cross-entropy", "用 q 嘅碼表應付 p：平均幾多 bit", "r1", BLUE),
              Tile("🎯", "最細 ＝ H(p)", "q 等於 p 嘅時候最細", "r2", GREEN),
              Tile("🤖", "語言模型 loss", "平均落嚟就係 cross-entropy", "r3", PURPLE),
              Tile("🗑️", "KL divergence", "用錯碼表嘥咗幾多 bit", "r4", RED),
          ], cols=2, height=250)),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]如果機械人四個指令變成機率一樣，但仲用緊舊碼表，cross-entropy 同 KL divergence 各係幾多？"
          "[[next]]多謝收睇，第三集見！",
          END),
]

build(VIDEO, scenes, opts, say=SAY)
