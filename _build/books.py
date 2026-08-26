# -*- coding: utf-8 -*-
"""
聖經 66 卷書 × 人物對照表，供 make_static_data.py 產生「依聖經卷別」的
閱讀進度統計使用（index.html 的「閱讀進度」頁籤）。

BOOK_ORDER  ── 66 卷書，依正典順序排列：(book_id, 中文書名, target)
  target 是本站對「這卷書中有完整情節、值得單獨立傳的人物」數量的估算，
  採用與 tier 分級相同的標準（見 make_static_data.py 檔頭說明）——
  不是「這卷書提到幾個名字」，而是「值得寫成一篇 PORTRAIT 的人物大約有幾位」。
  這是本站自己的策展估算，不是學術界的公認數字，會隨著擴充逐步校正。

PERSON_BOOK ── 人物 id → 主要出處書卷 id。
  多數人物橫跨數卷書（如大衛：撒上～王上），這裡只標記「故事重心最集中」的
  一卷；新增人物時記得補上，忘記補的話會在 make_static_data.py 執行時印出提醒。
"""

BOOK_ORDER = [
    ("genesis", "創世記", 28),
    ("exodus", "出埃及記", 10),
    ("leviticus", "利未記", 2),
    ("numbers", "民數記", 9),
    ("deuteronomy", "申命記", 1),
    ("joshua", "約書亞記", 6),
    ("judges", "士師記", 15),
    ("ruth", "路得記", 5),
    ("1samuel", "撒母耳記上", 20),
    ("2samuel", "撒母耳記下", 18),
    ("1kings", "列王紀上", 20),
    ("2kings", "列王紀下", 20),
    ("1chronicles", "歷代志上", 2),
    ("2chronicles", "歷代志下", 3),
    ("ezra", "以斯拉記", 4),
    ("nehemiah", "尼希米記", 4),
    ("esther", "以斯帖記", 5),
    ("job", "約伯記", 5),
    ("psalms", "詩篇", 1),
    ("proverbs", "箴言", 1),
    ("ecclesiastes", "傳道書", 1),
    ("songofsongs", "雅歌", 2),
    ("isaiah", "以賽亞書", 3),
    ("jeremiah", "耶利米書", 5),
    ("lamentations", "耶利米哀歌", 1),
    ("ezekiel", "以西結書", 1),
    ("daniel", "但以理書", 6),
    ("hosea", "何西阿書", 2),
    ("joel", "約珥書", 1),
    ("amos", "阿摩司書", 2),
    ("obadiah", "俄巴底亞書", 1),
    ("jonah", "約拿書", 2),
    ("micah", "彌迦書", 1),
    ("nahum", "那鴻書", 1),
    ("habakkuk", "哈巴谷書", 1),
    ("zephaniah", "西番雅書", 1),
    ("haggai", "哈該書", 1),
    ("zechariah", "撒迦利亞書", 2),
    ("malachi", "瑪拉基書", 1),
    ("matthew", "馬太福音", 8),
    ("mark", "馬可福音", 3),
    ("luke", "路加福音", 8),
    ("john", "約翰福音", 8),
    ("acts", "使徒行傳", 30),
    ("romans", "羅馬書", 3),
    ("1corinthians", "哥林多前書", 2),
    ("2corinthians", "哥林多後書", 2),
    ("galatians", "加拉太書", 1),
    ("ephesians", "以弗所書", 1),
    ("philippians", "腓立比書", 2),
    ("colossians", "歌羅西書", 2),
    ("1thessalonians", "帖撒羅尼迦前書", 1),
    ("2thessalonians", "帖撒羅尼迦後書", 1),
    ("1timothy", "提摩太前書", 2),
    ("2timothy", "提摩太後書", 2),
    ("titus", "提多書", 2),
    ("philemon", "腓利門書", 2),
    ("hebrews", "希伯來書", 1),
    ("james", "雅各書", 1),
    ("1peter", "彼得前書", 1),
    ("2peter", "彼得後書", 1),
    ("1john", "約翰一書", 1),
    ("2john", "約翰二書", 1),
    ("3john", "約翰三書", 2),
    ("jude", "猶大書", 1),
    ("revelation", "啟示錄", 3),
]

BOOK_NAME = {b: zh for b, zh, _ in BOOK_ORDER}
BOOK_TARGET = {b: t for b, zh, t in BOOK_ORDER}

