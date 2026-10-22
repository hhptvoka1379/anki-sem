#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the acceptance checks (a-g) on the built answer key.

    python3 work/verify.py --input-dir /tmp/answer_key_request \
        --out answer_key_output.jsonl --chunks-dir answer_key_chunks \
        --json work/verify.json

Exit status is 0 only if every check passes.
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import unicodedata

ALLOWED_CONF = {"high", "medium", "low"}
ALLOWED_FLAGS = {"needs_figure", "ambiguous", "no_correct_option",
                 "multiple_correct", "typo", "out_of_syllabus"}
MIN_REASON = 25


def norm(s):
    """case / whitespace / punctuation insensitive comparison key."""
    s = unicodedata.normalize("NFKC", s).casefold()
    return "".join(ch for ch in s if ch.isalnum())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check(input_dir, out_path, chunks_dir):
    needed = [json.loads(l) for l in open(os.path.join(input_dir, "NEEDED.jsonl"),
                                          encoding="utf-8")]
    rows = [json.loads(l) for l in open(out_path, encoding="utf-8")]
    results = []

    # a) count / ids / order
    n_ids = [r["id"] for r in rows]
    n_ids_needed = [r["id"] for r in needed]
    a_ok = (len(rows) == len(needed) == 257
            and len(set(n_ids)) == len(n_ids)
            and set(n_ids) == set(n_ids_needed)
            and n_ids == n_ids_needed)
    results.append(("a", "257 lines, 257 unique ids, same id set and order as NEEDED.jsonl",
                    f"{len(rows)} lines, {len(set(n_ids))} unique, order match "
                    f"{n_ids == n_ids_needed}", a_ok))

    # b) type matches the request
    b_bad = []
    for rec, row in zip(needed, rows):
        if rec["type"] == "mcq":
            if not ("letter" in row and "answer_text" in row) or "answers" in row:
                b_bad.append(row["id"])
        else:
            if "answers" not in row or "letter" in row or "answer_text" in row:
                b_bad.append(row["id"])
    results.append(("b", "type matches the request for all 257",
                    f"mismatches: {b_bad or 'none'}", not b_bad))

    # c) MCQ letter + answer_text vs options[letter]
    exactly = normeq = bad = 0
    bad_rows = []
    for rec, row in zip(needed, rows):
        if rec["type"] != "mcq":
            continue
        letter = row.get("letter")
        if letter not in rec["options"]:
            bad += 1; bad_rows.append((row["id"], letter)); continue
        target = rec["options"][letter]
        if row["answer_text"] == target:
            exactly += 1
        if norm(row["answer_text"]) == norm(target):
            normeq += 1
        else:
            bad += 1
            bad_rows.append((row["id"], row["answer_text"], target))
    n_mcq = sum(1 for r in needed if r["type"] == "mcq")
    c_ok = (normeq == n_mcq and bad == 0)
    results.append(("c", "MCQ: letter in A-E and answer_text == options[letter] "
                         "(case/space/punct insensitive)",
                    f"{exactly}/{n_mcq} byte-identical, {normeq}/{n_mcq} equal after "
                    f"normalisation, {bad} mismatched {bad_rows or ''}", c_ok))

    # d) cloze length
    d_bad = [row["id"] for rec, row in zip(needed, rows)
             if rec["type"] == "cloze" and len(row.get("answers", [])) != rec["blanks"]]
    n_cloze = sum(1 for r in needed if r["type"] == "cloze")
    results.append(("d", "cloze: len(answers) == blanks",
                    f"{n_cloze - len(d_bad)}/{n_cloze} ok", not d_bad))

    # e) confidence / flag vocabulary
    e_bad = []
    for row in rows:
        if row.get("confidence") not in ALLOWED_CONF:
            e_bad.append((row["id"], "confidence", row.get("confidence")))
        extra = set(row.get("flags", [])) - ALLOWED_FLAGS
        if extra:
            e_bad.append((row["id"], "flags", sorted(extra)))
    results.append(("e", "confidence in {high,medium,low}; flags subset of the allowed set",
                    f"violations: {e_bad or 'none'}", not e_bad))

    # f) reason length
    lengths = [len(row.get("reason", "")) for row in rows]
    results.append(("f", f"reason >= {MIN_REASON} chars on every row",
                    f"min {min(lengths)} chars", min(lengths) >= MIN_REASON))

    # g) chunk concatenation identical to the full file
    chunk_paths = sorted(glob.glob(os.path.join(chunks_dir, "chunk_*.jsonl")))
    joined = b"".join(open(p, "rb").read() for p in chunk_paths)
    full = open(out_path, "rb").read()
    full_sha, cat_sha = sha256(out_path), hashlib.sha256(joined).hexdigest()
    g_ok = joined == full
    results.append(("g", "chunk concatenation == full file, same sha256",
                    f"{len(chunk_paths)} chunks, sha256 {full_sha[:16]}… == "
                    f"{cat_sha[:16]}…: {g_ok}", g_ok))

    return {
        "rows": len(rows),
        "mcq": n_mcq,
        "cloze": n_cloze,
        "exact_answer_text": exactly,
        "normalised_answer_text": normeq,
        "min_reason_len": min(lengths),
        "sha256_full": full_sha,
        "sha256_concat": cat_sha,
        "chunks": [os.path.basename(p) for p in chunk_paths],
        "results": [{"check": c, "requirement": r, "observed": o, "status": "PASS" if ok else "FAIL"}
                    for c, r, o, ok in results],
        "all_pass": all(ok for *_, ok in results),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chunks-dir", required=True)
    ap.add_argument("--json", help="write the result blob here")
    args = ap.parse_args()

    res = check(args.input_dir, args.out, args.chunks_dir)
    for r in res["results"]:
        print(f"{r['check']}) {r['status']}: {r['requirement']}\n     {r['observed']}")
    print("\nALL:", "PASS" if res["all_pass"] else "FAIL")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0 if res["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
