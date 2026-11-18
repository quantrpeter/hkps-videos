#!/usr/bin/env python3
"""零 Code PM 點樣為禍香港

A satire of the 「零 Code PM」: the Hong Kong IT slang (Wikipedia: 零Code PM) for a software
project manager with no software-development knowledge. The running joke is the for loop: the PM
who thinks sending email to 1,000 customers means writing 1,000 lines. The video then teaches the
for loop in 30 seconds, and goes through the harms and causes the Wikipedia article lists
(credited on screen), a self-test, and a fair word on what a PM really needs to know.

The characters and dialogue are made up; no real person, company or project is named.

    python3 zero_code_pm.py              # -> out/zero_code_pm.mp4 (narration is cached; reruns are quick)
    python3 zero_code_pm.py --draft      # silent, estimated timing, fast: for checking layout
    python3 zero_code_pm.py --stills     # two PNGs per scene in build/zero_code_pm/stills/ (add --draft to skip TTS)
    python3 zero_code_pm.py --redo chat  # regenerate one scene's narration
    python3 zero_code_pm.py --help
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D

VIDEO = Video(slug=Path(__file__).stem, title="零 Code PM 點樣為禍香港", series="IT 職場講堂")
opts = options(VIDEO)

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "PM": "P M",
    "IT": "I T",
}

SOURCE = "資料來源：維基百科「零Code PM」條目，及其引用嘅香港 IT 討論區帖文"

PM = ("👔", "PM", PURPLE)
DEV = ("💻", "Programmer", TEAL)


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 42) -> Card:
    """Adds a centred coloured pill to any card (a punchline or a takeaway)."""
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


def source(card: Card, y: int = 868) -> Card:
    """The small credit line for scenes that report what the Wikipedia article says."""
    card.add_center(D.text_img(SOURCE, font(28), MUTED), y, at=None)
    return card


PM_CODE = """send_email(customer_1)
send_email(customer_2)
send_email(customer_3)
# ……仲有 996 行……
send_email(customer_1000)"""

FOR_CODE = """for customer in customers:
    send_email(customer)"""

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟 IT 職場講堂。上集講到，IT 團隊由上到下都要識 technical。"
          "今集，我哋講一個香港 IT 界人人識、人人怕嘅物種：零 Code PM。",
          TitleCard(VIDEO.series, "吐糟篇", "零 Code PM", VIDEO.title, "連 for loop 都唔識，點帶 IT 項目？")),
    Scene("what",
          "零 Code PM 呢個詞，由三部分組成：[[p0]]零，[[p1]]code，[[p2]]同埋 PM，即係 Project Manager。"
          "[[note]]意思就係：完全唔識軟件開發，但係就管住成個軟件項目嘅項目經理。"
          "[[src]]根據維基百科，呢個講法喺二零一零年代，由香港 IT 討論區開始流行。",
          pill(source(AnatomyCard("零 Code PM 係乜？", [
              Part("0", "零", RED, "p0"),
              Part(" Code ", "寫程式", BLUE, "p1"),
              Part("PM", "項目經理", PURPLE, "p2"),
          ], size=120, y=330, note=("唔識軟件開發，但管住成個軟件項目", "note"))),
               "2010 年代 · 香港 IT 討論區", 760, "src", BLUE)),
    Scene("chat",
          "睇吓一個經典場面。[[m1]]PM 問：系統要 send email 俾一千個客，你幾時寫完？"
          "[[m2]]Programmer 答：一個 for loop 就搞掂，十分鐘。"
          "[[m3]]PM 話：For 乜嘢？一千個客，咪要寫一千行？我俾你兩個禮拜。"
          "[[out]]For loop，就係零 Code PM 從未聽過嘅神秘力量。",
          ChatCard("經典場面", [PM, DEV], [
              Msg(0, "系統要 send email 俾一千個客，你幾時寫完？", "m1"),
              Msg(1, "一個 for loop 就搞掂，十分鐘。", "m2"),
              Msg(0, "For 乜嘢？一千個客，咪要寫一千行？我俾你兩個禮拜。", "m3"),
          ], footer=("For loop：零 Code PM 從未聽過嘅神秘力量", "out", RED))),
    Scene("code",
          "PM 心目中嘅 code 係咁：[[bad]]一行 send 一個客，一千個客就寫一千行。"
          "[[good]]但係識 for loop 嘅人，兩行就寫完：同每一個客，做同一件事。"
          "[[joke]]一千個客係兩行，一百萬個客，都係兩行。",
          pill(CodeCompareCard("一千個客，要寫幾多行？", [
              Pane("PM 心目中嘅 code：1000 行", PM_CODE, good=False, at="bad", name="send.py"),
              Pane("識 for loop：2 行", FOR_CODE, good=True, at="good", name="send.py"),
          ]), "1000 個客：2 行　·　100 萬個客：都係 2 行", 700, "joke", GREEN)),
    Scene("lesson",
          "既然咁，我哋免費幫 PM 補補課。[[a1]]for，即係重複做；[[a2]]customer，每次攞一個客出嚟；"
          "[[a3]]in customers，由客戶名單度攞；[[a4]]後面嗰句，就係每個客都要做嘅嘢。"
          "[[note]]三十秒學識，唔使兩個禮拜。",
          AnatomyCard("For loop 速成班（PM 專用）", [
              Part("for", "重複做", BLUE, "a1"),
              Part(" customer", "每次攞一個客", TEAL, "a2"),
              Part(" in customers:", "由客戶名單度攞", PURPLE, "a3"),
              Part(" send_email(customer)", "每個客都做", GREEN, "a4"),
          ], y=380, note=("30 秒學識，唔使兩個禮拜", "note"))),
    Scene("harm",
          "咁零 Code PM 點樣為禍香港？維基百科同網上討論提到幾樣嘢：[[h1]]第一，外行管內行，"
          "決策冇技術根據，技術難題淨係靠所謂軟技能去解決；[[h2]]第二，程式員擔心濫權同職場霸凌；"
          "[[h3]]第三，劣幣驅逐良幣，識做嘢嘅人頂唔順，走晒；[[h4]]留低嘅，就係更多零 Code PM。",
          source(TileCard("點樣為禍香港？", [
              Tile("🙈", "外行管內行", "決策冇技術根據，靠「軟技能」解決", "h1", RED),
              Tile("😡", "濫權、職場霸凌", "程式員最擔心嘅事", "h2", AMBER),
              Tile("🪙", "劣幣驅逐良幣", "識做嘢嘅人頂唔順，走晒", "h3", PURPLE),
              Tile("🔁", "惡性循環", "留低嘅，係更多零 Code PM", "h4", BLUE),
          ], cols=2, height=270, top=260, gap=36), y=870)),
    Scene("why",
          "點解香港會有咁多零 Code PM？維基百科話，[[e1]]千禧年之後科網股爆煲，"
          "[[e2]]好多學生驚 IT 冇前途，唔再讀 IT，[[e3]]結果 IT 人才斷層，識寫 code 嘅人唔夠，"
          "[[e4]]就出現咗零 Code PM 呢個現象，即係廣東話講嘅：[[say]]外行人管內行人。",
          pill(source(FlowCard("點解會有咁多零 Code PM？", [
              Row("成因", "維基百科", AMBER, [
                  Node("科網爆煲", "2000 年後", "e1"),
                  Node("冇人讀 IT", "驚冇前途", "e2"),
                  Node("人才斷層", "識 code 嘅人唔夠", "e3"),
                  Node("零 Code PM", "坐上管理位", "e4"),
              ]),
          ], top=340)), "「外行人管內行人」", 620, "say", RED, size=52)),
    Scene("quiz",
          "做個小測驗，睇吓你身邊有冇零 Code PM：[[t1]]聽到 for loop，會問 for 乜嘢；"
          "[[t2]]項目遲咗，就話加多幾個人一定會快啲；[[t3]]開會開足三個鐘，都冇人講到個 bug 喺邊。"
          "[[t4]]中晒三樣，恭喜你，你身邊有一位零 Code PM。",
          pill(BulletCard("零 Code PM 自我檢測", [
              ("聽到 for loop，會問「for 乜嘢？」", "t1"),
              ("項目遲咗，就話「加多幾個人一定快啲」", "t2"),
              ("開會開足三個鐘，都冇人講到個 bug 喺邊", "t3"),
          ]), "中晒三樣：恭喜你，身邊有位零 Code PM", 700, "t4", RED)),
    Scene("fair",
          "不過公道啲講，[[n1]]PM 唔使日日寫 code，[[n2]]亦唔使識晒所有 framework。"
          "[[y1]]但至少要識 for loop 呢啲基本概念，[[y2]]估得到一樣嘢大概要做幾耐，[[y3]]聽得明團隊講緊乜。"
          "[[sum]]就好似上集講，上下級都要識 technical，先至傾得埋。",
          CompareCard("公道啲講：PM 要識幾多？", [
              Column("🙆", "唔使識", [("日日寫 code", "n1"), ("識晒所有 framework", "n2")], MUTED),
              Column("✅", "一定要識", [("for loop 呢啲基本概念", "y1"), ("估到一樣嘢大概要做幾耐", "y2"),
                                        ("聽得明團隊講緊乜", "y3")], GREEN),
          ], footer=("上下級都要識 technical，先至傾得埋", "sum", BLUE))),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]用 for loop 寫個程式，同十個朋友講生日快樂。寫完，記得 send 埋俾你個 PM 睇吓。"
          "[[next]]多謝收睇，下次見！",
          EndCard("用 for loop 寫個程式，同十個朋友講生日快樂。寫完，記得 send 埋俾你個 PM 睇吓。",
                  "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
