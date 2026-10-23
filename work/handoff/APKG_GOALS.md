# GOALS — merge-safe explanations `.apkg` for the live "Semestre Filtro" deck

Every goal has a hard pass criterion that `verify_apkg.py` checks mechanically. "Expected" numbers come from repo evidence (`manifest.json`, `FINAL_ARTIFACTS.md`, `0c53ca03:work/questions.db`). If the user's export disagrees, **stop, report the delta, and ask**. Do not "fix" toward the expected number.

## G0 — Recon done and recorded
- [ ] All remote branches fetched. `work/handoff/out/recon.md` lists every branch, its tip SHA, the file-set diff vs. the others (by blob hash), and which files were read and why.
- [ ] Confirmed (or refuted, with evidence): the workpack zip is blob-identical on `main`, `0c53ca03`, `cc130265` and `d5111e50`; `validate.py`, `PROMPT.md`, `questions.csv` and `reference_hashes.json` are identical across the three explanation runs.

## G1 — Input snapshot is the live state
- [ ] `work/input/<export>` exists. Its sha256 is recorded, and it is only ever opened as a **copy** (`work/scratch/`).
- [ ] Schema read with the `unicase` collation registered. Recorded: notetype ids, names, field names in order, template names/count, notetype `mtime`, `kind` (0 basic / 1 cloze).
- [ ] Expected: 6,948 Semestre notes = 4,893 on basic `1813027267` + 2,055 on cloze `1481924269089`. Cards: 6,952. Field 0 `ItemID` unique and non-empty on all notes.
- [ ] **Precondition gate:** all 2,054 workpack `COMP` ids resolve to notes on a **cloze** notetype (`kind = 1`). If any is still basic, STOP. An `.apkg` cannot convert basic→cloze (importer: `NotetypeKindMergeConflict` or *conflicting* skip). Report to the user that the cloze conversion must first be applied by replacing the collection with the cloze `.colpkg`, and wait.

## G2 — Identity mapping is total and 1:1
- [ ] Every one of the 5,902 workpack ids maps to exactly one note via `ItemID`: 3,848 `NCOM` → basic, 2,054 `COMP` → cloze. Unmapped = 0, ambiguous = 0.
- [ ] The 6,948 − 5,902 = **1,046** notes outside the workpack (expected: 1,045 MCQ commentati/examples + 1 cloze) all already have a non-empty `ExplanationHTML`. List any exception in `report.md`.
- [ ] Workpack seal: for every id, `reference_hashes.json` matches the hash recomputed **from the live note** (stem, options, answer). Mismatch means the card changed after the workpack was made, so the reason is not applied: the note gets tag `sf::review::card-changed`.

## G3 — Every question has exactly one paired answer (all 6,948 notes, not just the workpack)
MCQ (basic):
- [ ] Options A–E: all 5 present, non-empty, pairwise distinct after whitespace normalisation. Known book duplicates (`CHIM-C01-NCOM-010`, `-069`, `CHIM-C10-NCOM-038`, `CHIM-C12-NCOM-157`, `BIO-C03-NCOM-216`, `FIS-C01-COMM-016`) are listed, not altered.
- [ ] Banner letter ∈ A–E. The banner text equals the keyed option text. `BackOptionsHTML` has **exactly one** `opt correct`, on the keyed letter. `FrontOptionsHTML` contains **no** `correct` marker (no answer leak).
- [ ] Workpack `answer` == the live banner letter for all 3,848 NCOM. Workpack `answer_text` == keyed option text, except the 4 known mismatches (`CHIM-C05-NCOM-042`, `CHIM-C09-NCOM-121`, `CHIM-C10-NCOM-080`, `FIS-C01-NCOM-001`), which are explained individually.
- [ ] **Allowed auto-repair (log each):** the 21 notes that lost the `opt correct` marker (list in `FINAL_ARTIFACTS.md` → "Known residual defects") get it restored on the banner's letter, only when the banner letter is unambiguous. No other key, option or banner edits.

Cloze:
- [ ] Every cloze note has ≥ 1 `{{cN::…}}`. The ordinals are contiguous from 1. No empty answers, no `::` or `}}` inside an answer, no leftover `blank-slot` span. Card count per note = distinct ordinals (expected: 2,051 × 1 + 4 × 2 → 2,059 cards; the 4 two-blank notes are `BIO-C01-COMP-008`, `BIO-C01-COMP-114`, `BIO-C04-COMP-017`, `BIO-C06-COMP-030`).
- [ ] For each COMP id, the cloze answer(s) == workpack `answer_text` (NFC, whitespace-normalised). Replacing each `{{cN::x}}` with `x` yields the workpack `back_stem`.
- [ ] Each cloze renders through the `anki` lib: front shows `[...]` + the typed-answer box, back shows the answer + `ExplanationHTML`. Check this for all 2,055 notes, not a sample.

Output: `pairing_report.csv` (one row per note: id, type, check, status, detail). Gate passes when 0 FAIL rows are unexplained.

