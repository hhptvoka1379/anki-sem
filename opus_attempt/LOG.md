# Orchestrator log

Update after every chapter, every gate, and before any context clear. See `RULES_ORCHESTRATOR.md`.

## Done
- (pre-run, by the setup session) Confirmed: `anki` Python library 26.9.3 imports an `.apkg` into a temporary collection, and copies media (including fonts with a leading underscore).
- (pre-run) Tested `assets/typed_answer.js` against Anki 26.9.3's real comparison HTML: 9/9 cases correct, including an elided article, a plural variant, accents, and an empty answer.
- (pre-run) The user confirmed on Anki desktop that the typed-answer probe card works.
- (pre-run) Downloaded the fonts the CSS uses into `assets/fonts/` (Space Grotesk, Space Mono, Syne, OFL licences included).

- (2026-10-23, orchestrator) Branch `opus-rebuild/semestre-filtro` active. `.venv` (Python 3.15) with genanki, anki 26.09.3, pymupdf: imports checked. `build/ids.json` written (model_id 2014733439; ROOT/CHIM/BIO/FIS deck ids). `STRUCTURE.md` (folders + record schemas), `STATE.md`, `DECISIONS.md`, `UNVERIFIED.md`, `CONFLICTS.md` created.

## In flight (background, started 2026-10-23)
- Opus `pagemap` → `work/pagemap/chim_ch1.json` first, then `work/pagemap/page_map.json`.
- Opus MUR research DONE (125k tok, 314 s), commit 98518a5: 20 sources, 7 UD per subject (2026 syllabi), 21 `ud::` slugs; 2026/27 format: 31 questions per subject (21 MCQ×5 options + 10 completamento), +1/0/−0.1, 50 min, pass 18/30.
- Sonnet-high QA: `qa-pipeline` → `work/qa-pipeline/findings.md` (templates + build.py); `qa-mur` → `work/qa-mur/findings.md` (exam_structure claims vs sources).
- Sonnet `template` DONE (65k tok, 101 s); Sonnet `buildscript` DONE (57k tok, 92 s). Orchestrator reviewed templates vs reference (structure + tap-to-pick + theme scripts kept; Google Fonts links removed; typed_answer.js embedded; NoteHTML box), aligned `fields.py` HTML to `work/template/sample_fields.json`, fixed font path, promoted to `templates/` and `scripts/build.py`+`scripts/fields.py`. Synthetic 3-note build with real templates: OK (3 notes, 7 media). Not yet checked: Anki import, renders, `{{type:}}` inside a `{{#TypedAnswer}}` section.
- Sonnet `gates` DONE (116k tok, 450 s); promoted to `scripts/gates/` (run_gates.py, render.js, typed_check.js; `npm install` done there). Orchestrator ran it on a 3-note package built with the real templates: gates 1,2,3,4,7,8 PASS; 6 FAIL as expected (test unverified card not in UNVERIFIED.md); 5 and 9 MANUAL by design. Gate 8 typed-answer matrix on the real back template: correct/variant show 'Risposta accettata', wrong does not, so `{{type:}}` inside `{{#TypedAnswer}}` works in the anki library render. `--chapters` takes space-separated keys (`--chapters CHIM-C01`). Gate 1 does not understand the page_map schema yet: align when build/page_map.json lands.
- Script `scripts/ocr_all.sh` → `work/ocr/pNNN.{txt,tsv}` (re-runnable, skips done pages).
- CHIM ch.1 map (from pagemap agent's chim_ch1.json, copied to build/chim_ch1_pagemap.json): COMM Q1–10 PDF 12–13, NCOM Q1–121 PDF 14–26, COMP Q1–47 PDF 27–29 = 178 cards; keys in CHIM RISPOSTE PDF 256–258 (offset 9 in chapter, 4 on solution pages).
- Method test (Sonnet medium, same 40 items COMM 1–10, NCOM 1–15, COMP 1–15): `xtest-ocr` (OCR-first, image when unsure) vs `xtest-img` (image-first, OCR cross-check); `croptool` → work/croptool/crop.py (question/solution/figure crops from Tesseract boxes). Next: a Sonnet comparison agent diffs the two extractions field by field against the images; pick method; then the 178-card chapter in ≤50-card chunks: COMM 1–10, NCOM 1–50, 51–100, 101–121, COMP 1–47.
- Chunk cost log: buildscript 57k/92 s, template 65k/101 s, MUR 125k/314 s (setup jobs, not card chunks).

## Working
- On the back side, Anki puts the comparison in `<code id=typeans>`. An exact match is one line. A wrong answer is the typed text, then `<br><span id=typearrow>`, then the expected text. `typed_answer.js` reads the first line, skipping `.typeMissed`.
- The library render (`card.answer()`) leaves `[[type:TypedAnswer]]` in place. For test renders, replace it with `col.compare_answer(expected, typed)`.

## Not working / tried and failed
- `anki -b <folder> file.apkg` while Anki is already running prints "Already running; reusing existing instance" and imports into the real profile. Never launch Anki.app.

## Next
(All agents stopped 2026-10-23 at user request: usage too high. pagemap (Opus), croptool, qa-pipeline were killed mid-task; only CHIM ch.1 map exists, `work/croptool/crop.py` is unfinished/untested, qa-pipeline findings lost. OCR script still running, no tokens. Commit 6febc7c not pushed yet: each push runs an Opus review per commit via the pre-push hook, so batch pushes.)
1. Workers are Haiku medium (DECISIONS). Done: NCOM 6–50 (`work/x-chim01-ncom-a/`, QA clean, 10/10 gold controls). Chunk cost: 92.6k tok, 164 s, 45 records. Open: NCOM-022 needs a figure crop; NCOM-050 worker note (option A 'carbonio e azoto') goes to derivation.
2. Remaining CHIM ch.1 extraction, one Haiku worker at a time with 10 gold controls each: NCOM 51–121 (two chunks), COMP 16–47 (the 40 test records already cover COMM 1–10, NCOM 1–15, COMP 1–15; reuse them).
3. Crops: finish crop.py myself or one small worker; check a sample.
4. Blind derivation, adjudication, explanations, build, gates, renders, pilot approval question.
5. Rest of page map later, only per chapter as needed.
