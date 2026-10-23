# Where the final files are

Snapshot taken 2026-10-21 23:54, the last write in the workspace.
There is no git history outside `repo/`, so this index is reconstructed from
file contents, hardcoded paths in `audit/scripts/*.py`, and birth/mtime.

## TL;DR

| What | Path | Bytes / hash |
|---|---|---|
| **THE deliverable** (corrected live collection, cloze-converted) | `audit/out/cloze/ankicup_21-10-cloze.colpkg` | 553,461,789 B · sha256 `a77174a72601a861aa8db4b5e3db5f103444b6dd09aeb62b2d4aee0e7a9ac7f8` |
| Collection DB inside it | `audit/out/cloze/collection_patched.db` | 19,898,368 B · sha256 `029204f8ab48b08a01d9724b703f1c424c4192e59846388e477e1a787a72b3a8` |
| Final pre-cloze DB (source of the above) | `audit/out/fixed/collection_fixed7.db` | 19,828,736 B |
| Pre-audit generated deck (v5, 10 themes) | `v5repo/output/Semestre_Filtro_Complete.apkg` | 34,443,759 B · 6,948 notes |
| Latest written report | `audit/out/open_items_review.md` | 23:54 |

Final collection stats (verified with sqlite3):
13,459 notes / 14,937 cards total; 4,893 notes on the v5 model `1813027267`
+ 2,055 notes converted to the new cloze model `1481924269089` (= 6,948 deck notes).
Zip has 14,809 entries: `meta`, `collection.anki21b`, `collection.anki2`,
14,805 media blobs, `media` index.

## The audit chain (newest work, 21:32 → 23:54)

Input: `ankicup_21-10.colpkg` (554,099,037 B, 20:50) → `workingdir/colpkg/collection_anki21b.db`
(the live collection). Reference deck: `workingdir/tmp/v5apkg/collection.anki2`
(the unzipped `Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine-5.apkg`).

| Step | Script | Produced |
|---|---|---|
| pair/diff | `audit/scripts/01_pair_diff.py` | `out/pairing.json`, `out/diff.json`, `out/changed_fields.json` |
| text + OCR scan | `02`–`06` | `out/{text_hits,ocr_flags,flagged,needs_review,sample}.{json,csv}`, `out/summary.md` |
| notation audit | `10_notation_audit.py` | `out/notation_audit.{csv,json,md}` |
| notation fixes | `11_fix_notation.py` (`--fixes out/notation_fixes_safe.json`) | `out/fixed/collection_fixed.db`, `notation_fix_report.json` |
| patches | `12_apply_patches.py` (→ `collection_fixed2..5.db`) | `out/fixed/patch_report.json` |
| PDF re-extraction | `13_apply_reextract.py` | `out/pdf_transcripts*.json` → **`collection_fixed7.db`** |
| page location | `14/14b/15/16/17` | `out/located.json`, `out/question_pages*.md`, `out/ocrfull/`, `out/global_match.csv` |
| cloze conversion | `07_cloze_convert.py` (`SF_INPUT_DB=collection_fixed7.db`) | `out/cloze/collection_patched.db`, `conversion_report.json` |
| validation | `08_validate_cloze.py` | `out/cloze/validation.json` — all checks PASS |
| packaging | `09_package_colpkg.py` | `out/cloze/ankicup_21-10-cloze.colpkg`, `package.json`, `check.*` |

**`collection_fixed6.db` is a trap.** It has a *later* mtime (23:48 vs 23:42)
but is an older/buggier chain state. Proof: `collection_patched.db` differs from
`fixed7` in exactly 2,055 notes (the cloze conversions) and from `fixed6` in
2,059 (those same 2,055 + 4 notes where fixed6 is worse: it dropped
`class="opt correct"`, kept a stale answer banner, and kept figure call-outs in
`FIS-C03-NCOM-090`). The packaged DB is therefore built on `fixed7`.
Do not delete `fixed7` and do not "upgrade" to `fixed6`.


## Final reports to read (in this order)

1. `audit/out/open_items_review.md` — the 29 open items, book vs card, verdicts (newest file).
2. `audit/out/notation_repair_status.md` — what was fixed (57 notes / 124 strings), what is left.
3. `audit/out/question_pages_final.md` — corrected PDF page numbers (supersedes `question_pages.md`).
4. `audit/out/summary.md` — pairing/diff overview of live vs v5.
5. `audit/out/cloze/README.md` + `cloze/validation.json` — conversion + 23 checks.
6. `workingdir/report.md` — earlier v4-vs-live import dry run. **Its headline
   "NOT SAFE TO IMPORT / 0 GUID matches" compares the old v4 build**
   (`repo/output/Semestre_Filtro_EdiSES_Complete.apkg`); the correct v5 apkg
   (`workingdir/tmp/v5apkg`) has 6,948/6,948 GUID match with live. Treat that
   verdict as superseded.
