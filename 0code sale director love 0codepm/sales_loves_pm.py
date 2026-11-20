#!/usr/bin/env python3
"""點解零 Code Sales Director 愛請零 Code PM

The sixth 「IT 職場講堂」 satire: why the 零 Code PM keeps getting hired. Behind them there is often
a Sales Director who isn't technical either. The video shows an interview (the technical PM says
three months, the 零 Code PM says no problem), six reasons the Director prefers the 零 Code PM, what
a non-technical interviewer can and can't judge, the PM's "strengths" as the Director sees them,
how one sales deal turns into a disaster, a self-test, a fair word and a challenge (ask the for-loop
question from 零 Code PM in the next PM interview).

The archetype is the channel's own observation, not a survey; the narration says not every Sales
Director is like this. The characters and dialogue are made up; no real person, company or project
is named.

    python3 sales_loves_pm.py              # -> out/sales_loves_pm.mp4 (narration is cached)
    python3 sales_loves_pm.py --draft      # silent, estimated timing, fast: for checking layout
    python3 sales_loves_pm.py --stills     # two PNGs per scene in build/sales_loves_pm/stills/
    python3 sales_loves_pm.py --redo chat  # regenerate one scene's narration
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D

VIDEO = Video(slug=Path(__file__).stem, title="點解零 Code Sales Director 愛請零 Code PM", series="IT 職場講堂")
opts = options(VIDEO)

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "PM": "P M",
    "IT": "I T",
    "AI": "A I",
}

# ChatCard puts speaker 1 on the right and every other speaker on the left.
TECH = ("🧑‍💻", "技術型 PM", TEAL)
DIRECTOR = ("💼", "Sales Director", AMBER)
ZERO = ("👔", "零 Code PM", PURPLE)


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 42) -> Card:
    """Adds a centred coloured pill to any card (a punchline or a takeaway)."""
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


scenes = [
    Scene("intro",
          "大家好！歡迎返嚟 IT 職場講堂。講咗咁多集零 Code PM，你可能會問：點解呢啲 PM，一直都有人請？"
          "今集講背後嘅另一個角色：同樣唔識 technical 嘅 Sales Director。",
          TitleCard(VIDEO.series, "吐糟篇", "Sales Director × 零 Code PM", VIDEO.title, "「客要乜，我哋都做到！」")),
    Scene("chat",
          "睇吓一場面試。[[m1]]Sales Director 問：客想下個月上線一個有 AI 嘅 app，做唔做到？"
          "[[m2]]第一位係技術型 PM，佢答：要先睇 requirement，單係 AI 嗰部份，起碼要三個月。"
          "[[m3]]第二位係零 Code PM，佢答：冇問題！我哋行 agile，下個月一定上到線！"
          "[[out]]你估吓，Director 請咗邊個？",
          ChatCard("一場面試", [TECH, DIRECTOR, ZERO], [
              Msg(1, "客想下個月上線一個有 AI 嘅 app，做唔做到？", "m1"),
              Msg(0, "要先睇 requirement。單係 AI 嗰部份，起碼要三個月。", "m2"),
              Msg(2, "冇問題！我哋行 agile，下個月一定上到線！", "m3"),
          ], footer=("你估吓，Director 請咗邊個？", "out", RED))),
    Scene("why",
          "點解 Sales Director 咁鍾意零 Code PM？[[r1]]一，同聲同氣，兩個都淨係講 buzzword。"
          "[[r2]]二，永遠話做到，冇人阻住簽單。[[r3]]三，唔會拆穿 sales 亂承諾。"
          "[[r4]]四，面試評唔到 technical，就評口才。[[r5]]五，人總係鍾意請似自己嘅人。"
          "[[r6]]六，項目遲咗，一齊話 programmer 慢。",
          TileCard("點解咁鍾意零 Code PM？", [
              Tile("🤝", "同聲同氣", "兩個都講 buzzword，唔講 code", "r1", BLUE),
              Tile("✅", "永遠話做到", "Sales 承諾乜都得，冇人阻簽單", "r2", GREEN),
              Tile("🙊", "唔會拆穿", "唔會喺客面前話 sales 亂承諾", "r3", PURPLE),
              Tile("🎤", "面試睇口才", "評唔到 technical，就評口才", "r4", AMBER),
              Tile("🪞", "似返自己", "人總係鍾意請同自己相似嘅人", "r5", TEAL),
              Tile("🎯", "有鑊一齊推", "項目遲咗，就話 programmer 慢", "r6", RED),
          ], cols=3, gap=36), seed=13),
    Scene("judge",
          "問題出喺面試。[[a1]]一個唔識 technical 嘅 Director，評得到口才同自信，"
          "[[a2]]評得到 PowerPoint 靚唔靚，[[a3]]評得到識唔識講 buzzword。"
          "[[b1]]但係佢評唔到估時間準唔準，[[b2]]評唔到技術方案啱唔啱，[[b3]]更加評唔到識唔識睇 code。"
          "[[sum]]評唔到嘅，自然就當咗唔重要。",
          CompareCard("Director 面試 PM，評到啲乜？", [
              Column("👀", "評得到", [("口才同自信", "a1"), ("PowerPoint 靚唔靚", "a2"), ("識唔識講 buzzword", "a3")], BLUE),
              Column("🙈", "評唔到", [("估時間準唔準", "b1"), ("技術方案啱唔啱", "b2"), ("識唔識睇 code", "b3")], RED),
          ], footer=("評唔到嘅，自然就當咗唔重要", "sum", RED))),
    Scene("eyes",
          "喺 Director 眼中，零 Code PM 渾身都係優點：[[e1]]從來唔話做唔到，其實係根本唔知做唔做到；"
          "[[e2]]同客好 friend，其實係客要乜都答應；[[e3]]開會好有 energy，但開完會冇人知要做乜；"
          "[[e4]]report 好靚，但入面嘅進度百分比，係估嘅；[[e5]]識講 AI 同 cloud，但係，只係識講。"
          "[[note]]原來優點同缺點，係同一樣嘢。",
          TableCard("Director 眼中嘅好 PM", ["Director 眼中", "實際上"], [
              (["「從來唔話做唔到」", "根本唔知做唔做到"], "e1"),
              (["「同客好 friend」", "客要乜都答應"], "e2"),
              (["「開會好有 energy」", "開完會冇人知要做乜"], "e3"),
              (["「Report 好靚」", "進度百分比係估嘅"], "e4"),
              (["「識講 AI、cloud」", "只係識講"], "e5"),
          ], code_cols=(), note=("原來優點同缺點，係同一樣嘢", "note"))),
    Scene("chain",
          "兩個人夾埋，一張單通常係咁變成災難：[[f1]]Sales 同客講，乜都做到；[[f2]]零 Code PM 喺隔籬點頭，話冇問題；"
          "[[f3]]合約寫明一個月交貨。[[g1]]簽完單，programmer 先知道，要通頂趕工；[[g2]]結果交貨遲咗，bug 又多；"
          "[[g3]]客戶嬲，Sales 就話係 IT 做得差。[[sum]]Sales 收 commission，programmer 收爛攤子。",
          pill(FlowCard("一張單點樣變成災難", [
              Row("簽單前", "講", AMBER, [
                  Node("Sales", "「乜都做到」", "f1"),
                  Node("零 Code PM", "「冇問題」", "f2"),
                  Node("合約", "一個月交貨", "f3"),
              ]),
              Row("簽單後", "做", RED, [
                  Node("Programmer", "通頂趕工", "g1"),
                  Node("交貨", "遲咗、bug 又多", "g2"),
                  Node("客戶嬲", "Sales 怪 IT 做得差", "g3"),
              ]),
          ], top=290, row_h=260), "Sales 收 commission，programmer 收爛攤子", 790, "sum", RED), seed=12),
    Scene("quiz",
          "做個小測驗，睇吓你公司係咪咁：[[t1]]面試 PM，冇一條 technical 問題；"
          "[[t2]]Sales 簽完單，先問 IT 做唔做到；[[t3]]項目遲咗，永遠係 programmer 嘅錯。"
          "[[t4]]中晒三樣，你公司嘅 PM，八成係 Sales 揀嘅。",
          pill(BulletCard("你公司係咪咁？", [
              ("面試 PM，冇一條 technical 問題", "t1"),
              ("Sales 簽完單，先問 IT 做唔做到", "t2"),
              ("項目遲咗，永遠係 programmer 嘅錯", "t3"),
          ]), "中晒三樣：你公司嘅 PM，八成係 Sales 揀嘅", 700, "t4", RED)),
    Scene("fair",
          "不過公道啲講，唔係個個 Sales Director 都係咁，口才同客戶關係都好重要。"
          "[[n1]]Sales Director 唔使識寫 code，[[n2]]亦唔使識揀 framework。"
          "[[y1]]但面試 PM，要有識 technical 嘅人；[[y2]]報價之前，先問 IT 估時間；"
          "[[y3]]聽到做唔到，當係有用資訊。[[sum]]賣嘢交俾 Sales，估時間交俾 IT。",
          CompareCard("公道啲講：Sales Director 要做乜？", [
              Column("🙆", "唔使識", [("寫 code", "n1"), ("揀 framework", "n2")], MUTED),
              Column("✅", "一定要做", [("面試 PM 要有 technical 嘅人", "y1"), ("報價之前，先問 IT 估時間", "y2"),
                                        ("「做唔到」當係有用資訊", "y3")], GREEN),
          ], footer=("賣嘢交俾 Sales，估時間交俾 IT", "sum", BLUE))),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]下次公司面試 PM，加一條問題：一千個客要 send email，要寫幾多行 code？"
          "答一千行嘅，唔好請。[[next]]多謝收睇，下次見！",
          EndCard("下次公司面試 PM，加一條問題：一千個客要 send email，要寫幾多行 code？答一千行嘅，唔好請。",
                  "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
