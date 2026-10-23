#!/usr/bin/env python3
"""Validate cloze_answers.jsonl against cloze_items.jsonl. Exit 1 on any error.

usage: python3 validate_cloze_answers.py [cloze_answers.jsonl]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent


def key(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    s = re.sub(r"^(il|lo|la|i|gli|le|un|uno|una)\s+|^(l|un|dell|nell|all|sull)['’]\s*", "", s.strip())
    return re.sub(r"\s+", " ", s).strip()


def main():
    items = [json.loads(l) for l in (HERE / "cloze_items.jsonl").open(encoding="utf-8")]
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "cloze_answers.jsonl"
    lines = [l for l in path.open(encoding="utf-8") if l.strip()]
    errs, warn = [], []
    if len(lines) != len(items):
        errs.append(f"line count {len(lines)} != {len(items)}")
    seen = set()
    for n, (line, it) in enumerate(zip(lines, items), 1):
        try:
            a = json.loads(line)
        except json.JSONDecodeError as e:
            errs.append(f"line {n}: bad JSON ({e})")
            continue
        if a.get("id") != it["id"]:
            errs.append(f"line {n}: id {a.get('id')} != {it['id']} (order must match)")
            continue
        if a["id"] in seen:
            errs.append(f"{a['id']}: duplicate")
        seen.add(a["id"])
        acc = a.get("accepted")
        if not isinstance(acc, dict) or set(acc) != set(it["book_answers"]):
            errs.append(f"{a['id']}: accepted must cover blanks {sorted(it['book_answers'])}")
            continue
        for b, alts in acc.items():
            if not isinstance(alts, list) or not all(isinstance(x, str) and x.strip() for x in alts):
                errs.append(f"{a['id']}[{b}]: alternatives must be non-empty strings")
                continue
            book = key(it["book_answers"][b])
            ks = [key(x) for x in alts]
            if book in ks:
                errs.append(f"{a['id']}[{b}]: repeats the book answer")
            if len(set(ks)) != len(ks):
                errs.append(f"{a['id']}[{b}]: duplicate alternatives after normalisation")
            for x in alts:
                if re.search(r"[<>*`|]|\[\[", x):
                    errs.append(f"{a['id']}[{b}]: markup or '|' in {x!r}")
            if len(alts) > 6:
                warn.append(f"{a['id']}[{b}]: {len(alts)} alternatives (suspiciously many)")
        if not isinstance(a.get("blank_ok"), bool):
            errs.append(f"{a['id']}: blank_ok must be true/false")
        if a.get("confidence") not in ("high", "medium", "low"):
            errs.append(f"{a['id']}: confidence must be high|medium|low")
        if a.get("blank_ok") is False and not a.get("issue"):
            errs.append(f"{a['id']}: blank_ok=false needs an issue")
    tot = sum(len(v) for l in lines for v in json.loads(l).get("accepted", {}).values()) if not errs else None
    for w in warn[:40]:
        print("WARN", w)
    for e in errs[:200]:
        print("ERROR", e)
    print(f"{'FAIL' if errs else 'PASS'}: {len(lines)} lines, {len(errs)} errors, {len(warn)} warnings"
          + (f", {tot} alternatives total" if tot is not None else ""))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