7. `repo/ANALYSIS_REPORT.md` — the original v4 defect critique (untracked in git).

## Everything else is scratch / superseded

- `repo/` — historical v4 baseline (git HEAD `4c3e01d`, Oct 20). Superseded by
  `v5repo/` → `workingdir/` → `audit/`.
- `workingdir/` — input staging + dry run. `colpkg/input.colpkg`,
  `apkg/input.apkg`, `tmp/v5apkg/` (8,127 extracted files), `samples/media/` are copies/scratch.
- `audit/out/fixed/collection_fixed{,2,3,4,5,6}.db` — superseded intermediates.
- `audit/out/{notation_batch*,notation_patches_*,pdf_batch*,pdf_transcripts{,_1,_3,4}.json}` — agent batch I/O.
- `audit/out/{pages,pages2,pages3,full,full_pages,crops,ocr,ocrfull}` — page renders/OCR, large and regenerable.
- `audit/out/cloze/check.*` — round-trip proof only.
- `v5repo/index.html`, `v5repo/output/themes/theme_showcase.html` — previews, not Anki content.
- Top-level: 5 PDF variants (+`.pdf alias` bookmark); keep
  `Eserciziario Unico per il Semestre Filtro  2.pdf` (196 MB, used by
  `16_relocate.py`) and the 23.6 MB `-lite-trim.pdf` (used by `14/14b`).


## Known residual defects in the shipped colpkg (verified)

1. **21 notes lost the green correct-answer marker.** Their `BackOptionsHTML`
   was regenerated by the options re-writer without `class="opt correct"`
   (`13_apply_reextract.py:24-28`), so the back shows no check mark/highlight;
   the "Risposta corretta: X" banner is still correct. Notes:
   CHIM-C07-COMM-004, CHIM-C09-COMM-003, CHIM-C10-COMM-024, CHIM-C11-COMM-007,
   CHIM-C11-COMM-027, CHIM-C12-COMM-002, CHIM-C12-COMM-033, BIO-C04-COMM-014,
   BIO-C04-COMM-035, BIO-C04-NCOM-182, BIO-C05-COMM-046, BIO-C06-COMM-011,
   BIO-C06-COMM-036, FIS-C02-COMM-007, FIS-C03-COMM-023, FIS-C04-COMM-004,
   FIS-C04-COMM-007, FIS-C04-COMM-008, FIS-C04-COMM-009, FIS-C06-COMM-012,
   FIS-C06-COMM-033. (`FIS-C01-COMM-018` was already like this in live.)
2. `CHIM-C10-NCOM-080` banner still reads `Risposta corretta: A. C,`
   (the options themselves are correct). Pre-existing in live, left unfixed.
3. `FIS-C04-COMM-007` explanation is still OCR garble
   (`P;+r*g -hibrovi=B+...`) — explicitly still open.
4. ~25 notes still carry a stray `*`, `,` or `#`; most are emphasis marks.

Re-run hazards: `11_fix_notation.py` default `--fixes` file does not exist;
`12`/`13` default in/out names mis-chain (this is what produced the
fixed6/fixed7 inversion); `09` hardcodes `ankicup_21-10.colpkg`;
`04b_regrade.py` imports `"scripts/04_ocr_corpus.py"` relative to CWD (must run
from `audit/`); `17_global_match.py` hardcodes `collection_fixed7.db`.


## Slim package (IMAT + Premed removed)

`workingdir/slim/ankicup_21-10-semestre-only.colpkg`
· 34,569,278 B (34.6 MB) · sha256 `8aa0b3a1098a82cadc9f44b3f40cf88d88312e00ffb9ef0e651ab4878b720bd1`

Built from `audit/out/cloze/ankicup_21-10-cloze.colpkg` (unchanged, sha still
`a77174a7…ac7f8`). Deleted: 111 deck rows (all `IMAT` + empty `Premed`),
6,511 notes, 7,985 cards, 1,604 revlog rows, 63 unused notetypes, 720 unused
tags, 6,678 media files. Graves added (usn=-1) so the deletion propagates on sync.

Verified: zip CRCs OK; SQLite `integrity_check` ok; 6,948 notes / 6,952 cards;
top-level decks only `Default` + `Semestre Filtro`; every surviving note and card
hash-identical to the corrected collection (fields, tags, due/ivl/factor/reps,
deck ids); 8,127 media referenced, 0 missing, all blob sha1s match the index.
Residue: 4 bytes `IMAT` in unused free pages; no IMAT objects, text or media.


