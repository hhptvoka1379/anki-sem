# Semestre Filtro — Verified & Deduplicated QA Dataset & Multi-Theme Anki Deck (`6,948` Unique Cards)

Deterministic computer-vision extraction, scan-verified scientific & OCR remediation, intra- and cross-subject deduplication, and multi-theme Anki `.apkg` packaging pipeline for **`Eserciziario Unico per il Semestre Filtro`** (*Chimica e Propedeutica Biochimica, Biologia e Genetica, Fisica* — 902 PDF pages).

---

## Key Outputs (`output/` & Root Audit Tables)

| Artifact | Description | Verified Metric |
|---|---|---|
| `output/Semestre_Filtro_Complete.apkg` | Master all-in-one Anki package across **84 hierarchical subdecks** (`Semestre Filtro::Materia::Capitolo::Tipo`) with **live in-card `00`–`10` corner theme switcher** across all 11 visual modes + all cleaned scans & diagrams | **`6,948` notes / `6,948` cards (`84` subdecks, `11` live switchable themes)** |
| `output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg` | Dedicated standalone **Neo-Brutalist Risoprint Zine** `6,948`-card Anki deck (`RISO.ZINE // REG.04`, independent Note-Type & Deck IDs so it never collides with `Complete.apkg`, without theme-switcher UI) | **`6,948` notes / `6,948` cards** |
| `output/themes/ThemeUpdater_01..10.apkg` & `output/themes/css/*.css` | Instant ~15 KB Anki Note-Type Theme Updaters + standalone CSS stylesheets across all **10 art-directed design systems** + interactive `output/themes/index.html` preview gallery | **`10 / 10` themes & updaters verified** |
| `output/figures/*.png` | Losslessly de-watermarked inline diagrams (graphs, circuits, pedigrees, cell stages, chemical structures, vectors, tables — `100%` of explicit visual stems populated in `FigureHTML`) | **`113` crisp diagrams (`0` missing `FigureHTML`, `0` orphan/dark PNGs)** |
| `output/qa_dataset.json` | Full structured UTF-8 JSON dataset with chapter metadata, exact restored `answer_book_page` (`252..901`), options, answers, explanations, and remediation/deduplication summary | **`6,948` unique items (`130` exact duplicates removed from `7,078` source items)** |
| `output/qa_dataset.jsonl` | Complete UTF-8 JSON Lines dataset (`1` JSON object per verified unique QA pair, `100.0%` 1-to-1 `question_images/<ID>.png` bijection) | **`6,948` rows** |
| `output/qa_dataset.csv` | Flat UTF-8 CSV table for spreadsheet / `pandas` inspection | **`6,948` records (`6,949` lines incl. header)** |
| `output/verification_report.json` | Automated structural, text, formula, deduplication, provenance page, HTML-entity, branding, multi-theme switcher, standalone Risoprint isolation, and pixel-level verification report | **`24 / 24` checks `PASS`** |
| `issues.csv` & `duplicates.csv` | Unified ground-truth audit log documenting every remediated text/key/image finding plus every deduplicated pair vs. retained distinct shared-stem question | **`100%` scan-verified & remediated** |

---

## Exact Breakdown by Subject & Quiz Type (`6,948` Unique Cards)

| Subject (`subject_code`) | Chapters | `Quiz commentati` | `Quiz non commentati` | `Quiz a completamento` | **Unique Cards** *(Source before dedup)* |
|---|---:|---:|---:|---:|---:|
| **Chimica e Propedeutica Biochimica (`CHIM`)** | 13 | 327 | 1,490 | 579 | **`2,396`** *(2,469; −73 redundant copies)* |
| **Biologia (`BIO`)** | 7 | 494 | 1,535 | 842 | **`2,871`** *(2,914; −43 redundant copies)* |
| **Fisica (`FIS`)** | 8 | 220 | 827 | 634 | **`1,681`** *(1,695; −14 redundant copies)* |
| **Grand Total** | **28 (`84` subdecks)** | **`1,041`** | **`3,852`** | **`2,055`** | **`6,948`** *(7,078; −130 redundant copies)* |

> **Deduplication priority guarantee:** Across all `130` intra-subject and cross-subject duplicate pairs removed (`CHIM`, `BIO`, and `FIS`), **100% (`1,041 / 1,041`)** of unique step-by-step `Quiz commentati` explanations are retained (`commentati > non_commentati > completamento`), while genuinely distinct questions sharing short stems (e.g., *"Il fruttosio è:"*, *"La cromatina è:"*, *"I mitocondri sono:"*, *"L'apparato del Golgi:"*) are preserved intact.

