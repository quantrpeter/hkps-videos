#!/usr/bin/env python3
"""識講唔識做：IT 出身嘅零 Code PM 有幾禍害

The fourth 「IT 職場講堂」 satire, after 零 Code PM and 零 Git Manager. This one is the PM who
studied IT at university: every sentence is cloud-native, microservice and AI-driven, but asked to
write a five-line login check, they can't. The video shows the jargon chat, the PM's "code", a
jargon-to-reality dictionary, why this PM is worse than one who never studied IT, the harms to the
team, a made-up project story, a self-test and a fair word on what a PM needs to know.

The archetype is the channel's own observation, not a survey. The characters, dialogue and the
project story are made up; no real person, company or project is named.

    python3 talk_only_pm.py              # -> out/talk_only_pm.mp4 (narration is cached)
    python3 talk_only_pm.py --draft      # silent, estimated timing, fast: for checking layout
    python3 talk_only_pm.py --stills     # two PNGs per scene in build/talk_only_pm/stills/
    python3 talk_only_pm.py --redo chat  # regenerate one scene's narration
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D

VIDEO = Video(slug=Path(__file__).stem, title="IT 出身嘅零 Code PM 有幾禍害", series="IT 職場講堂")
opts = options(VIDEO)

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "PM": "P M",
    "IT": "I T",
    "AI": "A I",
    "AI-driven": "A I driven",
    "cloud-native": "cloud native",
    "API": "A P I",
    "MVP": "M V P",
    "TODO": "to do",
}

PM = ("👔", "PM", PURPLE)
DEV = ("💻", "Programmer", TEAL)


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 42) -> Card:
    """Adds a centred coloured pill to any card (a punchline or a takeaway)."""
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


PM_CODE = """import AI
import blockchain

def login():
    AI.check_password()  # AI 會識
    blockchain.secure()  # 夠 secure
    # TODO: implementation detail"""

