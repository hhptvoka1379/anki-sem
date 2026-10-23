# Opus Handoff Pack (`work/opus_handoff/`) — Lossless Merge with `currnet_no_images.apkg`

This directory contains the pre-extracted live identity tables, exact current templates, special audit sets, and **196 self-contained chunk files (`≤ 45` items/chunk, `7,078` total EdiSES items)** so the next Opus run can work **chunk by chunk** and produce an `.apkg` that merges **100% losslessly** into the user's live Anki collection (`currnet_no_images.apkg.md`) while restoring the `130` previously deduplicated items, keeping all `7` Page-291 items verified, and preserving every fix from every prior branch.

---

## 1. Ground-Truth Profile of `currnet_no_images.apkg.md`

| Property | Exact Live Value in `currnet_no_images.apkg.md` |
|---|---|
| Archive format | Anki v3 `.apkg` (`collection.anki21b` Zstandard-compressed SQLite, schema `18`, media stub `9 B`) |
| Live counts | **`6,948` notes**, **`6,952` cards** (`4` two-blank Cloze notes emit `c1`+`c2`), `0` revlog rows in export |
| Modification timestamps | `max(notes.mod) = 1792749157`, `max(cards.mod) = 1792777729` → replacement notes **must** set `mod >= 1792777789` |
| Notetype 1 (`MCQ`) | **`id = 1813027267`**, `kind = 0` (`MODEL_STD`), name `'Semestre Filtro [04 Neo-Brutalist Risoprint Zine]++'`, `4,893` notes (`1,041 COMM + 3,852 NCOM`) |
| Notetype 2 (`COMP`) | **`id = 1481924269089`**, `kind = 1` (`MODEL_CLOZE`), name `'Semestre Filtro — Completamento (cloze)'`, `2,055` notes (`2,059` cards: `BIO-C01-COMP-008`, `BIO-C01-COMP-114`, `BIO-C04-COMP-017`, `BIO-C06-COMP-030` have `{{c1::...}}` + `{{c2::...}}`) |
| Field list (both models, 17 fields in exact `ord 0..16`) | `ItemID`, `Subject`, `SubjectCode`, `ChapterNum`, `ChapterTitle`, `QuizTypeLabel`, `QuestionNum`, `BookPage`, `FrontStemHTML`, `BackStemHTML`, `FrontOptionsHTML`, `BackOptionsHTML`, `AnswerBannerHTML`, `ExplanationHTML`, `FigureHTML`, `QuestionScanHTML`, `SolutionScanHTML` |
| GUID provenance | **Random Anki 64-bit Base91 GUIDs (`guid64()`)** created when `++` was instantiated in Anki Desktop (e.g., `CHIM-C01-COMM-001 -> o0r7#8We]|`, `CHIM-C01-COMP-001 -> wQQD:JD0f?`). **No hash formula can recompute them** — builders **must** read `target_schema/guid_map_7078.json`. |
| Deck tree | **`117` decks** (`1` root + `3` subject decks `01 Chimica e Propedeutica Biochimica`, `02 Biologia`, `03 Fisica` + `28` chapter decks `Cap. 01 - ...` + `84` leaf quiz-type decks `1. Quiz commentati` / `2. Quiz non commentati` / `3. Quiz a completamento` + `Default`), exact `did`s `1792587736226..1792587736341` saved in `target_schema/ids_and_decks.json`. |
| Explanations currently populated | `1,046 / 6,948` (`1,041/1,041 COMM`, `4/3,852 NCOM`, `1/2,055 COMP`); `5,902` empty (`100%` match with `uncommented_questions_workpack`). |
| Media `<img>` references still in HTML | `QuestionScanHTML` on all `6,948` (`<ItemID>.png`), `SolutionScanHTML` on `1,034` (`sol_p<page>_q<n>.png`), `FigureHTML` on `106` (`fig_p<page>_<idx>.png`). |

---

## 2. All 9 Compatibility Blockers Between `opus_attempt` and `currnet_no_images.apkg.md` (and Exact Fixes)

