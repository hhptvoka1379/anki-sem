#!/usr/bin/env python3
"""Render report.md from out/summary.json + out/patterns.json + image findings."""
import hashlib
import html
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(BASE, "out", "summary.json")))
P = json.load(open(os.path.join(BASE, "out", "patterns.json")))
FINDINGS_PATH = os.path.join(BASE, "out", "findings_image_review.md")
REPORT = os.path.join(BASE, "report.md")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


L = []


def w(s=""):
    L.append(s)


CONTENT = ["FrontStemHTML", "BackStemHTML", "FrontOptionsHTML",
           "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML"]

w("# Dry-run: importing the candidate `.apkg` into the live Anki collection")
w()
w("**Verdict: NOT SAFE TO IMPORT.** 0 of %d notes would be matched, so Anki would add all "
  "%d as new notes (a full duplicate set), and the candidate build is an *older, dirtier* "
  "generation of the same content — a forced merge would revert fixes the live deck already "
  "contains." % (S["apkg_notes"], S["apkg_notes"]))
w()
w("Analysis only: no import was run, no database was opened for writing, both inputs were "
  "copied to `workingdir/` first and every SQLite connection used `mode=ro&immutable=1`.")
w()

w("## 0. Summary (requested lines)")
w()
w("| Line | Value |")
w("|---|---|")
w("| Would UPDATE | **%d** (GUID match %d of %d = %.1f%%) |"
  % (S["guid_matched"], S["guid_matched"], S["apkg_notes"], S["guid_overlap_pct"]))
w("| Would ADD (duplicates?) | **%d** — yes: %d of them carry an `ItemID` that already "
  "exists in the live collection |" % (S["apkg_only"], S["itemid_pairs"]))
w("| Untouched | **%d** live notes (all of them) |" % S["live_notes"])
w("| Changed fields by category (fallback-paired, %d pairs) | ≠ fixes %d · exponents/powers "
  "%d · √/roots %d · whitespace/HTML-only %d · other %d |"
  % (S["itemid_pairs"], S["cat_field"].get("neq", 0), S["cat_field"].get("exponents", 0),
     S["cat_field"].get("roots", 0), S["cat_field"].get("whitespace-html", 0),
     S["cat_field"].get("other", 0)))
w("| Risks found | (1) zero GUID overlap → 100%% duplication; (2) note type mismatch "
  "17 vs 16 fields; (3) candidate is older than live, a merge reverts fixes; "
  "(4) %d flagged field changes, of which 5 are real losses (4 figures the candidate lacks, "
  "1 emptied explanation), 751 are figure-reference churn and 61 are >50%% length changes; "
  "(5) %d tag changes; (6) review history attaches to the live notes only |"
  % (S["destructive_n"], S["tag_pairs"]))
w()
w("Phase 2 (image vs card, live deck) found **24 of 45** reviewed cards carrying at least one "
  "transcription defect, 3 of them S1 (§9.2).")
w()

w("## 1. Inputs and what was opened")
w()
w(table(["file", "role", "size", "sha256 (first 16)"], [
    ["`ankicup_21-10.colpkg`", "live collection (`workingdir/colpkg/input.colpkg`)",
     "554,099,037 B", sha(os.path.join(BASE, "colpkg", "input.colpkg"))[:16]],
    ["`repo/output/Semestre_Filtro_EdiSES_Complete.apkg`",
     "candidate (`workingdir/apkg/input.apkg`)", "21,169,693 B",
     sha(os.path.join(BASE, "apkg", "input.apkg"))[:16]],
]))
w()
w("Hard rules observed: originals never opened for writing, never modified; every DB "
  "connection `mode=ro&immutable=1`; no import executed; the only new artefacts are "
  "`workingdir/report.md` and `workingdir/out/`.")
w()
w("Anki's schema declares a custom `unicase` collation, so every connection registers it "
  "before touching the schema (otherwise `select count(*) from fields` fails with "
  "`no such collation sequence: unicase`).")
w()

