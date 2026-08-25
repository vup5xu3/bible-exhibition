# -*- coding: utf-8 -*-
"""
從 _build/people/*.json 產生 Supabase 匯入 SQL。

每個人物的卡片資料（名字、副標、MBTI、分類、標籤…）只寫在 JSON 裡一次，
由本檔產生資料庫語句，避免「頁面做好了但忘記進資料庫」或兩邊資料不一致。

執行： python _build/make_sql.py
輸出： _db/migration_02_new_characters.sql
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEOPLE = os.path.join(ROOT, "_build", "people")
OUT = os.path.join(ROOT, "_db", "migration_02_new_characters.sql")

# 起始排序值：接在現有 14 筆之後
SORT_BASE = 100


def q(s):
    """單引號字串，跳脫內部單引號。"""
    if s is None or s == "":
        return "null"
    return "'" + str(s).replace("'", "''") + "'"


def arr(items):
    if not items:
        return "array[]::text[]"
    return "array[" + ", ".join(q(i) for i in items) + "]::text[]"


def main():
    rows = []
    for fn in sorted(os.listdir(PEOPLE)):
        if not fn.endswith(".json"):
            continue
        d = json.load(io.open(os.path.join(PEOPLE, fn), encoding="utf-8"))
        rows.append((fn[:-5], d))

    lines = [
        "-- ══════════════════════════════════════════════════════════════════",
        "-- PORTRAIT 聖經人物資料庫 · 遷移腳本 02：新增人物",
        "--",
        "-- 由 _build/make_sql.py 從 _build/people/*.json 自動產生，請勿手改。",
        "-- 需先執行 migration_01（本腳本會用到 epithet 與 tier 欄位）。",
        "--",
        "-- 使用 upsert：重複執行只會更新，不會產生重複資料。",
        "-- ══════════════════════════════════════════════════════════════════",
        "",
        "begin;",
        "",
        "insert into public.bible_characters",
        "  (id, name, epithet, name_en, avatar, description, mbti, tier, file_name, categories, tags, sort_order)",
        "values",
    ]

    vals = []
    for i, (pid, d) in enumerate(rows):
        vals.append(
            "  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %d)" % (
                q(pid), q(d["name"]), q(d.get("epithet")), q(d["nameEn"]), q(d["avatar"]),
                q(d["desc"]), q(d.get("mbti")), q(d.get("tier", "normal")),
                q("portrait_%s.html" % pid), arr(d.get("categories")), arr(d.get("tags")),
                SORT_BASE + i))
    lines.append(",\n".join(vals))

    lines += [
        "on conflict (id) do update set",
        "  name        = excluded.name,",
        "  epithet     = excluded.epithet,",
        "  name_en     = excluded.name_en,",
        "  avatar      = excluded.avatar,",
        "  description = excluded.description,",
        "  mbti        = excluded.mbti,",
        "  tier        = excluded.tier,",
        "  file_name   = excluded.file_name,",
        "  categories  = excluded.categories,",
        "  tags        = excluded.tags;",
        "",
        "commit;",
        "",
        "-- 驗證",
        "select id, name, epithet, mbti, tier, categories, file_name",
        "  from public.bible_characters",
        " where sort_order >= %d" % SORT_BASE,
        " order by sort_order;",
        "",
    ]

    io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("已寫出 %s（%d 位人物）" % (os.path.relpath(OUT, ROOT), len(rows)))
    for pid, d in rows:
        print("   %-18s %-8s %-6s %s" % (pid, d["name"], d.get("mbti", "-"), "/".join(d.get("categories", []))))


if __name__ == "__main__":
    main()
