"""Stage 1, step 4: scripted Tesseract cross-check over every question crop.

No vision model. Each note's crop is OCR'd once (cached), then the stem and each
option are compared against it. Flags: LOST_BLANK, CHAR_SWAP, NUMBER_FOR_WORD,
LOW_SIM. LOW_CONF is kept separate so layout noise does not drown real hits.
"""
import json
import multiprocessing as mp
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O

CACHE_PATH = f"{C.OUT}/ocr_cache.json"
RESULT_PATH = f"{C.OUT}/ocr_results.jsonl"


def work(args):
    item, stem, opts = args
    cache = {}
    tmpdir = tempfile.mkdtemp(prefix="ocrc_")
    path = f"{C.AUDIT_MEDIA}/{item}.png"
    try:
        rec = O.ocr_crop(path, cache, tmpdir)
    except Exception as exc:                      # noqa: BLE001
        return {"ItemID": item, "error": repr(exc)}
    tokens = rec["norm"].split()
    segs = [("FrontStemHTML", stem)] + [(f"FrontOptionsHTML:{l}", b) for l, b in opts]
    out = []
    for field, text in segs:
        plain = O.plain(text) if "<" in text else text
        ratio, window = O.best_match(plain, tokens)
        swaps = O.char_swaps(plain, window)
        nums = O.token_type_diffs(plain, window)
        out.append({"field": field, "text": plain, "ratio": round(ratio, 4),
                    "window": window, "swaps": swaps, "nums": nums})
    blank_lost = bool(rec["rules"]) and "<BLANK>" not in O.plain(stem)
    return {"ItemID": item, "ocr": rec["text"], "norm": rec["norm"],
            "conf": rec["mean_conf"], "rules": len(rec["rules"]),
            "blank_lost": blank_lost, "segments": out,
            "cache_key": f"{item}.png", "cache": rec}


def categorise(text, window, ratio):
    a = O.strip_blanks(text).split()
    b = window.split()
    missing = [w for w in a if w not in b]
    extra = [w for w in b if w not in a]
    if missing and not extra:
        return "MISSING_WORDS"
    if extra and not missing:
        return "EXTRA_WORDS"
    return "OTHER" if ratio < 0.9 else "OK"


def grade(rec):
    """Turn one OCR record into flag rows."""
    rows = []
    low_conf = rec["conf"] < 60
    for seg in rec["segments"]:
        base = {"ItemID": rec["ItemID"], "field": seg["field"],
                "card": seg["text"], "ocr": seg["window"],
                "similarity": seg["ratio"], "conf": rec["conf"],
                "crop": f"{C.AUDIT_MEDIA}/{rec['ItemID']}.png"}
        if seg["field"] == "FrontStemHTML" and rec["blank_lost"]:
            rows.append({**base, "category": "LOST_BLANK"})
        for x, y in seg["swaps"]:
            rows.append({**base, "category": "CHAR_SWAP",
                         "card": seg["text"], "ocr": seg["window"],
                         "detail": f"{x} -> {y}"})
        for x, y in seg["nums"]:
            rows.append({**base, "category": "NUMBER_FOR_WORD",
                         "detail": f"{x} -> {y}"})
        if seg["ratio"] < 0.90 and len(O.strip_blanks(seg["text"])) >= 12:
            rows.append({**base,
                         "category": categorise(seg["text"], seg["window"], seg["ratio"])})
    if low_conf:
        for row in rows:
            row["low_conf"] = True
    return rows


def main() -> None:
    live = C.live_notes()
    tasks = [(item, f[8], O.options(f[10])) for _, item, f in live]
    workers = min(8, os.cpu_count() or 4)
    cache, records = {}, []
    with mp.Pool(workers) as pool:
        for i, rec in enumerate(pool.imap_unordered(work, tasks, chunksize=8), 1):
            if "error" in rec:
                print("ERROR", rec["ItemID"], rec["error"])
                continue
            cache[rec.pop("cache_key")] = rec["cache"]
            records.append(rec)
            if i % 500 == 0:
                print(f"  {i}/{len(tasks)}", flush=True)

    os.makedirs(C.OUT, exist_ok=True)
    json.dump(cache, open(CACHE_PATH, "w"))
    with open(RESULT_PATH, "w") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    flags = []
    for rec in records:
        flags.extend(grade(rec))
    json.dump(flags, open(f"{C.OUT}/ocr_flags.json", "w"), ensure_ascii=False)
    import collections
    print("notes OCR'd:", len(records))
    print("flags:", len(flags), collections.Counter(f["category"] for f in flags))
    print("low_conf notes:", sum(1 for r in records if r["conf"] < 60))
    print("notes with rule detected:", sum(1 for r in records if r["rules"]))


if __name__ == "__main__":
    main()