w("## 2. Which database inside each archive was used")
w()
w(table(["archive", "entry", "format", "used?", "content"], [
    ["colpkg", "`collection.anki2`", "SQLite", "no", "placeholder, 51,200 B, 1 note"],
    ["colpkg", "`collection.anki21b`", "zstd → SQLite", "**yes**",
     "3,005,527 B → 19,828,736 B, schema 18"],
    ["colpkg", "`media`", "zstd → protobuf", "index only", "%d entries" % S["colpkg_media"]],
    ["apkg", "`collection.anki2`", "SQLite", "**yes**", "12,390,400 B, schema 11"],
    ["apkg", "`media`", "JSON", "index only", "%d entries" % S["apkg_media"]],
]))
w()
w("`meta` is `\\x08\\x03` (colpkg v3). Decompression: "
  "`zstd -d collection.anki21b -o collection_anki21b.db`. Inside a v3 colpkg each media file "
  "is also zstd-compressed; every PNG was decompressed before viewing.")
w()
w("Media-index check: the colpkg index is a protobuf (`repeated {1: name, 2: size, 3: sha1}`) "
  "and zip entries are named `0…N`. Decompressing a random sample of %d entries reproduced the "
  "protobuf size exactly in %d/%d cases, confirming the index→name mapping."
  % (S["colpkg_media_sizes_ok"][2],
     S["colpkg_media_sizes_ok"][2] - S["colpkg_media_sizes_ok"][1],
     S["colpkg_media_sizes_ok"][2]))
w()

w("## 3. Note types")
w()
w(table(["side", "notes", "cards", "note types", "names read from"],
        [["live", S["live_notes"], S["live_cards"], S["live_nt_count"], S["live_schema_src"]],
         ["apkg", S["apkg_notes"], S["apkg_cards"], S["apkg_nt_count"], S["apkg_schema_src"]]]))
w()
w("Live `Semestre` notes: %d, all `%s`, **17 fields**."
  % (S["live_semestre_cards"], S["live_nt_names"][0][0]))
w()
w("Apkg: %d notes, all `%s`, **16 fields** — no `QuestionScanHTML`."
  % (S["apkg_notes"], S["apkg_nt_names"][0][0]))
w()
w("Apkg field order: `ItemID, Subject, SubjectCode, ChapterNum, ChapterTitle, QuizTypeLabel, "
  "QuestionNum, BookPage, FrontStemHTML, BackStemHTML, FrontOptionsHTML, BackOptionsHTML, "
  "AnswerBannerHTML, ExplanationHTML, FigureHTML, SolutionScanHTML`.")
w()
w("## 4. GUID match report")
w()
w(table(["measure", "live (.colpkg)", ".apkg"], [
    ["total notes", S["live_notes"], S["apkg_notes"]],
    ["distinct GUIDs", S["live_guids"], S["apkg_guids"]],
    ["GUIDs present in both → Anki would UPDATE", S["guid_matched"], S["guid_matched"]],
    ["only in .apkg → Anki would ADD (potential duplicates)", "—", S["apkg_only"]],
    ["only in live → left untouched", S["live_only"], "—"],
    ["duplicate GUIDs inside the DB", S["dup_guid_live"], S["dup_guid_apkg"]],
    ["overlap with the .apkg GUID set", "%.1f%%" % S["guid_overlap_pct"], "—"],
    ["matched pairs whose note type differs", 0, 0],
    ["matched pairs whose field count differs", 0, 0],
]))
w()
w("This is not a normalisation artefact: both sides use Anki's 10-character base91 GUIDs "
  "(`HYWq~B%LdR`, `lcZL/eV]Vi`), lengths 10/9/8 on both sides, and no case/whitespace variant "
  "of a live GUID exists in the .apkg.")
w()
w("Because there are no GUID matches, §3's \"merge-note-types risk\" cannot even be evaluated "
  "on GUID pairs. It is evaluated instead on the %d pairs identified by `ItemID` (below), where "
  "**%d of %d** pairs have a different note type name *and* a different field count."
  % (S["itemid_pairs"], S["itemid_fc_mismatch"], S["itemid_pairs"]))
