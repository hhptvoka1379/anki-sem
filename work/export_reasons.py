#!/usr/bin/env python3
"""Dump the finished work for handback.

Writes, next to this script:
  reasons_done.jsonl   one {"id","reason"} per done row (what gets merged)
  flags_report.md      every flagged row, grouped by flag prefix

Usage: python3 export_reasons.py [--db questions.db] [--out reasons_done.jsonl]
"""
import argparse
import collections
import json
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(HERE, "questions.db"))
    ap.add_argument("--out", default=os.path.join(HERE, "reasons_done.jsonl"))
    a = ap.parse_args()

    con = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True, timeout=30)
    con.row_factory = sqlite3.Row
    done = con.execute(
        "select id, reason from questions where status='done' "
        "and trim(reason) <> '' order by ord").fetchall()
    flagged = con.execute(
        "select id, subject_code, chapter_num, qnum, page, flags from questions "
        "where status='flagged' order by ord").fetchall()
    con.close()

    with open(a.out, "w", encoding="utf-8") as fh:
        for r in done:
            fh.write(json.dumps({"id": r["id"], "reason": r["reason"].strip()},
                                ensure_ascii=False) + "\n")

    groups = collections.defaultdict(list)
    for r in flagged:
        try:
            items = json.loads(r["flags"]) if r["flags"] else ["(no flags)"]
        except json.JSONDecodeError:
            items = [f"(invalid JSON: {r['flags']})"]
        for it in items:
            groups[it.split(":", 1)[0].strip()].append((r, it))

    flags_path = os.path.join(os.path.dirname(a.out), "flags_report.md")
    with open(flags_path, "w", encoding="utf-8") as fh:
        fh.write(f"# Flagged rows ({len(flagged)})\n\n")
        for prefix in sorted(groups):
            fh.write(f"## {prefix} ({len(groups[prefix])})\n\n")
            fh.write("| id | subj | ch | q | page | flag |\n")
            fh.write("|---|---|---|---|---|---|\n")
            for r, it in groups[prefix]:
                fh.write(f"| {r['id']} | {r['subject_code']} | "
                         f"{r['chapter_num']} | {r['qnum']} | "
                         f"{r['page']} | {it.replace('|', '/')} |\n")
            fh.write("\n")

    lens = [len(r["reason"].strip()) for r in done]
    print(f"done: {len(done)} -> {a.out}")
    if lens:
        print(f"reason length: min {min(lens)} / mean {sum(lens)//len(lens)} / max {max(lens)}")
    print(f"flagged: {len(flagged)} -> flags_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
