#!/usr/bin/env python3
"""重新發明 Entropy：壓縮嘅極限（資訊理論・第一集）

A Cantonese explainer of Shannon's information and entropy, rewritten for 香港編程學會 from the
ideas in 3Blue1Brown's "Reinventing Entropy | Information theory, part 1" (credited on the title
and end cards). The narration is original Cantonese, not a translation; the screens are HKPS cards
with their own animations (entropy_cards.py), not the original's visuals.

The path: how few bits can text use? A moon robot with instructions ↑½ ↓¼ ←⅛ →⅛; a 2-bit code
against 0/10/110/111 (1.75 bits); decoding and prefix-free codes on the code-space diagram;
"perfect compression looks like random noise", which gives bits = −log₂ p; information of an event;
letters of language and the chain rule; Shannon's guessing experiments; entropy as an area;
the noiseless coding theorem; English at about 1 bit per letter.

Letter probabilities and the TH table are illustrative (the cards say 示意數字).

    python3 entropy_part1.py              # -> out/entropy_part1.mp4 (narration is cached)
    python3 entropy_part1.py --draft      # silent, estimated timing, fast: for checking layout
    python3 entropy_part1.py --stills     # two PNGs per scene in build/entropy_part1/stills/
    python3 entropy_part1.py --redo robot # regenerate one scene's narration
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D
from hkpsvid.style import LINE

from entropy_cards import (CLEVER, NAIVE, Claim, CodeSpaceCard, CueBarCard, DecodeCard, EntropyCard, EquationCard,
                           GraphCard, GuessCard, LetterCard, NoiseCard, PieBarCard, RobotCard, StreamCard, TermsCard,
                           TreeCard)

VIDEO = Video(slug=Path(__file__).stem, title="重新發明 Entropy", series="資訊理論")
opts = options(VIDEO)

CREDIT = "內容參考：3Blue1Brown〈Reinventing Entropy｜Information theory, part 1〉· 廣東話重新編寫"

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "ASCII": "ask key",
    "n": "N",
    "p": "P",
    "H": "H",
    "TH": "T H",
    "AI": "A I",
    "cross-entropy": "cross entropy",
    "prefix-free code": "prefix free code",
    "《Prediction and Entropy of Printed English》": "Prediction and Entropy of Printed English",
}


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 44) -> Card:
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


def credit(card: Card, y: int) -> Card:
    card.add_center(D.text_img(CREDIT, font(28), MUTED), y, at=None)
    return card


SEQ = "↑↓↑↑←↑↓↑→↑↑↓←↑↓→"          # 8 up, 4 down, 2 left, 2 right: 32 bits naive, 28 bits clever
LABELS = ["↑", "↓", "←", "→"]
ROBOT = [0.5, 0.25, 0.125, 0.125]
WORD_P = [0.05, 0.28, 0.01, 0.41, 0.98, 0.97, 0.75, 0.98, 0.99, 0.99, 0.99]    # INFORMATION, illustrative

GUESS_TEXT = "THERE IS NO PLACE LIKE HOME"
GUESS_MARK = "x..x. x. x. x.x.. x... ...."   # x: guessed wrong, so the letter is written down

QUOTE = Card("點解叫 entropy？")
_q = D.shadow_box(1500, 330, 30, WHITE, outline=LINE)
_p = _q.info["pad"]
_q.alpha_composite(D.text_img("「冇人真係知 entropy 係乜，\n所以辯論嘅時候，你一定佔上風。」", font(58, "bold"), NAVY,
                              line_h=1.5), (_p + 70, _p + 60))
QUOTE.add_center(_q, 290, at="q2", anim="pop", sound="pop")
QUOTE.add(D.text_img("— 據講係 von Neumann 對 Shannon 講嘅", font(38, "medium"), MUTED), 900, 660, "q2", anim="fade")
QUOTE.add_center(D.pill("呢個故事好可能係杜撰", font(36, "bold"), WHITE, MUTED, px=30, py=10), 760, at="note",
                 anim="pop", sound="pop")

END = EndCard("如果上、下、左、右四個指令機率一樣，最好嘅編碼平均要幾多 bit？用 entropy 計吓，再諗吓點解。",
              "下集：Cross-entropy", challenge_at="ch", next_at="next")
credit(END, 860)

scenes = [
    # -- the question ----------------------------------------------------------------------------
    Scene("intro",
          "大家好！歡迎收睇香港編程學會。今集講一個好根本嘅問題：一段文字，最少要用幾多個 bit 先存得落？"
          "答呢條問題嘅過程，會帶我哋重新發明資訊理論最重要嘅兩個概念：information 同 entropy。",
          credit(TitleCard(VIDEO.series, "第一集", "Entropy 熵", "重新發明 Entropy：壓縮嘅極限",
                           "一段文字，最少要用幾多個 bit？"), 830)),
    Scene("ascii",
          "電腦用 ASCII 存英文，[[b0]]每個字母用八個 bit，好嘥位。[[b1]]如果常用嘅字母用短啲嘅碼，平均可以減到大約四個 bit；"
          "[[b2]]再聰明啲，睇埋成段文字嘅規律，仲可以再少。[[b3]]咁，極限喺邊？",
          CueBarCard("每個字母要用幾多 bit？", [
              ("ASCII", 8, "8 bits", MUTED, "b0"),
              ("常用字母短碼", 4, "≈ 4 bits", BLUE, "b1"),
              ("睇成段規律", 2.5, "更少", TEAL, "b2"),
              ("極限", 1.2, "？", RED, "b3"),
          ], top=290, step=140)),
    Scene("why",
          "一九四八年，Claude Shannon 發表咗一篇論文，[[f1]]研究訊息最少要用幾多 bit，開創咗資訊理論。"
          "[[f2]]七十幾年後嘅今日，訓練大型語言模型，[[f3]]用嘅 loss 叫 cross-entropy，個名正正嚟自資訊理論。"
          "[[eq]]資訊理論仲有個結論：預測同壓縮，其實係同一枚銀幣嘅兩面。",
          pill(FlowCard("由 1948 到今日", [
              Row("1948", "Shannon", BLUE, [
                  Node("論文", "資訊理論誕生", "f1"),
                  Node("壓縮", "最少要幾多 bit？", ("f1", 0.8)),
              ]),
              Row("今日", "AI", PURPLE, [
                  Node("語言模型", "估下一個字", "f2"),
                  Node("交叉熵", "cross-entropy loss", "f3"),
              ]),
          ], top=280, row_h=250), "預測同壓縮：一枚銀幣嘅兩面", 800, "eq", AMBER)),
    Scene("plan",
          "今集嘅目標，係等你覺得：Shannon 嘅答案，你自己都發明得到。[[p1]]我哋先用一部月球機械人熱身；"
          "[[p2]]再推導出資訊量嘅公式；[[p3]]然後睇吓語言點計；[[p4]]最後重新發明 entropy。",
          BulletCard("今集路線", [
              ("熱身：月球機械人嘅指令", "p1"),
              ("推導資訊量：−log₂ p", "p2"),
              ("語言：每個字母有幾多資訊？", "p3"),
              ("重新發明 entropy", "p4"),
          ])),

    # -- the robot ---------------------------------------------------------------------------------
    Scene("robot",
          "想像我哋送咗一部機械人去一個好遠嘅月球。[[go]]我哋喺地球發指令，只有四種：上、下、左、右。"
          "[[p]]不過四種指令唔係平均出現：一半係上，四分一係下，左同右各佔八分一。",
          RobotCard("熱身：月球機械人", go="go", probs_at="p")),
    Scene("task",
          "為咗簡單，[[a]]每個指令都係獨立抽出嚟，唔理之前發過乜。[[b]]指令要變成一串 0 同 1 先傳得過去，"
          "[[c]]而太空通訊又慢又貴。[[q]]所以熱身題係：點樣編碼，先可以平均用最少 bit？",
          pill(BulletCard("熱身題", [
              ("每個指令獨立，按機率抽出嚟", "a"),
              ("要轉成一串 0 同 1 先傳得過去", "b"),
              ("太空通訊：又慢又貴", "c"),
          ]), "點樣編碼，平均先用最少 bit？", 720, "q", RED)),
    Scene("naive",
          "最直接嘅方法：每個指令用兩個 bit。[[c]]上係 00，下係 01，左係 10，右係 11。"
          "[[run]]機械人收到之後，兩個兩個咁切開，就解到碼，好簡單。[[avg]]平均每個指令：兩個 bit。",
          StreamCard("方法一：每個指令兩個 bit", SEQ, [("兩個 bit", NAIVE, MUTED)], start="run", end=("avg", -0.2),
                     book_at="c", pill=("平均：每個指令 2 bits", "avg", MUTED))),
    Scene("clever",
          "但係咁樣冇利用到「上」特別常見。[[c]]試吓用長短唔同嘅碼：上用一個 bit，0；下用 10；左用 110；右用 111。"
          "[[run]]同一串指令，用兩種方法編碼，[[cmp]]新方法明顯短啲。",
          StreamCard("方法二：常見嘅用短碼", SEQ, [("兩個 bit", NAIVE, MUTED), ("長短碼", CLEVER, BLUE)],
                     start="run", end=("cmp", -0.2), book_at="c", pill=("32 bits → 28 bits", "cmp", BLUE))),
    Scene("average",
          "計吓平均：[[t1]]一半時間用一個 bit，[[t2]]四分一時間用兩個 bit，[[t3]]剩低兩個八分一，各用三個 bit。"
          "[[sum]]加埋係一點七五個 bit。[[why]]雖然左右用多咗 bit，但佢哋出現得少，所以抵。",
          TermsCard("平均每個指令幾多 bit？", [
              ("½ × 1", "t1", BLUE),
              ("+ ¼ × 2", "t2", TEAL),
              ("+ ⅛ × 3 + ⅛ × 3", "t3", AMBER),
              ("= 1.75", "sum", RED),
          ], y=400, lines=[("比每個 2 bits 少", "sum", MUTED, 44)],
              pill=("長碼留俾少見嘅指令", "why", BLUE))),
    Scene("decode",
          "但長短唔同，機械人點知喺邊度切？[[go]]我哋由佢嘅角度睇：讀到 1，未知係乜；再讀到 0，10 就係下，冇其他可能，即刻記低。"
          "[[g2]]跟住讀到 0，一定係上。[[g3]]再讀 1、1、0，就係左。[[rule]]規則好簡單：一路讀，讀到完整嘅碼就停。",
          DecodeCard("機械人點樣解碼？", ["10", "0", "110", "0", "111", "10", "0"], CLEVER, start="go", end="rule")),
    Scene("prefix",
          "點解咁樣得？因為[[a1]]冇一個碼，係另一個碼嘅開頭。[[a2]]所以讀到完整嘅碼，就可以即刻解。"
          "[[b1]]但如果加多個第五個指令，用 100，[[b2]]讀到 10 嘅時候，就唔知係「下」，定係 100 嘅開頭。"
          "[[sum]]呢種冇衝突嘅編碼，叫 prefix-free code，通常亦叫 prefix code。",
          CompareCard("冇一個碼係另一個嘅開頭", [
              Column("✅", "0、10、110、111", [("冇一個碼係另一個嘅開頭", "a1"), ("讀到完整嘅碼，即刻解", "a2")], GREEN),
              Column("❌", "加多個 100", [("100 嘅開頭係 10", "b1"), ("讀到 10：係「下」，定未讀完？", "b2")], RED),
          ], footer=("Prefix-free code（又叫 prefix code）", "sum", BLUE))),
    Scene("space",
          "有個好靚嘅圖，可以睇晒所有可能嘅碼。[[l1]]第一行係一個 bit：0 同 1；"
          "[[l2]]下面每一行長多一個 bit，每一格都喺佢開頭嗰格下面。[[rule]]所以揀咗一個碼，佢下面成條柱都唔用得。",
          CodeSpaceCard("所有可能嘅碼", depth=4, rows_at=["l1", "l2", ("l2", 0.6), ("l2", 1.2)],
                        claims=[Claim("01", "揀咗", RED, "rule")])),
    Scene("claim",
          "用呢個圖睇長短碼：[[c1]]上揀咗 0，即係佔咗成個空間嘅一半；[[c2]]下揀 10，佔四分一；"
          "[[c3]]左同右，各佔八分一。[[full]]啱啱好用晒，一啲都冇嘥。[[aha]]再睇清楚：佔嘅空間，同每個指令嘅機率，一模一樣。",
          CodeSpaceCard("長短碼佔幾多空間？", depth=4, claims=[
              Claim("0", "↑", BLUE, "c1"), Claim("10", "↓", TEAL, "c2"),
              Claim("110", "←", AMBER, "c3"), Claim("111", "→", PURPLE, ("c3", 0.6)),
          ], fracs=([("0", "½"), ("10", "¼"), ("110", "⅛"), ("111", "⅛")], "aha"),
              pill=("佔用嘅空間 ＝ 出現嘅機率", ("aha", 1.2), BLUE))),

    # -- perfect compression looks like noise ----------------------------------------------------------
    Scene("best",
          "咁一點七五係咪已經最好？會唔會有更聰明嘅方法，將幾個指令夾埋一齊編碼，平均再少啲？"
          "[[idea]]要答呢條問題，有個好妙嘅諗法：[[noise]]完美嘅壓縮，出嚟嘅結果應該同隨機雜訊冇分別。",
          NoiseCard("1.75 已經係最好？", at="noise", pill=("完美壓縮嘅輸出 ≈ 隨機雜訊", ("noise", 1.0), BLUE))),
    Scene("noise",
          "點解？如果輸出仲有規律，[[r]]例如 0 出現得多過 1，[[r2]]咁就仲有得預測，[[r3]]即係仲可以再壓縮。"
          "[[d1]]所以完美壓縮嘅輸出，每個 bit 都應該一半機會係 0，[[d2]]而且互相獨立，[[d3]]冇得再壓。[[sum]]就好似擲公字咁。",
          CompareCard("點解似隨機雜訊？", [
              Column("📉", "仲有規律", [("例如 0 多過 1", "r"), ("即係仲有得預測", "r2"), ("仲可以再壓縮", "r3")], RED),
              Column("🪙", "隨機雜訊", [("每個 bit 一半機會係 0", "d1"), ("互相獨立", "d2"), ("冇得再壓", "d3")], GREEN),
          ], footer=("完美壓縮：每個 bit 都似擲公字", "sum", BLUE))),
    Scene("tree",
          "我哋嘅長短碼，係咪真係咁？[[b1]]第一個 bit：一半機會係上，即係 0；另一半係 1。"
          "[[b2]]如果係 1，下一個 bit 又係一半一半：下就係 0，否則係 1。[[b3]]再落一層，左同右又係一半一半。"
          "[[sum]]每個 bit 都似擲公字，所以呢個編碼真係完美。",
          TreeCard("長短碼：每個 bit 都係擲公字", ["b1", "b2", "b3"], pill=("每個 bit：50% / 50%", "sum", GREEN))),
    Scene("messages",
          "而家唔止講機械人，講任何資料，文字、圖片都得。[[n]]假設完美壓縮之後，收到一段 n 個 bit 嘅訊息。"
          "[[all]]n 個 bit 總共有 2 嘅 n 次方個可能，[[eq]]既然似隨機雜訊，個個機會均等，"
          "[[p]]所以每個原本訊息嘅機率，都係 2 嘅 n 次方分之一。",
          EquationCard("任何資料都一樣", [
              ("收到一段 n 個 bit 嘅訊息", "n", {"size": 54}),
              ("可能嘅組合：2^n 個", "all", {"size": 54}),
              ("似隨機雜訊 → 個個機會均等", "eq", {"size": 54}),
              ("每個訊息嘅機率 p = 1 / 2^n", "p", {"size": 62, "box": BLUE}),
          ], top=290)),
    Scene("rug",
          "點解隨機雜訊冇得再壓？用返個圖：[[s1]]假設有八個機會均等嘅訊息，個個用三個 bit。"
          "[[s2]]如果想慳啲，俾 A 只用兩個 bit，[[s3]]佢就會壓住 B 嗰格。"
          "[[s4]]B 要搬走，但冇空位，唯有同 C 擠埋一格，兩個都變成四個 bit。"
          "[[sum]]慳咗一個 bit，就要蝕多兩個，好似撳低地氈一邊，另一邊就拱起。",
          CodeSpaceCard("想慳 bit？會壓到人", depth=4, claims=[
              Claim("000", "A", BLUE, "s1", until="s2"),
              Claim("001", "B", BLUE, ("s1", 0.15), until="s3"),
              Claim("010", "C", BLUE, ("s1", 0.3), until="s4"),
              Claim("011", "D", BLUE, ("s1", 0.45)),
              Claim("100", "E", BLUE, ("s1", 0.6)),
              Claim("101", "F", BLUE, ("s1", 0.75)),
              Claim("110", "G", BLUE, ("s1", 0.9)),
              Claim("111", "H", BLUE, ("s1", 1.05)),
              Claim("00", "A", AMBER, "s2"),
              Claim("001", "B", RED, "s3", until="s4"),
              Claim("0100", "C", PURPLE, "s4"),
              Claim("0101", "B", PURPLE, ("s4", 0.4)),
          ], pill=("慳 1 bit，蝕 2 bit", "sum", RED))),

    # -- information ---------------------------------------------------------------------------------
    Scene("derive",
          "所以喺完美壓縮入面，[[l0]]一個用 n 個 bit 嘅訊息，機率係 2 嘅負 n 次方。[[l1]]兩邊取 log 二，"
          "[[l2]]再搬個負號過去，就得到：bit 數等於負 log 二 p。[[key]]呢條式，就係成個資訊理論最核心嘅公式。",
          EquationCard("由機率推出 bit 數", [
              ("p = 2^{-n}", "l0", {"size": 68}),
              ("log_2 p = -n", "l1", {"size": 68}),
              ("n = -log_2 p", "l2", {"size": 80, "box": AMBER, "weight": "bold"}),
          ], top=280, gap=44, pill=("成個資訊理論最核心嘅公式", "key", AMBER))),
    Scene("halving",
          "負 log 二 p 點樣理解？佢即係問：要將所有可能性切一半幾多次，先切到 p 咁細。"
          "[[p1]]p 係一半，切一次，一個 bit；[[p2]]四分一，兩個 bit；[[p3]]八分一，三個 bit；[[p4]]十六分一，四個 bit。"
          "[[curve]]畫成曲線，機率越細，數值越大。",
          GraphCard("−log₂ p：切一半要切幾多次？", ["p1", "p2", "p3", "p4"], "curve")),
    Scene("info",
          "[[def]]Shannon 將負 log 二 p 定義為一件事嘅資訊量，就算 p 唔係二嘅次方，計出小數都照用。"
          "[[low]]一件事越難發生，機率越細，資訊量就越大；[[high]]越肯定會發生，資訊量就越接近零。",
          PieBarCard("資訊量：越意外，資訊越多", [(None, 0.5), ("low", 0.02), ("high", 0.95)], formula_at="def")),
    Scene("bound",
          "呢個定義唔只係換個單位咁簡單。[[a]]喺完美壓縮入面，一個訊息用嘅 bit 數，正正等於佢嘅資訊量。"
          "[[b]]就算做唔到完美，資訊量都係一條下限：平均嚟講，冇方法可以壓得再細。",
          pill(BulletCard("資訊量有咩意思？", [
              ("完美壓縮：訊息用嘅 bit 數 ＝ 佢嘅資訊量", "a"),
              ("做唔到完美：資訊量係平均壓縮嘅下限", "b"),
          ]), "資訊量 ＝ 壓縮嘅極限", 640, "b", AMBER)),
    Scene("fit",
          "返去機械人：[[r1]]上，機率一半，資訊量一個 bit，碼長一；[[r2]]下，四分一，兩個 bit，碼長二；"
          "[[r3]]左同右，八分一，三個 bit，碼長三。[[sum]]每個碼長都等於資訊量，所以呢個編碼係完美。",
          TableCard("機械人：碼長 ＝ 資訊量", ["指令", "機率 p", "資訊量 −log₂ p", "長短碼"], [
              (["↑", "½", "1 bit", "0"], "r1"),
              (["↓", "¼", "2 bits", "10"], "r2"),
              (["←、→", "⅛", "3 bits", "110、111"], "r3"),
          ], widths=[0.7, 0.8, 1.3, 1], code_cols=(3,), size=46,
              note=("每個碼長都等於資訊量：完美編碼", "sum"))),

    # -- language ------------------------------------------------------------------------------------
    Scene("letters",
          "機械人嘅機率太整齊，全部係二嘅次方。語言就複雜得多。[[go]]呢度係一個語言模型逐個字母估機率，"
          "[[hi]]好難估嘅字母，資訊量高；[[lo]]好易估嘅，例如 information 後面幾個字母，資訊量幾乎係零。",
          LetterCard("每個字母有幾多資訊？", "INFORMATION", WORD_P, start="go", end="lo")),
    Scene("chain",
          "成句說話嘅機率，[[c1]]等於每個字母嘅機率乘埋，當然，每個機率都係睇住前文計。"
          "[[log]]而 log 會將乘數變成加數，[[sum]]所以成句嘅資訊量，就係每個字母嘅資訊量加埋。",
          EquationCard("成句說話嘅資訊量", [
              ("P(句子) = p_1 × p_2 × p_3 × … × p_n", "c1", {"size": 56}),
              ("-log_2 P = (-log_2 p_1) + (-log_2 p_2) + … + (-log_2 p_n)", "log", {"size": 48}),
              ("總資訊量 = 每個字母嘅資訊量加埋", "sum", {"size": 56, "box": AMBER, "weight": "bold"}),
          ], top=300, gap=60)),
    Scene("fraction",
          "咁一個字母四點幾個 bit，係咪真係有個四點幾 bit 長嘅碼？[[no]]唔係。"
          "[[yes]]真正意思係對成段訊息嚟講：有方法可以將成段文字，壓到差唔多等於資訊量總和，只差一兩個 bit。"
          "[[next]]呢個方法，我哋第三集再講。",
          CompareCard("小數 bit 點理解？", [
              Column("❌", "唔係咁", [("每個字母有個 4.3 bit 長嘅碼", "no")], RED),
              Column("✅", "係咁", [("成段文字壓到 ≈ 資訊量總和", "yes"), ("只差一兩個 bit", ("yes", 1.5))], GREEN),
          ], footer=("實際點壓？第三集再講", "next", BLUE))),
    Scene("ngram",
          "但最大嘅問題係：每個字母嘅機率，點樣得知？[[ng]]Shannon 早期嘅做法，係數書入面嘅字母組合，"
          "例如統計 TH 後面最常跟住乜。[[e]]E 最多，跟住係 A、I、O。"
          "[[prob]]問題係前文一長，書入面根本冇出現過，但偏偏前文越長，越容易估中。",
          CueBarCard("TH 後面通常跟乜？", [
              ("THE", 0.62, "", BLUE, "e"),
              ("THA", 0.16, "", TEAL, ("e", 0.4)),
              ("THI", 0.12, "", AMBER, ("e", 0.8)),
              ("THO", 0.06, "", PURPLE, ("e", 1.2)),
          ], top=290, step=120, note="示意數字", pill=("前文一長，書入面根本冇出現過", "prob", RED))),
    Scene("betty",
          "於是 Shannon 用咗另一個語言模型：佢太太 Betty。據講，[[go]]佢揀一本書，叫 Betty 逐個字母估，"
          "估中就寫一劃，估唔中就寫低正確嘅字母。[[res]]記錄入面嘅字母少咗好多，但只要有個一模一樣嘅 Betty，就還原得返成句。",
          GuessCard("Shannon 嘅估字遊戲", GUESS_TEXT, GUESS_MARK, start="go", end=("res", -0.3), result_at="res")),
    Scene("paper",
          "後來喺一九五一年，Shannon 發表咗《Prediction and Entropy of Printed English》。"
          "[[a]]今次唔止記估啱定估錯，[[b]]仲記低要估幾多次先估中，再由次數推算機率。"
          "[[c]]佢研究嘅，其實係人腦入面嗰個語言模型，一個睇唔透嘅黑盒。[[d]]到咗今日，我哋由研究黑盒，變成自己設計：大型語言模型。",
          TimelineCard("由人腦到語言模型", [
              Event("1951", "Prediction and Entropy", "of Printed English", "a", BLUE),
              Event("方法", "估幾多次先中", "再推算機率", "b", TEAL),
              Event("本質", "研究人腦", "一個睇唔透嘅黑盒", "c", PURPLE),
              Event("2020s", "自己設計黑盒", "大型語言模型", "d", AMBER),
          ])),

    # -- entropy -------------------------------------------------------------------------------------
    Scene("entropy",
          "終於可以重新發明 entropy。[[q]]問題係：一個訊號，平均每個符號有幾多資訊？"
          "[[bars]]下面每段嘅闊度係機率，上面每格嘅高度係資訊量。[[area]]所以總面積，就係 p 乘負 log 二 p，全部加埋。"
          "[[val]]機械人嘅答案係一點七五，同我哋之前計嘅一樣。",
          EntropyCard("Entropy：平均資訊量", [(None, ROBOT, LABELS)], strip_at="bars", blocks_at=("bars", 1.2),
                      value_at="val", formula_at="area")),
    Scene("name",
          "點解叫 entropy？有個傳聞話，von Neumann 叫 Shannon 用呢個名，[[q1]]一來統計力學已經有條差唔多嘅式；"
          "[[q2]]二來冇人真係知 entropy 係乜，辯論嘅時候你一定佔上風。[[note]]呢個故事好可能係杜撰，但 Shannon 最後真係叫佢 entropy，用 H 代表。",
          QUOTE),
    Scene("play",
          "我哋玩吓佢。[[even]]分佈越平均，entropy 越高：四個機會均等嘅符號，係兩個 bit。"
          "[[skew]]如果一個符號差唔多包晒，entropy 就好低，因為佢冇乜資訊。"
          "[[more]]符號越多，例如十六個平均分，就係四個 bit。[[sum]]直覺上，entropy 量度嘅係：有幾唔確定。",
          pill(EntropyCard("玩吓 entropy", [
              (None, ROBOT, LABELS),
              ("even", [0.25] * 4, LABELS),
              ("skew", [0.94, 0.02, 0.02, 0.02], LABELS),
              ("more", [1 / 16] * 16, None),
          ]), "Entropy ＝ 有幾唔確定", 868, "sum", BLUE, size=38)),
    Scene("theorem",
          "精確啲講，entropy 就係呢種訊號，平均每個符號最少要用幾多 bit。[[t1]]呢個就係 Shannon 一九四八年嘅 noiseless coding theorem："
          "[[t2]]冇任何編碼可以平均低過 entropy；[[t3]]但係你可以無限咁接近佢。",
          TileCard("Noiseless coding theorem（1948）", [
              Tile("🚫", "冇得低過 H", "任何編碼，平均都唔會少過 H", "t2", RED),
              Tile("🎯", "可以無限接近 H", "將越嚟越長嘅訊息一齊編碼", "t3", GREEN),
          ], cols=2, height=300, footer=("Entropy ＝ 平均每個符號最少要幾多 bit", "t1"))),
    Scene("english",
          "語言就複雜得多，每個字母嘅分佈都唔同，要用一個叫 entropy rate 嘅概念，[[est]]而且冇公式計得到，Shannon 只能靠實驗估。"
          "[[one]]當估嘅人睇到前面一百個字母，佢估計英文大約係每個字母一個 bit。"
          "[[wow]]即係話，英文理論上可以壓到每個字母一條是非題咁少。",
          CueBarCard("英文每個字母要幾多 bit？", [
              ("ASCII", 8, "8 bits", MUTED, None),
              ("常用字母短碼", 4, "≈ 4 bits", BLUE, None),
              ("Shannon 估計", 1, "≈ 1 bit", GREEN, "one"),
          ], top=300, step=150, pill=("每個字母 ≈ 一條是非題", "wow", GREEN))),

    # -- wrap up ---------------------------------------------------------------------------------------
    Scene("recap",
          "總結一下：[[r1]]一件事嘅資訊量係負 log 二 p，越意外，資訊越多；[[r2]]entropy 係平均資訊量，亦即係壓縮嘅極限；"
          "[[r3]]要知道語言有幾難壓，就要有個識預測嘅模型。[[next]]下一集，我哋講 cross-entropy，同埋點解訓練語言模型會用佢。",
          TileCard("今集重點", [
              Tile("🎲", "資訊量", "−log₂ p：越意外，資訊越多", "r1", AMBER),
              Tile("📦", "Entropy", "平均資訊量 ＝ 壓縮嘅極限", "r2", BLUE),
              Tile("🧠", "預測 ＝ 壓縮", "估得越準，壓得越細", "r3", PURPLE),
          ], cols=3, height=320, footer=("下集：Cross-entropy", "next"))),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]如果四個指令機率一樣，最好嘅編碼平均要幾多 bit？用 entropy 計吓。[[next]]多謝收睇，下集見！",
          END),
]

build(VIDEO, scenes, opts, say=SAY)
