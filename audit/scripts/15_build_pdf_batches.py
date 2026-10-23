"""Turn located.json into agent batches (page image + keywords + exercise no.)."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


def main() -> None:
    loc = json.load(open(f"{C.OUT}/located.json"))
    items = {x["ItemID"]: x for x in json.load(open(f"{C.OUT}/pdf_reextract.json"))}
    good = []
    for row in loc:
        base = items[row["ItemID"]]
        if not row["found_page"]:
            continue
        good.append({
            "ItemID": row["ItemID"],
            "page": row["found_page"],
            "page_image": f"{C.OUT}/pages/p{row['found_page']}-{row['found_page']:03d}.png",
            "score": row["score"],
            "keywords": row["keys"],
            "current_stem": base["stem"],
            "current_options": base["options"],
        })
    good.sort(key=lambda r: -r["score"])
    n = 4
    for i in range(n):
        batch = good[i::n]
        json.dump(batch, open(f"{C.OUT}/pdf_batch2_{i}.json", "w"), indent=1,
                  ensure_ascii=False)
        print(f"batch2_{i}: {len(batch)}  scores {[b['score'] for b in batch]}")
    print("located:", len(good), "unlocated:", len(loc) - len(good))


if __name__ == "__main__":
    main()
