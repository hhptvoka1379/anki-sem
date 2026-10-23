"""Stage 1, step 4 calibration: the five cards already checked by eye.

Prints, per card, whether the scripted cross-check would catch the known error.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O

CASES = [
    ("CHIM-C06-COMP-024", "brief: lost ______ gap", "stem"),
    ("CHIM-C13-NCOM-103", "option A acetaltico -> acetilico", "option A"),
    ("CHIM-C07-COMP-012", "lost blank ('La legge di ______ massa')", "stem"),
    ("CHIM-C07-COMP-012", "'sl' for 'si'", "stem"),
    ("CHIM-C09-COMP-032", "'Il ______' became '0'", "stem"),
    ("CHIM-C11-NCOM-161", "option E tdrogenoc. -> Idrogenoc.", "option E"),
]


def segments(f):
    stem = O.plain(f[8])
    segs = [("stem", stem)]
    for letter, body in O.options(f[10]):
        segs.append((f"option {letter}", body))
    return segs


def main() -> None:
    cache_path = f"{C.OUT}/ocr_cache.json"
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    tmpdir = tempfile.mkdtemp(prefix="ocr_")
    live = {item: f for _, item, f in C.live_notes()}
    results = {}
    for item in dict.fromkeys(c[0] for c in CASES):
        f = live[item]
        crop = f"{C.AUDIT_MEDIA}/{item}.png"
        rec = O.ocr_crop(crop, cache, tmpdir)
        toks = rec["norm"].split()
        rows = []
        for name, text in segments(f):
            ratio, window = O.best_match(text, toks)
            swaps = O.char_swaps(text, window)
            nums = O.token_type_diffs(text, window)
            rows.append({"seg": name, "ratio": round(ratio, 3),
                         "swaps": swaps, "nums": nums, "window": window, "text": text})
        results[item] = {"ocr": rec["text"], "rules": rec["rules"],
                         "mean_conf": rec["mean_conf"], "segs": rows}
    json.dump(cache, open(cache_path, "w"))

    for case, desc, seg_name in CASES:
        r = results[case]
        seg = next((s for s in r["segs"] if s["seg"] == seg_name), None)
        print("=" * 90)
        print(f"{case} :: {desc}")
        print(f"  rules={len(r['rules'])} mean_conf={r['mean_conf']}")
        print(f"  ocr: {r['ocr'][:160]!r}")
        if seg:
            print(f"  {seg['seg']}: ratio={seg['ratio']} swaps={seg['swaps']} num_for_word={seg['nums']}")
            print(f"    card: {seg['text']!r}")
            print(f"    best: {seg['window']!r}")
        if seg_name == "stem":
            print(f"  blank in card: {'<BLANK>' in O.plain(live[case][8])}")
    print(json.dumps({k: {"rules": len(v["rules"]), "conf": v["mean_conf"]}
                      for k, v in results.items()}, indent=2))


if __name__ == "__main__":
    main()
