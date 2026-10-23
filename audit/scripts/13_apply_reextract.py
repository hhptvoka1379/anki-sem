"""Replace whole exercises with the transcription read from the PDF page.

Gates: certainty >= 80, five non-empty options, a non-empty stem, and at least
half of the old stem's words present in the new one (so a neighbouring exercise
cannot be applied by mistake). Notes whose stem carries a blank-slot are skipped:
those blanks are not in the printed page.
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
import ocr_lib as O

LETTERS = "ABCDE"
OPT = ('<div class="opt"><span class="opt-letter">{}</span>'
       '<span class="opt-body">{}</span></div>')


def options_html(bodies):
    return ('<div class="options">'
            + "".join(OPT.format(l, bodies[l]) for l in LETTERS)
            + "</div>")


def words(s):
    return set(re.findall(r"[A-Za-zÀ-ÿ]{3,}", s.lower()))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=f"{C.OUT}/pdf_transcripts.json")
    ap.add_argument("--input", default=f"{C.OUT}/fixed/collection_fixed3.db")
    ap.add_argument("--output", default=f"{C.OUT}/fixed/collection_fixed4.db")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = json.load(open(args.data))
    if not args.dry_run:
        shutil.copy2(args.input, args.output)
    db = sqlite3.connect(args.output if not args.dry_run else args.input)
    db.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                        - (a.casefold() < b.casefold()))

    applied, rejected = [], []
    for e in data:
        item = e["ItemID"]
        cert = e.get("certainty", 0)
        stem = (e.get("stem") or "").strip()
        opts = e.get("options") or {}
        if cert < 80 or not stem or len(opts) != 5 or not all(
                (opts.get(l) or "").strip() for l in LETTERS):
            rejected.append((item, f"gate: cert={cert} opts={len(opts)}"))
            continue
        row = db.execute("select id, flds from notes where sfld=?",
                         (item,)).fetchone()
        if not row:
            rejected.append((item, "note not found"))
            continue
        nid, flds = row
        f = flds.split("\x1f")
        old_stem_plain = O.plain(f[8])
        if "blank-slot" in f[8]:
            rejected.append((item, "completamento note skipped"))
            continue
        overlap = len(words(old_stem_plain) & words(stem)) / max(
            1, len(words(old_stem_plain)))
        if overlap < 0.5:
            rejected.append((item, f"stem overlap {overlap:.2f}"))
            continue
        f[8] = stem
        if O.plain(f[9]).strip() == old_stem_plain.strip():
            f[9] = stem
        f[10] = options_html({l: opts[l].strip() for l in LETTERS})
        if f[11].strip():
            f[11] = f[10]
        m = re.match(r"(Risposta corretta:\s*)([A-E])(\.\s*)(.*)", f[12], re.S)
        if m and m.group(4).strip():
            f[12] = m.group(1) + m.group(2) + m.group(3) + opts[m.group(2)].strip()
        if not args.dry_run:
            db.execute("update notes set flds=?, mod=strftime('%s','now'), "
                       "usn=-1 where id=?", ("\x1f".join(f), nid))
        applied.append((item, cert, round(overlap, 2)))
    if not args.dry_run:
        db.commit()
    print(f"applied: {len(applied)}  rejected: {len(rejected)}")
    for a in applied:
        print("  OK ", a)
    for r in rejected:
        print("  REJ", r)
    json.dump({"applied": applied, "rejected": rejected},
              open(f"{C.OUT}/fixed/reextract_report.json", "w"), indent=2,
              ensure_ascii=False)
    db.close()


if __name__ == "__main__":
    main()
