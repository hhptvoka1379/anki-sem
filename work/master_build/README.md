# Semestre Filtro — Master 7,078-Item Anki Deck (`Semestre_Filtro_Master_7078.apkg`)

**Deliverable**: `work/master_build/Semestre_Filtro_Master_7078.apkg` (`2.81 MB`, Anki v3 `collection.anki21b` schema `18` + `141` collision-free delta media files)

Built and end-to-end verified against `/tmp/arena-coding-uploads/currnet_no_images.apkg.md` using the **official Anki Rust/Python engine (`anki.collection.Collection.import_anki_package`)** under Anki's default double-click import settings (`update_notes=IF_NEWER`, `update_notetypes=IF_NEWER`, `merge_notetypes=False`, `with_scheduling=False`).

---

## 1. Real-Anki Merge Verification Summary

| Check | Result |
|---|---|
| Pre-merge user collection (`currnet_no_images.apkg.md`) | `6,948` notes / `6,952` cards |
| `ImportLog.updated` (in-place live GUID updates, user scheduling preserved) | **`6,948 / 6,948`** |
| `ImportLog.new` (restored book duplicates under distinct `ItemID`s & GUIDs) | **`130 / 130`** |
| `ImportLog.duplicate` / `conflicting` / `missing_notetype` / `missing_deck` | **`0 / 0 / 0 / 0`** |
| Post-merge user collection | **`7,078` notes / `7,082` cards** (`5,008` MCQ + `2,074` Cloze across `2,070` Cloze notes) |
| Cards with non-empty Italian `ExplanationHTML` | **`7,078 / 7,078` (`100.00%`)** |
| Cards with official MUR 2026 `ud::<slug>` tag | **`7,078 / 7,078` (`21 / 21` Unità Didattiche populated)** |
| Delta media files bundled (collision-free with existing `collection.media`) | **`141` files** (`130` `restored_<id>.png` + `5` `restored_fig_<id>_1.png` + `2` `restored_sol_<id>_1.png` + `4` offline `_*.ttf` fonts) |

### One-Click Import Instructions
1. Open Anki Desktop (23.10+ / 24.x / 25.x), AnkiMobile, or AnkiDroid where your current `Semestre Filtro` collection is loaded.
2. Import **`Semestre_Filtro_Master_7078.apkg`** with Anki's default settings (*Update existing notes: If newer*, *Update note types: If newer*, *Import learning progress: Off*).
3. All `6,948` existing notes and both notetypes (`1813027267` MCQ and `1481924269089` Cloze) update in place **without touching your review intervals, ease factors, or existing ~8,127 scan/figure PNGs**, while adding all `130` restored items + their `137` collision-free `restored_*.png` images + `4` offline Risoprint Zine fonts (`_SpaceGrotesk-Variable.ttf`, `_SpaceMono-Regular.ttf`, `_SpaceMono-Bold.ttf`, `_Syne-Variable.ttf`).

---

## 2. Exact Reconciliation of Explanation Counts (`7,078 / 7,078`)

| Subset | Count | Source in Master Deck |
|---|---:|---|
| Live `COMM` (`Quiz commentati`) already explained in `currnet_no_images` | `1,040` | Preserved + OCR cleaned (including all `7` Page-291 items `CHIM-C11-COMM-017..023`) |
| Live `COMM` with corrupted Bernoulli explanation (`FIS-C04-COMM-007`) | `1` | Replaced with clean continuity + Bernoulli derivation (`explanations_fis_127.py`) |
| Live `NCOM + COMP` already pre-populated in `currnet_no_images` | `5` | Verified / upgraded |
| Live `NCOM + COMP` explained by `cc130265` (`status = done`, strict pass) | `4,905` | `4,776` (`cc130265` ∩ `0c53ca03`) + `129` (`cc130265` done, `0c53ca03` flagged) |
| Live `NCOM + COMP` flagged by `cc130265` for OCR/ambiguity, explained by `0c53ca03` | `563` | OCR/formula glitches cleaned (`clean_563_and_ud_tags.py`) + `0c53ca03` explanations |
| Live `NCOM + COMP` flagged empty by **both** runs (`189 CHIM + 118 BIO + 127 FIS`) | `434` | **100% bespoke scan-verified explanations + `.note-box` caveats** (`explanations_{chim_189,bio_118,fis_127}.py`) |
| Restored `130` previously deduplicated items (`113 NCOM + 15 COMP + 2 COMM`) | `130` | **100% OCR-cleaned & option-letter-remapped explanations** (`patches_130_restored.py`) |
| **Total** | **`7,078`** | **`7,078 / 7,078` (`100.00%`)** |