## Can `audit/out/cloze/ankicup_21-10-cloze.colpkg` be imported?

Yes. It is a full collection package built from your own export, and it keeps
all progress and media. Verified against the source collection
(`workingdir/colpkg/collection_anki21b.db`):

| Check | Result |
|---|---|
| zip integrity | 14,809 entries, all CRCs OK |
| media | 14,805 blobs, byte-identical to the input export |
| `meta`, `collection.anki2` | byte-identical to the input export (placeholder unchanged) |
| notes | 13,459 (same); 11,404 byte-identical, 2,055 converted to cloze |
| cards | 14,933 kept with **same card IDs**, 4 added, **0 deleted** |
| card scheduling (`type/queue/due/ivl/factor/reps/lapses/deck/ord`) | **unchanged** on every existing card; only `data` `{}`→`''` on the 2,055 converted ones |
| review history | revlog identical (3,211 rows, same min/max id), no new orphans |
| decks / tags / deck options / creation date / graves | identical (228 / 1,475 / 1 / `crt=1768359600` / 14,020) |
| last review in the file | 2026-10-21 19:36, i.e. before the 20:50 export → nothing studied since is missing |

Things to know before importing:

- A `.colpkg` **replaces the whole collection**, it does not merge. Confirm the
  "replace collection" prompt. Since the file derives from your 20:50 export and
  your last review was 19:36, replacing loses nothing.
- Anki takes automatic backups; `ankicup_21-10.colpkg` is also your untouched
  original — keep both.
- Needs a recent Anki (2.1.50+ / AnkiDroid 2.16+): the real DB is
  `collection.anki21b`. That is exactly the format your original export used,
  so compatibility is unchanged.
- The cloze notetype reuses ID `1481924269089`, which existed in the collection
  as an unused `Cloze-Brosencephalon` model (6 fields, 0 notes, 0 cards). It was
  overwritten — nothing else loses data, only that unused model's template.
- Cosmetic leftovers: 21 notes without the green correct-option highlight, and
  `CHIM-C10-NCOM-080`'s banner still says `Risposta corretta: A. C,`.

## Slim package: IMAT + Premed removed (2026-10-22 00:52)

**Use this if you only want the Semestre Filtro deck:**

    workingdir/slim-final/ankicup_21-10-semestre-only.colpkg
    34,317,797 B · sha256 4a049e1faf84dcebdb6e1af4626310661fccc7826b0327df849ada6604fb698e

Built from `audit/out/cloze/ankicup_21-10-cloze.colpkg` (sha unchanged
`a77174a7…ac7f8`), streaming the source zip; build script is at
`/tmp/slimbuild/build2.py`, log at `/tmp/slimbuild/run.log`.

Removed: the whole `IMAT` tree (110 deck rows, 7,985 cards, 6,511 notes,
1,604 revlog rows) and the empty `Premed` deck, plus 63 now-unused
notetypes and 720 unused tags. Deletions are recorded in `graves` (7,985
card + 6,511 note + 111 deck graves, usn=-1) so they propagate on sync.

### Verified (build checks + independent re-check + reviewer APPROVE)

| Criterion | Result |
|---|---|
| notes / cards | 6,948 / 6,952 — every note (guid,flds) and every card row identical to the source |
| decks | 117: `Default` + `Semestre Filtro` tree only; 0 names containing IMAT/Premed |
| notetypes / tags | 2 (the Semestre ones) / 755, all in use |
| metadata | surviving deck rows, notetype rows, `col` row, `deck_config` unchanged |
| media | 8,127 index entries = 8,127 blobs = 8,127 referenced names; all 8,127 blobs decompressed and sha1+size verified |
| DB hygiene | `integrity_check` ok, `freelist_count` 0, no `sqlite_stat*` tables |
| residue | 0 hits for 10 long IMAT strings, `IMAT\x1f`, `Premed\x1f`, `(Past) IMAT All Anki Decks`; only explained prefixes (`…Zine]+` of the surviving `…Zine]++`) |
| zip | 8,131 entries, all CRCs OK, `meta`/`collection.anki2` byte-identical to the source |
| source package | untouched (sha verified at start and end) |

### Caveats

- 1,370 revlog rows still point at cards that were already missing in the
  source (inherited, not introduced); Anki ignores them for stats.