## G4 — Reason source and accuracy
- [ ] Primary source: `0c53ca03:work/questions.db`. `python3 validate.py` there must exit 0 (no `--allow-pending`) before you use it. Use `status='done'` rows only.
- [ ] Disagreement audit: the **563** ids that are `done` on `0c53ca03` but `flagged` on `cc130265`. Re-solve each from the card alone, then compare with the reason. On any factual or OCR doubt, downgrade to flagged (`sf::flag::<prefix>`, no explanation). Record the outcome per id.
- [ ] Optional uplift: the **123** ids flagged on `0c53ca03` but `done` on `cc130265`/`d5111e50`. Ship a borrowed reason only after an independent re-solve agrees with it and with the book key, and it passes the workpack validator rules (80–600 chars, plain text, no duplicates > 2 casefold). Otherwise keep the flag.
- [ ] Spot check: 5 random applied reasons per 100 (seeded, seed recorded), re-verified against the rendered card. 0 defects is required; any defect expands the audit to that whole chapter.
- [ ] The 6 `CHEM_JUDGEMENT.md` ids remain flagged with no explanation.

## G5 — Key disputes surfaced, never applied
- [ ] `key_disputes.md` lists every id where any source contradicts the book key. That covers the 25 `key: suspect` flags plus the letter disagreements from `0c0900a2`/`9d2e065b` (expected among them: `CHIM-C06-NCOM-088`, `CHIM-C11-NCOM-019`, `CHIM-C11-NCOM-170`, `CHIM-C13-NCOM-104`, `BIO-C01-NCOM-216`, `BIO-C03-NCOM-189`, `BIO-C04-NCOM-204`, `FIS-C03-NCOM-011`, `FIS-C03-NCOM-185`). Each row: book key, proposed key, sources, one-line reasoning, recommended action.
- [ ] 0 keys changed in the package. Disputed notes get tag `sf::review::key-dispute`.

## G6 — Package content is minimal and identity-exact
- [ ] Built by: copy export → edit with the `anki` lib (`col.update_notes`, which bumps `mtime`) → Anki's own `.apkg` exporter limited to the changed note ids, scheduling OFF, media OFF (or only referenced files that are byte-identical to the live ones).
- [ ] Inside the package: notetype ids ⊆ {`1813027267`, `1481924269089`}. Field names/order, template count/names and `kind` are byte-equal to the live ones, and so is the notetype `mtime`, so templates are not touched. Note count = changed-note count. Every GUID ∈ live GUID set (0 foreign GUIDs). Every note `mtime` > its live `mtime`.
- [ ] Changed fields limited to `ExplanationHTML`, tags, and the logged G3 marker repairs. For every other field, a diff against live shows 0 changes.
- [ ] Tags added: `sf::explanation::generated` (applied reasons), `sf::flag::{ocr,chem,ambiguous,key-suspect,missing}`, `sf::review::{key-dispute,card-changed}`. Existing tags preserved.
- [ ] Zip opens, CRCs OK, `integrity_check` = ok. Recorded: size, sha256, and the format (legacy vs `anki21b`; prefer what passes G7 on the oldest target client).

## G7 — Proven by a real import (the decisive gate)
- [ ] Into a **fresh scratch copy** of the user's export, import the package with the `anki` lib using the exact user settings (merge notetypes OFF, update notes IF_NEWER, update notetypes NEVER, no scheduling).
- [ ] ImportLog: `updated` = changed-note count. `new` = 0, `conflicting` = 0, `duplicate` = 0, `missing_notetype` = 0, `missing_deck` = 0, `first_field_match` = 0.
- [ ] After import: notes 6,948, cards 6,952 (or 6,952 + any intended additions, which should be 0), notetype count unchanged, deck tree unchanged, revlog row count unchanged. All card scheduling columns (`type, queue, due, ivl, factor, reps, lapses, did, ord`) are byte-identical to before.
- [ ] Post-import `ExplanationHTML` equals the intended value for 100 % of the changed notes. Exactly the expected set is non-empty (G2 + G4).
- [ ] Idempotence: importing the same package a second time gives `updated` = 0 and no other changes.
- [ ] Media check (`col.media.check()`): 0 missing, 0 newly unused.

## G8 — Rendering on all targets
- [ ] Render every changed card's question and answer HTML through the `anki` lib. Fail on: unrendered `{{`, visible `&lt;`/`&amp;` artefacts, empty answer side, `[...]` on an MCQ, a missing explanation block on a note that should have one.
- [ ] Screenshot 10 seeded cards (5 MCQ, 5 cloze incl. 1 two-blank note) in light and dark mode at phone width (≈ 390 px). Save them under `work/handoff/out/renders/`.

## G9 — Repo hygiene and handoff
- [ ] `git status` clean except intended files under `work/`. No export, collection, `.venv`, media or PDF committed. `.gitignore` covers `work/input/`, `work/scratch/`, `*.colpkg`, `*.anki2`, `*.anki21*`.
- [ ] `report.md` contains: the gate table (goal, check, expected, actual, PASS/FAIL), ImportLog verbatim, counts per subject × chapter × type (explained / flagged / review), flags by prefix, key disputes, residual defects (`FIS-C04-COMM-007` garbled explanation, `CHIM-C10-NCOM-080` banner, the stray `*`/`#` notes), and user import steps with the four settings plus "back up first (File → Create Backup)".
- [ ] Committed and pushed to the session branch. The final message states any deviation in its first sentence.

## Definition of done
G0–G9 all PASS in `verify_apkg.py` (exit 0). The real-import test shows **0 new, 0 conflicting, 0 duplicates, scheduling untouched**. Every one of the 6,948 notes has a verified question↔answer pairing, and all 2,055 cloze notes render with their answer. Every note either carries a validated explanation or a visible flag tag, and no answer key was changed without human sign-off.
