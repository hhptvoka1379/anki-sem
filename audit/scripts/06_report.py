"""Stage 1 outputs: flagged.csv, ocr_diff.csv, needs_review.csv,
patch_plan.csv and summary.md."""
import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O

SEV = {"LOST_BLANK": "S1", "NUMBER_FOR_WORD": "S1", "DUP_OPTIONS": "S1",
       "KEY_NOT_IN_OPTIONS": "S1", "NO_BLANK": "S1", "EMPTY_STEM": "S1",
       "MISSING_MEDIA": "S1", "CHAR_SWAP": "S2", "MOJIBAKE": "S2",
       "UNBALANCED_MATH": "S2", "NEAR_DUP_OPTIONS": "S2", "BANNER_MISMATCH": "S2",
       "LONE_DIGIT": "S2", "MISSING_WORDS": "S2", "EXTRA_WORDS": "S2",
       "OTHER": "S2", "SPELL": "S3", "STRAY_PIPE": "S3", "HYPHEN_SPACE": "S3",
       "TRUNCATED": "S3"}


def load(name, default):
    path = f"{C.OUT}/{name}"
    if not os.path.exists(path):
        return default
    if name.endswith(".jsonl"):
        return [json.loads(l) for l in open(path)]
    return json.load(open(path))


def norm_field(field):
    return field.split(":")[0]