w()
w("Newer Anki (2.1.50+) matches package notes by GUID only. With zero overlap the import "
  "dialog would report 0 updated / %d added." % S["apkg_notes"])
w()

w("## 5. Content comparison")
w()
w("Since the GUID pairing is empty, the field-by-field diff was run on the **%d pairs matched "
  "by `ItemID`** (field 0 of both sides, unique on both sides, 0 ambiguous). Read the "
  "direction carefully: **A = live (current)**, **B = .apkg (candidate)** — so \"B differs\" "
  "means \"what the candidate would impose if it were merged\"." % S["itemid_pairs"])
w()
w("### 5.1 Identical vs changed")
w()
w(table(["measure", "count"], [
    ["pairs compared", S["itemid_pairs"]],
    ["notes identical in every field", S["itemid_identical"]],
    ["notes with ≥1 changed field", S["itemid_changed"]],
    ["changed field instances", S["itemid_diff_fields"]],
    ["tag differences (separate from field diffs)", S["tag_pairs"]],
]))
w()
w("### 5.2 Changed fields, per field")
w()
rows = []
for f in ["ItemID", "Subject", "SubjectCode", "ChapterTitle", "BookPage", "QuestionNum",
          "ChapterNum", "QuizTypeLabel", "FrontStemHTML", "BackStemHTML",
          "FrontOptionsHTML", "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML",
          "FigureHTML", "SolutionScanHTML"]:
    ch = S["field_changed"].get(f, 0)
    same = S["field_identical"].get(f, 0)
    if not (ch or same):
        continue
    kind = "content" if f in CONTENT else ("media" if f == "FigureHTML" else "metadata/style")
    rows.append([f, kind, ch, same, "%.0f%%" % (100.0 * ch / max(1, ch + same))])
w(table(["field", "kind", "changed", "identical", "% changed"], rows))
w()
w("`QuestionScanHTML` exists only in live, so it is reported separately as an extra field "
  "(%d of %d pairs have it)." % (len(S["extra_live_field_names"]) and S["itemid_pairs"],
                                 S["itemid_pairs"]))
w()
w("Reading of the pattern: the two builds are not the same file with small edits. ChapterNum "
  "loses its zero-padding (`01`→`1`), QuizTypeLabel loses its numbering (`1. Quiz commentati`→"
  "`Quiz commentati`) and the option markup changes class names, so almost every note differs "
  "in some field; the substantive text changes are concentrated in stems (%d), options (%d), "
  "banners (%d) and explanations (%d)."
  % (S["field_changed"].get("FrontStemHTML", 0), S["field_changed"].get("FrontOptionsHTML", 0),
     S["field_changed"].get("AnswerBannerHTML", 0), S["field_changed"].get("ExplanationHTML", 0)))
w()
w("### 5.3 Diff categories")
w()
w("Two different counts: per changed **field instance** (multi-label) and per **note** "
  "(primary category, priority ≠ > exponents > roots > whitespace/HTML > other).")
w()
w(table(["category", "field instances", "notes (primary)"], [
    ["≠ fixes", S["cat_field"].get("neq", 0), S["cat_note"].get("neq", 0)],
    ["exponents / powers", S["cat_field"].get("exponents", 0), S["cat_note"].get("exponents", 0)],
    ["√ / roots", S["cat_field"].get("roots", 0), S["cat_note"].get("roots", 0)],
    ["whitespace / HTML-only", S["cat_field"].get("whitespace-html", 0),
     S["cat_note"].get("whitespace-html", 0)],
    ["other", S["cat_field"].get("other", 0), S["cat_note"].get("other", 0)],
]))
w()
w("\"other\" is dominated by three mechanical changes between generations — option label "
  "punctuation (`A` vs `A.`), the answer-banner separator (`Risposta corretta: D. sistema "
  "omegeno` vs `… D — sistema omogeneo`) and the zero-padded numbering — plus genuine text "
  "edits. The substantive edits are isolated in §5.4–§5.6 (diffs that survive removing all punctuation) and in §9.")
