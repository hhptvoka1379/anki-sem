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
- Opus MUR research → `sources/mur/`, `exam_structure.md`.
- Sonnet `template` → `work/template/{front.html,back.html,style.css,sample_fields.json,NOTES.md}`.
- Sonnet `buildscript` → `work/buildscript/build.py` (+fields.py, tests).
- Sonnet `gates` → `work/gates/run_gates.py`, `render.js`.
- Script `scripts/ocr_all.sh` → `work/ocr/pNNN.{txt,tsv}` (re-runnable, skips done pages).
- Chunk cost log: none yet.

## Working
- On the back side, Anki puts the comparison in `<code id=typeans>`. An exact match is one line. A wrong answer is the typed text, then `<br><span id=typearrow>`, then the expected text. `typed_answer.js` reads the first line, skipping `.typeMissed`.
- The library render (`card.answer()`) leaves `[[type:TypedAnswer]]` in place. For test renders, replace it with `col.compare_answer(expected, typed)`.

## Not working / tried and failed
- `anki -b <folder> file.apkg` while Anki is already running prints "Already running; reusing existing instance" and imports into the real profile. Never launch Anki.app.

## Next
1. When `work/pagemap/chim_ch1.json` appears: split CHIM ch.1 into ≤50-card chunks; start Sonnet extraction workers (OCR from `work/ocr/`, image only when unsure), then blind derivation workers.
2. Review template / build / gate drafts; promote to `templates/` and `scripts/`.
3. Adjudicate disagreements (Opus), explanations + second-worker check, build `Semestre_Filtro_v1.0.apkg` for CHIM-C01, run all §7 gates, renders.
4. Push, notify, AskUserQuestion for pilot approval; meanwhile workers extract CHIM ch.2 only.
If restarted: re-run `scripts/ocr_all.sh` (resumes); check which work/ outputs exist before restarting any agent.
