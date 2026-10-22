# Answer key — 257 flagged cards

Output of the `PROMPT.md` task on `NEEDED.jsonl` (257 lines: 239 MCQ + 18 cloze).

## Files
- `answer_key_output.jsonl` — the answer key, one object per input line, same ids, same order.
- `answer_key_chunks/chunk_000..002.jsonl` — the same key split 100 / 100 / 57.

## Method
Every card was read from its scan (`images/<id>.png`) next to the OCR text; where the two
disagreed the scan was used. `letter` is the answer; `answer_text` is the printed text of
that option.

`reason` names the principle, formula or definition that decides the item.
`confidence` is `high` (245) or `medium` (12) where the key or the OCR leaves real doubt.

## Note on `answer_text`
The deck's `options` are themselves OCR of the scans and 147 of the 239 chosen strings were
mangled (`Visotopo` for `L'isotopo`, `0,` for `O₂`, `Ss` for `5s`, `5e3` for `5 e 3`,
`HNO₄` for `HNO₂`, `107` for `10⁻¹¹`, `SON` for `50 N`, …). For those the printed text is
used, restored in `work/answer_text_fixes.py`; the mapping is one-to-one and `letter`
still points at the deck's own option. Where the string was already clean it is verbatim.

## Verification
Every answer was re-derived a second time from the stem alone (not from the first pass)
and cross-checked against the scans. That pass caught and fixed:
- `CHIM-C09-NCOM-060` — wrong letter (Br oxidises, I reduces → B).
- `FIS-C06-NCOM-026` — volt = coulomb/farad → **E**, not D.
- `CHIM-C03-NCOM-137` — the ionisation table is aluminium → **group 13**.
- `BIO-C02-NCOM-005` — G2 quantity Y = 4C, so metaphase II = **0.5 Y**.
- `CHIM-C06-NCOM-023` (0.0001 mol in 1 mL), `CHIM-C11-COMM-007` (100 L),
  `CHIM-C11-COMM-027` (4 g), `FIS-C04-NCOM-034` (90 N), `CHIM-C11-NCOM-009` (monoprotico).

## Flags used
- `needs_figure` (6) — the record carries a `figure`; answered from the diagram/table.
- `typo` (3) — OCR mangles the formula/option (`HNO₄`, `10^1/2`, `60 = 107?`).
- `multiple_correct` (2) — two options are both tenable as printed
  (`CHIM-C11-NCOM-170` pH decrease vs buffer; `FIS-C06-NCOM-157` "tre rami" vs "più di due terminali").
- `ambiguous` (1) — `FIS-C03-NCOM-011`: exact equilibrant is 1.93F, options stop at 2F.

## Cards where the book itself has no valid option
`CHIM-C06-NCOM-088` (osmotic pressure is π, not offered) and `CHIM-C04-NCOM-014`
(energy "lost by the atoms") — the closest option is marked and reasoned, not silently guessed.