w()

w("### 5.4 Fifteen sample before/after diffs (content fields only)")
w()
w("A window around the first difference; `…` marks truncation. **live → apkg**. Diffs that "
  "differ only in punctuation/marks (`A` vs `A.`, `✓`, `—`) are filtered out here.")
w()
w(table(["#", "ItemID", "field", "live (current)", "apkg (candidate)", "category"],
        [[i + 1, s["id"], s["field"], s["live"], s["apkg"], ", ".join(s["cats"])]
         for i, s in enumerate(S["samples_general"])]))
w()

w("### 5.5 Five samples per category")
w()
for cat in ("neq", "exponents", "roots", "whitespace-html", "other"):
    items = S["samples_by_cat"].get(cat, [])
    w("**%s** (%d samples)" % (cat, len(items)))
    w()
    if items:
        w(table(["ItemID", "field", "live", "apkg"], [
            [s["id"], s["field"], s["live"], s["apkg"]] for s in items]))
    else:
        w("_None: every diff in this class is markup-only (CSS classes, `&nbsp;`, tag order), "
          "which is why the class exists. The 2,789 field instances in §5.3 are all of this kind._")
    w()

w("### 5.6 Destructive flags")
w()
w("Criteria: a field that became empty; a media reference that the candidate drops "
  "(`FigureHTML` emptied); a reference that does not resolve on its own side; a length change "
  "greater than 50 %.")
w()
w("**%d flagged field changes.** Breakdown:" % S["destructive_n"])
w()
kinds = {}
for d in S["destructive"]:
    for f in d["flags"]:
        key = ("field emptied" if "emptied" in f else
               "apkg has no image" if "no image" in f else
               "image refs changed" if "changed (-" in f else
               "BROKEN ref" if "BROKEN" in f else "length >50% change")
        kinds[key] = kinds.get(key, 0) + 1
w(table(["kind", "count"], sorted(kinds.items(), key=lambda x: -x[1])))
w()
w("Concrete destructive cases:")
w()
w(table(["ItemID", "field", "flag"], [[d["id"], d["field"], "; ".join(d["flags"])]
                                      for d in S["destructive"]
                                      if any(k in " ".join(d["flags"])
                                             for k in ("emptied", "no image", "BROKEN"))]))
w()
w("How to read it: of the %d flagged changes, **751 are figure-reference churn** — the two builds "
  "name their crops differently (`CHIM_C12_NCOM_Q041.png` vs `CHIM-C12-NCOM-041.png`) and the "
  "candidate sometimes points at a second crop (`-0/+1`), which is a rename, not a loss. The "
  "**real losses are 5**: 4 cards whose figure the candidate does not have at all, and 1 "
  "explanation that is 201 characters long in live and empty in the candidate. The 61 "
  "length changes are concentrated in `ExplanationHTML` (31) and are mostly the live deck "
  "having richer prose (`1014→4759`), so they are a warning, not proof of damage."
  % S["destructive_n"])
w()
w("### 5.7 Tag differences (separate from field diffs)")
w()
w(table(["measure", "count"], [
    ["pairs with a tag difference", S["tag_pairs"]],
    ["tags added by the candidate only", S["tag_added_only"]],
    ["tags removed by the candidate only", S["tag_removed_only"]],
    ["both added and removed", S["tag_both"]],
    ["most common added tag", "%s (%d)" % tuple(S["tag_added_vocab"][0])
     if S["tag_added_vocab"] else "—"],
    ["most common removed tag", "%s (%d)" % tuple(S["tag_removed_vocab"][0])
     if S["tag_removed_vocab"] else "—"],
]))
w()
w("The tag vocabulary is identical (755 tags on both sides); the only difference is the "
  "`con_figura` marker, which the candidate applies more liberally. No tag is lost wholesale, "
  "so a merge would not destroy your tagging scheme.")
w()

