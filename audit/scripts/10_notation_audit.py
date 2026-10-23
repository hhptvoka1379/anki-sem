"""10% notation audit: chemical formulas, charges, sub/superscripts.

Two passes:
  A. 695 notes (10.0% of 6,948) sampled with a fixed seed, stratified by
     subject, plus every note carrying a defect-prone notation class
     (asterisk, '#', sqrt, 10^), because those classes are rare and cheap.
  B. each sampled note's formula-like tokens compared with the OCR text of its
     own question scan, normalising unicode sub/superscripts to ASCII.

OCR is not ground truth for superscripts, so every disagreement is written out
for visual confirmation instead of being counted as an error.
"""
import collections
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import ocr_lib as O

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉₊₋", "0123456789+-")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-")

CLASSES = {
    "ASTERISK_SUP": re.compile(r"\b[A-Za-z]{1,3}\*"),
    "HASH_FOR_NEQ": re.compile(r"(?<![\w#])#\s?\d"),
    "SQRT": re.compile(r"√"),
    "TEN_POWER": re.compile(r"10\s?\^"),
    "BROKEN_SUB": re.compile(r"[A-Z][a-z]?,\d"),
    "MOJIBAKE": re.compile(r"Ã.|â€"),
}


def tokens(text):
    """Formula-ish tokens: anything with a digit or a sub/superscript char."""
    out = set()
    for t in re.findall(r"[^\s,;:]+", text):
        if re.search(r"[0-9\u2080-\u209c\u2070-\u207f]", t) and len(t) <= 24:
            out.add(t.strip("().[]"))
    return {t for t in out if t}


def norm(t):
    return t.translate(SUB).translate(SUP).replace(" ", "").lower()


def main() -> None:
    live = [(item, f) for _, item, f in C.live_notes()]
    by_subject = collections.defaultdict(list)
    for item, f in live:
        by_subject[f[2]].append((item, f))

    rng = random.Random(7)
    sample = []
    for subj, rows in sorted(by_subject.items()):
        k = round(695 * len(rows) / len(live))
        sample += rng.sample(rows, k)
    forced = [(i, f) for i, f in live
              if any(p.search(" ".join(f[8:17])) for p in CLASSES.values())]
    forced_items = {i for i, _ in forced}
    sample_items = {i for i, _ in sample}
    extra = [(i, f) for i, f in forced if i not in sample_items]
    universe = sample + extra

    cache = json.load(open(f"{C.OUT}/ocr_cache.json"))
    rows, counts = [], collections.Counter()
    for item, f in universe:
        text = O.plain(" ".join(f[8:17]))
        card_tokens = tokens(text)
        ocr = cache.get(f"{item}.png", {}).get("text", "")
        ocr_tokens = {norm(t) for t in tokens(ocr)}
        missing = sorted(t for t in card_tokens if norm(t) not in ocr_tokens)
        hits = [k for k, p in CLASSES.items() if p.search(text)]
        for k in hits:
            counts[k] += 1
        if missing:
            counts["TOKEN_NOT_IN_OCR"] += 1
        rows.append({"ItemID": item, "subject": f[2], "classes": hits,
                     "missing": missing[:8], "n_tokens": len(card_tokens)})

    sample_only = [r for r in rows if r["ItemID"] in sample_items]
    clean = sum(1 for r in sample_only if not r["missing"])
    out = {
        "universe": len(live),
        "sample": len(sample),
        "sample_pct": round(100 * len(sample) / len(live), 2),
        "forced_extra": len(extra),
        "audited": len(rows),
        "sample_notes_with_all_tokens_in_ocr": clean,
        "sample_notes_clean_pct": round(100 * clean / max(1, len(sample_only)), 1),
        "class_counts": dict(counts),
    }
    print(json.dumps(out, indent=2))
    with open(f"{C.OUT}/notation_audit.csv", "w") as fh:
        fh.write("ItemID,subject,classes,missing_tokens,n_tokens\n")
        for r in rows:
            fh.write("%s,%s,%s,%s,%d\n" % (r["ItemID"], r["subject"],
                                           "|".join(r["classes"]),
                                           "|".join(r["missing"]),
                                           r["n_tokens"]))
    json.dump(out, open(f"{C.OUT}/notation_audit.json", "w"), indent=2)
    worst = sorted([r for r in rows if r["missing"]],
                   key=lambda r: -len(r["missing"]))[:12]
    print("\nmost disagreements:")
    for r in worst:
        print(" ", r["ItemID"], r["classes"], r["missing"][:5])


if __name__ == "__main__":
    main()
