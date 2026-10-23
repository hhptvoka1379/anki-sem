# Verification report

- Package: `build/Semestre_Filtro_v1.0.apkg`
- Run: 2026-10-23T17:14:07; scope: CHIM-C01
- Command: `scripts/gates/run_gates.py build/Semestre_Filtro_v1.0.apkg --extracted build/extracted.jsonl --verification build/verification.jsonl --page-map build/chim_ch1_pagemap.json --unverified UNVERIFIED.md --out build/verification_report.md --chapters CHIM-C01`
- Summary: **NOT all gates pass — gate 5: MANUAL; gate 9: MANUAL.**

| Gate | Name | Result |
|---|---|---|
| 1 | Completeness | PASS |
| 2 | Answers | PASS |
| 3 | Typos (refusi) and OCR damage | PASS |
| 4 | Refusal text | PASS |
| 5 | Formulas and units | MANUAL |
| 6 | Status | PASS |
| 7 | No-script fallback | PASS |
| 8 | Import | PASS |
| 9 | Visual | MANUAL |

## Gate 1: Completeness — PASS

Check: sqlite3 on the unzipped collection: note/card counts vs extracted.jsonl, per-chapter/type counts, deck count, note type, every src=/url() media reference and the 4 fonts in the package media map

Output:
```
Package collection file: collection.anki2. Scope: chapters CHIM-C01.
Expected printed questions (extracted.jsonl filtered): 178
Notes found: 178 (note type 'Semestre Filtro — Quiz & Completamento'); all notes in file: 178; cards in file: 178; notes outside the chapter filter: 0
Distinct (subject, chapter, type) groups: expected 3, found 3
page_map.json: schema not recognised by the checker (no objects with chapter + quiz_type); per-chapter/type counts were checked against extracted.jsonl only.
Subdecks 'Semestre Filtro::<Materia>::<Capitolo>::<Tipo>': found 3, expected 3 (filtered run: one per (subject, chapter, type) in extracted.jsonl; full run: 84); non-empty: 3
Note type 'Semestre Filtro — Quiz & Completamento': present; note types in file: ['Semestre Filtro — Quiz & Completamento']
Field list and order match the frozen 20 fields.
Media entries in package: 192 (fonts present: 4/4)
Distinct local media references in fields/CSS/templates: 192; external references: 0
```

## Gate 2: Answers — PASS

Check: Parse BackOptionsHTML: exactly one 'opt correct', same letter/text as the banner and verification final_key; fill-in: TypedAnswer set, banner shows it, AcceptedAnswers match verification

Output:
```
Checked 131 multiple-choice and 47 fill-in notes.
```

## Gate 3: Typos (refusi) and OCR damage — PASS

Check: Regex scan for OCR damage over every field (FAIL on any hit); hunspell it_IT word check (unknown words listed for review in build/typo_candidates.tsv, not auto-fail)

Output:
```
Dictionary method: hunspell binary (/opt/homebrew/bin/hunspell) with /Users/db/Documents/projects/anki/_tools/it_IT.dic/.aff (full affix rules)
Distinct words checked: 1202 (all-caps tokens of up to 4 letters skipped as acronyms: 17); unknown to dictionary: 37
Unknown words for the orchestrator to review: build/typo_candidates.tsv (37 rows). Top: dell×47, possiede×45, all×21, Fe×8, Na×8, He×7, sull×6, nell×5, NaCl×4, Cs×3, Nell×3, dall×3
OCR-damage hits: 0 (full list: build/ocr_damage.tsv)
```

## Gate 4: Refusal text — PASS

Check: Case-insensitive search of all field text and raw HTML for: I can't, I cannot, I'm sorry, Mi dispiace, non posso, come modello

Output:
```
Hits: 0
```

## Gate 5: Formulas and units — MANUAL

Check: Regex extraction of every field containing number+unit, chemical formula, sub/superscripts or reaction/relation symbols -> build/formula_review.tsv

Output:
```
110 field(s) with formulas/units listed in build/formula_review.tsv. Checking each against the scan and recomputing calculated answers is not automatable.
MANUAL — see file build/formula_review.tsv
```

## Gate 6: Status — PASS

Check: Tags on every note: exactly one verify::<status>, matches verification.jsonl; unverified count vs UNVERIFIED.md; NoteHTML present for unverified/corrected/derived

Output:
```
Status tag counts: {'verified': 176, 'unverified': 2}
verify::unverified in deck: 2; ids in UNVERIFIED.md (filtered): 2
```

## Gate 7: No-script fallback — PASS

