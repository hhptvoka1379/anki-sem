# Workpack — 5,902 cards without an explanation

Generated from the live Anki collection (read-only). Nothing here writes to
Anki.

## Contents

| file | purpose |
|---|---|
| `PROMPT.md` | **the full task specification** — give it to the model verbatim |
| `questions.db` | SQLite: source of truth, 5,902 rows + `examples` (4 filled) |
| `questions.csv` | same rows, UTF-8, for spreadsheet filters (read-only mirror) |
| `reference_hashes.json` | tamper seal per id (question/options/answer) |
| `manifest.json` | counts, source fingerprint, sha256 of db/csv |
| `validate.py` | hard gate; exits 1 on any violation |
| `export_reasons.py` | dumps finished reasons to `reasons_done.jsonl` |
| `CHEM_JUDGEMENT.md` | 9 known damaged cards: flag them, do not repair |

## Scope

- `status = 'pending'` → **5,902** cards, all queued: 3,848 MCQ
  (CHIM 1,482 · BIO 1,534 · FIS 832) and 2,054 cloze
  (CHIM 582 · BIO 843 · FIS 629).
- `examples` table → the 4 explanations already written; style reference only.
- Cloze rows carry `back_stem` (the filled sentence); `question` keeps the
  `{{c1::term}}` marker and `answer_text` is the term.

## Schema (table `questions`)

```
ord, id, quiz_type, subject_code, chapter_num, chapter_title, qnum, page,
question, option_a..option_e, answer, answer_text, back_stem,
reason, flags, status, ref_hash, updated_at, scan
```

- `answer` is the book's key (letter). Never edit it.
- `ord` — stable work order 0..N-1 (CHIM → BIO → FIS, book order inside each).
  It covers all 5,902 rows, so it has no gaps.
- `reason` — the only free-text field you write.
- `flags` — JSON array as text, e.g. `["ocr: H,S0,, likely H₂SO₃"]`.
- `status` — `pending` | `done` | `flagged`.
- `ref_hash` — sha256 seal; `validate.py` recomputes it from the content.

Views: `v_pending`, `v_flagged`, `v_progress`.

## Useful filters

```sql
-- work queue, book order (always ORDER BY ord; views don't guarantee order)
SELECT * FROM v_pending ORDER BY ord;
-- one chapter
SELECT * FROM v_pending WHERE subject_code = 'CHIM' AND chapter_num = 11
ORDER BY ord;
-- one page
SELECT * FROM questions WHERE page = 170;
-- everything flagged, grouped
SELECT json_extract(flags,'$[0]') prefix, count(*) FROM v_flagged GROUP BY 1;
-- progress
SELECT * FROM v_progress;
-- remaining per subject/chapter
SELECT subject_code, chapter_num, count(*) FROM v_pending
GROUP BY 1, 2 ORDER BY 1, 2;
```

## Workflow

1. Copy the folder somewhere writable.
2. Give the model `PROMPT.md` and the folder path.
3. Model edits `questions.db` only (`reason`, `flags`, `status`, `updated_at`).
4. `python3 validate.py` must exit 0 (model runs it every 100 rows).
5. `python3 export_reasons.py` → `reasons_done.jsonl`.
6. Hand back `questions.db` **or** `reasons_done.jsonl`; the reasons get merged
   into Anki with a WAL-safe, stats-preserving script (never via `.colpkg`).

## CSV caveat

`questions.csv` is a snapshot for filtering/eyeballing. If you edit the CSV
instead of the DB, only `id`, `reason`, `flags` are meaningful on handback —
everything else is ignored, and the DB remains authoritative.

Excel/LibreOffice: import as UTF-8 (Data → Text to Columns → UTF-8) so `₂`,
`⁻`, `⇌` survive.