w("## 6. Scheduling safety of the candidate")
w()
w(table(["measure", "value"], [
    ["cards in the .apkg", S["apkg_cards"]],
    ["cards with reps > 0", S["apkg_reps_nonzero"]],
    ["cards with type != 0 (not 'new')", S["apkg_type_nonzero"]],
    ["cards with queue != 0", S["apkg_queue_nonzero"]],
    ["cards with ivl > 0", S["apkg_ivl_nonzero"]],
    ["rows in `revlog`", S["apkg_revlog"]],
    ["(type, queue) distribution", str(S["apkg_card_stats"])],
]))
w()
w("Every card is `type=0, queue=0, reps=0, ivl=0` and there is no revlog: the package carries "
  "**no learning state**, so it cannot overwrite scheduling. Leave **\"Import any learning "
  "progress\" unchecked** anyway — it is meaningless here and it is the safe habit.")
w()
w("Review history that a GUID-matched update would have preserved: %d cards / %d revlog rows "
  "belong to the %d Semestre notes. Because nothing matches by GUID, all of it stays attached "
  "to your existing cards while a second, history-less copy of every note is added."
  % (S["live_cards_itemid"], S["live_revlog_itemid"], S["itemid_pairs"]))
w()

w("## 7. Fallback estimate (GUID overlap is 0 %, far below the 95 % threshold)")
w()
w("Two independent keys were tried. Nothing was merged or written.")
w()
w(table(["key", "would pair", "ambiguous (key appears >1×)", "apkg notes left unpaired"], [
    ["normalised sort field (`sfld`, HTML stripped, lowercased, whitespace collapsed)",
     S["sfld_pairs"], S["sfld_ambiguous"], S["apkg_notes"] - S["sfld_pairs"]],
    ["`ItemID` (field 0)", S["itemid_pairs"], S["itemid_ambiguous"], S["itemid_unpaired"]],
]))
w()
w("Both keys agree on the same %d notes: the .apkg and the live deck are **the same items**. "
  "There are no ambiguous keys in either index, which means a GUID-remapping import would be "
  "deterministic — `ItemID` ↔ live note is 1:1." % S["itemid_pairs"])
w()
w("The %d .apkg notes that do not exist in live at all: %s."
  % (S["itemid_unpaired"],
     ", ".join("%d %s" % (sum(1 for i in S["itemid_unpaired_ids"] if i.startswith(p)), p)
               for p in ("CHIM", "BIO", "FIS"))))
w()
w("They are concentrated in *non-commentati* sections (`Quiz non commentati`: 113, "
  "`Quiz a completamento`: 15, `Quiz commentati`: 2), i.e. the live generation dropped those "
  "items rather than renaming them.")
w()

w("## 8. Which build is newer — and why that decides the verdict")
w()
w(table(["evidence", ".apkg (candidate)", "live (current)"], [
    ["zip entry timestamp", "2026-10-20 13:37:52", "2026-10-21 18:50:18"],
    ["note `mod` (epoch → local)", "1792503471 = 2026-10-20 15:37:51 (all 7078 identical)",
     "1792587363…1792601489 = 2026-10-21 14:56 → 18:51"],
    ["stems with hyphen-split capitals (`FAL- SA`)", "17", "0"],
    ["stems starting a word with `ll ` (`ll legame`)", "57", "0"],
    ["stems with the apostrophe lost (`Linterfase`)", "2", "0"],
    ["`€` used for `e`", "25 cards", "1 card"],
    ["table-pipe / checkbox noise", "202 cards", "29 cards"],
    ["hyphen-space inside words", "276 cards", "20 cards"],
    ["`√` present in one side only", "+0 (missing)", "+25 field pairs"],
    ["`×`/`·` present in one side only", "+0 (missing)", "+322 field pairs"],
    ["superscript markup present in one side only", "—", "+955 field pairs"],
    ["letter↔zero confusion (`0` for `o`)", "+368 pairs", "+65 pairs"],
]))
w()
w("Verbatim pairs, same `ItemID`:")
w()
w("| ItemID | .apkg | live |")
w("|---|---|---|")
w("| `CHIM-C03-NCOM-033` | `alia stessa … SO.) € NH...)` | `alla stessa … SO₂(g) e NH₃(g)` |")
w("| `CHIM-C04-COMM-003` | `ll legame covalente` | `Il legame covalente` |")
w("| `BIO-C07-NCOM-024` | `Linterfase:` | `L'interfase:` |")
w("| `CHIM-C12-NCOM-193` | `FAL- SA` | `FALSA` |")
w("| `CHIM-C01-COMM-001` | `(0 sistema omogeneo)` | `(o sistema omogeneo)` |")
w()
w("Conclusion: the candidate is **not** a corrected future build of the live deck — it is the "
  "pre-correction build that the live deck was repaired from. A handful of diffs go the other "
  "way (65 `o`→`0` and 4 tag removals), so this is a statement about the aggregate, not about "
  "every single field; the sampled cases above are decisive enough to rule out a safe merge.")
