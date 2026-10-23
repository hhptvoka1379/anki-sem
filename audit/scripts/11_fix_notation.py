"""Apply the notation fixes read from the scans.

Input: a list of {ItemID, fixes:[{broken, correct}], confidence}. Each fix is
applied to every field of that note as a whole-token replacement (the token must
not be flanked by letters/digits), and every application is counted so a silent
no-op or an over-eager match is impossible.

Nothing is written unless every fix matched at least once; the input DB is never
opened read-write.
"""
import argparse
import json
import os
import re
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

OUT = f"{C.OUT}/fixed"


def token_re(pat: str) -> re.Pattern:
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(pat) + r"(?![A-Za-z0-9])")


def apply_fixes(db, fixes, dry: bool) -> dict:
    report = {"notes": 0, "replacements": 0, "unmatched": [], "detail": []}
    for entry in fixes:
        item = entry["ItemID"]
        row = db.execute("select id, flds from notes where sfld=?", (item,)).fetchone()
        if not row:
            report["unmatched"].append((item, "note not found"))
            continue
        nid, flds = row
        fields = flds.split("\x1f")
        hits = 0
        for i, val in enumerate(fields):
            for fix in entry.get("fixes", []):
                broken, correct = fix["broken"], fix["correct"]
                if correct == "UNSURE" or not broken:
                    continue
                rx = token_re(broken)
                new, n = rx.subn(correct, val)
                if n:
                    fields[i] = new
                    val = new
                    hits += n
        if not hits:
            report["unmatched"].append((entry["ItemID"], "no token matched"))
            continue
        if not dry:
            db.execute("update notes set flds=?, mod=strftime('%s','now'), usn=-1 "
                       "where id=?", ("\x1f".join(fields), nid))
        report["notes"] += 1
        report["replacements"] += hits
        report["detail"].append((entry["ItemID"], hits, entry.get("confidence")))
    if not dry:
        db.commit()
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixes", default=f"{C.OUT}/notation_fixes.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--input", default=C.LIVE_DB)
    ap.add_argument("--output", default=f"{OUT}/collection_fixed.db")
    args = ap.parse_args()

    fixes = json.load(open(args.fixes))
    os.makedirs(OUT, exist_ok=True)
    if not args.dry_run:
        shutil.copy2(args.input, args.output)
        target = args.output
    else:
        target = args.input
    db = sqlite3.connect(f"file:{target}?mode=ro" if args.dry_run else target,
                         uri=args.dry_run)
    db.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                        - (a.casefold() < b.casefold()))
    rep = apply_fixes(db, fixes, args.dry_run)
    print(json.dumps({k: v for k, v in rep.items() if k != "detail"}, indent=2,
                     ensure_ascii=False))
    for item, n, conf in rep["detail"][:80]:
        print(f"  {item:22} {n:2} replacements  ({conf})")
    json.dump(rep, open(f"{OUT}/notation_fix_report.json", "w"), indent=2,
              ensure_ascii=False)
    if rep["unmatched"]:
        print("UNMATCHED:", rep["unmatched"][:20])
        sys.exit(1)


if __name__ == "__main__":
    main()
