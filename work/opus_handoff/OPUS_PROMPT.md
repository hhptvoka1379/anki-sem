# Semestre Filtro — Chunk-by-Chunk Anki Rebuild & Lossless Merge Prompt (`7,078` Items / `196` Chunks)

## Mission
Process all **196 pre-joined chunks** (`work/opus_handoff/chunk_manifest.json`, `≤ 45` items/chunk, **`7,078` total EdiSES items** = `6,948` live cards + `130` restored duplicate book items) and emit a single Anki package (`build/Semestre_Filtro_Complete.apkg` plus a no-media updater `build/Semestre_Filtro_Text_And_Templates_Update.apkg`) that merges **100% losslessly in place** into the user's live collection (`currnet_no_images.apkg.md`) with **zero duplicate notes, zero lost review history, 100% verified keys, and 100% Italian explanations**.

Read `work/opus_handoff/README.md`, `work/opus_handoff/GOALS.md`, and `work/opus_handoff/target_schema/ids_and_decks.json` before writing code.

---

## Non-Negotiable Live-Collection Compatibility Contract
Your output `.apkg` **must** match the live collection schema in `work/opus_handoff/target_schema/`:
1. **Exact Note GUIDs**: Never call `genanki.guid_for(id)` on existing cards — the `6,948` live cards use random Anki `guid64()` strings (`CHIM-C01-COMM-001 -> o0r7#8We]|`). Always set `note.guid = guid_map_7078[id]["guid"]` from `target_schema/guid_map_7078.json` (`6,948` exact live GUIDs + `130` collision-free deterministic GUIDs = `7,078` unique GUIDs).
2. **Exact Two Notetypes & Frozen 17 Fields**:
   - **`mid = 1813027267`** (`genanki.Model.FRONT_BACK`, `'Semestre Filtro [04 Neo-Brutalist Risoprint Zine]++'`) for all `COMM` + `NCOM` MCQs (`5,008` notes: `4,893` live + `115` restored).
   - **`mid = 1481924269089`** (`genanki.Model.CLOZE`, `'Semestre Filtro — Completamento (cloze)'`) for all `COMP` clozes (`2,070` notes / `2,074` cards: `2,055` live + `15` restored; preserve two-blank `{{c1::...}}` + `{{c2::...}}` on `BIO-C01-COMP-008`, `BIO-C01-COMP-114`, `BIO-C04-COMP-017`, `BIO-C06-COMP-030`).
   - **Exact 17 fields (`ord 0..16`, DO NOT add/remove/reorder fields)**: `ItemID`, `Subject`, `SubjectCode`, `ChapterNum`, `ChapterTitle`, `QuizTypeLabel`, `QuestionNum`, `BookPage`, `FrontStemHTML`, `BackStemHTML`, `FrontOptionsHTML`, `BackOptionsHTML`, `AnswerBannerHTML`, `ExplanationHTML`, `FigureHTML`, `QuestionScanHTML`, `SolutionScanHTML`.
   - Store accepted `COMP` synonyms inside `AnswerBannerHTML` as `<span class="sf-acc-data" data-c1="syn1|syn2" data-c2="..." hidden></span>` for `typed_answer.js`, and prepend errata/ambiguity callouts (`<div class="note-box">...</div>`) inside `ExplanationHTML`.
3. **Exact 117 Deck Names & `did`s**: Assign every note to `guid_map_7078[id]["did"]` and `deck_name` (`Semestre Filtro::01 Chimica e Propedeutica Biochimica / 02 Biologia / 03 Fisica::Cap. XX - <Title>::1. Quiz commentati / 2. Quiz non commentati / 3. Quiz a completamento`).
4. **Timestamp Floor (`mod >= 1792777789`)**: Live cards have `max(mod) = 1792777729`. Post-process `collection.anki2` before zipping so `notes.mod` and `col.mod` are `>= max(1792777789, int(time.time()))`, otherwise Anki skips updates!
5. **Exact Media Filenames & Templates**: Keep live `<img>` filenames (`<ItemID>.png`, `sol_p<page>_q<num>.png`, `fig_p<page>_<idx>.png`). Upgrade `target_schema/current_templates/{mcq_1813027267,cloze_1481924269089}` in place: bundle offline `_*.ttf` fonts (remove Google Fonts `@import`/`<link>`), keep `#sf-mode-pill` (`sf_mode_04_neobrutalist_bauhaus`) + `.opt.correct` + `{{cloze:FrontStemHTML}}` + `{{type:cloze:FrontStemHTML}}`, collapse front `QuestionScanHTML` inside `<details class="scan-details">` on `1481924269089`, and inject tolerant Italian/scientific `typed_answer.js` on `1481924269089`.