*(Note: `1,040 + 1 = 1,041` `COMM`; `4,905 + 563 + 434 = 5,902` `NCOM+COMP` in `uncommented_questions_workpack`, where `5` overlapped pre-filled live notes so `1,041 + 5 + 5,902 = 6,948` live notes; `+ 130` restored = `7,078` total notes.)*

---

## 3. All 8 Tie-Break Verdicts (Live `6,948`-ID Space)

| # | Live `ItemID` | Disputed Keys (`9d2e065b` vs `0c0900a2`) | Final Key | Scientific & Book-Scan Proof |
|---:|---|:---:|:---:|---|
| 1 | `CHIM-C06-NCOM-088` | `E` vs `C` | **`E`** | Osmotic pressure symbol $\pi$ (`Π`) is absent from A–D (`P`, `i`, `R`, `M`); EdiSES `bp_275 = E` (`Nessuna delle risposte è corretta`). |
| 2 | `CHIM-C11-NCOM-019` | `B` vs `A` | **`B`** | Asks for **base secondo Lewis**; C/D/E define Lewis acid and A (`sapore amaro`) is organoleptic, not Lewis's electron-pair donor definition (`bp_293 = B`). |
| 3 | `CHIM-C13-NCOM-104` | `C` vs `E` | **`C`** | Covalent bonds defining primary structure per EdiSES `bp_305` & IUPAC/Sanger = peptide (`B`) + disulfide (`D`) → `C: B e D` (Lehninger strict `E: solo di tipo B` noted in `.note-box`). |
| 4 | `BIO-C01-NCOM-216` | `B (2)` vs `D (6)` | **`A` (`8`)** | From free phosphate, deoxyribose, and bases: $3\times(1\text{ glycosidic}+1\text{ phosphoester}) + 2\text{ phosphodiester} = 8$ condensations (EdiSES `bp_605 = D (6)` erratum documented in `.note-box`). |
| 5 | `BIO-C02-COMP-016` | `metafasici` vs `interfasici` | **`interfasici`** | Chromosome territories are discrete nuclear domains occupied by decondensed **interphase** chromosomes (`bp_610 = interfasici`; leading `I ` restored). |
| 6 | `BIO-C04-COMM-014` | `A` vs `B` | **`A`** | Hairless ($Hh$, with $HH$ lethal) $\times$ hairless ($Hh$) yields $2/3$ (`66.7%`) live hairless pups vs $1/2$ (`50%`) in $Hh \times hh$ (`B`). |
| 7 | `BIO-C04-NCOM-204` | `C` vs `E` | **`C`** | Deleting $G_7$ in `5'-CUGAUCGUAAUGCGC-3'` shifts reading frame to `CUG-AUC-UAA-UGC-GC`, creating an immediate **`UAA` stop codon** right after `Ile` (EdiSES `bp_634 = E` erratum documented in `.note-box`). |
| 8 | `FIS-C03-NCOM-185` | `C` vs `flag` | **`C`** | Lever moment balance $R\cdot X_R = P\cdot X_P \Rightarrow G = R/P = X_P/X_R$ (`G = Xp/ Xp` OCR typo on option A cleaned; scan verified). |

---

## 4. Reproducible Build Pipeline (`work/master_build/`)

```bash
work/.venv/bin/python3 work/master_build/build_master_apkg.py
work/.venv/bin/python3 work/master_build/verify_master_apkg.py
```
