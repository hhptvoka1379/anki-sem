#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate ANSWER_KEY_README.md and review.md from the built artifacts.

    python3 work/make_docs.py --input-dir /tmp/answer_key_request \
        --out answer_key_output.jsonl --stats work/stats.json \
        --verify work/verify.json --readme ANSWER_KEY_README.md --review review.md

Every count, hash and PASS/FAIL in the two documents is read from the JSONL and
from work/verify.json, never typed by hand.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notable import NOTABLE  # noqa: E402

FLAG_ORDER = ["needs_figure", "ambiguous", "no_correct_option",
              "multiple_correct", "typo", "out_of_syllabus"]

MEDIUM_NOTE = {
    "CHIM-C06-NCOM-038": "the printed masses are 60×10⁻² g / 36×10⁻² g; only the ratio of the "
                         "molecular weights fixes the intended option, and the OCR garbles it.",
    "CHIM-C07-COMM-004": "equivalents vs moles: the option speaks of 'un grammo equivalente', "
                         "which is loose wording for an equivalent.",
    "CHIM-C09-NCOM-052": "the reaction as printed consumes Br₂ and produces Cl₂, so the labels "
                         "'ossida/riduce' can be read from either side; judged from the Br/Cl "
                         "oxidation numbers.",
    "CHIM-C11-NCOM-019": "the correct definition (a base donates an electron pair) is not among "
                         "the options; D says 'acquista una coppia di elettroni', the opposite, "
                         "so the residual option 'nessuna delle altre risposte e corretta' is the answer.",
    "CHIM-C11-NCOM-170": "both 'il pH diminuisce' and 'si può ottenere una soluzione tampone' "
                         "are true; the first is the direct effect asked for.",
    "CHIM-C12-COMM-002": "optical activity implies a stereocentre, but the option states only "
                         "'a tetrahedral carbon', which is necessary rather than sufficient.",
    "BIO-C01-NCOM-202": "the deck omits DNA from the options; RNA is the only nucleic acid offered.",
    "BIO-C02-COMP-016": "the blank is a summary word from the chapter text ('attivi'); the source "
                        "wording is not visible in the scan.",
    "BIO-C03-NCOM-189": "U2 is the snRNA that contacts the 3' splice site in the committed "
                        "complex; some texts attribute the AG recognition to U5/U6.",
    "BIO-C04-COMM-056": "read from the pedigree drawing: dominant transmission fits, but the "
                        "pedigree is small enough that recessivity cannot be excluded by inspection.",
    "FIS-C03-NCOM-011": "the exact equilibrant is 2F·cos15° ≈ 1.93F; no option matches, 2F is "
                        "the closest and the intended one.",
}


FLAG_NOTE = {
    "CHIM-C10-NCOM-018": "printed page: A = CO₃⁻, E = CO₂ → **E is the printed answer**; the "
                         "A/E duplication exists only in the OCR of option A.",
    "FIS-C03-NCOM-011": "no option matches the exact equilibrant 2F·cos15° ≈ 1.93F; 2F is the "
                        "intended option.",
    "CHIM-C11-NCOM-170": "both 'il pH diminuisce' and 'si può ottenere una soluzione tampone' "
                         "hold; D is the direct effect, E is the buffer statement.",
    "FIS-C06-NCOM-157": "A and E say the same thing ('at least three branches' / 'more than two "
                        "terminals'); A follows the textbook wording.",
    "CHIM-C06-NCOM-038": "OCR turns 60 × 10⁻² into '107?'; the intended pair is 0,6 g / 0,36 g.",
    "FIS-C01-COMM-022": "OCR gives '2-F' for 2·F·cos(α/2).",
    "FIS-C02-NCOM-027": "OCR gives '101/2' for 10²/(2·9,8).",
}


def one_line(row, extra=""):
    if "letter" in row:
        head = f"`{row['id']}` — **{row['letter']}** — {extra}"
    else:
        head = f"`{row['id']}` — **{' / '.join(row['answers'])}** — {extra}"
    return head


def short_reason(row, limit=150):
    r = row["reason"]
    cut = r.find(". ")
    s = r[:cut + 1] if 0 < cut < limit else r
    if len(s) > limit:
        s = s[:limit - 1].rstrip() + "…"
    return s


