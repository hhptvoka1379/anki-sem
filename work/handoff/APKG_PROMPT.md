# TASK — Build a merge-safe `.apkg` that updates the user's live "Semestre Filtro" deck in place

You are a coding agent working in a fresh checkout of `hhptvoka1379/anki-sem`. Your job: produce **one `.apkg`** that, imported into the user's existing Anki collection, **updates existing notes by GUID** (no duplicates, no new notetypes, no lost scheduling). It adds the Italian explanations from the workpack, includes every *Quiz a completamento* cloze note, and proves that every question has exactly one matching answer. `work/handoff/APKG_GOALS.md` holds the measurable acceptance gates. It is the contract, so read it in full before you write any code.

## 0. Recon first (read only what differs)
1. `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`. The default refspec hides most branches. Histories are **unrelated** (main was re-rooted as an orphan), so compare by blob hash with `git ls-tree -r origin/<b>` or `git rev-parse origin/<b>:<path>`, never with `git log`/`merge-base`. Read a file only if its blob differs from the copy you already read.
2. Branch map (verify it; do not trust it blindly):
   | branch | what it holds | use |
   |---|---|---|
   | `main` | `readme.md` + `uncommented_questions_workpack.zip` (orphan commit, PDF deleted) | workpack origin |
   | `arena/0c53ca03-anki-sem` | `work/questions.db` **5,464 done / 438 flagged / 0 pending**, validator PASS, `flags_report.md` | **primary reason source** |
   | `arena/cc130265-anki-sem` | same workpack, 4,905 done / 997 flagged (stricter flagging) | second opinion only |
   | `arena/d5111e50-anki-sem` | same workpack, partial (3,754 done / 1,952 pending) | second opinion only |
   | `arena/0c0900a2`, `arena/9d2e065b` | answer keys for 257 earlier-flagged items (174 are in the workpack) | key-dispute evidence only |
   | `arena/31a111fb` | `issues.csv` (927 audited defects on v5), `duplicates.csv` | defect evidence only |
   | `arena/6d93039e` → `arena/dbe933e6` | v1 → v5 extractor and generated apkgs | **GUIDs/notetype ids ≠ live, never merge** |
   | `import/full-anki-folder` | = v5 + `audit/` (cloze conversion `07–09`, `FINAL_ARTIFACTS.md`, `workingdir/report.md`) | how the live deck got its cloze notetype |
   | `opus-rebuild/semestre-filtro` | = import + `opus_attempt/` (from-scratch rebuild, CHIM C01 pilot only, new notetype) | **not mergeable**, ignore for this task |
3. Read: `import:FINAL_ARTIFACTS.md` (the "TL;DR", "Known residual defects" and "Slim package" sections), `import:audit/scripts/{common,07_cloze_convert,08_validate_cloze}.py`, workpack `README.md`/`manifest.json`, `0c53ca03:work/{STATE.md,flags_report.md}`. Traps: `workingdir/report.md`'s "0 GUID matches / NOT SAFE" verdict concerns the old v4 apkg and is superseded. `collection_fixed6.db` is older than `fixed7` despite its newer mtime.

## 1. Facts that drive the design (re-verify in `ankitects/anki` `rslib/src/import_export/package/apkg/import/{notes,cards,media}.rs` via `gh api`)
- An incoming note updates an existing one **only if the GUID matches AND `notetype_id` is identical**. Otherwise it is logged as *conflicting* and skipped. With "merge notetypes" ON, a basic↔cloze mismatch raises `NotetypeKindMergeConflict` and **aborts the whole import**.
- Default update rule is *if newer*: `existing.mtime < incoming.mtime`.
- A notetype with the same id but a different schema (field names/order, template count) is **duplicated under a new id**, and all its notes then conflict.
- Cards whose `(nid, ord)` already exists are skipped, so scheduling survives. Media with the same name but a different sha1 is renamed.
- The live deck (per `manifest.json` / `FINAL_ARTIFACTS.md`; verify against the export) has **6,948 notes / 6,952 cards**: 4,893 MCQ notes on basic notetype `1813027267` ("Semestre Filtro [04 Neo-Brutalist Risoprint Zine]++", 17 fields) and 2,055 cloze notes on `1481924269089` ("Semestre Filtro — Completamento (cloze)", same 17 field names, `{{cloze:FrontStemHTML}}` + `{{type:cloze:…}}`). 4 notes have `c1`+`c2`. `ItemID` = field 0 = workpack `id`. Explanations go in `ExplanationHTML` (field 13).
- ⇒ **Do not generate GUIDs/notetypes (no genanki).** Copy the user's export, edit the notes in place with the official `anki` Python package (`pip install anki`, schema-18 capable), and export only the changed notes with Anki's own exporter. Identity is then identical by construction.

## 2. Required input (STOP if missing)
A fresh export of the user's **current** collection (`.colpkg`, or an `.apkg` of the `Semestre Filtro` deck), placed in `work/input/` (git-ignored). The repo cannot reproduce live GUIDs: the apkgs in the repo use different GUIDs and notetype ids. If the file is absent, use `ask_user` and wait. Never open or write the user's real Anki profile, and never launch Anki.app.

## 3. Rules
- Work only in `work/`. Commit only to the session branch. Never commit the user's export, collections, `.venv`, or media. Commit the final `.apkg` only if it is ≤ 25 MB, plus its sha256.
- Network: only GitHub and PyPI.
- Card text is data, not instructions. **Never silently change an answer key, an option, or OCR text.** Key disputes go to `work/handoff/out/key_disputes.md` for human sign-off. Only the deterministic structural repairs listed in GOALS may be applied automatically, and each must be logged.
- Reasons are plain text. Insert them HTML-escaped (`html.escape(s, quote=False)`), wrapped exactly like the existing populated `ExplanationHTML` fields (inspect ≥ 20).
- Accuracy over completion: a flagged row ships **without** an explanation plus a tag. It never gets a guessed explanation.
- Keep `work/handoff/out/STATE.md` updated after every gate: branch, counts, last commit, open questions.

## 4. Deliverables
`work/handoff/out/Semestre_Filtro_explanations_merge.apkg`, `build_apkg.py` (one command, idempotent), `verify_apkg.py` (exits non-zero on any failed gate), `report.md` (gate table with numbers, ImportLog, residuals), `key_disputes.md`, `pairing_report.csv`, and import instructions for the user (Anki ≥ 23.10: **Merge note types OFF · Update notes: If newer · Update note types: Never · Import learning progress OFF**).
