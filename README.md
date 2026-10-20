# Semestre Filtro — EdiSES Complete Verified QA Dataset & Anki Deck (`7,078` Cards)

Deterministic computer-vision, dual-scale OCR consensus, scientific-lexicon refinement, and Anki `.apkg` generation pipeline for **`Eserciziario Unico per il Semestre Filtro`** (*Chimica e Propedeutica Biochimica, Biologia, Fisica* — EdiSES, 902 PDF pages).

---

## Key Outputs (`output/`)

| Artifact | Description | Verified Metric |
|---|---|---|
| `output/Semestre_Filtro_EdiSES_Complete.apkg` | Styled light/dark-mode Anki package across **84 hierarchical subdecks** (`Materia::Capitolo::Tipo`) embedding **all `7,078` full question scans + `118` inline diagrams + `1,068` commentary scans** | **`7,078` notes / `7,078` cards (`32.64 MB`, `8,264` verified white-paper PNGs)** |
| `output/question_images/*.png` | Complete **1-to-1 full stitched question scan PNGs** (`CHIM-C01-COMM-001.png` .. `FIS-C08-COMP-054.png`, footer-cleaned & 2-bit explicit-palette encoded) | **`7,078 / 7,078` question PNGs (`100.0%` 1-to-1 bijection, `25.17 MB`)** |
| `output/figures/*.png` | Surgically whitespace-cropped genuine inline diagrams (graphs, circuits, pedigrees, cell stages, chemical structures, vectors, tables — `100%` of explicit visual stems covered) | **`118` pure diagrams (`0.28 MB`, `0` orphan or dark files)** |
| `output/qa_dataset.jsonl` | Complete UTF-8 JSON Lines dataset (`1` JSON object per verified QA pair, each paired via `"question_image": "question_images/<ID>.png"`) | **`7,078` rows (`100.0%` 1-to-1 image + QA pair bijection)** |
| `output/qa_dataset.json` | Structured full dataset with subject, chapter, and quiz-type metadata | **`7,078` items across `84` subsections** |
| `output/qa_dataset.csv` | Flat UTF-8 CSV table for spreadsheet / `pandas` analysis | **`7,078` records** |
| `output/verification_report.json` | Automated structural, text, formula, 1-to-1 image bijection, and pixel-level audit report | **`17 / 17` checks `PASS`** |

---

## Exact Breakdown by Subject & Quiz Type

| Subject (`subject_code`) | Chapters | `Quiz commentati` | `Quiz non commentati` | `Quiz a completamento` | **Total QA Pairs** |
|---|---:|---:|---:|---:|---:|
| **Chimica e Propedeutica Biochimica (`CHIM`)** | 13 | 329 | 1,547 | 593 | **2,469** |
| **Biologia (`BIO`)** | 7 | 494 | 1,577 | 843 | **2,914** |
| **Fisica (`FIS`)** | 8 | 220 | 841 | 634 | **1,695** |
| **Grand Total** | **28 (`84` subdecks)** | **1,043** | **3,965** | **2,070** | **7,078** |

---

## 5-Stage Pipeline Architecture (`extractor/`)

1. **`stage1_canonicalize.py` — Canonical Page De-duplication & Vector Span Extraction**
   - Resolves split single-page renders (`PDF pp. 5–60`), normalizes rotated spreads (`90°`/`270°`), splits true two-page spreads (`PDF pp. 62–901`) along gutter minima into `894` canonical 300-DPI pages (`bp_003`–`bp_901`), and extracts native vector glyphs + superscripts/subscripts on PDF page `669`.
2. **`ocr_cache.py` & `stage2_answers.py` — Dual-Scale Answer-Key & Commentary Extraction**
   - Upscales answer and MCQ zones bicubically (`2.0×`) with float32 LSTM `tessdata_best` (`ita+ell+eng`) while processing `completamento` prose at native `1.0×` scale so faint dotted rules never trigger false text lines (`0` missing blanks across all `2,070` fill-in-the-blank items; `100.000%` answer agreement across all `7,078` keys).
3. **`stage3_questions.py` — Global Monotonic DP Aligner**
   - Aligns every chapter's question stream to its exact ground-truth cardinality `(N_comm, N_non_comm, N_compl)` across column and page boundaries, strips running headers/footers/watermarks, and recovers inline option markers (`A..E`).
4. **`quality_refiner.py` & `visual_formula_overrides.py` — Dual-Scale Consensus, Lexicon & Surgical Diagram Cropper**
   - **Dual-Scale Token Consensus & Italian Scientific Lexicon:** Aligns `1.0×` and `2.0×` OCR streams token-by-token using `wordfreq('it')`, resolves `100%` of line-break hyphenations (`274 -> 0`), splits fused OCR tokens via dynamic programming while protecting scientific compounds/proteins, restores subscripted decimal commas (`112 -> 0`), and normalizes units (`g·mol⁻¹`, `g·eq⁻¹`, `Ω`, `μF`, `μg`, `dm³`, `10⁻ⁿ`).
   - **Visual Formula Verification:** Incorporates `166` directly verified textbook transcriptions for 2D stacked fractions (`Q/(4πε₀r²)`, series/parallel resistor networks), nuclear isotopes (`²³⁸₉₂U`, `⁵⁷₂₇Co..⁶⁰₂₇Co`), orbital configurations (`1s² 2s² 2p⁶...`), and inline printed options, and documents all `7` verbatim EdiSES printed duplicate-option typos by exact page number.
   - **Surgical Diagram Filtering & Band-Cropping:** Masks recognized text bounding boxes, removes solid black `EdiSES` footer bars and margin tabs, prunes `89%` false-positive plain-text crops (`915 -> 100` pure diagrams), and snaps vertical diagram crops strictly into pure-white inter-line gaps so zero half-sliced prose lines ever appear above or below a diagram.
5. **`stage4_export.py` & `verify.py` — Contrast-Safe Grayscale PNG Export & 16-Gate Verification Suite**
   - Exports contrast-anchored 8-bit grayscale PNGs (avoiding Pillow `Palette.ADAPTIVE` bilevel palette corruption so `0 / 1,168` embedded media images render dark or blank) and enforces **16 automated structural + content quality assertions**.

---

## Running Verification or Full Rebuild

```bash
# Run all 16 structural, prose, formula, and pixel-level .apkg verification checks:
.venv/bin/python -m extractor.verify

# Run end-to-end extraction, quality refinement, Anki .apkg export, and 16-gate verification:
.venv/bin/python extract_all.py
```
