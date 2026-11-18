#!/usr/bin/env python3
"""IT 團隊：上下級都要識 technical

In a normal IT team the boss and the staff both have to understand the technical side, or they
cannot talk to each other. Two failed conversations (a non-technical boss, a non-technical junior),
the same problem talked through by two people who both know the tech, then what each level needs
to know and how to get there.

    python3 it_technical.py              # -> out/it_technical.mp4 (narration is cached; reruns are quick)
    python3 it_technical.py --draft      # silent, estimated timing, fast: for checking layout
    python3 it_technical.py --stills     # two PNGs per scene in build/it_technical/stills/ (add --draft to skip TTS)
    python3 it_technical.py --redo chat_boss   # regenerate one scene's narration
    python3 it_technical.py --help
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)

VIDEO = Video(slug=Path(__file__).stem, title="IT 團隊：上下級都要識 technical", series="IT 職場講堂")
opts = options(VIDEO)

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "CTO": "C T O",
    "API": "A P I",
}

BOSS = ("👔", "上司", PURPLE)
STAFF = ("💻", "同事", TEAL)
LEAD = ("🧭", "Team Lead", BLUE)

scenes = [
    Scene("intro",
          "大家好！歡迎收睇香港編程學會。今集唔講 code，我哋講吓 IT 公司入面一個好實際嘅問題："
          "點解上司同下屬，都一定要識 technical？",
          TitleCard(VIDEO.series, "溝通篇", "上司 × 下屬", VIDEO.title, "廣東話 · 唔識 technical，根本傾唔埋")),
    Scene("goal",
          "今集會講四樣嘢：[[b1]]一個正常嘅 IT 團隊係點分工；[[b2]]唔識 technical，溝通會出咩問題；"
          "[[b3]]上級同下級，各自要識到幾多；[[b4]]仲有點樣改善。",
          BulletCard("今集學識", [("一個正常 IT 團隊點分工", "b1"), ("唔識 technical 會點樣傾唔埋", "b2"),
                                ("上級、下級各自要識到幾多", "b3"), ("點樣改善", "b4")])),
    Scene("team",
          "一個正常嘅 IT 團隊大概係咁：[[cto]]最上面有 CTO 或者 IT 經理，決定技術方向同預算；"
          "[[lead]]跟住係 Team Lead，負責拆工、review code；[[senior]]Senior developer 寫核心部分，帶新人；"
          "[[junior]]Junior developer 就跟住 ticket 做嘢、改 bug。"
          "[[same]]由上到下，大家講嘅都係同一種語言：technical 嘅語言。",
          TileCard("一個正常 IT 團隊", [
              Tile("🧭", "CTO", "IT 經理\n定技術方向、批預算", "cto", PURPLE),
              Tile("🧩", "Team Lead", "拆工、review code", "lead", BLUE),
              Tile("🛠️", "Senior", "寫核心部分\n帶新人", "senior", TEAL),
              Tile("🌱", "Junior", "跟 ticket 做嘢\n改 bug", "junior", GREEN),
          ], cols=4, height=330, footer=("由上到下：講同一種語言", "same"))),
    Scene("chat_boss",
          "先睇第一個情況：上司唔識 technical。[[m1]]上司話：個 app 好慢，你今日搞掂佢。"
          "[[m2]]同事問：慢喺邊度？係 API 慢，定係 database 慢？[[m3]]上司答：我唔理，總之要快！"
          "[[out]]結果同事唔知從邊度入手，只可以靠估。",
          ChatCard("情況一：上司唔識 technical", [BOSS, STAFF], [
              Msg(0, "個 app 好慢，你今日搞掂佢。", "m1"),
              Msg(1, "慢喺邊度？係 API 慢，定係 database 慢？", "m2"),
              Msg(0, "我唔理，總之要快！", "m3"),
          ], footer=("結果：唔知從邊度入手，只可以靠估", "out", RED))),
    Scene("boss_cost",
          "上司唔識 technical，會有咩後果？[[c1]]第一，佢定唔到優先次序，成隊人估錯方向，嘥晒時間。"
          "[[c2]]第二，佢唔知一樣嘢要做幾耐，deadline 亂咁定。"
          "[[c3]]第三，佢分唔到邊個做得好，好嘅同事頂唔順，就會走。",
          TileCard("上司唔識 technical 嘅後果", [
              Tile("🧭", "方向錯", "定唔到優先次序\n成隊人嘥晒時間", "c1", RED),
              Tile("⏰", "Deadline 亂定", "唔知一樣嘢\n要做幾耐", "c2", AMBER),
              Tile("🚪", "人才流失", "分唔到邊個做得好\n好嘅同事會走", "c3", PURPLE),
          ], height=400)),
    Scene("chat_staff",
          "反過嚟，下屬唔識 technical 又點？[[m1]]上司話：幫我睇吓個 log，係咪 timeout。"
          "[[m2]]同事問：log 喺邊度睇㗎？[[m3]]上司再問：咁你啲 code commit 咗未？[[m4]]同事答：commit 係咩嚟？"
          "[[out]]每一句都要由頭解釋，上司冇咁多時間，最後只好自己做埋。",
          ChatCard("情況二：下屬唔識 technical", [LEAD, STAFF], [
              Msg(0, "幫我睇吓個 log，係咪 timeout。", "m1"),
              Msg(1, "Log 喺邊度睇㗎？", "m2"),
              Msg(0, "咁你啲 code commit 咗未？", "m3"),
              Msg(1, "Commit 係咩嚟？", "m4"),
          ], footer=("結果：每句都要解釋，上司自己做埋", "out", RED))),
    Scene("chat_good",
          "如果兩邊都識 technical，同一件事可以咁傾。[[m1]]上司話：API 嘅反應時間由零點二秒升到兩秒，"
          "懷疑係新加嗰個 query 冇 index。[[m2]]同事答：我查吓個 query plan，加咗 index，喺 staging 測完先 deploy。"
          "[[m3]]上司話：好，記得 update 張 ticket。[[out]]三句講完，大家都知道問題喺邊、點做、點驗收。",
          ChatCard("兩邊都識 technical", [LEAD, STAFF], [
              Msg(0, "API 反應時間由 0.2 秒升到 2 秒，懷疑新加嗰個 query 冇 index。", "m1"),
              Msg(1, "我查吓個 query plan，加咗 index，喺 staging 測完先 deploy。", "m2"),
              Msg(0, "好，記得 update 張 ticket。", "m3"),
          ], footer=("三句講完：問題喺邊、點做、點驗收", "out", GREEN))),
    Scene("words",
          "所以 IT 團隊有一套共同語言。[[w1]]API、[[w2]]bug、[[w3]]deploy、[[w4]]commit、[[w5]]ticket，"
          "[[note]]呢啲字唔係扮專業，而係令溝通又快又準。",
          TableCard("IT 團隊嘅共同語言", ["詞彙", "意思"], [
              (["API", "程式同程式之間溝通嘅接口"], "w1"),
              (["bug", "程式入面嘅錯誤"], "w2"),
              (["deploy", "將新版本放上伺服器"], "w3"),
              (["commit", "將改動存入 Git"], "w4"),
              (["ticket", "一件要做嘅工作，有人跟、有記錄"], "w5"),
          ], widths=[1, 2.6], note=("唔係扮專業：係令溝通又快又準", "note"))),
    Scene("levels",
          "咁上級同下級，各自要識到幾多？[[l1]]上級唔一定日日寫 code，但要睇得明系統架構同 code，"
          "[[l2]]估得出工作量，[[l3]]拆得開問題、定得出優先次序。"
          "[[r1]]下級就要有基本功：Git、debug、睇 log，[[r2]]講得清楚問題喺邊，[[r3]]仲要識問好問題。",
          CompareCard("各自要識到幾多？", [
              Column("👔", "上級要識", [("睇得明系統架構同 code", "l1"), ("估得出工作量", "l2"),
                                       ("拆得開問題、定優先次序", "l3")], PURPLE),
              Column("💻", "下級要識", [("基本功：Git、debug、睇 log", "r1"), ("講得清楚問題喺邊", "r2"),
                                       ("識問好問題", "r3")], TEAL),
          ])),
    Scene("myth",
          "有人話：[[bad]]管理只係管人，唔使識技術。喺其他行業可能得，[[good]]但係喺 IT 行業，你管嘅人，做緊嘅就係技術。"
          "[[why]]唔識 technical，你連佢做得好唔好都判斷唔到。[[sum]]所以 IT 管理，就係管人加管技術。",
          CompareCard("「管理唔使識技術」？", [
              Column("❌", "常見講法", [("管理只係管人", "bad"), ("技術交俾下面做就得", "bad")], RED),
              Column("✅", "IT 行業現實", [("你管嘅人，做緊嘅就係技術", "good"),
                                         ("唔識就判斷唔到做得好唔好", "why")], GREEN),
          ], footer=("IT 管理 ＝ 管人 ＋ 管技術", "sum", BLUE))),
    Scene("tips",
          "點樣改善？[[s1]]上級：定期參與 code review，保持技術觸覺。"
          "[[s2]]下級：問問題之前，先講清楚你試過啲乜、見到咩 error。"
          "[[s3]]大家：重要嘅嘢寫落 ticket 同文件，唔好淨係靠口講。",
          StepsCard("點樣改善？", [
              Step("上級：定期參與 code review，保持技術觸覺", at="s1"),
              Step("下級：問問題之前，先講清楚試過乜、見到咩 error", at="s2"),
              Step("大家：重要嘅嘢寫落 ticket 同文件，唔好淨係靠口講", at="s3"),
          ], icon="🔧", gap=48)),
    Scene("recap",
          "總結一下：[[r1]]IT 團隊由上到下，都係用 technical 嘅語言溝通；"
          "[[r2]]上級唔識，方向會錯，人才會走；[[r3]]下級唔識，每句都要解釋，成隊人都慢晒。",
          BulletCard("今集重點", [("IT 團隊由上到下，都用 technical 嘅語言溝通", "r1"),
                                ("上級唔識：方向錯、deadline 亂定、人才流失", "r2"),
                                ("下級唔識：每句都要解釋，成隊人慢晒", "r3")])),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]下次開會，記低一個你唔明嘅技術名詞，查清楚，再用自己嘅說話解釋俾同事聽。"
          "[[next]]多謝收睇，下次見！",
          EndCard("下次開會，記低一個你唔明嘅技術名詞，查清楚，再用自己嘅說話解釋俾同事聽。",
                  "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
