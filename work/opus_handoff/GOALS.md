# GOALS.md — Acceptance Gates for Chunked Rebuild & Lossless `currnet_no_images.apkg` Merge

Every gate is binary (**PASS / FAIL**) and must be verified by automated script (`scripts/verify_gates.py`) before completion.

---

## Gate 1 — Full 196-Chunk / 7,078-Item Completeness
- [ ] All **`196 / 196`** chunk files in `work/opus_handoff/finalized/chunk_001..196.jsonl` exist and validate (`0` pending chunks in `PROGRESS.json`).
- [ ] Total unique `ItemID`s = **`7,078`** (`6,948` existing live items + `130` restored duplicate book items from `special_sets/missing_130_restored.jsonl`), with contiguous `1..N` numbering in all `84` `(chapter, quiz_type)` subsections.
- [ ] Total Anki notes = **`7,078`** (`5,008` MCQ on `mid=1813027267` + `2,070` Cloze on `mid=1481924269089`); total Anki cards = **`7,082`** (`+4` `c2` cards on `BIO-C01-COMP-008`, `BIO-C01-COMP-114`, `BIO-C04-COMP-017`, `BIO-C06-COMP-030`).

## Gate 2 — 100% Live-Collection Binary Compatibility (`currnet_no_images.apkg.md`)
- [ ] **GUID Identity (`6,948 / 6,948`)**: Every one of the `6,948` live items has `notes.guid == guid_map_7078[ItemID]["guid"]` (`100.0%` exact match to `currnet_no_images.apkg.md`), and all `7,078` GUIDs are globally unique (`0` collisions).
- [ ] **Notetype Parity**: Only two notetypes exist: `1813027267` (`kind=0` Basic, `'Semestre Filtro [04 Neo-Brutalist Risoprint Zine]++'`) and `1481924269089` (`kind=1` Cloze, `'Semestre Filtro — Completamento (cloze)'`), both having the **exact 17 fields (`ord 0..16`)** in identical order.
- [ ] **Cloze Syntax Integrity (`2,070 / 2,070`)**: Every note on `1481924269089` contains valid `{{c1::...}}` in `FrontStemHTML` (`0` Anki "Empty card" errors), and the `4` two-blank notes preserve both `{{c1::...}}` and `{{c2::...}}`.
- [ ] **Deck ID Parity (`117` decks / `84` leaf subdecks)**: Every card's `did` and `::`-hierarchy matches `target_schema/ids_and_decks.json` (`1792587736226..1792587736341`).
- [ ] **Timestamp Update Gate**: Every note has `notes.mod >= 1792777789` (strictly greater than live `max(cards.mod) = 1792777729`).
- [ ] **Live-Merge Simulation Test**: Importing the built `.apkg` into a temporary copy of `currnet_no_images.apkg.md` results in **`6,948` updated notes, `130` added notes, `0` skipped notes, and `0` duplicate `ItemID`s** (`SELECT count(*), count(DISTINCT substr(flds, 1, instr(flds, char(31))-1)) FROM notes` == `(7078, 7078)`).

## Gate 3 — Scientific Accuracy, Page 291, 130 Restored Items & Explanations (`7,078 / 7,078`)
- [ ] **Zero unanswered cards**: `5,008 / 5,008` MCQs have exactly one `<div class="opt correct">` (`A..E`) matching `AnswerBannerHTML`; `2,070 / 2,070` `COMP` cards have non-empty `{{c1::...}}` + `<span class="sf-acc-data" data-c1="..." hidden></span>`.
- [ ] **Page 291 (`CHIM-C11-COMM-017..023`)**: Keys equal `17:C, 18:D, 19:C, 20:A, 21:E, 22:A, 23:B` with clean formulas (`HCl`, `CH₃COOH`, `NH₄Cl`, `K₂CO₃`).
- [ ] **130 Restored Items**: OCR cleaned against scans, keys verified against `twin_answer_text` (including `CHIM-C09-NCOM-013`, `CHIM-C13-NCOM-048`, `FIS-C05-NCOM-108`), and **zero stale twin option-letter references** (`risposta X` where `X != item.answer`) in `ExplanationHTML`.
- [ ] **Residual Live Bugs Closed**: `CHIM-C10-NCOM-080` banner reads `Risposta corretta: A. Cs` (not `A. C,`); `FIS-C04-COMM-007` has clean Bernoulli equation HTML + figure; all `8` `9d2e065b` vs `0c0900a2` key disagreements explicitly adjudicated.
- [ ] **100% Explanation Coverage**: `7,078 / 7,078` notes have non-empty, scientifically sound Italian `ExplanationHTML` (`0` meta-text like `"Dal testo"`, `"Secondo EdiSES"`, `"Opzione corretta"`).

## Gate 4 — Typography, Media, Offline Assets & UX
- [ ] **Zero raw OCR / LaTeX artifacts**: `0` occurrences of `$...$`, `\frac`, `H2O`/`H2SO4`/`CO2` plain digits in formulas, `10^-`, `HC)`/`HCi`/`HC!`, `diluirst`, `ma le cole`, `dil mm`, or stray trailing commas in banners.
- [ ] **Zero external network calls**: `0` `https://fonts.googleapis.com` or CDN URLs in CSS/HTML; bundled `_*.ttf` fonts present in package media.
- [ ] **Media integrity**: `0` broken `<img src="...">` references in full `.apkg`; all `34` `cc130265_missing:` figure items have rendered `FigureHTML` crops; front `QuestionScanHTML` is collapsed inside `<details class="scan-details">` on **both** `1813027267` and `1481924269089`.
- [ ] **Interactive UX preserved & upgraded**: `#sf-mode-pill` (`sf_mode_04_neobrutalist_bauhaus`) works on both notetypes, MCQ options support tap-to-eliminate / click-to-preview, and `typed_answer.js` grades `COMP` answers tolerantly (case/accent/whitespace/article/synonym-insensitive).