---

## Chunk-by-Chunk Execution Protocol (`chunk_001` → `chunk_196`)
Never load the whole 7,078-item corpus into an LLM context window. Process **one chunk file (`≤ 45` items, ~85 KB)** at a time from `work/opus_handoff/chunk_manifest.json` and write finalized chunk outputs to `work/opus_handoff/finalized/chunk_<NNN>.jsonl` with a persistent checkpoint ledger `work/opus_handoff/PROGRESS.json`:

For each item in `chunk_<NNN>.jsonl`:
1. **Fast-Path Clean Items (`needs_attention == []`, `5,938 / 7,078` items)**:
   - Stem, options, Cloze syntax, and answer key are already remediated (`remediated_card` + `live_anki`) and consensus-verified across prior runs (`solved_work.cc130265` / `0c53ca03` / EdiSES `COMM`).
   - Verify HTML chemical/math typography (`<sub>`, `<sup>`, `→`, `⇌`, Greek letters; zero raw LaTeX `$...$` or ASCII `H2SO4` / `10^-3`) and emit finalized 17 fields + merged tags (`live_tags` ∪ `{ud_tag}` ∪ `dup_tags`).
2. **Targeted Scan & Science Audit (`needs_attention != []`, `1,140 / 7,078` items)**:
   - **`restored_duplicate_130` (`130` items)**: Pre-remediation records from `6d93039e`. Clean OCR (`ma le cole`, `diluirst`, `dil mm`, raw subscripts) against `<ItemID>.png` / book scan `question_book_page`, verify the key against `solved_work.restored_twin_ref.twin_answer_text` (watch `CHIM-C09-NCOM-013`, `CHIM-C13-NCOM-048`, `FIS-C05-NCOM-108`), and **remap or strip any option-letter references (`risposta C`)** in `twin_explanation` (`97 / 130` pairs have shuffled option letters relative to their twin!). Convert the `15` restored `COMP` stems to `{{c1::answer}}`.
   - **Residual live defects (`2` items)**: Fix `CHIM-C10-NCOM-080` banner (`A. C,` → `A. Cs`) and rewrite `FIS-C04-COMM-007`'s garbled Bernoulli explanation + attach figure crop.
   - **Page 291 (`CHIM-C11-COMM-017..023`, `7` items)**: Keep unanimous 6-source keys (`17:C, 18:D, 19:C, 20:A, 21:E, 22:A, 23:B`) and clean HTML explanations.
   - **`ak257_review` & `cc130265_key: suspect` / `ambiguous:` (`~145` items, incl. the `8` `9d2e065b` vs `0c0900a2` disagreements)**: Inspect 300–600 DPI question + answer-table crops, solve independently from first principles, set the authoritative key + `<div class="note-box">` errata note if EdiSES printed a defective key, and write a rigorous 2–5 sentence Italian explanation (120–420 chars).
   - **`cc130265_ocr:` / `chem:` (`~810` items)**: Compare `remediated_card` against `<ItemID>.png` crop, repair any surviving OCR typo or valence/formula error, then reuse `solved_work.0c53ca03.reason` if clean and accurate or write a fresh Italian explanation.
   - **`cc130265_missing:` (`34` figure-dependent items)**: Crop the missing figure/diagram/circuit/structure from the source PDF page into `FigureHTML` (`_fig_<ItemID>.png`), add `con_figura` tag, and write the Italian explanation referencing the figure.

---

## Subagent Policy & Verification Loop
- Dispatch bounded subagents on batches of **1–4 chunk files (`45–180` items max)** with explicit read/write paths; verify every finalized chunk with a deterministic validator script before marking it `done` in `PROGRESS.json`.
- After all `196` chunks pass validation, assemble the `.apkg` packages and run the **Live-Merge Simulation Test** in `GOALS.md` (importing your built `.apkg` into a temporary SQLite copy of `currnet_no_images.apkg.md` and proving `6,948` in-place updates + `130` clean insertions = `7,078` notes / `7,082` cards, `0` duplicate `ItemID`s).