1. **GUID Mismatch (`0 / 6,948` match in `opus_attempt`)**
   - *Bug*: `opus_attempt/scripts/build.py` calls `genanki.guid_for(c["id"])`, producing `0%` match against the live random Anki GUIDs (`o0r7#8We]|`, etc.), duplicating all 6,948 cards on import.
   - *Fix*: Load `guid = guid_map_7078[item_id]["guid"]` from `target_schema/guid_map_7078.json` (`6,948` exact live GUIDs + `130` collision-checked deterministic Base91 GUIDs for restored duplicates).
2. **Model ID & Model Kind Split (`Basic` + `Cloze`, NOT single `Basic`)**
   - *Bug*: `opus_attempt` uses a single `Basic` (`kind=0`) model `2014733439`. Anki's `.apkg` importer **refuses** to update a `Cloze` (`kind=1`, `mid=1481924269089`) note with a `Basic` note, stranding all `2,055` `COMP` cards.
   - *Fix*: Emit two `genanki.Model` objects matching live `id`, `name`, and `model_type`: `1813027267` (`genanki.Model.FRONT_BACK`) for `COMM`+`NCOM`, and `1481924269089` (`genanki.Model.CLOZE`) for `COMP`.
3. **Field Count & Order (`20` fields in `opus_attempt` vs `17` frozen live fields)**
   - *Bug*: `opus_attempt` appends `TypedAnswer`, `AcceptedAnswers`, `NoteHTML` (20 fields). Standard Anki `.apkg` import without `merge_notetypes=True` will not update notes when field counts diverge.
   - *Fix*: Keep the exact **17-field** schema (`ord 0..16`). Embed accepted synonyms invisibly inside `AnswerBannerHTML` (`<span class="sf-acc-data" data-c1="syn1|syn2" data-c2="..." hidden></span>`) for `typed_answer.js`, and render warning/errata callouts (`<div class="note-box">...</div>`) at the top of `ExplanationHTML`.
4. **Cloze Stem Markup (`<span class="blank-slot">` vs `{{c1::...}}` / `{{c2::...}}`)**
   - *Bug*: `opus_attempt` replaces blanks with `<span class="blank-slot">…</span>` and `{{type:TypedAnswer}}`, which breaks Anki Cloze notetype `1481924269089` ("Empty card" error because `{{cloze:FrontStemHTML}}` finds no `{{c1::...}}`).
   - *Fix*: On `1481924269089`, `FrontStemHTML` **must** preserve `{{c1::answer}}` (and `{{c2::answer2}}` on `BIO-C01-COMP-008`, `BIO-C01-COMP-114`, `BIO-C04-COMP-017`, `BIO-C06-COMP-030`) and keep `{{cloze:FrontStemHTML}}` + `{{type:cloze:FrontStemHTML}}` in the Cloze template while upgrading grading via `typed_answer.js`.
5. **Deck Paths & `deck_id`s (`0 / 84` leaf subdecks match in `opus_attempt`)**
   - *Bug*: `opus_attempt` builds `'Semestre Filtro::Biologia::01 — ...::1. Quiz commentati'` with hash `deck_id`s, whereas the live deck uses `'Semestre Filtro::02 Biologia::Cap. 01 - ...::1. Quiz commentati'` with explicit `did`s `1792587736226..1792587736341`.
   - *Fix*: Read `did` and `deck_name` directly from `target_schema/ids_and_decks.json` (`decks_by_name`) / `guid_map_7078.json`.
6. **Timestamp (`notes.mod`) Gate (`1792777729` live floor)**
   - *Bug*: `currnet_no_images.apkg.md` has future-shifted `mod` timestamps up to `1792777729` (2026-10-23+). Any `.apkg` built with real wall-clock `time.time()` below `1792777729` is **silently skipped** by Anki on import as "older than existing note".
   - *Fix*: Post-process `collection.anki2` before zipping so `UPDATE notes SET mod = MAX(1792777789, CAST(strftime('%s','now') AS INT))` and `col.mod` exceeds `1792777789`.
