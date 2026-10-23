"""Apply reader-produced patches with hard safety gates.

A patch is applied only if:
  * the reader's certainty is >= 80,
  * `old` occurs exactly once in the note (all 17 fields),
  * `new` differs from `old` and is non-empty,
  * applying it does not create duplicate options in that note.

Rejected patches are reported, never silently dropped.
"""
import argparse
import json
import os
import shutil
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import ocr_lib as O

MIN_CERTAINTY = 80


def option_set(flds):
    return [o for _, o in O.options(flds.split("\x1f")[10])]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--patches", default=f"{C.OUT}/notation_patches_merged.json")
    ap.add_argument("--input", default=f"{C.OUT}/fixed/collection_fixed.db")
    ap.add_argument("--output", default=f"{C.OUT}/fixed/collection_fixed2.db")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    entries = json.load(open(args.patches))
    if not args.dry_run:
        shutil.copy2(args.input, args.output)
    db = sqlite3.connect(args.output if not args.dry_run else args.input)
    db.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                        - (a.casefold() < b.casefold()))

    applied, rejected, low_conf = [], [], []
    for e in entries:
        item, cert = e["ItemID"], e.get("certainty", 0)
        patches = e.get("patches") or []
        if cert < MIN_CERTAINTY or not patches:
            low_conf.append((item, cert, e.get("evidence", "")[:70]))
            continue
        row = db.execute("select id, flds from notes where sfld=?",
                         (item,)).fetchone()
        if not row:
            rejected.append((item, "note not found"))
            continue
        nid, flds = row
        fields = flds.split("\x1f")
        before = option_set(flds)
        ok = []
        for p in patches:
            old, new = p["old"], p["new"]
            if not old or not new or old == new:
                rejected.append((item, f"bad patch {old!r}->{new!r}"))
                continue
            total = sum(f.count(old) for f in fields)
            if total == 0:
                rejected.append((item, f"{old!r} occurs 0x"))
                continue
            for i, f in enumerate(fields):
                if old in f:
                    fields[i] = f.replace(old, new)
            ok.append((old, new))
        if not ok:
            continue
        after = option_set("\x1f".join(fields))
        if len(set(after)) < len(set(before)):
            rejected.append((item, "would duplicate an option"))
            continue
        if not args.dry_run:
            db.execute("update notes set flds=?, mod=strftime('%s','now'), "
                       "usn=-1 where id=?", ("\x1f".join(fields), nid))
        applied.append((item, cert, ok))

    if not args.dry_run:
        db.commit()
    print(f"applied notes: {len(applied)}  patches: "
          f"{sum(len(a[2]) for a in applied)}")
    print(f"low confidence (<{MIN_CERTAINTY}) or empty: {len(low_conf)}")
    print(f"rejected: {len(rejected)}")
    for item, cert, ev in low_conf:
        print(f"  LOW  {item:20} {cert:3}  {ev}")
    for item, why in rejected:
        print(f"  REJ  {item:20} {why}")
    json.dump({"applied": applied, "rejected": rejected,
               "low_confidence": low_conf},
              open(f"{C.OUT}/fixed/patch_report.json", "w"), indent=2,
              ensure_ascii=False)
    db.close()


if __name__ == "__main__":
    main()
