# Structure

```
opus_attempt/
  PROMPT.md RULES_ORCHESTRATOR.md RULES_WORKER.md LOG.md        # spec + log (read-only for workers)
  STRUCTURE.md STATE.md DECISIONS.md UNVERIFIED.md CONFLICTS.md  # orchestrator only
  assets/            fonts, typed_answer.js (read-only)
  exam_structure.md  sources/mur/        # MUR research agent
  scripts/           orchestrator-owned pipeline code (build.py, gates/, render/)
  templates/         front.html back.html style.css (note type)
  work/<agent-name>/ each subagent writes only here
  work/ocr/          full-book OCR: pNNN.txt (text), pNNN.tsv (word confidences); NNN = 1-based PDF page, 3 digits
  work/anki-test/    temporary anki collections (delete freely)
  build/             orchestrator only: ids.json page_map.json extracted.jsonl verification.jsonl media/ renders/ verification_report.md Semestre_Filtro_v<maj>.<min>.apkg
  .venv/             python 3.15: genanki, anki 26.09.3, pymupdf
```

Git: subagents do not commit; the orchestrator commits and pushes (avoids index.lock races between parallel agents).

## Record schema: `extracted.jsonl` (one JSON object per printed question)

| key | type | notes |
|---|---|---|
| id | str | `<SUBJ>-C<nn>-<COMM\|NCOM\|COMP>-<qqq>`, e.g. `CHIM-C01-COMM-007` |
| subject_code | str | `CHIM` `BIO` `FIS` |
| subject | str | `Chimica e Propedeutica Biochimica`, `Biologia e Genetica`, `Fisica` |
| chapter | int | |
| chapter_title | str | as printed |
| quiz_type | str | `COMM` `NCOM` `COMP` |
| question_num | int | as printed |
| pdf_page | int | 1-based PDF page of the question |
| printed_page | int | printed page number of the question |
| stem | str | plain text, Unicode formulas; COMP: the blank is written `_____` (5 underscores) |
| options | obj or null | `{"A": "...", ..., "E": "..."}` for COMM/NCOM; null for COMP |
| printed_key | str or null | letter for MCQ, word(s) for COMP; null if no key in the scan |
| key_page | int or null | printed page where the key was read |
| printed_reasoning | str or null | COMM reasoning block, plain text |
| figure | str or null | media filename, figure needed to answer |
| figure_side | str | `front` (default) or `back` (figure only in the solution section) |
| question_crop | str | media filename of the question as printed |
| solution_crop | str or null | media filename of the printed solution |
| ocr_flags | list | e.g. `[{"span": "...", "page": 12, "status": "ocr_fallback_needed"}]` |
| worker_notes | str | anything odd, empty if none |

Media filenames: `<id>_q.png`, `<id>_s.png`, `<id>_fig.png` (lowercase id ok). Files go in `work/<agent>/media/`.

## Record schema: `verification.jsonl`

`id`, `printed_key`, `derived_key`, `derived_by` (list of agent names), `derived_confidence`, `adjudicated` (bool), `status` (`verified` `book-corrected` `derived` `unverified`), `reason` (list of reason tags: `ocr` `no-key` `figure` `ambiguous` `disputed`), `evidence` (`{"page": int, "quote": str}`), `final_key`, `accepted_answers` (list, COMP), `explanation`, `explanation_origin` (`book` `generated`), `note_html` (str or empty), `dup` (list of ids), `ud` (str slug).

## Tags on each note
`verify::<status>` (exactly one), `verify::<reason>` for each reason, `ud::<slug>`, `dup::<id>` per duplicate.
