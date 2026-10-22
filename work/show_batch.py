#!/usr/bin/env python3
import sqlite3, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
con = sqlite3.connect("file:questions.db?mode=ro", uri=True, timeout=30)
con.row_factory = sqlite3.Row
rows = con.execute(
    "SELECT ord,id,quiz_type,subject_code,chapter_num,qnum,page,question,"
    "option_a,option_b,option_c,option_d,option_e,answer,answer_text,back_stem "
    "FROM v_pending ORDER BY ord LIMIT ?", (n,)).fetchall()
for r in rows:
    t = "CLOZE" if r["quiz_type"] == "Quiz a completamento" else "MCQ"
    print(f"== ord={r['ord']} {r['id']} {t} {r['subject_code']}C{r['chapter_num']} q{r['qnum']} p{r['page']}")
    print("Q:", r["question"])
    if t == "MCQ":
        for c in "abcde":
            print(f"  {c.upper()})", r["option_" + c])
        print("KEY:", r["answer"], "|", r["answer_text"])
    else:
        print("TERM:", r["answer_text"])
        print("BACK:", r["back_stem"])
print(f"-- {len(rows)} rows")