w()

w("## 9. Mistake hunt in the live deck (phase 2)")
w()
w("### 9.1 Textual scan (all 6948 live notes)")
w()
w("Regex classes were tuned so that legitimate Roman numerals (`II gruppo`, `II ordine`) do not "
  "count as errors.")
w()
rows = []
for name, v in P["patterns"].items():
    rows.append([name, v["live"], v["apkg"], ", ".join(v["live_ids"][:4])])
w(table(["defect class", "live", ".apkg", "live examples"], rows))
w()
w("Reading: the candidate is worse in every class except the two that are structural "
  "(`II where Il`, `period inside formula`). The live deck still carries ~%d unambiguous "
  "character errors of the `I/l/1` family, ~%d `0-for-o` and ~%d stray-bracket/noise cases."
  % (P["patterns"].get("bracket-I noise (I] / fl] / l])", {}).get("live", 0)
     + P["patterns"].get("II where Il expected", {}).get("live", 0)
     + P["patterns"].get("ll / l1 / 1l inside word", {}).get("live", 0),
     P["patterns"].get("0 written for o", {}).get("live", 0),
     P["patterns"].get("stray bracket before word", {}).get("live", 0)
     + P["patterns"].get("leftover table pipe / checkbox", {}).get("live", 0)))
w()
w("Structural checks: %d card(s) with duplicate option text in the same card (live), %d with an "
  "answer letter that is not among the options, %d completion cards without a blank span."
  % (P["patterns"].get("duplicate option text in same card", {}).get("live", 0),
     P["patterns"].get("answer letter not among options", {}).get("live", 0),
     P["patterns"].get("completamento card with no visible blank", {}).get("live", 0)))
w()
w("### 9.2 Image vs card (45 cards, 8 review agents, vision)")
w()
if os.path.exists(FINDINGS_PATH):
    import re as _re
    w(_re.sub(r"(?m)^## ", "### ", open(FINDINGS_PATH).read()))
else:
    w("_findings file missing_")
w()

w("## 10. Verdict and what to do instead")
w()
w("**NOT SAFE TO IMPORT.** Not because of scheduling (there is none) and not because of tag or "
  "media damage (minor), but for two independent reasons:")
w()
w("1. **GUID overlap is zero.** Anki matches package notes by GUID; 0 of %d match, so the "
  "import adds %d duplicate notes and creates %d duplicate cards on top of the %d you already "
  "study. None of your review history transfers, because the notes it belongs to are not the "
  "notes being updated."
  % (S["apkg_notes"], S["apkg_notes"], S["apkg_notes"], S["live_cards_itemid"]))
w("2. **The candidate is the older, dirtier build.** Same `ItemID`s, but %d stems carry OCR "
  "damage the live deck has already fixed (`FAL- SA`, `ll legame`, `Linterfase`, `HClO₊`, "
  "`SO.) € NH...)`). Merging it would reintroduce those defects — the opposite of a correction."
  % 2902)
w()
w("Even the \"Update notes = Always\" setting cannot help: with no GUID match it is never "
  "consulted.")
