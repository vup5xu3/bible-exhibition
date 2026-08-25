# -*- coding: utf-8 -*-
"""
PORTRAIT 聖經人物頁面產生器
────────────────────────────────────────────────────────────
把 _build/people/*.json 的內容資料，套進 portrait_template.html 的版型，
產出 portrait_{id}.html。

用途：人物數量擴充到數百位時，確保每一頁的八大維度結構完全一致；
      版型若要調整，改 _build/shell_head.html 與本檔後全部重新產生即可。

執行： python _build/render.py            # 產生全部
      python _build/render.py peter paul  # 只產生指定人物
"""
import io, json, os, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "_build")
PEOPLE = os.path.join(BUILD, "people")

DOT_CLASS = {"major": "major", "dark": "dark", "final": "final", "normal": ""}
BADGE_CLASS = {"major": "badge-major", "dark": "badge-dark", "final": "badge-normal", "normal": "badge-normal"}
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def e(s):
    """一般文字：完整跳脫。"""
    return html.escape(str(s if s is not None else ""), quote=False)


def r(s):
    """允許內嵌 <br> 的欄位：先跳脫再還原 <br>。"""
    return e(s).replace("&lt;br&gt;", "<br>")


# ── 各章節渲染 ─────────────────────────────────────────────

def hero(d):
    m = d["hero"]["meta"]
    epithet = d.get("epithet", "")
    name = e(d["name"]) + (("・" + e(epithet)) if epithet else "")
    cells = "".join(
        '\n    <div class="hero-meta-item">'
        '\n      <span class="hero-meta-label">%s</span>'
        '\n      <span class="hero-meta-value">%s</span>'
        '\n    </div>' % (e(k), r(v)) for k, v in m
    )
    return """
<!-- HERO -->
<div class="hero">
  <div class="hero-label">PORTRAIT · 聖經人物深度研究報告</div>
  <h1 class="hero-name">%s</h1>
  <span class="hero-name-en">%s · %s</span>
  <p class="hero-slogan">「%s」</p>
  <div class="hero-meta">%s
  </div>
  <div class="hero-divider"></div>
</div>

<!-- NAV -->
<nav class="nav">
  <a class="nav-home" href="index.html">← 返回總目錄</a>
  <a href="#portrait">I · 人物素描</a>
  <a href="#timeline">II · 生命軌跡</a>
  <a href="#character">III · 性格剖析</a>
  <a href="#relations">IV · 關係網絡</a>
  <a href="#theology">V · 神學意義</a>
  <a href="#mirror">VI · 鏡照今日</a>
  <a href="#voice">VII · 現代轉譯</a>
  <a href="#legacy">VIII · 歷史遺產</a>
</nav>

<div class="container">
""" % (name, e(d["nameEn"]), e(d["original"]), r(d["hero"]["slogan"]), cells)


def head(n, title, subtitle, epigraph):
    return """
  <div class="section" id="%s">
    <div class="section-header">
      <span class="section-roman">%s</span>
      <h2 class="section-title">%s</h2>
      <span class="section-subtitle">%s</span>
    </div>
    <p class="section-epigraph">%s</p>
""" % (n, ROMAN[SECTIONS.index(n)], title, subtitle, r(epigraph))


SECTIONS = ["portrait", "timeline", "character", "relations", "theology", "mirror", "voice", "legacy"]


def sec_portrait(d):
    s = d["portrait"]
    cells = "".join(
        '\n      <div class="info-cell">'
        '\n        <span class="info-cell-label">%s</span>'
        '\n        <div class="info-cell-value">%s</div>'
        '\n      </div>' % (e(k), r(v)) for k, v in s["info"]
    )
    paras = "".join("\n    <p>%s</p>" % r(p) for p in s["paragraphs"])
    return (head("portrait", "Portrait · 人物素描", "時代、身份與背景", s["epigraph"])
            + '\n    <div class="info-grid">%s\n    </div>\n%s\n  </div>\n' % (cells, paras))


def sec_timeline(d):
    s = d["timeline"]
    items = ""
    for it in s["items"]:
        k = it.get("kind", "normal")
        dot = ("timeline-dot " + DOT_CLASS[k]).strip()
        items += """
      <div class="timeline-item">
        <div class="%s"></div>
        <span class="timeline-badge %s">%s</span>
        <div class="timeline-title">%s</div>
        <div class="timeline-body">%s</div>
        <div class="timeline-ref">%s</div>
      </div>
""" % (dot, BADGE_CLASS[k], e(it["badge"]), e(it["title"]), r(it["body"]), e(it["ref"]))
    return (head("timeline", "Timeline · 生命軌跡", "一生的轉折", s["epigraph"])
            + '\n    <div class="timeline">%s    </div>\n  </div>\n' % items)