def build_readme(stats, verify, args):
    c = stats["confidence"]
    f = stats["flags"]
    chunks = ", ".join(verify["chunks"])
    checks = "\n".join(
        f"| {r['check']} | {r['requirement']} | {r['observed'].replace('|', '/')} | **{r['status']}** |"
        for r in verify["results"]
    )
    notable = "\n".join(f"- `{i}` — {note}" for i, note in NOTABLE)

    return f"""# Answer key — 257 flagged cards

Output of the `PROMPT.md` task on `NEEDED.jsonl` (257 lines: **{stats['mcq']} MCQ + {stats['cloze']} cloze**).

## Files

- `answer_key_output.jsonl` — the key: one object per input line, same ids, same order, UTF-8 (no BOM), `\\n` line endings.
- `answer_key_chunks/`: {chunks} — the same key split at {args.chunk_size}-row boundaries, byte-identical to the concatenation of the full file.
- `review.md` — the rows that need a human look (medium confidence, flagged, notable corrections).

## Output contract

- `letter` (MCQ) and `answers` (cloze) are the answer and are authoritative.
- `answer_text` is **always `options[letter]` of the matching NEEDED record, verbatim** ({verify['exact_answer_text']}/{verify['mcq']} byte-identical), so a consumer that re-derives the text from the card can never disagree with this file.
- `printed_text` (present on {stats['printed_text_rows']} rows) carries the text as printed on the page, where the deck's own option string is OCR damage of it (`Visotopo` for `L'isotopo`, `0e0` for `O e O`, `HNO₄` for `HNO₂`, `SON` for `50 N`, …). It is informational only — the consumer may ignore it.
- `reason` names the principle, formula or definition that decides the item.
- `confidence` is `high` {c['high']} / `medium` {c['medium']} / `low` {c['low']}.

## Reproducibility

Inputs: the 257-row `NEEDED.jsonl` plus the `images/` scans from the request pack, and the
answer sources in `work/` (`answers_part1..6.py`, `answer_text_fixes.py`).

```bash
python3 work/build.py \\
    --input-dir  /tmp/answer_key_request \\
    --overrides  work/answer_text_fixes.py \\
    --parts-dir  work \\
    --out        answer_key_output.jsonl \\
    --chunks-dir answer_key_chunks \\
    --stats      work/stats.json

python3 work/verify.py \\
    --input-dir  /tmp/answer_key_request \\
    --out        answer_key_output.jsonl \\
    --chunks-dir answer_key_chunks \\
    --json       work/verify.json

python3 work/make_docs.py \\
    --input-dir  /tmp/answer_key_request \\
    --out        answer_key_output.jsonl \\
    --stats      work/stats.json \\
    --verify     work/verify.json \\
    --readme     ANSWER_KEY_README.md \\
    --review     review.md
```

`--input-dir` is the directory that holds `NEEDED.jsonl` — the unpacked
`answer_key_request/` folder (in this run: `/tmp/subset2/answer_key_request`);
every other path is relative to the repository root. Re-running these three
commands reproduces the two JSONL trees and this README byte-for-byte.

## Acceptance

Run by `work/verify.py` on the delivered files; exit status 0 only if all pass.

| # | requirement | observed | status |
|---|---|---|---|
{checks}

**Overall: {'PASS' if verify['all_pass'] else 'FAIL'}** — {verify['rows']} rows, min reason length {verify['min_reason_len']} chars.

Integrity:

- `sha256(answer_key_output.jsonl)` = `{verify['sha256_full']}`
- `sha256(cat answer_key_chunks/chunk_*.jsonl)` = `{verify['sha256_concat']}`
- identical: **{verify['sha256_full'] == verify['sha256_concat']}**

## Flags

| flag | rows |
|---|---|
""" + "\n".join(f"| `{k}` | {f[k]} |" for k in FLAG_ORDER if f.get(k)) + f"""

`needs_figure` is the union of the flags the answer sources carry and the flags implied by a
`figure` key in the record ({f.get('needs_figure', 0)} rows), not an inference from the image alone.

`CHIM-C10-NCOM-018` carries `ambiguous`: the deck's options A and E both read `CO₂` after OCR,
but the printed page has **A = CO₃⁻** and **E = CO₂**. **E is the printed answer**; A is an OCR
error and the duplication is not real.

## Notable corrections

Rows where this key deliberately differs from what a naive or printed key would say.
Also listed one per line in `review.md`.

{notable}

## Note on the source PDF (not shipped)

Page lookups **were** done against the book scan, `Eserciziario Unico per il Semestre Filtro
2-lite-trim.pdf`: header OCR was used to map printed page numbers to PDF pages, in order to
find where the printed solutions live. That route was abandoned — the solution pages are not
in the scan — and the key was then built from the per-card `images/<id>.png` scans plus
subject knowledge.

The 23.6 MB PDF is **not part of this deliverable**: it is untracked and listed in
`.gitignore`, so it contributes nothing to the archive. It is still recoverable from history
(`git show 262ba0f:'Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf' > book.pdf`)
and a copy sits outside the repository at `/home/user/source-scan/`. Nothing in the build
reads it: `work/build.py` needs only `NEEDED.jsonl` and `work/`.

`work/find_pages.py` and `work/ocr_answers.py` are the one-off page-lookup scaffolding from
that abandoned route; they are not imported by the build and need `pymupdf`/`rapidocr` if run.
"""


def build_review(rows, stats):
    medium = [r for r in rows if r["confidence"] == "medium"]
    flagged = [r for r in rows if r["flags"]]
    out = ["# Review list — 257 flagged cards", "",
           "Rows a human should look at before the key is merged. Generated by `work/make_docs.py`.",
           "",
           f"## Medium confidence ({len(medium)})", ""]
    for r in medium:
        why = MEDIUM_NOTE.get(r["id"], short_reason(r))
        out.append(one_line(r, f"{r['confidence']} — {why}"))
    out += ["", f"## Rows carrying a flag ({len(flagged)})", ""]
    for r in flagged:
        extra = ", ".join(f"`{x}`" for x in r["flags"])
        if r["id"] in FLAG_NOTE:
            extra += " — " + FLAG_NOTE[r["id"]]
        out.append(one_line(r, extra))
    out += ["", f"## Notable corrections ({len(NOTABLE)})", ""]
    index = {r["id"]: r for r in rows}
    for rid, note in NOTABLE:
        r = index[rid]
        out.append(one_line(r, f"{r['confidence']} — {note}"))
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stats", required=True)
    ap.add_argument("--verify", required=True)
    ap.add_argument("--readme", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--chunk-size", type=int, default=100)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.out, encoding="utf-8")]
    stats = json.load(open(args.stats, encoding="utf-8"))
    verify = json.load(open(args.verify, encoding="utf-8"))

    with open(args.readme, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_readme(stats, verify, args))
    with open(args.review, "w", encoding="utf-8", newline="\n") as f:
        f.write(build_review(rows, stats))
    print(f"wrote {args.readme} and {args.review} from {len(rows)} rows")


if __name__ == "__main__":
    main()