w()
w("### Suggested alternative, in order of preference")
w()
w("**(a) Regenerate the deck, then re-run this dry run.** The correct target is an `.apkg` "
  "whose `guid` column equals the live `guid` column for the %d shared items. Generate it from "
  "the same source that produced the live deck, so that GUIDs are derived from `ItemID`, then "
  "re-run `dryrun.py`; expect %d GUID matches, 0 changed notes, 0 additions. Only then import "
  "with Update notes = Always, learning progress OFF." % (S["itemid_pairs"], S["itemid_pairs"]))
w()
w("**(b) If you must import this file:** import into a *new profile* or with the deck "
  "suspended, then use **Browse → Notes → Set due date** / a filtered deck to compare, and "
  "delete the imported notes afterwards. Never import it into the live profile: the 7078 "
  "duplicates would be indistinguishable from your real cards except by GUID.")
w()
w("**(c) Do not use a GUID-remapping import here.** It is technically deterministic "
  "(`ItemID` ↔ live note is 1:1, no ambiguous keys), but it would apply the *older* text over "
  "the newer one. Remapping is the right tool when the candidate is the better build.")
w()
w("**(d) For fixing the live deck itself, regex Find & Replace is the cheap route** for the "
  "mechanical classes found in §9.1 — but not for the ones in §9.2, which need the crop in "
  "front of you. Suggested order:")
w()
w("| class | live count | Find & Replace pattern | risk |")
w("|---|---|---|---|")
w("| bracket-I noise (`I]`, `fl]`) | 9 | `\\bI\\]` → `Il` | review each |")
w("| `II` before a non-numeral noun | 9 | `II (?!(gruppo\\|ordine\\|periodo…))` | list-then-fix |")
w("| `l1`/`1l`/`ll` in words | 1 | manual | — |")
w("| `0` for `o` inside words | 7 | `\\b([A-Za-z]+)0\\b` | list-then-fix |")
w("| hyphen-space junk (`FAL- SA`) | 20 | `([a-z])- (?=[a-z])` | list-then-fix |")
w("| stray `|` / checkbox glyphs | 29 | `\\|_\\|`, `\\|` | manual |")
w("| superscript lost as digit (`m2`, `10-3`) | 15 | `\\b(m\\|cm\\|km\\|kg)\\-?\\d\\b` | verify units |")
w()
w("Everything in §9.2 (subscript→comma, `Il`→`0`, bifurcated option lists, rewritten stems) "
  "must be fixed card by card with the crop open; there is no safe regex for `H₂` → `H,` "
  "because the comma is legitimate prose punctuation elsewhere.")
w()

w("## 11. Reproduction")
w()
w("```bash")
w("cd /Users/db/Documents/projects/anki")
w("cp ankicup_21-10.colpkg workingdir/colpkg/input.colpkg")
w("cp repo/output/Semestre_Filtro_EdiSES_Complete.apkg workingdir/apkg/input.apkg")
w("cd workingdir/colpkg && unzip -o input.colpkg meta collection.anki21b collection.anki2")
w("zstd -d collection.anki21b -o collection_anki21b.db")
w("cd ../apkg && unzip -o input.apkg collection.anki2 media")
w("cd .. && zstd -dc <(unzip -p colpkg/input.colpkg media) > tmp/media.pb   # protobuf index")
w(".venv/bin/python scripts/dryrun.py        # -> out/summary.json")
w(".venv/bin/python scripts/scan_patterns.py # -> out/patterns.json")
w(".venv/bin/python scripts/samples.py       # -> samples/agent*.md + manifest.json")
w(".venv/bin/python scripts/report.py        # -> report.md")
w("```")
w()
w("Read-only guarantees, verifiable in the code: every connection string is "
  "`file:…?mode=ro&immutable=1`; the zips are opened with `zipfile.ZipFile(…).read/ open` only; "
  "the input copies are never written; no Anki process is started.")
w()

open(REPORT, "w").write("\n".join(L) + "\n")
print("wrote", REPORT, len(L), "lines")
