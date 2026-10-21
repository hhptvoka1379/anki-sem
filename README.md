# Semestre Filtro — Unified Verified QA Dataset & Anki Deck (`7,078` Cards)

Deterministic computer-vision extraction, dual-audit scientific & OCR remediation, and multi-theme Anki `.apkg` packaging pipeline for **`Eserciziario Unico per il Semestre Filtro`** (*Chimica e Propedeutica Biochimica, Biologia e Genetica, Fisica* — 902 PDF pages).

---

## Key Outputs (`output/` & Root Audit Tables)

| Artifact | Description | Verified Metric |
|---|---|---|
| `output/Semestre_Filtro_EdiSES_Complete.apkg` | Master light/dark-mode Anki package across **84 hierarchical subdecks** (`Materia::Capitolo::Tipo`) embedding **all `7,078` cleaned question scans + `118` lossless de-watermarked diagrams + `1,068` commentary scans** | **`7,078` notes / `7,078` cards (`33.18 MB`, `8,264` verified white-paper PNGs)** |
| `output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg` | Complete standalone themed `7,078`-card Anki deck with unified CSS/JS option & badge selectors (`RISO.ZINE // REG.04`) | **`7,078` notes / `7,078` cards (`33.18 MB`, `8,264` PNGs)** |
| `output/themes/ThemeUpdater_01..10.apkg` & `output/themes/css/*.css` | Instant ~15 KB Anki Note-Type Theme Updaters + standalone CSS stylesheets across all **10 art-directed design systems** + interactive `output/themes/index.html` preview gallery | **`10 / 10` themes & updaters verified** |
| `output/figures/*.png` | Losslessly de-watermarked genuine inline diagrams (graphs, circuits, pedigrees, cell stages, chemical structures, vectors, tables — `100%` of explicit visual stems populated in `FigureHTML`) | **`118` crisp diagrams (`0` missing `FigureHTML`, `0` orphan/dark PNGs)** |
| `output/qa_dataset.json` | Full structured UTF-8 JSON dataset with chapter metadata, exact restored `answer_book_page` (`252..901`), options, answers, explanations, and remediation summary | **`7,078` items across `84` subsections** |
| `output/qa_dataset.jsonl` | Complete UTF-8 JSON Lines dataset (`1` JSON object per verified QA pair, `100.0%` 1-to-1 `question_images/<ID>.png` bijection) | **`7,078` rows** |
| `output/qa_dataset.csv` | Flat UTF-8 CSV table for spreadsheet / `pandas` inspection | **`7,078` records (`7,079` lines incl. header)** |
| `output/verification_report.json` | Automated structural, text, formula, duplicate-option, provenance page, HTML-entity, watermark, and pixel-level verification report | **`21 / 21` checks `PASS`** |
| `issues.csv` & `duplicates.csv` | Unified, ground-truth-verified audit log merging both independent deck audits (`866` remediated item/field findings across `699` cards + `7,071` restored `answer_book_page` records; `344` cataloged duplicate pairs with all conflicts resolved) | **`100%` verified & remediated** |

---

## Exact Breakdown by Subject & Quiz Type

| Subject (`subject_code`) | Chapters | `Quiz commentati` | `Quiz non commentati` | `Quiz a completamento` | **Total QA Pairs** |
|---|---:|---:|---:|---:|---:|
| **Chimica e Propedeutica Biochimica (`CHIM`)** | 13 | 329 | 1,547 | 593 | **2,469** |
| **Biologia (`BIO`)** | 7 | 494 | 1,577 | 843 | **2,914** |
| **Fisica (`FIS`)** | 8 | 220 | 841 | 634 | **1,695** |
| **Grand Total** | **28 (`84` subdecks)** | **1,043** | **3,965** | **2,070** | **7,078** |

---

## Architecture (`extractor/`)

1. **`stage1_canonicalize.py` — Canonical Page De-duplication & Vector Span Extraction**
   - Reconstructs `894` unannotated canonical book pages (`bp_003`–`bp_901`) from raw PDF XObjects, strips annotations/watermarks/headers, resolves split pages and 8 two-page spreads, fixes swapped pages `666 <-> 667`, and extracts native vector typography on PDF p. `669`.
2. **`ocr_cache.py` & `stage2_answers.py` — Multi-Engine Answer-Key & Commentary Extraction**
   - Extracts all `84` `Risposte` subsections (`1,043` `commentati`, `3,965` `non_commentati`, `2,070` `completamento`) and reconstructs missing source PDF page `291` (`CHIM-C11-COMM-017..023`).
3. **`stage3_questions.py`, `quality_refiner.py` & `visual_formula_overrides.py` — Question Alignment, Scientific Lexicon & Diagram Extraction**
   - Aligns every subsection monotonically, crops `118` genuine inline diagrams cleanly into `output/figures/`, and applies visual formula transcriptions.
4. **`audit_remediation.py` — Unified Dual-Audit Remediation Engine**
   - Fixes all verified answer-key errors (`CHIM-C09-COMM-001`, `CHIM-C12-NCOM-289`, `CHIM-C07-NCOM-010`, `FIS-C06-NCOM-133`, `FIS-C06-NCOM-150`, plus `35` `completamento` answers), splits wrapped stems out of Option A (`CHIM-C07-COMM-008`, `CHIM-C07-NCOM-005`, `CHIM-C09-NCOM-058`, `CHIM-C12-NCOM-195`, `CHIM-C11-NCOM-036`, `FIS-C06-NCOM-123`), deduplicates all `8` duplicate-option MCQs (`0 / 5,008` remaining), replaces shifted/wrong/missing explanations, restores `μF`/`μC` vs true `pF`/`pC` capacitance/charge units from original scans, repairs chemical subscripts and physics exponents, removes leaked headers/watermarks, and restores exact printed `answer_book_page` (`252..901`) across all `84` subsections.
5. **`stage4_export.py`, `anki_themes.py` & `verify.py` — Multi-Theme Anki Packaging & 21-Gate Verification**
   - Exports `qa_dataset.{json,jsonl,csv}`, `Semestre_Filtro_EdiSES_Complete.apkg`, all `10` Anki themes (`Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg` + `ThemeUpdater_01..10.apkg`), and enforces **21 automated structural, scientific, provenance, HTML, CSS/JS, and pixel-level verification gates**.

---

## Running Verification & Theme Packaging

```bash
# Run all 21 structural, content, provenance, CSS/JS, and pixel-level verification gates:
python3 -m extractor.verify

# Repackage the master .apkg into any of the 10 standalone themed .apkg decks:
python3 output/themes/build_theme_apkg.py 04
```
