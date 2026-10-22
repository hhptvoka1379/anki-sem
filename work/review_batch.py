#!/usr/bin/env python3
"""Re-read the last N processed rows (by ord) with reasons/flags for self-check."""
import sqlite3, sys
lo = int(sys.argv[1]); hi = int(sys.argv[2])
con = sqlite3.connect("file:questions.db?mode=ro", uri=True, timeout=30)
con.row_factory = sqlite3.Row
rows = con.execute(
    "SELECT ord,id,quiz_type,question,option_a,option_b,option_c,option_d,option_e,"
    "answer,answer_text,back_stem,reason,flags,status FROM questions "
    "WHERE ord BETWEEN ? AND ? ORDER BY ord", (lo, hi)).fetchall()
for r in rows:
    print(f"== ord={r['ord']} {r['id']} [{r['status']}]")
    q = r["question"] or ""
    print("Q:", q if len(q) <= 160 else q[:160] + " …")
    if r["answer"]:
        print("KEY:", r["answer"], "|", r["answer_text"])
    else:
        print("TERM:", r["answer_text"])
    if r["reason"]:
        print(f"REASON ({len(r['reason'])}):", r["reason"])
    if r["flags"]:
        print("FLAGS:", r["flags"])