- `config.curModel` (1792577635461) names a removed notetype; Anki falls back.
- Pre-2.1.50 clients read the stub `collection.anki2` (empty, identical to the
  source's) — same limitation as the original export.
- `workingdir/slim/unzipped/` is scratch (the extracted 553 MB package); safe to delete.

## Slim package — IMAT and Premed removed (2026-10-22 00:50)

**Import this one instead of the 553 MB file:**

`workingdir/final/ankicup_21-10-semestre-only.colpkg`

- 34,317,797 B · sha256 `6cfe5359e9741cd10b7b1656a91fa4c899c8f17a6883df90efbfb19dfd14bdba`
- Zip: 8,131 entries, all CRCs OK; only `collection.anki21b` differs from the source layout.
- Removed: 110 `IMAT*` decks + the empty `Premed` deck, 6,511 notes, 7,985 cards,
  1,604 revlog rows, 63 notetypes, 720 tags (recorded in graves so the deletion
  propagates on sync).
- Kept: `Default` + `Semestre Filtro` — 6,948 notes / 6,952 cards / 755 tags /
  117 deck rows / 2 notetypes / 8,127 media files.
- Source of truth for the Semestre content is unchanged: `audit/out/cloze/ankicup_21-10-cloze.colpkg`
  still has sha256 `a77174a7...` (553 MB). The slim file is separate.

Verified (independent reviewer + own checks):

| Check | Result |
|---|---|
| Semestre notes (guid + all 11 columns) | 0 differences |
| Semestre cards (all 18 columns) | 0 differences |
| Deck rows / notetypes / fields / templates / col / deck_config | 0 differences |
| Media | 8,127 refs = 8,127 index entries = 8,127 blobs, all sha1+size verified |
| DB | integrity ok, `VACUUM`ed, freelist 0, no `sqlite_stat*` tables |
| IMAT/Premed residue in raw DB bytes | `IMAT` 0, `Premed` 0, removed deck/notetype names 0 |
| Zip | all CRCs OK, 8,131 entries, `meta` and `collection.anki2` byte-identical |

Build location: source extracted to `workingdir/slim/unzipped/`; DB surgery +
`VACUUM` produced `workingdir/slim2/collection.db` (14,770,176 B); package written
to `workingdir/slim2/` and copied to `workingdir/final/`.

Known, non-blocking:
- `config.curModel` still points at a removed notetype (Anki falls back to the first one).
- 1,370 revlog rows reference cards that were already absent in the source (inherited, not introduced).
- Clients older than Anki 2.1.50 read only the legacy `collection.anki2` stub (empty), exactly as with the original export.

## Slim package — IMAT + Premed removed (2026-10-22 00:50)

**Use this file if you want only the Semestre Filtro deck:**

`workingdir/slim2/ankicup_21-10-semestre-only.colpkg` — 34,317,797 B
sha256 `6cfe5359e9741cd10b7b1656a91fa4c899c8f17a6883df90efbfb19dfd14bdba`

Built from `audit/out/cloze/ankicup_21-10-cloze.colpkg` (source sha unchanged:
`a77174a7…ac7f8`). Only the package's DB and media set changed; the full 553 MB
originals were not modified.

| Check | Result |
|---|---|
| IMAT deck tree | 110 decks, 6,511 notes, 7,985 cards removed |
| Premed | empty deck removed |
| decks left | 117 = `Default` + `Semestre Filtro` (116 rows) |
| notes / cards | 6,948 / 6,952 |
| Semestre fidelity | 0 notes differing, 0 cards differing, 0 deck rows differing — all columns |
| notetypes | 2 (the Semestre quiz + cloze models); 63 unused removed |
| tags | 755 used only (720 unused removed) |
| media | 8,127 kept, 8,127/8,127 blob sha1+size verified; 0 unresolved refs |
| graves | +14,607 entries (7,985 cards, 6,511 notes, 111 decks), all `usn=-1` |
| residue | bare `IMAT` 0 bytes (source 664), `Premed` 0 (source 4), removed names 0 |
| compaction | VACUUM: 4,858 → 3,606 pages, freelist 0, no `sqlite_stat*` |
| zip | 8,131 entries, all CRCs OK, `meta` and `collection.anki2` byte-identical to source |
| review | independent reviewer: **APPROVE** |

Caveats (all inherited from the source, none introduced):
- `config.curModel` and `3` ids in `activeDecks` point at removed objects; Anki
  falls back to defaults. Identical bytes in the source.
- 1,370 revlog rows reference cards deleted long ago; present in the source too.
- Pre-2.1.50 Anki clients read the `collection.anki2` stub (1 dummy note) and
  would import effectively nothing — same behaviour as your original export.
- `workingdir/slim/unzipped/` (557 MB) and `workingdir/slim2/collection.db`
  (14.8 MB) are build scratch and can be deleted.
