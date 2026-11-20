#!/usr/bin/env python3
"""零 Code PM 講 OOP：滿口 inheritance、polymorphism，但唔知係乜

The fifth 「IT 職場講堂」 satire. The 零 Code PM who talks object-oriented programming all day
but has the terms wrong: inheritance is a handover when someone resigns, polymorphism is one person
doing three jobs. The video shows the chat, what the PM thinks each term means next to what it
really means, OOP in one small Python program, the PM's own class design (Email inherits Payment
inherits Order inherits Customer) against is-a and has-a, the harms, a self-test, a fair word and
a polymorphism challenge.

The archetype is the channel's own observation, not a survey. The characters and dialogue are made
up; no real person, company or project is named.

    python3 oop_pm.py              # -> out/oop_pm.mp4 (narration is cached)
    python3 oop_pm.py --draft      # silent, estimated timing, fast: for checking layout
    python3 oop_pm.py --stills     # two PNGs per scene in build/oop_pm/stills/
    python3 oop_pm.py --redo chat  # regenerate one scene's narration
"""

from pathlib import Path

from hkpsvid import *  # noqa: F403  (switches to the video venv first if needed)
from hkpsvid import draw as D

VIDEO = Video(slug=Path(__file__).stem, title="零 Code PM 講 OOP", series="IT 職場講堂")
opts = options(VIDEO)

# What the TTS is given for words it would otherwise misread (the subtitles keep the display form).
SAY = {
    "PM": "P M",
    "IT": "I T",
    "OOP": "O O P",
    "VIP": "V I P",
}

PM = ("👔", "PM", PURPLE)
DEV = ("💻", "Programmer", TEAL)


def pill(card: Card, text: str, y: int, at, color=AMBER, size: int = 42) -> Card:
    """Adds a centred coloured pill to any card (a punchline or a takeaway)."""
    card.add_center(D.pill(text, font(size, "bold"), WHITE, color, px=40, py=14), y, at=at, anim="pop", sound="pop")
    return card


OOP_CODE = """class Customer:
    def __init__(self, name):
        self.name = name
        self.__points = 0
    def discount(self):
        return 0

class VIP(Customer):
    def discount(self):
        return 0.2

for c in [Customer("阿明"), VIP("陳生")]:
    print(c.name, c.discount())"""

PM_DESIGN = """class Customer: ...
class Order(Customer): ...    # 屬於客戶
class Payment(Order): ...     # 跟住訂單
class Email(Payment): ...     # 付完款 send"""

GOOD_DESIGN = """class Customer: ...
class VIP(Customer): ...      # 係一種客戶

class Order:
    def __init__(self, customer):
        self.customer = customer  # 有一個客戶"""