REAL_CODE = """def login(user, password):
    row = db.find_user(user)
    if row is None:
        return False
    return check_hash(password, row.hash)"""

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟 IT 職場講堂。上兩集講完零 Code PM 同零 Git Manager，"
          "今集講一個更加難搞嘅版本：大學讀 IT 出身，開口埋口都係 technical term，"
          "但係叫佢寫幾行 code，就寫唔出。我哋叫佢做：識講唔識做 PM。",
          TitleCard(VIDEO.series, "吐糟篇", "識講唔識做 PM", VIDEO.title, "滿口 technical term，幾行 code 都寫唔出")),
    Scene("chat",
          "睇吓一個經典場面。[[m1]]PM 話：呢個 project 要 cloud-native、microservice、AI-driven，仲要 scalable！"
          "[[m2]]Programmer 問：明白。咁 user 資料用咩 database？login 點做？"
          "[[m3]]PM 話：呢啲係 implementation detail，你哋 handle 啦。我大學都讀 IT 㗎。"
          "[[out]]Term 識講十個，問題答唔到一個。",
          ChatCard("經典場面", [PM, DEV], [
              Msg(0, "呢個 project 要 cloud-native、microservice、AI-driven，仲要 scalable！", "m1"),
              Msg(1, "明白。咁 user 資料用咩 database？login 點做？", "m2"),
              Msg(0, "呢啲係 implementation detail，你哋 handle 啦。我大學都讀 IT 㗎。", "m3"),
          ], footer=("Term 識講十個，問題答唔到一個", "out", RED))),
    Scene("code",
          "有 programmer 忍唔住，請佢示範吓：寫個 function，檢查 password 啱唔啱。"
          "[[bad]]佢寫出嚟係咁：import 咗 AI 同 blockchain，最後一句 TODO，交俾 dev 跟進。"
          "[[good]]真正嘅寫法，五行：搵個 user，搵唔到就 return false，搵到就 check 個 password hash。"
          "[[joke]]名詞識講十個，code 寫唔出五行。",
          pill(CodeCompareCard("寫個 login，檢查 password", [
              Pane("PM 寫嘅 code", PM_CODE, good=False, at="bad", name="login.py"),
              Pane("真正嘅 code：5 行", REAL_CODE, good=True, at="good", name="login.py"),
          ]), "名詞識講十個，code 寫唔出五行", 760, "joke", RED)),
    Scene("dict",
          "識講唔識做 PM 嘅說話，要翻譯先聽得明。[[d1]]佢話好 simple，加個 button 啫，"
          "實際係要改 database、API 同三個 page；[[d2]]佢話我哋要 agile，意思係冇 spec，requirement 隨時改；"
          "[[d3]]佢話先做個 MVP，但個 MVP 嘅 scope，等於成個 product；[[d4]]佢話要 scalable，"
          "其實係冇人知會有幾多 user；[[d5]]佢話用 AI 做埋佢，其實係冇人知想 AI 做乜。"
          "[[note]]結果 programmer 除咗寫 code，仲要兼職做翻譯。",
          TableCard("PM 講嘅 vs 實際意思", ["PM 講", "實際意思"], [
              (["「好 simple，加個 button 啫」", "要改 database、API、三個 page"], "d1"),
              (["「我哋要 agile」", "冇 spec，requirement 隨時改"], "d2"),
              (["「先做個 MVP」", "MVP 嘅 scope ＝ 成個 product"], "d3"),
              (["「要 scalable」", "冇人知會有幾多 user"], "d4"),
              (["「用 AI 做埋佢」", "冇人知想 AI 做乜"], "d5"),
          ], widths=[1, 1.1], code_cols=(), note=("Programmer 嘅工作：寫 code ＋ 兼職翻譯", "note"))),
    Scene("worse",
          "你可能會問，讀過 IT，總好過完全唔識啩？其實未必。[[a1]]完全唔識 IT 嘅 PM，至少知自己唔識，會問；"
          "[[a2]]亦肯聽 programmer 意見。[[b1]]但係 IT 出身嘅零 Code PM，以為自己識，所以唔問；"
          "[[b2]]你一反駁，佢就話：我讀書嗰陣都寫過；[[b3]]估時間，靠十年前做 assignment 嘅印象。"
          "[[sum]]唔識唔可怕，扮識先最可怕。",
          CompareCard("讀過 IT，一定好啲？", [
              Column("🤷", "完全唔識 IT 嘅 PM", [("知自己唔識，會問", "a1"), ("肯聽 programmer 意見", "a2")], MUTED),
              Column("🎓", "IT 出身零 Code PM", [("以為自己識，所以唔問", "b1"), ("一反駁就話「我讀書都寫過」", "b2"),
                                               ("估時間靠十年前做 assignment", "b3")], RED),
          ], footer=("唔識唔可怕，扮識先最可怕", "sum", RED))),
    Scene("harm",
          "咁對團隊有幾大影響？[[h1]]第一，估錯時間：佢話半日，實際兩個禮拜。"
          "[[h2]]第二，亂揀技術：跟潮流名詞揀，唔跟需要揀。[[h3]]第三，對客亂承諾：同客講咗先，返嚟先問做唔做到。"
          "[[h4]]第四，開會變上堂：programmer 要逐個 term 解釋。[[h5]]第五，打擊士氣：一句我讀書都寫過，壓晒所有意見。"
          "[[h6]]最後，出事 programmer 揹鑊：計劃係佢定，錯就係你做。",
          TileCard("對團隊有幾大影響？", [
              Tile("🕐", "估錯時間", "佢話半日，實際兩個禮拜", "h1", RED),
              Tile("🧩", "亂揀技術", "跟潮流名詞揀，唔跟需要揀", "h2", AMBER),
              Tile("📢", "對客亂承諾", "講咗先，返嚟先問做唔做到", "h3", PURPLE),
              Tile("🗣️", "開會變上堂", "programmer 要逐個 term 解釋", "h4", BLUE),
              Tile("😞", "打擊士氣", "「我讀書都寫過」壓晒所有意見", "h5", TEAL),
              Tile("🎯", "出事 dev 揹鑊", "計劃係佢定，錯就係你做", "h6", RED),
          ], cols=3, gap=36)),
    Scene("story",
          "講個完全虛構、但你可能覺得似曾相識嘅故事。[[e1]]第一個禮拜，PM 同客講：我哋用 microservice 加 AI，事前冇問過 dev；"
          "[[e2]]第二個禮拜，三個 programmer 拆咗十二個 service，每人管四個；"
          "[[e3]]第二個月，一個 bug 穿過五個 service，冇人搵到喺邊；"
          "[[e4]]第三個月，deadline 過咗，PM 話：你哋唔夠 agile；"
          "[[e5]]第四個月，團隊入面最勁嗰位 programmer 辭職。[[fix]]其實呢個系統，一個簡單嘅 monolith 已經夠用。",
          TimelineCard("一個項目嘅一生", [
              Event("第 1 週", "對客講 microservice", "事前冇問過 dev", "e1", AMBER),
              Event("第 2 週", "3 個人拆 12 個 service", "每人管 4 個", "e2", AMBER),
              Event("第 2 個月", "bug 穿過 5 個 service", "冇人搵到喺邊", "e3", RED),
              Event("第 3 個月", "Deadline 過咗", "PM：「你哋唔夠 agile」", "e4", RED),
              Event("第 4 個月", "最勁嗰位 dev 辭職", "", "e5", PURPLE),
          ], callout=("其實一個簡單嘅 monolith 已經夠用", "fix"))),
    Scene("quiz",
          "做個小測驗，睇吓你身邊有冇識講唔識做 PM：[[t1]]講得出 Docker、microservice，但連 terminal 都開唔到；"
          "[[t2]]估時間永遠係：好 simple，半日搞掂；[[t3]]一問細節，就話：呢啲係 implementation detail。"
          "[[t4]]中晒三樣，恭喜你，你身邊有一位識講唔識做 PM。",
          pill(BulletCard("識講唔識做 PM 自我檢測", [
              ("講得出 Docker、microservice，但連 terminal 都開唔到", "t1"),
              ("估時間永遠係「好 simple，半日搞掂」", "t2"),
              ("一問細節，就話「呢啲係 implementation detail」", "t3"),
          ]), "中晒三樣：恭喜你，身邊有位識講唔識做 PM", 700, "t4", RED)),
    Scene("fair",
          "不過公道啲講，[[n1]]PM 唔使寫 production code，[[n2]]亦唔使追晒所有新 framework。"
          "[[y1]]但每講一個 technical term，都要講得出佢嘅代價；[[y2]]自己至少寫得出幾十行簡單嘅 code；"
          "[[y3]]唔識就問，唔好扮識。[[sum]]Technical term 係用嚟溝通，唔係用嚟壓人。",
          CompareCard("公道啲講：PM 要識幾多？", [
              Column("🙆", "唔使識", [("寫 production code", "n1"), ("追晒所有新 framework", "n2")], MUTED),
              Column("✅", "一定要識", [("每個 term 講得出代價", "y1"), ("寫得出幾十行簡單 code", "y2"),
                                        ("唔識就問，唔好扮識", "y3")], GREEN),
          ], footer=("Technical term 係用嚟溝通，唔係用嚟壓人", "sum", BLUE))),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]揀一個你成日講嘅 technical term，用十行 code 示範俾人睇。"
          "示範唔到，就唔好講住。[[next]]多謝收睇，下次見！",
          EndCard("揀一個你成日講嘅 technical term，用十行 code 示範俾人睇。示範唔到，就唔好講住。",
                  "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