PERSON_BOOK = {
    # ── 創世記 ──
    "abraham": "genesis", "sarah": "genesis", "lot": "genesis", "melchizedek": "genesis",
    "hagar": "genesis", "ishmael": "genesis", "isaac": "genesis", "rebekah": "genesis", "esau": "genesis",
    "jacob": "genesis", "leah": "genesis", "rachel": "genesis", "dinah": "genesis", "reuben": "genesis",
    "judah": "genesis", "tamar_judah": "genesis", "perez": "genesis", "zerah": "genesis",
    "hezron": "genesis", "joseph_patriarch": "genesis", "potiphars_wife": "genesis", "benjamin": "genesis",
    "genesis_primeval": "genesis", "enoch": "genesis",

    # ── 出埃及記／民數記 ──
    "moses": "exodus", "jethro": "exodus", "aaron": "exodus", "miriam": "exodus",
    "korah": "numbers", "balaam": "numbers", "balak": "numbers", "amminadab": "numbers", "nahshon": "numbers", "caleb": "numbers",

    # ── 約書亞記 ──
    "joshua": "joshua", "rahab": "joshua", "achan": "joshua",

    # ── 士師記 ──
    "ehud": "judges", "deborah": "judges", "jael": "judges", "gideon": "judges",
    "jephthah": "judges", "manoah": "judges", "samson": "judges", "delilah": "judges",

    # ── 路得記 ──
    "naomi": "ruth", "ruth": "ruth", "boaz": "ruth", "jesse": "ruth", "ram": "ruth",

    # ── 撒母耳記上 ──
    "eli": "1samuel", "hannah": "1samuel", "samuel": "1samuel", "saul_king": "1samuel",
    "jonathan": "1samuel", "abner": "1samuel", "michal": "1samuel", "abigail": "1samuel",
    "nabal": "1samuel",

    # ── 撒母耳記下 ──
    "david": "2samuel", "mephibosheth": "2samuel", "rizpah": "2samuel", "bathsheba": "2samuel", "uriah": "2samuel",
    "nathan_prophet": "2samuel", "absalom": "2samuel", "tamar_david": "2samuel", "amnon": "2samuel", "shimei": "2samuel",
    "ahithophel": "2samuel", "joab": "2samuel",

    # ── 列王紀上 ──
    "adonijah": "1kings", "solomon": "1kings", "queen_of_sheba": "1kings", "jeroboam": "1kings", "rehoboam": "1kings",
    "abijah_king": "1kings", "asa": "1kings", "jehoshaphat": "1kings", "joram_king": "1kings",
    "ahab": "1kings", "jezebel": "1kings", "elijah": "1kings", "widow_zarephath": "1kings",
    "naboth": "1kings",

    # ── 列王紀下 ──
    "elisha": "2kings", "shunammite_woman": "2kings", "naaman": "2kings", "gehazi": "2kings",
    "jehu": "2kings", "athaliah": "2kings", "uzziah": "2kings", "jotham": "2kings", "ahaz": "2kings",
    "hezekiah": "2kings", "manasseh": "2kings", "amon": "2kings", "josiah": "2kings",
    "jeconiah": "2kings",

    # ── 先知書（各書以自己為主要出處）──
    "jonah": "jonah", "hosea": "hosea", "isaiah": "isaiah", "jeremiah": "jeremiah",
    "ezekiel": "ezekiel", "daniel": "daniel",

    # ── 以斯帖記 ──
    "vashti": "esther", "esther": "esther", "haman": "esther", "mordecai": "esther",

    # ── 以斯拉記／尼希米記 ──
    "shealtiel": "ezra", "zerubbabel": "ezra", "ezra": "ezra", "nehemiah": "nehemiah",

    # ── 約伯記 ──
    "job": "job",

    # ── 家譜過渡（馬太福音 1 章的橋接名單）──
    "genealogy_silent_nine": "matthew",

    # ── 路加福音（誕生敘事）──
    "zechariah_elizabeth": "luke", "john_baptist": "luke", "mary_mother": "luke", "jesus_christ": "luke",
    "simeon_anna": "luke", "zacchaeus": "luke", "samaritan_leper": "luke", "cleopas": "luke",

    # ── 馬太福音 ──
    "joseph_husband": "matthew", "peter": "matthew", "andrew": "matthew",
    "james_zebedee": "matthew", "john_apostle": "matthew", "philip_apostle": "matthew",
    "bartholomew": "matthew", "matthew": "matthew", "james_alphaeus": "matthew",
    "thaddaeus": "matthew", "simon_zealot": "matthew", "judas_iscariot": "matthew",
    "centurion_capernaum": "matthew",
    "canaanite_woman": "matthew", "rich_young_ruler": "matthew", "caiaphas": "matthew",
    "pontius_pilate": "matthew", "barabbas": "matthew",

    # ── 馬可福音 ──
    "gerasene_demoniac": "mark", "jairus": "mark", "bleeding_woman": "mark", "herod_antipas": "mark", "herodias": "mark",
    "bartimaeus": "mark", "simon_cyrene": "mark",

    # ── 約翰福音 ──
    "nicodemus": "john", "samaritan_woman": "john", "woman_adultery": "john", "martha": "john", "mary_bethany": "john",
    "lazarus": "john", "thomas": "john", "mary_magdalene": "john", "joseph_arimathea": "john",

    # ── 使徒行傳 ──
    "james_brother": "acts", "jude_brother": "acts", "matthias": "acts", "barnabas": "acts",
    "ananias_sapphira": "acts", "gamaliel": "acts", "stephen": "acts", "paul": "acts",
    "philip_evangelist": "acts", "simon_magus": "acts", "ethiopian_eunuch": "acts",
    "ananias_damascus": "acts", "dorcas": "acts", "cornelius": "acts", "herod_agrippa_i": "acts",
    "john_mark": "acts",
    "silas": "acts", "timothy": "acts", "lydia": "acts", "philippian_jailer": "acts",
    "priscilla_aquila": "acts", "apollos": "acts", "eutychus": "acts", "luke": "acts",

    # ── 書信 ──
    "titus": "titus", "phoebe": "romans", "onesimus": "philemon",
}
