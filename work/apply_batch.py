#!/usr/bin/env python3
"""Apply work/batch_current.json: list of {id, reason} or {id, flags:[...]}.
Only pending -> done/flagged; asserts changes()==1 per row; single transaction."""
import json, re, sqlite3, sys
path = sys.argv[1] if len(sys.argv) > 1 else "batch_current.json"
items = json.load(open(path, encoding="utf-8"))
TAG = re.compile(r"</?[a-zA-Z][^>]*>")
MD = re.compile(r"(\*\*|__|`|^#{1,6}\s|\[[^\]]*\]\([^)]*\))", re.M)
con = sqlite3.connect("questions.db", timeout=30)
con.execute("BEGIN IMMEDIATE")
try:
    for it in items:
        rid = it["id"]
        if "flags" in it:
            flags = it["flags"]
            assert isinstance(flags, list) and flags and all(isinstance(x, str) and x.strip() for x in flags), rid
            cur = con.execute(
                "UPDATE questions SET reason='', flags=?, status='flagged', "
                "updated_at=strftime('%Y-%m-%dT%H:%M:%SZ','now') "
                "WHERE id=? AND status='pending'",
                (json.dumps(flags, ensure_ascii=False), rid))
        else:
            reason = it["reason"].strip()
            assert 80 <= len(reason) <= 600, (rid, len(reason))
            assert "\n" not in reason and "\r" not in reason, rid
            assert not TAG.search(reason), rid
            assert not MD.search(reason), rid
            cur = con.execute(
                "UPDATE questions SET reason=?, flags='', status='done', "
                "updated_at=strftime('%Y-%m-%dT%H:%M:%SZ','now') "
                "WHERE id=? AND status='pending'", (reason, rid))
        assert cur.rowcount == 1, (rid, cur.rowcount)
    con.execute("COMMIT")
except Exception:
    con.execute("ROLLBACK")
    raise
prog = con.execute("SELECT * FROM v_progress").fetchall()
counts = con.execute("SELECT status, count(*) FROM questions GROUP BY 1").fetchall()
print("applied:", len(items))
print("counts:", counts)
print("v_pending:", con.execute("SELECT count(*) FROM v_pending").fetchone()[0])