7. **Media Filenames (`<id>_q.png` vs live `<id>.png` / `sol_p...` / `fig_p...`)**
   - *Bug*: `opus_attempt` renames scan images to `<id>_q.png`, `<id>_s.png`, `<id>_fig.png`, orphaning/duplicating all ~8,127 media filenames already referenced in the user's Anki `collection.media`.
   - *Fix*: Preserve the exact live filenames (`<ItemID>.png` in `QuestionScanHTML`, `sol_p<page>_q<num>.png` in `SolutionScanHTML`, `fig_p<page>_<idx>.png` in `FigureHTML` — stored in each chunk's `live_anki` dict; only add new `_fig_<id>.png` where freshly cropped for the 34 missing-figure items).
8. **Theme Toggle (`#sf-mode-pill`) & Offline Fonts (`_*.ttf`)**
   - *Bug*: Live CSS uses network `@import url('https://fonts.googleapis.com/...')` (fails offline), while `opus_attempt` dropped the user's Paper/CRT toggle (`#sf-mode-pill`, `localStorage['sf_mode_04_neobrutalist_bauhaus']`) and left `QuestionScanHTML` uncollapsed on the front of `1481924269089`.
   - *Fix*: Bundle `_SpaceGrotesk.ttf`, `_IBM_Plex_Sans.ttf`, `_JetBrainsMono.ttf` offline via `@font-face`, preserve `#sf-mode-pill` + `.opt.correct` + `.ans-box` across **both** `1813027267` and `1481924269089`, and wrap `QuestionScanHTML` inside `<details class="scan-details">` on the front of `1481924269089` (matching `1813027267`).
9. **Tags & Residual Content Bugs in `currnet_no_images.apkg.md`**
   - *Fix*: Keep live `materia:: / capitolo:: / tipo:: / pagina:: / con_figura` tags and append `ud::<slug>`, `dup::<twin_id>`, and `verify::<flag>`. Also fix the two live defects still present in `currnet_no_images.apkg.md`:
     - `CHIM-C10-NCOM-080`: `AnswerBannerHTML` says `Risposta corretta: A. C,` instead of `A. Cs`.
     - `FIS-C04-COMM-007`: `ExplanationHTML` contains OCR-garbled Bernoulli equation (`P;+r*g -hibrovi=...`) and needs clean math + figure crop.

---

## 3. Answers on the 130 Missing Items & Page 291 (`CHIM-C11-COMM-017..023`)

### A. Where Are the 130 Missing Items & Their Answers?
- **Exact source**: **`origin/arena/6d93039e-anki-sem:output/qa_dataset.jsonl`** (`7,078` items = `6,948` in `currnet_no_images` + **`130` missing items**, **100% (`130 / 130`) populated with `answer` + `answer_text`**) and its built `.apkg` packages (`output/Semestre_Filtro_EdiSES_Complete.apkg` and `output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg`).
- **Why they were missing**: Every single one (`130 / 130`) is a `Resolution == "deduplicated"` duplicate in `origin/arena/dbe933e6-anki-sem:duplicates.csv` (`115 NCOM`, `15 COMP`, `2 COMM`: `CHIM-C06-COMM-020` & `CHIM-C10-COMM-004`).
- **Critical Trap Caught During Pre-Join (`97 / 130` option-letter permutations + pre-remediation OCR)**:
  - All `130` items are now extracted into `special_sets/missing_130_restored.jsonl` (and placed in their exact chapter/section chunks) with `restored_twin_ref` linking each item to its `KeptItemID` twin and its twin's explanation.
  - **HOWEVER**: (1) `6d93039e` was exported *before* `dbe933e6`'s 3 rounds of OCR/key remediation (so stems/options have raw OCR like `ma le cole`, `diluirst`, `dil mm`, and `CHIM-C09-NCOM-013` has `- 1` vs twin `+1`, `FIS-C05-NCOM-108` has `B` vs twin `E`), and (2) in **`97 / 130`** pairs EdiSES permuted the option order (`A..E`) relative to the twin! When finalizing any of the `130` items, verify the stem/options against the scan crop, verify the answer against `twin_answer_text`, and **remap or remove any option-letter references (`risposta C`)** before reusing `twin_explanation`.

### B. Who Answered Page 291 (`CHIM-C11-COMM-017..023`) & Do All Runs Agree?
Book page 291 omitted the printed `Risposta corretta` lines for `CHIM-C11-COMM-017..023` (`7` items). **Six independent sources across the repository answered all 7 items with unanimous `7 / 7` consensus** (and they are already populated in `currnet_no_images.apkg.md`):

| ItemID | Unanimous Key | Correct Option Text | Verified Across All 6 Independent Sources |
|---|:---:|---|---|
| `CHIM-C11-COMM-017` | **`C`** | `basica` (idrolisi basica di $\text{K}_2\text{CO}_3$) | `currnet_no_images`, `dbe933e6:stage2_answers.py`, `6d93039e`, `9d2e065b`, `0c0900a2`, `full-anki:take3+model2` |
| `CHIM-C11-COMM-018` | **`D`** | `acida` ($\text{NH}_4\text{Cl}$ da $\text{NH}_3$ debole + $\text{HCl}$ forte) | Unanimous 6/6 |
| `CHIM-C11-COMM-019` | **`C`** | `Cloruro di ammonio` ($\text{pH} < 7$ in acqua) | Unanimous 6/6 |
| `CHIM-C11-COMM-020` | **`A`** | `basica` ($\text{CH}_3\text{COONa}$, idrolisi acetato) | Unanimous 6/6 |
| `CHIM-C11-COMM-021` | **`E`** | `HCl e KCl` (acido forte + suo sale = **non** tampone; OCR `HC)`/`HCi`/`HC!`/`CH₃C00H` already cleaned in live deck) | Unanimous 6/6 |
| `CHIM-C11-COMM-022` | **`A`** | `basica` ($0{,}1\text{ M }\text{NH}_3 + 0{,}1\text{ M }\text{NH}_4\text{Cl}$, tampone ammoniacale $\text{pH}\approx 9{,}25$) | Unanimous 6/6 |
| `CHIM-C11-COMM-023` | **`B`** | `Il suo pH rimane pressoché invariato...` (definizione soluzione tampone) | Unanimous 6/6 |

Full records + explanations are in `special_sets/page_291_chim_c11_comm_17_23.jsonl`.

---

## 4. Complete Reference Registry of All Solved Issues Across Every Branch

Every chunk record in `chunks/<SUBJ>-C<nn>/chunk_*.jsonl` already embeds the per-item outputs from these sources, and you can inspect the original scripts via `git show <branch>:<path>` at any time:

1. **OCR, Chemical Subscripts/Superscripts, Answer-Key Overrides & Cloze Conversion (`origin/arena/dbe933e6-anki-sem`)**:
   - `extractor/stage2_answers.py`: `MISSING_BP291_CHIM_CAP11` (Page 291), `SCAN_VERIFIED_NCOM_ANSWERS`, multi-blank Cloze splits.
   - `extractor/audit_remediation.py`, `extractor/round2_remediation.py`, `extractor/round3_remediation.py`, `extractor/round3_extra_fixes.py`: 3 rounds of deterministic + scan-verified stem/option/formula fixes.
   - `extractor/scan_verified_overrides.py` & `extractor/visual_formula_overrides.py`: manual scan-verified chemical/physics equations and ion charges.
   - `issues.csv` (`1,764` logged issue fixes — embedded per item in `issues_fixed_log`) & `duplicates.csv` (`375` duplicate pairs — embedded in `dup_tags` and `restored_twin_ref`).
2. **Independent Audit Pipeline & Patch Scripts (`origin/import/full-anki-folder`)**:
   - `audit/scripts/07_cloze_convert.py`, `10_notation_audit.py`, `11_fix_notation.py`, `12_apply_patches.py`, `13_apply_reextract.py`, `FINAL_ARTIFACTS.md`.
3. **257 Missing/Corrupt Answer-Key Adjudications (`origin/arena/9d2e065b-anki-sem` & `origin/arena/0c0900a2-anki-sem`)**:
   - `9d2e065b:answer_key_output.jsonl` + `review.md` and `0c0900a2:answers.jsonl` (plus `import/full-anki-folder:workingdir/take3.answer_key_output.jsonl` & `model2_answers.jsonl`).
   - Merged in `special_sets/adjudicated_257_keys.jsonl`: **`249 / 257` agree**; **`8` items disagree** between `9d2e065b` and `0c0900a2` and require scan tie-break during chunk processing (`CHIM-C06-NCOM-088`, `CHIM-C11-NCOM-019`, `CHIM-C13-NCOM-104`, `BIO-C01-NCOM-216`, `BIO-C02-COMP-016`, `BIO-C04-COMM-014`, `BIO-C04-NCOM-204`, `FIS-C03-NCOM-185`).
4. **5,902 Uncommented Explanations & Defect Flags (`origin/arena/cc130265-anki-sem` & `origin/arena/0c53ca03-anki-sem`)**:
   - `cc130265` (`work/uncommented_questions_workpack/questions.db`): strict pass (`4,905 done`, `997 flagged` catching subtle OCR/key/ambiguous/figure issues).
   - `0c53ca03` (`work/questions.db`): broad pass (`5,464 done`, `438 flagged`).
   - Union already covers **`5,468 / 5,902` (`92.6%`)** uncommented items with ready Italian explanations; both `cc130265` and `0c53ca03` entries are embedded on every chunk item under `solved_work`!
5. **`CHIM-C01` 600-DPI Opus Pilot (`origin/opus-rebuild/semestre-filtro`)**:
   - `opus_attempt/work/deepseek/chim01/{adjudications,corrections}.jsonl` (`8` adjudications incl. `CHIM-C01-NCOM-091, -092`; `3` scan fixes `CHIM-C01-NCOM-070, -022, -081`) + `opus_attempt/exam_structure.md` (`21` MUR `ud::` tags) + `opus_attempt/templates/typed_answer.js` — embedded in `solved_work.opus_chim01`.

---

## 5. Directory Layout for Chunk-by-Chunk Processing

```text
work/opus_handoff/
├── README.md                                 # This architecture, compatibility & provenance guide
├── OPUS_PROMPT.md                            # Copy-paste chunk-by-chunk prompt for the next Opus run
├── GOALS.md                                  # Machine-verifiable gates for lossless currnet_no_images merge
├── build_handoff_chunks.py                   # Reproducible generator script
├── chunk_manifest.json                       # Ordered queue of all 196 chunks (<=45 items each, 7,078 total)
├── target_schema/
│   ├── ids_and_decks.json                    # Exact notetypes (1813027267 & 1481924269089), 17 fields, mod floor, 117 deck IDs
│   ├── guid_map_7078.json                    # Exact ItemID -> {guid, mid, did, deck_name, in_current_apkg, kept_twin_id}
│   └── current_templates/                    # Live HTML/CSS from currnet_no_images.apkg.md
│       ├── mcq_1813027267/{front,back,style}
│       └── cloze_1481924269089/{front,back,style}
├── special_sets/
│   ├── missing_130_restored.jsonl            # All 130 restored items + twin answers/explanations
│   ├── page_291_chim_c11_comm_17_23.jsonl    # All 7 Page-291 items (unanimous 6-source verified)
│   ├── adjudicated_257_keys.jsonl            # All 257 answer-key adjudications (249 unanimous + 8 tie-breaks)
│   └── items_needing_scan_or_key_check.jsonl # All 1,140 items with any flag/restore/residual defect
└── chunks/
    ├── CHIM-C01/chunk_001_CHIM-C01_COMM_001-035.jsonl
    ├── ...                                   # 196 files across 28 chapters, <=45 items (~85 KB) per file!
    └── FIS-C08/chunk_196_FIS-C08_COMP_001-027.jsonl
```
