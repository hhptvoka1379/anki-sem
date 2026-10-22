# Answer key — 257 flagged cards

Output of the `PROMPT.md` task on `NEEDED.jsonl` (257 lines: **239 MCQ + 18 cloze**).

## Files

- `answer_key_output.jsonl` — the key: one object per input line, same ids, same order, UTF-8 (no BOM), `\n` line endings.
- `answer_key_chunks/`: chunk_000.jsonl, chunk_001.jsonl, chunk_002.jsonl — the same key split at 100-row boundaries, byte-identical to the concatenation of the full file.
- `review.md` — the rows that need a human look (medium confidence, flagged, notable corrections).

## Output contract

- `letter` (MCQ) and `answers` (cloze) are the answer and are authoritative.
- `answer_text` is **always `options[letter]` of the matching NEEDED record, verbatim** (239/239 byte-identical), so a consumer that re-derives the text from the card can never disagree with this file.
- `printed_text` (present on 147 rows) carries the text as printed on the page, where the deck's own option string is OCR damage of it (`Visotopo` for `L'isotopo`, `0e0` for `O e O`, `HNO₄` for `HNO₂`, `SON` for `50 N`, …). It is informational only — the consumer may ignore it.
- `reason` names the principle, formula or definition that decides the item.
- `confidence` is `high` 246 / `medium` 11 / `low` 0.

## Reproducibility

Inputs: the 257-row `NEEDED.jsonl` plus the `images/` scans from the request pack, and the
answer sources in `work/` (`answers_part1..6.py`, `answer_text_fixes.py`).

```bash
python3 work/build.py \
    --input-dir  /tmp/answer_key_request \
    --overrides  work/answer_text_fixes.py \
    --parts-dir  work \
    --out        answer_key_output.jsonl \
    --chunks-dir answer_key_chunks \
    --stats      work/stats.json

python3 work/verify.py \
    --input-dir  /tmp/answer_key_request \
    --out        answer_key_output.jsonl \
    --chunks-dir answer_key_chunks \
    --json       work/verify.json

python3 work/make_docs.py \
    --input-dir  /tmp/answer_key_request \
    --out        answer_key_output.jsonl \
    --stats      work/stats.json \
    --verify     work/verify.json \
    --readme     ANSWER_KEY_README.md \
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
| a | 257 lines, 257 unique ids, same id set and order as NEEDED.jsonl | 257 lines, 257 unique, order match True | **PASS** |
| b | type matches the request for all 257 | mismatches: none | **PASS** |
| c | MCQ: letter in A-E and answer_text == options[letter] (case/space/punct insensitive) | 239/239 byte-identical, 239/239 equal after normalisation, 0 mismatched  | **PASS** |
| d | cloze: len(answers) == blanks | 18/18 ok | **PASS** |
| e | confidence in {high,medium,low}; flags subset of the allowed set | violations: none | **PASS** |
| f | reason >= 25 chars on every row | min 125 chars | **PASS** |
| g | chunk concatenation == full file, same sha256 | 3 chunks, sha256 97eecd0a57c1d07c… == 97eecd0a57c1d07c…: True | **PASS** |

**Overall: PASS** — 257 rows, min reason length 125 chars.

Integrity:

- `sha256(answer_key_output.jsonl)` = `97eecd0a57c1d07c329cc071e9f3ae9ccff205d7bb7c816d1d15a88e95fab166`
- `sha256(cat answer_key_chunks/chunk_*.jsonl)` = `97eecd0a57c1d07c329cc071e9f3ae9ccff205d7bb7c816d1d15a88e95fab166`
- identical: **True**

## Flags

| flag | rows |
|---|---|
| `needs_figure` | 9 |
| `ambiguous` | 2 |
| `multiple_correct` | 2 |
| `typo` | 3 |

`needs_figure` is the union of the flags the answer sources carry and the flags implied by a
`figure` key in the record (9 rows), not an inference from the image alone.

`CHIM-C10-NCOM-018` carries `ambiguous`: the deck's options A and E both read `CO₂` after OCR,
but the printed page has **A = CO₃⁻** and **E = CO₂**. **E is the printed answer**; A is an OCR
error and the duplication is not real.

## Notable corrections

Rows where this key deliberately differs from what a naive or printed key would say.
Also listed one per line in `review.md`.

- `CHIM-C03-NCOM-137` — the ionisation table (578 / 1817 / 2745 → 11577 kJ/mol) is aluminium: three valence electrons, group 13. A first pass misread the jump as 5→6 (group 15).
- `BIO-C02-NCOM-005` — G2 of meiosis means DNA already duplicated (Y = 4C); after meiosis I each cell has 2C, so metaphase II = 0.5 Y, not Y.
- `CHIM-C06-NCOM-023` — 0.1 M = 0.0001 mol per mL, i.e. 0.0001 mol in 1 mL; 0.001 mol in 100 mL would be 0.01 M.
- `CHIM-C11-COMM-007` — pH 2 → 4 is a 100-fold dilution of [H⁺]; from 1 L the final volume is 100 L.
- `CHIM-C11-COMM-027` — pH 2 in 10 L = 0.1 mol H⁺ = 0.1 mol NaOH = 4 g; the option 0.4 g uses the wrong volume.
- `FIS-C04-NCOM-034` — p·A = ρgh·A with A = 10³ cm² = 0.1 m² gives 900 Pa × 0.1 m² = 90 N, the same for cone and cylinder (hydrostatic paradox).
- `CHIM-C09-NCOM-060` — in 2 HBr + I₂ → 2 HI + Br₂ the bromine goes −1 → 0 (oxidised) and iodine 0 → −1 (reduced); an earlier draft had this letter inverted.
- `FIS-C06-NCOM-026` — 1 F = 1 C/V, so 1 V = 1 coulomb / 1 farad (option E); option D is '1 joule · 1 coulomb', which is not a volt.

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
