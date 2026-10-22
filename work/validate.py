#!/usr/bin/env python3
"""Hard gate for the explanation workpack.

Exit 0 only if every invariant holds. Run after each 100 completed rows and
once at the end; a failure means stop, not "fix later".

Usage: python3 validate.py [--db questions.db] [--quiet] [--allow-pending]
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED = {"pending", "done", "flagged"}
TAG = re.compile(r"</?[a-zA-Z][^>]*>")
MD = re.compile(r"(\*\*|__|`|^#{1,6}\s|\[[^\]]*\]\([^)]*\))", re.M)
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PLACEHOLDERS = {"da definire", "todo", "tbd", "n/a", "-", "—", "…"}


def content_hash(r) -> str:
    parts = [str(r["ord"]), r["id"], r["question"]]
    parts += [r["option_" + c] for c in "abcde"]
    parts += [r["answer"], r["answer_text"]]
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(HERE, "questions.db"))
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--allow-pending", action="store_true",
                    help="do not fail while rows are still pending (mid-run)")
    a = ap.parse_args()

    ref = json.load(open(os.path.join(HERE, "reference_hashes.json"),
                         encoding="utf-8"))
    con = sqlite3.connect(f"file:{a.db}?mode=ro", uri=True, timeout=30)
    con.row_factory = sqlite3.Row
    rows = {r["id"]: dict(r) for r in con.execute("select * from questions")}
    ex = con.execute("select count(*) from examples where trim(reason) <> ''"
                     ).fetchone()[0]
    con.close()

    err, warn = [], []
    if set(rows) != set(ref):
        err.append(f"id set differs: +{sorted(set(rows)-set(ref))[:5]} "
                   f"-{sorted(set(ref)-set(rows))[:5]}")
    if ex != 4:
        warn.append(f"examples with reason: {ex} (expected 4)")
    if sorted(r["ord"] for r in rows.values()) != list(range(len(rows))):
        err.append("ord values are not a 0..N-1 permutation")

    for i, r in rows.items():
        st = r["status"]
        if st not in ALLOWED:
            err.append(f"{i}: bad status {st!r}")
            continue
        if r["ref_hash"] != ref.get(i, ""):
            err.append(f"{i}: ref_hash column changed")
        if content_hash(r) != ref.get(i, ""):
            err.append(f"{i}: content differs from reference "
                       f"(question/options/answer/ord edited)")
        reason = (r["reason"] or "").strip()
        flags = (r["flags"] or "").strip()
        upd = (r["updated_at"] or "").strip()

        if r["quiz_type"] == "Quiz non commentati":
            if r["answer"] not in list("ABCDE"):
                err.append(f"{i}: answer {r['answer']!r} not A-E")
            if not all((r["option_" + c] or "").strip() for c in "abcde"):
                err.append(f"{i}: empty option")
            if r["back_stem"]:
                err.append(f"{i}: MCQ has back_stem")
        if r["quiz_type"] == "Quiz a completamento":
            if r["answer"]:
                err.append(f"{i}: cloze has an answer letter")
            if not r["back_stem"]:
                err.append(f"{i}: cloze without back_stem")
            if "{{c" not in (r["question"] or ""):
                err.append(f"{i}: cloze question has no cloze marker")
        if not (r["question"] or "").strip():
            err.append(f"{i}: empty question")
        if st == "pending":
            if reason or flags:
                err.append(f"{i}: pending row already has reason/flags")
            continue

        if not ISO.match(upd):
            err.append(f"{i}: updated_at not ISO-8601 Z ({upd!r})")
        if st == "done":
            if flags:
                err.append(f"{i}: done row has flags (use flagged)")
            if not 80 <= len(reason) <= 600:
                err.append(f"{i}: reason length {len(reason)} not in 80..600")
            if reason.casefold() in PLACEHOLDERS:
                err.append(f"{i}: placeholder reason")
            if reason.casefold() == (r["answer_text"] or "").strip().casefold():
                err.append(f"{i}: reason just repeats answer_text")
        if st == "flagged":
            if not reason and not flags:
                err.append(f"{i}: flagged row has neither reason nor flags")
            try:
                lst = json.loads(flags) if flags else []
                if not isinstance(lst, list) or not lst or \
                        not all(isinstance(x, str) and x.strip() for x in lst):
                    err.append(f"{i}: flags is not a non-empty JSON string array")
            except json.JSONDecodeError:
                err.append(f"{i}: flags is not valid JSON")
        if reason:
            if "\n" in reason or "\r" in reason:
                err.append(f"{i}: reason contains a newline")
            if TAG.search(reason):
                err.append(f"{i}: reason contains an HTML tag")
            if MD.search(reason):
                err.append(f"{i}: reason contains Markdown")
            if len(reason) > 600:
                err.append(f"{i}: reason longer than 600 chars")

    counts = {}
    for r in rows.values():
        if r["status"] == "done":
            k = (r["reason"] or "").strip().casefold()
            counts[k] = counts.get(k, 0) + 1
    for k, n in counts.items():
        if n > 2:
            err.append(f"reason repeated {n} times: {k[:60]!r}")

    pending = sum(1 for r in rows.values() if r["status"] == "pending")
    if pending and not a.allow_pending:
        err.append(f"{pending} rows still pending")

    per = {}
    for r in rows.values():
        key = (r["subject_code"], r["chapter_num"])
        d = per.setdefault(key, {"pending": 0, "done": 0, "flagged": 0})
        d[r["status"]] += 1
    order = lambda k: ({"CHIM": 0, "BIO": 1, "FIS": 2}.get(k[0], 3), k[1])
    for key in sorted(per, key=order):
        d = per[key]
        work = d["done"] + d["flagged"]
        if work and d["flagged"] / work > 0.05:
            warn.append(f"{key[0]} C{key[1]:02d}: {d['flagged']}/{work} flagged "
                        f"({d['flagged']/work:.0%}) - systematic scan problem?")

    s = (f"rows={len(rows)} pending={pending} "
         f"done={sum(1 for r in rows.values() if r['status']=='done')} "
         f"flagged={sum(1 for r in rows.values() if r['status']=='flagged')}")
    if err:
        print("FAIL:", s)
        for e in err[:80]:
            print("  -", e)
        if len(err) > 80:
            print(f"  ... and {len(err)-80} more")
        return 1
    print(("PASS: " if not a.quiet else "") + s)
    if not a.quiet:
        for key in sorted(per, key=order):
            d = per[key]
            print(f"  {key[0]} C{key[1]:02d} pending={d['pending']:4d} "
                  f"done={d['done']:4d} flagged={d['flagged']:3d}")
    for w in warn:
        print("WARN:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())

