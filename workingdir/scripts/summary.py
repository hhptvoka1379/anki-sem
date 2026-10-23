#!/usr/bin/env python3
"""Print the dry-run summary table to the terminal."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open(os.path.join(BASE, "out", "summary.json")))

print()
print("=" * 78)
print(" DRY RUN: candidate .apkg -> live collection (nothing modified)")
print("=" * 78)
print(" live : %d notes, %d cards   (%s)" % (S["live_notes"], S["live_cards"], S["live_semestre_cards"]))
print(" apkg : %d notes, %d cards" % (S["apkg_notes"], S["apkg_cards"]))
print("-" * 78)
print(" Would UPDATE (GUID match) : %d" % S["guid_matched"])
print(" Would ADD (duplicates?)   : %d  (%d share an ItemID with a live note)"
      % (S["apkg_only"], S["itemid_pairs"]))
print(" Untouched                 : %d live notes" % S["live_notes"])
print("-" * 78)
print(" Changed fields by category (fallback-paired, %d pairs, %d field diffs):"
      % (S["itemid_pairs"], S["itemid_diff_fields"]))
for k, label in (("neq", "≠ fixes"), ("exponents", "exponents/powers"),
                 ("roots", "√ / roots"), ("whitespace-html", "whitespace/HTML-only"),
                 ("other", "other")):
    print("   %-22s %6d field instances  (%d notes)" % (label, S["cat_field"].get(k, 0),
                                                       S["cat_note"].get(k, 0)))
print("-" * 78)
print(" Risks:")
print("   - GUID overlap 0.0% -> full duplicate set, review history not transferred")
print("   - note type differs: 17 fields (live) vs 16 (apkg), QuestionScanHTML missing")
print("   - candidate is OLDER than live: 17 'FAL- SA', 57 'll legame', 276 hyphen-junk")
print("     vs 0 / 0 / 20 in live -> a merge would revert fixes")
print("   - 5 real losses: 4 cards whose figure the apkg lacks, 1 explanation emptied")
print("   - 748 tag differences (con_figura marker only)")
print("   - scheduling: all %d cards type=0/reps=0/ivl=0, revlog empty"
      % S["apkg_cards"])
print()
print(" Mistake hunt (live deck, 45 cards x vision): 24 defective, 3 S1")
print("   - subscript -> comma (H₂ -> 'H,', PIP₃ -> 'PIP,', ClO₄⁻ -> 'CIO,')")
print("   - Il -> 0 and L' -> 1 before a blank; l -> ) ! i (HCl -> HC))")
print("   - multiplication dot -> hyphen (kcal/kg·°C -> kcal/kg - °C)")
print("   - option lists bifurcated (book D/E -> card D/E both wrong)")
print("   - rewritten stems presented as OCR (BIO-C04-COMM-057)")
print("-" * 78)
print(" VERDICT: NOT SAFE TO IMPORT")
print("   reason: 0 GUID matches (adds %d duplicates) AND the candidate is the" % S["apkg_notes"])
print("   pre-correction build (merging reverts fixes).")
print("   do: regenerate the .apkg with GUIDs derived from ItemID, re-run this")
print("   dry run, expect %d matches / 0 added, then import with" % S["itemid_pairs"])
print("   Update notes = Always and 'Import any learning progress' OFF.")
print(" Full report: %s" % os.path.join(BASE, "report.md"))
print("=" * 78)