def sec_character(d):
    s = d["character"]
    rows = ""
    for icon, label, title, body in s["soul"]:
        rows += """
      <div class="soul-row">
        <div class="soul-icon">%s</div>
        <div>
          <span class="soul-label">%s</span>
          <div class="soul-title">%s</div>
          <div class="soul-body">%s</div>
        </div>
      </div>
""" % (icon, e(label), e(title), r(body))
    m = s["mbti"]
    fns = ""
    for label, code, name, body in m["functions"]:
        fns += """
        <div class="mbti-fn">
          <span class="mbti-fn-label">%s</span>
          <span class="mbti-fn-code">%s · %s</span>
          <div class="mbti-fn-body">%s</div>
        </div>
""" % (e(label), e(code), e(name), r(body))
    return (head("character", "Character · 性格剖析", "靈魂的輪廓", s["epigraph"])
            + '\n    <div class="soul-grid">%s    </div>\n' % rows
            + '\n    <div class="insight-box">%s</div>\n' % r(s["insight"])
            + '\n    <h3 style="font-family:\'Noto Serif TC\',serif; font-size:16px; font-weight:500; color:var(--ink); margin: 28px 0 16px; letter-spacing:0.05em;">MBTI 認知功能微觀分析</h3>'
            + """
    <div class="mbti-card">
      <span class="mbti-type">%s</span>
      <div class="mbti-name">%s · %s</div>
      <div class="mbti-slogan">「%s」</div>
      <div class="mbti-functions">%s      </div>
    </div>
  </div>
""" % (e(m["type"]), e(m["name"]), e(m["alias"]), r(m["slogan"]), fns))


def sec_relations(d):
    s = d["relations"]
    cards = ""
    for c in s["cards"]:
        cards += """
      <div class="relation-card">
        <div class="relation-name-block">
          <div class="relation-avatar">%s</div>
          <div class="relation-name">%s</div>
          <div class="relation-type-badge">%s</div>
        </div>
        <div>
          <span class="relation-label">關鍵影響</span>
          <div class="relation-value">%s</div>
          <div class="relation-ref">%s</div>
        </div>
      </div>
""" % (e(c["avatar"]), e(c["name"]), e(c["type"]), r(c["body"]), e(c["ref"]))
    return (head("relations", "Relations · 關係網絡", "愛、忠誠與張力", s["epigraph"])
            + '\n    <div class="relation-list">%s    </div>\n  </div>\n' % cards)


def sec_theology(d):
    s = d["theology"]
    words = ""
    for w in s["words"]:
        words += """
      <div class="word-card">
        <span class="word-original">%s</span>
        <div class="word-transliteration">%s · %s</div>
        <span class="word-section-label">字面原意</span>
        <div class="word-section-body">%s</div>
        <span class="word-section-label">神學重量</span>
        <div class="word-section-body">%s</div>
      </div>
""" % (e(w["original"]), e(w["translit"]), e(w["lang"]), r(w["literal"]), r(w["weight"]))
    ins = "".join("""
    <div class="theology-insight">
      <div class="theology-insight-title">%s</div>
      <div class="theology-insight-body">%s</div>
    </div>
""" % (e(t), r(b)) for t, b in s["insights"])
    typ = ""
    for t in s["typology"]:
        typ += """
      <div class="typology-item">
        <div class="typology-cell">
          <span class="typology-cell-label">舊約影子 Type</span>
          <div class="typology-cell-body">%s</div>
        </div>
        <div class="typology-cell bridge">
          <span class="typology-cell-label">神學救贖連結</span>
          <div class="typology-cell-body">%s</div>
        </div>
        <div class="typology-cell">
          <span class="typology-cell-label">新約應驗 Antitype</span>
          <div class="typology-cell-body">%s</div>
        </div>
      </div>
""" % (r(t["type"]), r(t["bridge"]), r(t["antitype"]))
    H3 = '<h3 style="font-family:\'Noto Serif TC\',serif; font-size:15px; font-weight:500; color:var(--ink); margin-bottom:16px;">%s</h3>'
    return (head("theology", "Theology · 神學意義", "預表與應驗", s["epigraph"])
            + """
    <div class="verse-block">
      <div class="verse-text">「%s」</div>
      <div class="verse-ref">%s</div>
    </div>
""" % (r(s["verse"]["text"]), e(s["verse"]["ref"]))
            + "\n    " + H3 % "原文詞彙拆解"
            + '\n    <div class="word-cards">%s    </div>\n' % words
            + "\n    " + H3 % "救贖史神學洞察" + ins
            + '\n    <h3 style="font-family:\'Noto Serif TC\',serif; font-size:15px; font-weight:500; color:var(--ink); margin: 28px 0 16px;">基督預表對照</h3>'
            + '\n    <div class="typology-list">%s    </div>\n  </div>\n' % typ)


