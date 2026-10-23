"""Stage 1, step 5: 150 random notes (seed 42), stratified by ItemID chapter prefix.

Excludes notes already flagged. No vision model: this is for you to review.
"""
import csv
import collections
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O

SEED = 42
N = 150


def flagged_items():
    items = set()
    path = f"{C.OUT}/ocr_flags.json"
    if os.path.exists(path):
        items |= {r["ItemID"] for r in json.load(open(path))}
    path = f"{C.OUT}/text_hits.json"
    if os.path.exists(path):
        items |= {r["ItemID"] for r in json.load(open(path)) if r.get("ItemID")}
    return items


def ocr_status():
    """ItemID -> (flagged?, conf) from the corpus run."""
    out = {}
    path = f"{C.OUT}/ocr_results.jsonl"
    if not os.path.exists(path):
        return out
    for line in open(path):
        rec = json.loads(line)
        out[rec["ItemID"]] = rec
    return out


def main() -> None:
    rnd = random.Random(SEED)
    notes = C.live_notes()
    skip = flagged_items()
    pool = [n for n in notes if n[1] not in skip]
    strata = collections.defaultdict(list)
    for note in pool:
        parts = note[1].split("-")
        strata["-".join(parts[:2])].append(note)

    total = len(pool)
    quota = {k: max(1, round(N * len(v) / total)) for k, v in strata.items()}
    while sum(quota.values()) > N:            # trim largest quotas above 1
        k = max((k for k in quota if quota[k] > 1), key=lambda k: quota[k])
        quota[k] -= 1
    while sum(quota.values()) < N:            # top up largest strata
        k = max(quota, key=lambda k: len(strata[k]) - quota[k])
        quota[k] += 1

    picked = []
    for k, n in sorted(quota.items()):
        picked.extend(rnd.sample(strata[k], min(n, len(strata[k]))))
    picked.sort(key=lambda n: n[1])

    ocr = ocr_status()
    flagged = set()
    if os.path.exists(f"{C.OUT}/ocr_flags.json"):
        flagged = {r["ItemID"] for r in json.load(open(f"{C.OUT}/ocr_flags.json"))}
    flagged_n = sum(1 for _, item, _ in picked if item in flagged)

    with open(f"{C.OUT}/sample.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["ItemID"] + C.FIELD_NAMES[1:] + ["crop", "ocr_flagged", "ocr_conf"])
        for _, item, f in picked:
            rec = ocr.get(item)
            has = "yes" if item in flagged else "no"
            w.writerow([item] + f[1:] + [f"{C.AUDIT_MEDIA}/{item}.png", has,
                                         rec["conf"] if rec else ""])
    print("strata:", len(strata), "pool:", total, "picked:", len(picked),
          "ocr-flagged in sample:", flagged_n)


if __name__ == "__main__":
    main()