---

## Architecture (`extractor/`)

1. **`stage1_canonicalize.py` — Canonical Page De-duplication & Vector Span Extraction**
   - Reconstructs `894` unannotated canonical book pages (`bp_003`–`bp_901`) from raw PDF XObjects, strips annotations/watermarks/headers, resolves split pages and 8 two-page spreads, fixes swapped pages `666 <-> 667`, and extracts native vector typography on PDF p. `669`.
2. **`ocr_cache.py` & `stage2_answers.py` — Multi-Engine Answer-Key & Commentary Extraction**
   - Extracts all `84` `Risposte` subsections (`7,078` source items) and reconstructs missing source PDF page `291` (`CHIM-C11-COMM-017..023`).
3. **`stage3_questions.py`, `quality_refiner.py` & `visual_formula_overrides.py` — Question Alignment, Scientific Lexicon & Diagram Extraction**
   - Aligns every subsection monotonically, crops genuine inline diagrams cleanly into `output/figures/`, and applies visual formula transcriptions.
4. **`audit_remediation.py`, `scan_verified_overrides.py` & `round2_remediation.py` — Scan-Verified Remediation & Deduplication Engine**
   - Fixes all verified answer-key errors, chemical structural formulas (`-CH₂-`, `-CHO`, `-COOH`, `-OH`, `K₂Cr₂O₇`, `KMnO₄`, `CH₃CH₂OCH₂CH₃`), Greek biological notation (`α`/`β`/`γ`/`σ`, `ΔG`), physics units/exponents, OCR word splits/merges (`ossidrile`, `Usa la circolazione sanguigna`, `a temperatura costante`, `Il logaritmo`, `La concentrazione`, `ossidrilionica`), mid-card running headers in PNG scans, publisher watermarks/branding, and `130` exact intra- & cross-subject duplicate cards (`7,078 -> 6,948`).
5. **`stage4_export.py`, `anki_themes.py` & `verify.py` — Multi-Theme Anki Packaging & Automated Verification**
   - Exports `qa_dataset.{json,jsonl,csv}`, `Semestre_Filtro_Complete.apkg`, all `10` Anki themes (`Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg` + `ThemeUpdater_01..10.apkg`), and enforces **all 22 automated verification gates**.

---

## Quick Install, Theme Packaging & Safe Repo Cleanup (`git clone` -> Import -> Delete Repo)

Every `.apkg` package is **100% self-contained** (all `6,948` cards, stylesheets, `DARK`/`LIGHT` toggle scripts, and all `8,127` embedded diagrams & page scans are copied directly into Anki's internal `collection.media` folder on import). Once imported into Anki, **you can safely delete the cloned repository folder completely**:

```bash
git clone <repo-url> anki-sem
cd anki-sem

# Optional: generate standalone full 6,948-card .apkg files for ALL 10 design systems
# (100% pure Python 3 standard library — works with built-in macOS/Linux/Windows python3, NO pip install needed!):
python3 output/themes/build_theme_apkg.py all

# Now double-click whichever .apkg file(s) you want in Finder / File Explorer to import into Anki:
#   - output/Semestre_Filtro_Complete.apkg                          (All-in-one: 00–10 top-right switcher + top-left DARK/LIGHT toggle)
#   - output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg  (Standalone #04 Risoprint + top-left DARK/LIGHT toggle)
#   - output/themes/Semestre_Filtro_01_...apkg .. 10_...apkg        (Any other standalone theme built above)
#
# Tip if updating an already-imported Note Type in Anki:
#   Either enable "Update note types" in Anki's Import dialog, delete the old deck first,
#   OR paste front.html / back.html / style.css directly from output/themes/templates/<theme>/ into Anki -> Browse -> Cards...

cd ..
rm -rf anki-sem
```

---

## Running Full Rebuild & Automated Verification (`25 / 25` Gates)

```bash
# Rebuild dataset files, master .apkg, themed .apkg, 12 template bundles, 10 theme updaters, and audit CSVs:
python3 rebuild_all.py

# Run all 25 automated structural, scientific, deduplication, branding, template-tag, and pixel-level verification gates:
python3 -m extractor.verify
```