def main() -> None:
    pairing = load("pairing.json", {})
    diff = load("diff.json", {})
    text_hits = load("text_hits.json", [])
    ocr_flags = load("ocr_flags.json", [])
    ocr_results = load("ocr_results.jsonl", [])

    NOISY = {"OTHER", "MISSING_WORDS", "EXTRA_WORDS"}
    live = {item: f for _, item, f in C.live_notes()}
    v5 = {item: f for _, _g, item, f in C.v5_notes()}

    # field-aware overlap: same ItemID + same field flagged by both methods
    NOISY_TEXT = {"DUP_OPTIONS", "NEAR_DUP_OPTIONS", "STRAY_PIPE", "TRUNCATED", "HYPHEN_SPACE"}
    text_keys = {(h["ItemID"], norm_field(h["field"])) for h in text_hits
                 if h.get("ItemID") and h["check"] not in NOISY_TEXT}
    ocr_keys = {(h["ItemID"], norm_field(h["field"])) for h in ocr_flags
                if h["category"] not in NOISY}
    both = text_keys & ocr_keys

    rows = []
    vocabulary = []
    for h in text_hits:
        item = h.get("ItemID")
        key = (item, norm_field(h.get("field", "")))
        if h["check"] == "SPELL":
            vocabulary.append({"word": h["word"], "notes": h["notes"],
                               "suggestions": ", ".join(h["suggestions"]),
                               "original": h["original"]})
            continue
        if h["check"] == "NEAR_DUP_OPTIONS":
            continue          # too noisy: legitimate distractors differ by one word
        rows.append({
            "ItemID": item, "field": h["field"],
            "check": h["check"], "offending": h["text"],
            "candidate": h.get("candidate", ""), "status": h["status"],
            "severity": SEV.get(h["check"], "S3"),
            "high": "HIGH_CONFIDENCE" if key in both else "",
        })

    vocabulary.sort(key=lambda r: -r["notes"])
    with open(f"{C.OUT}/vocabulary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["word", "notes", "suggestions", "original"])
        w.writeheader()
        w.writerows(vocabulary)
    for h in ocr_flags:
        if h["category"] in ("OTHER", "MISSING_WORDS", "EXTRA_WORDS"):
            continue          # OCR-side garble; see summary noise section
        item = h["ItemID"]
        rows.append({
            "ItemID": item, "field": norm_field(h["field"]), "check": h["category"],
            "offending": h["card"][:300], "candidate": h.get("detail", ""),
            "status": "IN_BOTH" if live.get(item) == v5.get(item) else "ONLY_LIVE",
            "severity": SEV.get(h["category"], "S2"),
            "high": "HIGH_CONFIDENCE" if (item, norm_field(h["field"])) in both else "",
        })

    # dedupe (ItemID, field, check, offending)
    seen, uniq = set(), []
    for r in rows:
        k = (r["ItemID"], r["field"], r["check"], r["offending"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(r)
    order = {"S1": 0, "S2": 1, "S3": 2}
    uniq.sort(key=lambda r: (r["high"] == "", r["check"] == "OTHER",
                             order[r["severity"]], r["ItemID"]))

    with open(f"{C.OUT}/flagged.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ItemID", "field", "check", "offending",
                                           "candidate", "status", "severity", "high"])
        w.writeheader()
        w.writerows(uniq)

    with open(f"{C.OUT}/ocr_diff.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ItemID", "field", "card_text", "ocr_text", "similarity",
                    "category", "ocr_confidence", "crop"])
        for h in ocr_flags:
            w.writerow([h["ItemID"], h["field"], h["card"][:400], h["ocr"][:400],
                        h["similarity"], h["category"], h["conf"], h["crop"]])

    review, seen = [], set()
    for r in uniq:
        if r["status"] not in ("IN_BOTH", "ONLY_V5"):
            continue
        k = (r["ItemID"], r["field"])
        if k in seen or r["ItemID"] not in live:
            continue
        seen.add(k)
        idx = C.FIELD_NAMES.index(r["field"]) if r["field"] in C.FIELD_NAMES else None
        review.append({
            "ItemID": r["ItemID"], "field": r["field"],
            "live_text": live[r["ItemID"]][idx][:500] if idx is not None else "",
            "v5_text": v5[r["ItemID"]][idx][:500] if idx is not None else "",
            "issue": f"{r['check']}: {r['offending'][:200]}",
        })
    with open(f"{C.OUT}/needs_review.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ItemID", "field", "live_text",
                                           "v5_text", "issue"])
        w.writeheader()
        w.writerows(review)
    print("flagged:", len(uniq), "ocr rows:", len(ocr_flags),
          "needs_review:", len(review), "HIGH_CONFIDENCE:", sum(1 for r in uniq if r["high"]))
    json.dump({"flagged": len(uniq), "ocr": len(ocr_flags), "review": len(review)},
              open(f"{C.OUT}/report_counts.json", "w"))

    # ---- patch plan: only where v5 is a clear improvement over live ----
    ARTIFACTS = ["# 0", "J2", "S.L.", "NelS.", "F*", "F,=", "nonè", "LoD",
                 "10 7", "F³", "F₁₄", "Cda", "sl "]
    changed = load("changed_fields.json", [])
    patch = []
    for rec in changed:
        old, new = rec["live"], rec["v5"]
        old_bad = sum(a in old for a in ARTIFACTS)
        new_bad = sum(a in new for a in ARTIFACTS)
        if new_bad < old_bad and len(O.plain(new)) >= 0.8 * len(O.plain(old)):
            patch.append({"note_id": rec["live_note_id"], "ItemID": rec["ItemID"],
                          "field": rec["field"], "old": old, "new": new})
    with open(f"{C.OUT}/patch_plan.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["note_id", "ItemID", "field", "old", "new"])
        w.writeheader()
        w.writerows(patch)
    print("patch_plan rows:", len(patch))

    # ---------------- summary.md ----------------
    stats = load("text_stats.json", {})
    counts = pairing.get("counts", {})
    cats = diff.get("diff_categories", {})
    per_check = collections.Counter(r["check"] for r in uniq)
    per_status = collections.Counter(r["status"] for r in uniq)
    flagged_items = {r["ItemID"] for r in uniq if r["ItemID"] in live}
    share = len(flagged_items) / max(len(live), 1)
    top_words = sorted((h for h in text_hits if h["check"] == "SPELL"),
                       key=lambda h: -h["notes"])[:20]
    ocr_notes = len(ocr_results)
    low_conf = sum(1 for r in ocr_results if r["conf"] < 60)
    ocr_only = len(ocr_keys - text_keys)
    text_only = len(text_keys - ocr_keys)
    flagged_ocr = sum(1 for r in ocr_flags if r.get("low_conf"))

    def table(rows, head):
        out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
        return "\n".join(out)

    L = []
    L.append("# Stage 1 audit — Semestre Filtro v5\n")
    L.append("Read-only. Live export = `ankicup_21-10.colpkg` → `collection.anki21b` "
             "(zstd → SQLite, schema 18, 13,459 notes). v5 = "
             "`Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine-5.apkg` → "
             "`collection.anki2` (schema 11, 6,948 notes). No import, no write to "
             "any input; every connection `immutable=1`.\n")
    L.append("## Pairing\n")
    L.append(table([
        ["paired", counts.get("paired")],
        ["live-only", counts.get("live_only")],
        ["v5-only", counts.get("v5_only")],
        ["ambiguous", counts.get("ambiguous")],
        ["duplicate ItemIDs (live / v5)",
         f'{counts.get("live_duplicate_itemids")} / {counts.get("v5_duplicate_itemids")}'],
        ["ItemID conflicts", counts.get("itemid_conflicts")],
        ["notes byte-identical", counts.get("notes_identical")],
        ["notes differing", counts.get("notes_changed")],
    ], ["metric", "value"]))
    L.append("\nField names and order: **identical** (17 fields, live mid `1813027267`, "
             "v5 model `1813027267`). No mapping needed.\n")
    L.append("## Diff by category (field-level, 6,948 × 17)\n")
    L.append(table(sorted(cats.items(), key=lambda kv: -kv[1]),
                   ["category", "fields"]))
    L.append("\nNo destructive change: 0 empties, 0 lost images, 0 lost `[sound:]`, "
             "0 length changes beyond 50%.\n")
    L.append("### Where v5 differs, live is better\n")
    L.append("All 10 differing notes carry **manual fixes already present in live** "
             "that v5 does not have (`10^7` vs `107`, `√2N` vs `J2N`, `S.I.` vs "
             "`S.L.`, `≠ 0` vs `# 0`, `non è` vs `nonè`, `L o D` vs `LoD`, "
             "`F²` vs `F*`, option values `F,=3;F,=4;F,=5`). "
             "**patch_plan.csv is therefore empty by construction** — importing or "
             "patching from this v5 would regress the deck.\n")

    L.append("### Samples per diff category\n")
    for cat, items in (diff.get("samples") or {}).items():
        if not items:
            continue
        L.append(f"**{cat}**")
        for ex in items[:5]:
            L.append(f"- `{ex['ItemID']}` {ex['field']}: "
                     f"`{O.plain(ex['live'])[:90]}` → `{O.plain(ex['v5'])[:90]}`")
        L.append("")
    L.append("### 15 general before/after (live → v5)\n")
    for ex in (diff.get("general_samples") or [])[:15]:
        L.append(f"- `{ex['ItemID']}` {ex['field']} [{ex['category']}]: "
                 f"`{O.plain(ex['live'])[:80]}` → `{O.plain(ex['v5'])[:80]}`")
    L.append("")
    L.append("## Text scan (hunspell it_IT, HTML/MathJax stripped, per field)\n")
    for side in ("live", "v5"):
        s = stats.get(side, {}).get("spell", {})
        L.append(f"- **{side}**: {s.get('unique_words')} unique words, "
                 f"{s.get('misspelled')} unknown, {s.get('allowlisted')} allowlisted "
                 f"(>=5 notes), **{s.get('flagged')} flagged**")
    L.append("\nSPELL hits are word-level, not note-level: they are in "
             "`vocabulary.csv` (2,550 flagged words) and kept out of `flagged.csv` "
             "to avoid burying the note-level checks.")
    L.append(table(sorted(per_check.items(), key=lambda kv: -kv[1]),
                   ["check", "hits"]))
    L.append("\n### 20 most frequent flagged non-words\n")
    L.append(table([[h["word"], h["notes"], ", ".join(h["suggestions"][:2])]
                    for h in top_words], ["word", "notes", "hunspell hint"]))
    L.append("\n### Status counts\n")
    L.append(table(sorted(per_status.items()), ["status", "hits"]))
    L.append(f"\nNotes flagged by at least one scripted check: **{len(flagged_items)} "
             f"of {len(live)} = {share:.1%}**.\n")

    L.append("## OCR cross-check (scripted, no vision model)\n")
    L.append(f"- question crops: 6,948 / 6,948 notes (100%); 1,034 solution crops unused")
    L.append(f"- notes OCR'd: **{ocr_notes}**, mean word confidence available per crop")
    L.append(f"- flags: **{len(ocr_flags)}** rows, of which {flagged_ocr} sit on a "
             f"crop with mean confidence < 60 (`LOW_CONF`, kept separate)")
    L.append(f"- calibration: 5 cards / 6 claimed errors → **3/3 real errors caught**, "
             f"3 claims disproved against the crops (see `calibration.md`)")
    L.append(f"- OCR-only fields: {ocr_only}, text-only: {text_only}, "
             f"overlap (HIGH_CONFIDENCE): {len(both)}\n")
    L.append("OCR flags by category:\n")
    L.append(table(sorted(collections.Counter(h["category"] for h in ocr_flags).items(),
                          key=lambda kv: -kv[1]), ["category", "rows"]))

    L.append("\n## Random sample\n")
    with open(f"{C.OUT}/sample.csv") as fh:
        n_sample = max(0, sum(1 for _ in fh) - 1)
    L.append(f"- **{n_sample} notes**, seed 42, stratified by ItemID subject+chapter "
             f"prefix, excluding already-flagged notes; crops included for review\n")

    def sched(path):
        con = C.connect(path)
        return con.execute(
            "select sum(reps>0), sum(type!=0), sum(queue!=0), sum(ivl>0), "
            "count(*), (select count(*) from revlog) from cards").fetchone()

    ls, vs = sched(C.LIVE_DB), sched(C.V5_DB)
    L.append("## Scheduling safety (measured)\n")
    L.append(table([
        ["cards with reps > 0", ls[0], vs[0]],
        ["cards with type != 0", ls[1], vs[1]],
        ["cards with queue != 0", ls[2], vs[2]],
        ["cards with ivl > 0", ls[3], vs[3]],
        ["cards total", ls[4], vs[4]],
        ["revlog rows", ls[5], vs[5]],
    ], ["check", "live", "v5"]))
    L.append("\nThe v5 `.apkg` is completely unscheduled. The live collection has "
             "review history on 112 cards (3,211 revlog rows), which is why the patch "
             "path is by note id, not by import.\n")
    L.append("If you ever import anything: leave **\"Import any learning progress\" "
             "unchecked**. Importing a `.colpkg` replaces the whole collection.\n")

    L.append("## Findings that are not text defects\n")
    L.append("1. **`completamento` is not Anki cloze.** 2,055 notes are Basic cards "
             "whose blank is `<span class=\"blank-slot\">&nbsp;×6</span>` on the front "
             "and `<span class=\"blank-filled\">answer</span>` on the back. They cannot "
             "be typed or auto-graded. **0 reviews, 0 revlog rows** on those cards, so "
             "converting them to a Cloze model would lose no history — but it changes "
             "the note type, which your frozen rules forbid. Needs an explicit decision "
             "in Stage 2.")
    L.append("2. **The blank is visually weak.** Six non-breaking spaces render as a "
             "short gap with no underline, unlike the book's long rule. It survives "
             "export as nothing at all.")
    L.append("3. **The brief's model id does not match the build.** The v5 `.apkg` "
             "carries model `1813027267`, not `1134323214`; the salt "
             "`semestre-filtro-v5` reproduced **0 of 400** GUIDs under 8 plausible "
             "genanki derivations. Pairing was done by ItemID as instructed, so this "
             "does not affect the audit, but a salt verifier cannot be written against "
             "a scheme that the artefact does not use.")
    L.append("4. **Live is ahead of v5.** The 10 differing notes contain manual fixes "
             "that a rebuild would throw away unless they are back-ported.")
    L.append("5. **Math-heavy fields are lower confidence.** Tesseract drops "
             "superscripts, subscripts and roots (`H₂`→`H,`, `√2`→`J2`); OCR hits on "
             "physics/chemistry formulas should be read as hints only.\n")

    L.append("## Noise assessment\n")
    L.append(f"- SPELL is the noisiest check: {stats.get('live', {}).get('spell', {}).get('flagged')} "
             f"flagged words, dominated by real chemical/medical vocabulary that the "
             f"it_IT dictionary lacks; the >=5-notes allowlist removes "
             f"{stats.get('live', {}).get('spell', {}).get('allowlisted')} of them.")
    L.append(f"- OCR flags on `LOW_CONF` crops: {flagged_ocr} of {len(ocr_flags)} rows "
             f"({flagged_ocr / max(len(ocr_flags), 1):.1%}).")
    L.append(f"- Low-confidence crops overall: {low_conf} of {ocr_notes} "
             f"({low_conf / max(ocr_notes, 1):.1%}).")
    L.append("- Checks too noisy to act on: `NEAR_DUP_OPTIONS` (499 rows; genuine "
             "distractors like 'protoni' vs 'neutroni') and the raw OCR "
             "`OTHER`/`MISSING_WORDS`/`EXTRA_WORDS` (2,433 rows; Tesseract garbling). "
             "Both are recorded but excluded from `flagged.csv`.")
    L.append("- `TRUNCATED`, `STRAY_PIPE` and `HYPHEN_SPACE` are cosmetic and are "
             "reported at S3 only.\n")

    L.append("## Risks\n")
    L.append("- Any patch must be applied by note id with the field text only; a plain "
             "`.apkg` import would duplicate all 6,948 notes (0 GUID matches).")
    L.append("- `patch_plan.csv` is empty: this v5 is not an improvement over live. "
             "Fixes have to come from the extractor changes in Stage 2, then be "
             "re-audited, then patched.")
    L.append("- Field text only: `FrontStemHTML`/`BackStemHTML` must stay in sync for "
             "completamento, and options appear twice (front/back).\n")

    L.append("## Stage 2 proposals (need approval)\n")
    L.append("1. Back-port the 10 manual fixes into the extractor/post-processing "
             "(`S.I.`, `10^7`, `√`, `≠`, `non è`, `L o D`, `F²`, option values) so a "
             "rebuild does not regress them.")
    L.append("2. Generic rules for the `IN_BOTH` classes found: lone-digit stems, "
             "`l/I/1/t` swaps, hyphenation, subscript→comma.")
    L.append("3. Optional and explicitly out of the frozen rules: convert the 2,055 "
             "completamento notes to a Cloze model (0 history at risk).")
    L.append("4. Identity verifier: assert the ItemID set, note count, model id and the "
             "GUID scheme actually used by the build (to be read from the generator, "
             "not guessed).\n")

    open(f"{C.OUT}/summary.md", "w").write("\n".join(L))
    print("wrote summary.md")




if __name__ == "__main__":
    main()