def sec_mirror(d):
    s = d["mirror"]
    qs = "".join("""
      <div class="question-card">
        <span class="question-num">%02d</span>
        <div class="question-text">%s</div>
      </div>
""" % (i + 1, r(q)) for i, q in enumerate(s["questions"]))
    g = s["generations"]
    H3 = '<h3 style="font-family:\'Noto Serif TC\',serif; font-size:15px; font-weight:500; color:var(--ink); margin-bottom:16px;">%s</h3>'
    return (head("mirror", "Mirror · 鏡照今日", "生命應用與反思", s["epigraph"])
            + '\n    <div class="insight-box" style="margin-bottom:28px;">%s</div>\n' % r(s["application"])
            + "\n    " + H3 % "靈魂反思四詰問"
            + '\n    <div class="questions-grid">%s    </div>\n' % qs
            + "\n    " + H3 % "家族系統代際遺傳分析"
            + """
    <div class="gen-table">
      <div class="gen-cell">
        <span class="gen-label">第一代 · %s</span>
        <div class="gen-title">%s</div>
        <div class="gen-body">%s</div>
      </div>
      <div class="gen-cell">
        <span class="gen-label">第二代 · %s</span>
        <div class="gen-title">%s</div>
        <div class="gen-body">%s</div>
      </div>
      <div class="gen-cell">
        <span class="gen-label light">恩典的突變與打斷</span>
        <div class="gen-title light">神的介入</div>
        <div class="gen-body light">%s</div>
      </div>
    </div>
  </div>
""" % (e(g["g1_who"]), e(g["g1_title"]), r(g["g1_body"]),
       e(g["g2_who"]), e(g["g2_title"]), r(g["g2_body"]), r(g["grace"])))


def sec_voice(d):
    s = d["voice"]
    tags = "".join('\n      <span class="tag">#%s</span>' % e(t) for t in s["tags"])
    prose = "".join("\n      <p>%s</p>" % r(p) for p in s["prose"])
    memo = "".join('\n      <p%s>%s</p>' % ("" if i == 0 else ' style="margin-top:12px;"', r(p))
                   for i, p in enumerate(s["memo"]))
    return (head("voice", "Voice · 現代語言轉譯", "社群白話文", s["epigraph"])
            + '\n    <div class="tags">%s\n    </div>\n' % tags
            + '\n    <div class="voice-prose">%s'
              '\n      <p style="font-weight:500; color:var(--ink);">%s</p>\n    </div>\n'
              % (prose, r(s["conclusion"]))
            + '\n    <div class="memo-card">'
              '\n      <span class="memo-label">給現代靈魂的備忘錄</span>%s'
              '\n      <p style="margin-top:12px; font-weight:500; color:#D4AF5A;">%s</p>\n    </div>\n'
              % (memo, r(s["memo_call"]))
            + '\n    <div class="insight-box">%s</div>\n  </div>\n' % r(s["extension"]))


def sec_legacy(d):
    s = d["legacy"]
    items = "".join("""
      <div class="legacy-item">
        <div class="legacy-num">%s</div>
        <div>
          <div class="legacy-title">%s</div>
          <div class="legacy-body">%s</div>
        </div>
      </div>
""" % (ROMAN[i], e(t), r(b)) for i, (t, b) in enumerate(s["items"]))
    return (head("legacy", "Legacy · 歷史遺產", "終章", s["epigraph"])
            + '\n    <div class="legacy-list">%s    </div>\n' % items
            + """
    <div class="final-verse">
      <div class="final-verse-text">「%s」</div>
      <div class="final-verse-ref">%s</div>
    </div>

    <div class="final-question">%s</div>
  </div>
""" % (r(s["final_verse"]["text"]), e(s["final_verse"]["ref"]), r(s["final_question"])))


def render(d, shell):
    title = "%s · PORTRAIT 聖經人物深度研究報告" % d["name"]
    body = (hero(d) + sec_portrait(d) + sec_timeline(d) + sec_character(d) + sec_relations(d)
            + sec_theology(d) + sec_mirror(d) + sec_voice(d) + sec_legacy(d))
    footer = ('\n</div>\n\n<div class="footer">\n  PORTRAIT 聖經人物深度研究 · %s '
              '<span>%s</span> · %s</div>\n\n'
              '<!-- 閱讀紀錄（localStorage，見 progress.js）：右下角標記已讀按鈕 -->\n'
              '<script src="progress.js"></script>\n\n</body>\n</html>\n'
              % (e(d["name"]), e(d["original"]), e(d["role"])))
    return shell.replace("__TITLE__", html.escape(title, quote=False)) + "\n<body>\n" + body + footer


def main():
    shell = io.open(os.path.join(BUILD, "shell_head.html"), encoding="utf-8").read()
    only = set(sys.argv[1:])
    names = sorted(f for f in os.listdir(PEOPLE) if f.endswith(".json"))
    made = 0
    for fn in names:
        pid = fn[:-5]
        if only and pid not in only:
            continue
        d = json.load(io.open(os.path.join(PEOPLE, fn), encoding="utf-8"))
        out = os.path.join(ROOT, "portrait_%s.html" % pid)
        io.open(out, "w", encoding="utf-8", newline="\n").write(render(d, shell))
        print("  ✓ portrait_%-24s %s  %s" % (pid + ".html", d["name"], d["mbti"]))
        made += 1
    print("\n共產生 %d 頁" % made)


if __name__ == "__main__":
    main()