scenes = [
    Scene("intro",
          "大家好！歡迎返嚟 IT 職場講堂。今集嘅零 Code PM，開口埋口都係 OOP："
          "inheritance、polymorphism、encapsulation，講到好專業咁。"
          "但係你問佢 class 同 object 有咩分別，佢就答唔出。",
          TitleCard(VIDEO.series, "吐糟篇", "滿口 OOP 嘅零 Code PM", VIDEO.title,
                    "Inheritance、polymorphism：講得出，答唔出"), seed=12),
    Scene("chat",
          "睇吓一個經典場面。[[m1]]PM 話：呢個系統一定要 OOP，inheritance、polymorphism，全部用晒！"
          "[[m2]]Programmer 問：好呀。咁 VIP 客戶係咪繼承普通客戶？discount 點計？"
          "[[m3]]PM 話：Inheritance 即係有人辭職，啲嘢交俾邊個 inherit 囉。咁都唔識？"
          "[[out]]原來喺佢心目中，inheritance 即係工作交接。",
          ChatCard("經典場面", [PM, DEV], [
              Msg(0, "呢個系統一定要 OOP，inheritance、polymorphism，全部用晒！", "m1"),
              Msg(1, "好呀。咁 VIP 客戶係咪繼承普通客戶？discount 點計？", "m2"),
              Msg(0, "Inheritance 即係有人辭職，啲嘢交俾邊個 inherit 囉。咁都唔識？", "m3"),
          ], footer=("Inheritance ≠ 工作交接", "out", RED))),
    Scene("dict",
          "零 Code PM 心目中嘅 OOP，係咁嘅：[[d1]]object，佢以為係開會問：有冇人 object？"
          "[[d2]]inheritance，佢以為係工作交接；[[d3]]polymorphism，佢以為係一個人做幾份工；"
          "[[d4]]encapsulation，佢以為係打包成 zip；[[d5]]abstraction，佢以為係 spec 寫抽象啲，等 dev 自己諗。"
          "[[note]]右邊，先係真正嘅意思。",
          TableCard("PM 以為 vs 真正意思", ["Term", "PM 以為", "真正意思"], [
              (["Object", "「有冇人 object？冇就照做」", "有資料、有行為嘅一件嘢"], "d1"),
              (["Inheritance", "同事辭職，工作交接", "子 class 自動有 parent 嘅嘢"], "d2"),
              (["Polymorphism", "一個人做幾份工", "同一個 method，唔同 object 唔同做法"], "d3"),
              (["Encapsulation", "打包成 zip", "收埋內部資料，唔俾外面亂改"], "d4"),
              (["Abstraction", "Spec 寫抽象啲，dev 自己諗", "隱藏細節，只露出要用嘅功能"], "d5"),
          ], widths=[0.8, 1.1, 1.3], size=36, note=("講得出名，唔代表知係乜", "note"))),
    Scene("lesson",
          "既然咁，我哋用十三行 code，幫 PM 補補課。[[c1]]Class 係藍圖，例如客戶呢個概念；"
          "[[c2]]積分收埋喺入面，唔俾外面亂改，就係 encapsulation；"
          "[[c3]]VIP 繼承 Customer，自動有晒名同積分，就係 inheritance；"
          "[[c4]]同樣問一句 discount，普通客答零，VIP 答兩成，就係 polymorphism；"
          "[[c5]]最後用藍圖整出阿明同陳生兩個客，佢哋就係 object。",
          CodeCard("OOP 速成班（PM 專用）", OOP_CODE, name="shop.py", size=28, marks=[
              ((1, 1), "Class：藍圖", "c1", BLUE),
              ((4, 4), "Encapsulation：收埋", "c2", PURPLE),
              ((8, 8), "Inheritance：繼承", "c3", TEAL),
              ((9, 10), "Polymorphism：唔同做法", "c4", AMBER),
              ((12, 12), "Object：整出嚟嘅客", "c5", GREEN),
          ], width=1000)),
    Scene("design",
          "PM 仲要親自落手設計 class。[[bad]]佢話訂單屬於客戶，所以 Order 繼承 Customer；"
          "付款跟住訂單，所以 Payment 繼承 Order；再嚟 Email 繼承 Payment。"
          "結果一封 email，有齊客戶資料、訂單同信用卡。"
          "[[good]]正確做法：訂單唔係一種客戶，佢只係有一個客戶，所以將 customer 放入 Order 入面；"
          "而 VIP 真係一種客戶，先用繼承。[[rule]]係一種，先用 inheritance；有一個，就用 composition。",
          pill(CodeCompareCard("PM 設計嘅 class", [
              Pane("PM 設計：一路繼承落去", PM_DESIGN, good=False, at="bad", name="design.py"),
              Pane("正確：分清「係」同「有」", GOOD_DESIGN, good=True, at="good", name="design.py"),
          ], size=28), "「係一種」用 inheritance　·　「有一個」用 composition", 720, "rule", BLUE, size=40)),
    Scene("harm",
          "咁對團隊有咩影響？[[h1]]第一，過度設計：三行搞掂嘅嘢，要求開十個 class。"
          "[[h2]]第二，繼承地獄：一路繼承落去，改一個 parent，成條鏈爛晒。"
          "[[h3]]第三，用 term 做 KPI：規定每個 module 都要有 polymorphism。"
          "[[h4]]第四，開會雞同鴨講：佢講 inheritance，你諗 code，佢諗交接。"
          "[[h5]]第五，解釋 term 嘅時間，多過寫 code。[[h6]]最後，冇人敢反駁，因為一開口，佢就話你唔識 OOP。",
          TileCard("對團隊有咩影響？", [
              Tile("🏗️", "過度設計", "三行搞掂嘅嘢，要開十個 class", "h1", RED),
              Tile("🌳", "繼承地獄", "改一個 parent，成條鏈爛晒", "h2", AMBER),
              Tile("📋", "用 term 做 KPI", "「每個 module 都要有 polymorphism」", "h3", PURPLE),
              Tile("🦆", "雞同鴨講", "你講 inheritance，佢諗交接", "h4", BLUE),
              Tile("⏳", "浪費時間", "解釋 term 多過寫 code", "h5", TEAL),
              Tile("🤐", "冇人敢反駁", "一開口就話你「唔識 OOP」", "h6", RED),
          ], cols=3, gap=36)),
    Scene("quiz",
          "做個小測驗，睇吓你身邊有冇滿口 OOP 嘅零 Code PM：[[t1]]以為 inheritance 即係工作交接；"
          "[[t2]]規定全部 code 都要用 polymorphism；[[t3]]問佢 class 同 object 有咩分別，佢話：一樣啫。"
          "[[t4]]中晒三樣，恭喜你，你身邊有一位 OOP 零 Code PM。",
          pill(BulletCard("OOP 零 Code PM 自我檢測", [
              ("以為 inheritance 即係工作交接", "t1"),
              ("規定全部 code 都要用 polymorphism", "t2"),
              ("問佢 class 同 object 有咩分別，佢話「一樣啫」", "t3"),
          ]), "中晒三樣：恭喜你，身邊有位 OOP 零 Code PM", 700, "t4", RED)),
    Scene("fair",
          "不過公道啲講，[[n1]]PM 唔使背晒二十三個 design pattern，[[n2]]亦唔使親手寫 class。"
          "[[y1]]但至少要知 class 同 object 嘅分別；[[y2]]分得清係一種同有一個；"
          "[[y3]]知道用 OOP，係為咗 code 易改、易重用，唔係為咗好聽。[[sum]]OOP 係工具，唔係口號。",
          CompareCard("公道啲講：PM 要識幾多？", [
              Column("🙆", "唔使識", [("背晒 23 個 design pattern", "n1"), ("親手寫 class", "n2")], MUTED),
              Column("✅", "一定要識", [("class 同 object 嘅分別", "y1"), ("分得清「係一種」同「有一個」", "y2"),
                                        ("用 OOP 係為咗易改、易重用", "y3")], GREEN),
          ], footer=("OOP 係工具，唔係口號", "sum", BLUE))),
    Scene("outro",
          "最後俾個小挑戰你：[[ch]]寫一個 Animal class，再整 Dog 同 Cat，各自叫一聲。"
          "寫完 send 俾你個 PM，問佢呢個係咩 concept。[[next]]多謝收睇，下次見！",
          EndCard("寫一個 Animal class，再整 Dog 同 Cat，各自叫一聲。寫完 send 俾你個 PM，問佢呢個係咩 concept。",
                  "香港編程學會 · 一齊學、一齊傾", challenge_at="ch", next_at="next")),
]

build(VIDEO, scenes, opts, say=SAY)
