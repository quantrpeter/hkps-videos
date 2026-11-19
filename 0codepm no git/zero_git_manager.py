#!/usr/bin/env python3
"""零 Git Manager：IT Manager 唔識 Git 有幾禍害

The third 「IT 職場講堂」 satire, after 零 Code PM. Many Hong Kong IT managers never learned Git, so
their teams pass code around as zip files, email and USB sticks. The video shows what that looks
like (a Desktop of project_final_最終版_真係最後.zip), what Git is, the harms, a Friday-night
production story, the five commands a manager needs, a self-test and a fair word.

The claim is the channel's own observation, not a survey: the narration says so. The characters,
dialogue and the Friday-night story are made up; no real person, company or project is named.

    python3 zero_git_manager.py              # -> out/zero_git_manager.mp4 (narration is cached)
    python3 zero_git_manager.py --draft      # silent, estimated timing, fast: for checking layout
    python3 zero_git_manager.py --stills     # two PNGs per scene in build/zero_git_manager/stills/
    python3 zero_git_manager.py --redo chat  # regenerate one scene's narration
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D

VIDEO = Video(slug=Path(__file__).stem, title="IT Manager 唔識 Git 有幾禍害", series="IT 職場講堂")
opts = options(VIDEO)

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "PM": "P M",
    "PR": "P R",
    "USB": "U S B",
    "GitHub": "Git Hub",
}

BOSS = ("👔", "IT Manager", PURPLE)
DEV = ("💻", "Programmer", TEAL)


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 42) -> Card:
    """Adds a centred coloured pill to any card (a punchline or a takeaway)."""
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


DESKTOP = """~/Desktop/
  project.zip
  project_v2.zip
  project_v2_改咗login.zip
  project_final.zip
  project_final_最終版.zip
  project_final_最終版(1).zip
  project_final_最終版_真係最後.zip
  阿明部手提/project_new.zip"""

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟 IT 職場講堂。上集講完零 Code PM，今集踢爆一個香港 IT 界公開嘅秘密："
          "喺我哋見過嘅香港 IT 公司入面，大部份 IT Manager，都唔識用 Git。",
          TitleCard(VIDEO.series, "吐糟篇", "零 Git Manager", VIDEO.title, "project_最終版_真係最後.zip，你見過未？")),
    Scene("desktop",
          "唔用 Git 嘅團隊，個 Desktop 通常係咁：[[v]]v2、改咗 login、final、最終版，"
          "[[last]]仲有一個叫「最終版真係最後」。[[gone]]而真正最新嗰份，原來喺上個月離職嗰位同事部手提度。"
          "[[q]]邊個先係最新版本？冇人知。",
          pill(CodeCard("你公司個 Desktop，係咪咁？", DESKTOP, name="files.txt", marks=[
              ((3, 4), "v2？改咗乜？", "v", BLUE),
              ((8, 8), "真係最後？", "last", RED),
              ((9, 9), "阿明已經離職", "gone", PURPLE),
          ], width=1100), "邊個先係最新版本？冇人知", 720, "q", RED)),
    Scene("chat",
          "睇吓一個經典場面。[[m1]]Manager 話：你改完 zip 埋 email 俾我，我再 forward 俾阿明。"
          "[[m2]]Programmer 答：不如用 Git 啦，開個 branch，做埋 code review。"
          "[[m3]]Manager 話：Git？要俾錢㗎？用 USB 手指 copy 咪得囉。"
          "[[out]]其實 Git 完全免費，仲開源，已經用咗廿幾年。",
          ChatCard("經典場面", [BOSS, DEV], [
              Msg(0, "你改完 zip 埋 email 俾我，我再 forward 俾阿明。", "m1"),
              Msg(1, "不如用 Git 啦，開個 branch，做埋 code review。", "m2"),
              Msg(0, "Git？要俾錢㗎？用 USB 手指 copy 咪得囉。", "m3"),
          ], footer=("Git：免費、開源，2005 年面世", "out", GREEN))),
    Scene("what",
          "咁 Git 係乜？簡單講，就係 code 嘅時光機，兼記錄冊。[[g1]]每次改動，邊個、幾時、改咗乜，一清二楚；"
          "[[g2]]改壞咗，隨時返去任何一個版本；[[g3]]幾個人可以各自開 branch，同時做嘢唔會撞；"
          "[[g4]]合併之前，有人睇過先上。[[sum]]呢啲，就係專業軟件團隊嘅最低要求。",
          TileCard("Git 係乜？code 嘅時光機", [
              Tile("📜", "記錄每次改動", "邊個、幾時、改咗乜，一清二楚", "g1", BLUE),
              Tile("⏪", "隨時還原", "改壞咗，返去任何一個版本", "g2", GREEN),
              Tile("🌿", "分 branch 做嘢", "幾個人同時改，唔會撞", "g3", TEAL),
              Tile("👀", "Code review", "合併之前，有人睇過先上", "g4", PURPLE),
          ], cols=2, height=250, footer=("專業軟件團隊嘅最低要求", "sum"))),
    Scene("harm",
          "咁 IT Manager 唔識 Git，禍害有幾大？[[h1]]第一，兩個人改同一個 file，後 save 嗰個贏，前面嘅心血冇晒。"
          "[[h2]]第二，出事返唔到轉頭，只可以通頂。[[h3]]第三，冇記錄，邊個改咗乜，冇人知。"
          "[[h4]]第四，冇 code review，bug 直上 production。[[h5]]第五，source code 跟人走，同事一離職，最新版本就消失。"
          "[[h6]]最後，識做嘢嘅 programmer 頂唔順，走晒。",
          TileCard("唔識 Git，禍害有幾大？", [
              Tile("💥", "互相覆蓋", "同一個 file，後 save 嗰個贏", "h1", RED),
              Tile("⏪", "返唔到轉頭", "出事冇得 rollback，只可以通頂", "h2", AMBER),
              Tile("🔍", "責任不清", "冇記錄，邊個改咗乜冇人知", "h3", PURPLE),
              Tile("🐛", "冇 code review", "bug 直上 production", "h4", RED),
              Tile("💼", "Code 跟人走", "同事一離職，最新版本就消失", "h5", BLUE),
              Tile("🏃", "人才流失", "識做嘢嘅 programmer 走晒", "h6", TEAL),
          ], cols=3, gap=36)),
    Scene("story",
          "講個香港 IT 界經典鬼故。[[e1]]星期五六點，有人直接喺 server 度改 code；[[e2]]七點，網站死咗；"
          "[[e3]]九點想還原，先發現冇舊版本；[[e4]]凌晨三點，要打俾前同事，因為佢部手提先有舊 code；"
          "[[e5]]星期一，老闆問邊個改咗乜，冇人答得到。[[fix]]如果有 Git，一句 git revert，一分鐘搞掂。",
          TimelineCard("星期五晚嘅鬼故", [
              Event("星期五 6pm", "直接喺 server 改 code", "冇 commit、冇 review", "e1", AMBER),
              Event("7pm", "網站死咗", "客戶入唔到", "e2", RED),
              Event("9pm", "想還原", "先發現冇舊版本", "e3", RED),
              Event("凌晨 3am", "打俾前同事", "佢部手提先有舊 code", "e4", PURPLE),
              Event("星期一", "老闆問邊個改咗乜", "冇人答得到", "e5", MUTED),
          ], callout=("有 Git：git revert，一分鐘搞掂", "fix"))),
    Scene("lesson",
          "Manager 唔使做 Git 專家，但呢五個 command 一定要識。[[c1]]git clone，攞成個項目返嚟；"
          "[[c2]]git log，睇晒每次改動；[[c3]]git diff，睇今次改咗邊幾行；[[c4]]git blame，查呢行 code 邊個寫；"
          "[[c5]]git revert，出事即刻還原。[[note]]五個 command，半個鐘學識。",
          TableCard("Manager 必識五個 command", ["Command", "做乜"], [
              (["git clone <repo>", "攞成個項目返嚟"], "c1"),
              (["git log --oneline", "睇晒每次改動：邊個、幾時、改咗乜"], "c2"),
              (["git diff main", "今次改咗邊幾行"], "c3"),
              (["git blame login.py", "呢行 code 邊個寫"], "c4"),
              (["git revert a1b2c3d", "出事即刻還原"], "c5"),
          ], widths=[1, 1.25], note=("五個 command，半個鐘學識", "note"))),
    Scene("quiz",
          "做個小測驗，睇吓你個 Manager 係咪零 Git：[[t1]]叫同事 zip 埋份 code，email 俾佢 review；"
          "[[t2]]以為 Git 同 GitHub 係同一樣嘢；[[t3]]試過直接喺 production server 度改 code。"
          "[[t4]]中晒三樣，恭喜你，你身邊有一位零 Git Manager。",
          pill(BulletCard("零 Git Manager 自我檢測", [
              ("叫同事 zip 埋份 code，email 俾佢 review", "t1"),
              ("以為 Git 同 GitHub 係同一樣嘢", "t2"),
              ("試過直接喺 production server 改 code", "t3"),
          ]), "中晒三樣：恭喜你，身邊有位零 Git Manager", 700, "t4", RED)),
    Scene("fair",
          "不過公道啲講，[[n1]]Manager 唔使識 rebase、cherry-pick 呢啲進階招式，[[n2]]亦唔使親手解晒所有 merge conflict。"
          "[[y1]]但至少要知道 code 放喺邊個 repo，[[y2]]堅持每次改動都要 code review，[[y3]]出事識得 rollback。"
          "[[sum]]唔識寫 code 可以慢慢學，唔識 Git，就真係冇藉口。",
          CompareCard("公道啲講：Manager 要識幾多？", [
              Column("🙆", "唔使識", [("rebase、cherry-pick", "n1"), ("親手解晒 merge conflict", "n2")], MUTED),
              Column("✅", "一定要識", [("code 放喺邊個 repo", "y1"), ("每次改動都要 code review", "y2"),
                                        ("出事識得 rollback", "y3")], GREEN),
          ], footer=("唔識寫 code 可以學，唔識 Git 冇藉口", "sum", BLUE))),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]開一個 Git repo，commit 三次，再用 git log 睇返。學識咗，就 send 條 link 俾你個 Manager，記住，唔好 send zip。"
          "[[next]]多謝收睇，下次見！",
          EndCard("開一個 Git repo，commit 三次，再用 git log 睇返。學識咗，就 send 條 link 俾你個 Manager。記住：唔好 send zip。",
                  "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
