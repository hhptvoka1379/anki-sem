"""Re-grade OCR results after narrowing blank-rule detection.

Table borders were being read as fill-in blanks. A real blank rule is a short
line (4-55% of the image width); a table border spans most of the width.
Uses the cached OCR text, so no crop is re-OCR'd.
"""
import json
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O
import importlib.util

spec = importlib.util.spec_from_file_location("ocr4", "scripts/04_ocr_corpus.py")
ocr4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ocr4)


def main() -> None:
    cache = json.load(open(f"{C.OUT}/ocr_cache.json"))
    results = [json.loads(l) for l in open(f"{C.OUT}/ocr_results.jsonl")]
    live = {item: f for _, item, f in C.live_notes()}

    kept = dropped = 0
    flags = []
    for rec in results:
        rules = cache.get(f"{rec['ItemID']}.png", {}).get("rules", [])
        key = f"{rec['ItemID']}.png"
        width = Image.open(f"{C.AUDIT_MEDIA}/{key}").width * cache.get(key, {}).get("scale", 1)
        good = [r for r in rules
                if 0.04 * width <= (r["x1"] - r["x0"]) <= 0.55 * width]
        kept += len(good)
        dropped += len(rules) - len(good)
        rec["rules"] = len(good)
        flds = live[rec["ItemID"]]
        completamento = "completamento" in flds[5].lower()
        rec["blank_lost"] = (bool(good) and completamento
                             and "<BLANK>" not in O.plain(flds[8]))
        if good and not completamento:
            rec["rule_on_mcq"] = True
        flags.extend(ocr4.grade(rec))

    json.dump(flags, open(f"{C.OUT}/ocr_flags.json", "w"), ensure_ascii=False)
    import collections
    print("rules kept:", kept, "dropped as table borders:", dropped)
    print("flags:", len(flags), collections.Counter(f["category"] for f in flags))
    print("notes with a real blank rule:",
          sum(1 for r in results if r["rules"]))


if __name__ == "__main__":
    main()
