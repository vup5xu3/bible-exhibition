# -*- coding: utf-8 -*-
"""
產生靜態資料檔 data.js，取代 Supabase 作為 index.html 的資料來源。

來源：
  1. _build/legacy_cards.json   — 專案早期就存在、非 JSON 驅動的人物（族長系列等）
  2. _build/people/*.json       — 本次擴充、由 render.py 同時產生頁面的人物

輸出：
  data.js（專案根目錄）— 定義 window.BIBLE_CHARACTERS 陣列，供 index.html 直接引用。

執行： python _build/make_static_data.py

── tier 欄位（重要度，三級，累進篩選：全部 ⊇ 常見人物 ⊇ 重要人物）──
  "major"  重要人物 — 聖經敘事核心角色／貫穿多卷書／信仰教導上最常被引用（如亞伯拉罕、大衛、保羅）
  "common" 常見人物 — 有完整、能獨立成篇的情節，一般讀者聽過或講道常引用，但非核心主線
           （如波阿斯、拿俄米、尼哥底母、該亞法、十二使徒中較少被談及的幾位）
  "normal" 其餘人物 — 主要為家譜連結／單次提及／篇幅極短，缺乏獨立情節（如家譜中的父子鏈、單一經節人物）
  新增人物 JSON 時請依此標準指定 tier；index.html 的「常見人物」篩選鈕會自動包含 major。
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.dirname(os.path.abspath(__file__))
PEOPLE = os.path.join(BUILD, "people")
LEGACY = os.path.join(BUILD, "legacy_cards.json")
OUT = os.path.join(ROOT, "data.js")

sys.path.insert(0, BUILD)
from books import BOOK_ORDER, PERSON_BOOK  # noqa: E402

# ── 卡片顯示順序：依人物在聖經敘事中首次出現的先後（創世記→...→使徒書信），
#    唯一例外是 zhu_hongen（末後首位使徒）依使用者要求固定排在最前面。
#    新增人物時，請把 id 插入這個清單中對應的歷史／敘事位置；若忘記加入，
#    程式會把它們依字母序放在最後並印出提醒，而不會遺漏或報錯。
CHRONO_ORDER = [
    "zhu_hongen", "genesis_primeval", "enoch", "abraham", "sarah", "lot", "melchizedek",
    "hagar", "ishmael", "isaac", "rebekah", "esau", "jacob", "leah",
    "rachel", "dinah", "reuben", "judah", "tamar_judah", "perez", "zerah",
    "hezron", "joseph_patriarch", "potiphars_wife", "benjamin", "job", "moses", "jethro", "aaron",
    "miriam", "korah", "balaam", "balak", "ram", "amminadab", "nahshon", "caleb",
    "joshua", "rahab", "achan", "ehud", "deborah", "jael",
    "gideon", "jephthah", "manoah", "samson", "delilah", "naomi",
    "ruth", "boaz", "jesse", "eli", "hannah", "samuel",
    "saul_king", "jonathan", "abner", "rizpah", "michal", "abigail", "nabal",
    "david", "mephibosheth", "bathsheba", "uriah", "nathan_prophet",
    "tamar_david", "amnon", "absalom", "ahithophel", "shimei", "joab", "adonijah",
    "solomon", "queen_of_sheba", "jeroboam",
    "rehoboam", "abijah_king", "asa", "jehoshaphat", "joram_king", "ahab",
    "jezebel", "elijah", "widow_zarephath", "naboth", "elisha", "shunammite_woman",
    "naaman", "gehazi", "jehu", "athaliah", "jonah", "hosea", "isaiah",
    "uzziah", "jotham", "ahaz", "hezekiah",
    "manasseh", "amon", "josiah", "jeremiah", "jeconiah", "ezekiel",
    "daniel", "vashti", "esther", "haman", "mordecai", "shealtiel", "zerubbabel",
    "ezra", "nehemiah", "genealogy_silent_nine",
    "zechariah_elizabeth", "john_baptist", "mary_mother", "joseph_husband", "simeon_anna", "peter",
    "andrew", "james_zebedee", "john_apostle", "philip_apostle", "bartholomew", "thomas",
    "matthew", "james_alphaeus", "thaddaeus", "simon_zealot", "judas_iscariot", "centurion_capernaum",
    "nicodemus",
    "samaritan_woman", "gerasene_demoniac", "jairus", "bleeding_woman", "canaanite_woman", "herod_antipas", "herodias",
    "rich_young_ruler", "woman_adultery",
    "martha", "mary_bethany", "lazarus", "zacchaeus", "bartimaeus", "samaritan_leper",
    "mary_magdalene", "cleopas", "james_brother", "jude_brother", "caiaphas", "pontius_pilate", "barabbas",
    "simon_cyrene", "joseph_arimathea", "matthias", "barnabas", "ananias_sapphira", "gamaliel",
    "stephen", "paul", "philip_evangelist", "simon_magus", "ethiopian_eunuch", "ananias_damascus",
    "dorcas", "cornelius", "herod_agrippa_i", "john_mark", "silas", "timothy", "lydia",
    "philippian_jailer", "priscilla_aquila", "apollos", "eutychus", "titus", "phoebe",
    "onesimus", "luke",
]


def card_from_person_json(pid, d):
    """把 render.py 用的完整人物 JSON，抽取成卡片所需的精簡欄位。"""
    return {
        "id": pid,
        "name": d["name"],
        "epithet": d.get("epithet") or None,
        "name_en": d["nameEn"],
        "avatar": d["avatar"],
        "description": d["desc"],
        "mbti": d.get("mbti") or None,
        "file_name": "portrait_%s.html" % pid,
        "categories": d.get("categories", []),
        "tags": d.get("tags", []),
        "tier": d.get("tier", "normal"),
        "book": PERSON_BOOK.get(pid),
    }


def main():
    cards = []

    # 1. legacy 卡片（保留原本的 sort_order）
    legacy = json.load(io.open(LEGACY, encoding="utf-8"))
    for r in legacy:
        cards.append({
            "id": r["id"], "name": r["name"], "epithet": r.get("epithet"),
            "name_en": r["name_en"], "avatar": r["avatar"],
            "description": r["description"], "mbti": r.get("mbti"),
            "file_name": r["file_name"], "categories": r["categories"],
            "tags": r.get("tags", []), "tier": r.get("tier", "normal"),
            "book": PERSON_BOOK.get(r["id"]),
        })

    # 2. 本次擴充的人物（依檔名字母序，穩定排序）
    new_ids = sorted(f[:-5] for f in os.listdir(PEOPLE) if f.endswith(".json"))
    for pid in new_ids:
        d = json.load(io.open(os.path.join(PEOPLE, pid + ".json"), encoding="utf-8"))
        cards.append(card_from_person_json(pid, d))

    # 3. 依 CHRONO_ORDER（聖經敘事出現先後，朱虹恩例外置頂）排序，重新編號 sort_order。
    #    不在清單中的新人物：印出提醒，並依字母序接在最後，不影響其餘人排序。
    rank = {pid: i for i, pid in enumerate(CHRONO_ORDER)}
    unranked = sorted(c["id"] for c in cards if c["id"] not in rank)
    if unranked:
        print("⚠ 尚未加入 CHRONO_ORDER，暫時排在最後（請補進 make_static_data.py）：%s" % ", ".join(unranked))
    cards.sort(key=lambda c: (rank.get(c["id"], len(CHRONO_ORDER)), c["id"]))
    for i, c in enumerate(cards, start=1):
        c["sort_order"] = i

    # 朱虹恩非聖經人物，book 欄位保持 None（前端「依聖經卷別」統計會自動略過）；
    # 其餘若忘記在 books.py 補上對照，同樣印出提醒但不中斷產生流程。
    unbooked = sorted(c["id"] for c in cards if c["book"] is None and c["id"] != "zhu_hongen"
                       and "study" not in c["categories"])
    if unbooked:
        print("⚠ 尚未加入 books.py 的 PERSON_BOOK，「依聖經卷別」統計會略過：%s" % ", ".join(unbooked))

    books_js = [{"id": b, "name": zh, "target": t} for b, zh, t in BOOK_ORDER]

    js = (
        "// 本檔由 _build/make_static_data.py 自動產生，請勿手動編輯。\n"
        "// 如需新增/修改人物：編輯 _build/people/*.json 或 _build/legacy_cards.json，\n"
        "// 然後重新執行 python _build/make_static_data.py 覆蓋本檔。\n"
        "window.BIBLE_CHARACTERS = "
        + json.dumps(cards, ensure_ascii=False, indent=2)
        + ";\n\n"
        "// 聖經 66 卷書的顯示順序與「預估有情節人物數」，供閱讀進度頁籤的\n"
        "// 「依聖經卷別」區塊使用（估算方式見 _build/books.py 檔頭說明）。\n"
        "window.BIBLE_BOOKS = "
        + json.dumps(books_js, ensure_ascii=False, indent=2)
        + ";\n"
    )
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(js)

    print("已寫出 %s（共 %d 位人物：legacy %d + 新增 %d）" % (
        os.path.relpath(OUT, ROOT), len(cards), len(legacy), len(new_ids)))
    major = sum(1 for c in cards if c["tier"] == "major")
    common = sum(1 for c in cards if c["tier"] == "common")
    normal = sum(1 for c in cards if c["tier"] not in ("major", "common"))
    with_mbti = sum(1 for c in cards if c["mbti"])
    print("  重要人物(major): %d｜常見人物(common): %d｜其餘(normal): %d｜有 MBTI: %d" % (
        major, common, normal, with_mbti))


if __name__ == "__main__":
    main()