Check: Back HTML with every <script> removed: banner, accepted answers, TypedAnswer, correct option, NoteHTML, explanation present as text (all cards); then sample cards loaded in Chromium with JavaScript disabled and checked via innerText

Output:
```
String checks (banner, accepted answers, TypedAnswer, correct option, NoteHTML, explanation) run on the script-free back of 178 card(s).
JavaScript-off Chromium innerText check on 6 sample card(s): mcq missing=0 of 4, mcq missing=0 of 4, mcq missing=0 of 3, fill missing=0 of 3, fill missing=0 of 3, fill missing=0 of 3
```

## Gate 8: Import — PASS

Check: anki library: new Collection under work/anki-test/<timestamp>/, col.import_anki_package(ImportAnkiPackageRequest(... with_scheduling=False)); counts, decks, note type, media in col.media.dir(), card.question()/answer() for every card, [[type:TypedAnswer]] replaced by col.compare_answer(), typed_answer.js run in Node+jsdom

Output:
```
Import log: new=178 updated=0 duplicate=0 conflicting=0 first_field_match=0
Collection after import: notes=178, cards=178 (expected 178)
Subdecks: 3 (expected 3)
Note type present, 20 fields, 1 template(s): ['Domanda -> Risposta']
Media: 192 files in col.media.dir(); package lists 188 + fonts; missing: 0
Rendered card.question() and card.answer() for 178 card(s).
Saved 18 sample HTML file(s) to /Users/db/Documents/projects/anki/opus_attempt/build/renders/html (media copied alongside).
Typed-answer matrix (typed_answer.js run in jsdom with the card's scripts; 'shown' = 'Risposta accettata' visible):
  ok  CHIM-C01-COMP-001 correct ('chimica'): typed_read='chimica' matcher_accepts=True shown=True expected_shown=True errors=[]
  ok  CHIM-C01-COMP-001 article-prefixed ('il chimica'): typed_read='il chimica' matcher_accepts=True shown=True expected_shown=True errors=[]
  ok  CHIM-C01-COMP-001 wrong ('zzxqj'): typed_read='zzxqj' matcher_accepts=False shown=False expected_shown=False errors=[]
  ok  CHIM-C01-COMP-002 correct ('materia'): typed_read='materia' matcher_accepts=True shown=True expected_shown=True errors=[]
  ok  CHIM-C01-COMP-002 article-prefixed ('il materia'): typed_read='il materia' matcher_accepts=True shown=True expected_shown=True errors=[]
  ok  CHIM-C01-COMP-002 wrong ('zzxqj'): typed_read='zzxqj' matcher_accepts=False shown=False expected_shown=False errors=[]
  ok  CHIM-C01-COMP-003 correct ('reazione chimica'): typed_read='reazione chimica' matcher_accepts=True shown=True expected_shown=True errors=[]
  ok  CHIM-C01-COMP-003 article-prefixed ('il reazione chimica'): typed_read='il reazione chimica' matcher_accepts=True shown=True expected_shown=True errors=[]
  ok  CHIM-C01-COMP-003 wrong ('zzxqj'): typed_read='zzxqj' matcher_accepts=False shown=False expected_shown=False errors=[]
Not covered here: AnkiMobile/AnkiDroid/AnkiWeb behaviour and real Anki night-mode class handling; see the manual steps in gate 9.
```

## Gate 9: Visual — MANUAL

Check: node work/gates/render.js: MCQ + fill-in card, front/back, light/dark (body.nightMode), 390 px wide, bundled fonts, to build/renders/*.png

Output:
```
Command: node work/gates/render.js /Users/db/Documents/projects/anki/opus_attempt/build/renders/_manifest.json /Users/db/Documents/projects/anki/opus_attempt/build/renders  -> exit 0
PNGs written: 8/8 in /Users/db/Documents/projects/anki/opus_attempt/build/renders
Declared but not used by the rendered cards (status 'unloaded', not an error): ['Space Mono:unloaded']
Checked automatically: PNG exists, no horizontal overflow at 390 px, @font-face fonts reach 'loaded'. What the cards look like (layout, colours, dark mode contrast) was NOT judged by this script.
Manual check in Anki desktop: import the .apkg (File > Import), open a CHIM chapter deck, study one multiple-choice and one fill-in card, tap an option / type an answer, press Show Answer; expect pink-framed yellow dotted card, mint correct option, yellow banner, the DARK/LIGHT button toggles, and 'Risposta accettata' for an accepted variant. On a phone: sync, repeat, and turn Airplane Mode on to confirm the fonts still load.
RENDERED — visual review MANUAL (open the PNGs in build/renders/ and follow the steps above)
```
