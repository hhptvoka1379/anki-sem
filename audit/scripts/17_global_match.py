"""Match every deck note against the full-book OCR index (out/ocrfull/*.txt).

For each note:
  * take distinctive tokens from the question stem (field 8),
  * find the page(s) containing them (inverted index over 902 OCR pages),
  * score the best page by token coverage + longest common substring ratio,
  * record best page, score and the printed snippet.

Output: out/global_match.csv (ItemID, page, score, coverage, stem, snippet)
A low score means the deck text does not occur anywhere in the book as OCR'd,
i.e. a candidate for real damage (or OCR noise) rather than a page problem.
"""
import csv
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import ocr_lib as O

OCR_DIR = os.path.join(C.OUT, "ocrfull")
DB = os.path.join(C.OUT, "fixed", "collection_fixed7.db")

STOP = set("""che chi cui dei del della delle dello degli nel nella nelle nello negli
sono essere viene vengono quale quali seguenti seguente risposta corretta indicare
delle nella alla alle dallo dalla degli suoi suo una uno degli questo questa come
quando dove perche perché anche solo tutti tutte ogni tra fra dopo prima durante
quale delle stesso stessa maggiore minore uguale numero valore
""".split())


def tokens(text: str):
    return [t for t in re.findall(r"[a-zàèéìòù]+", text.lower()) if len(t) >= 5]


def main() -> None:
    pages = {}
    for f in sorted(os.listdir(OCR_DIR)):
        if f.endswith(".txt"):
            p = int(re.search(r"pg-(\d+)", f).group(1))
            pages[p] = " ".join(open(os.path.join(OCR_DIR, f),
                                     encoding="utf-8", errors="ignore").read().split())
    print(f"pages: {len(pages)}", flush=True)

    tok_pages = {p: set(tokens(t)) for p, t in pages.items()}
    df = defaultdict(set)
    for p, ts in tok_pages.items():
        for t in ts:
            df[t].add(p)

    db = sqlite3.connect(f"file:{DB}?immutable=1", uri=True)
    db.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                        - (a.casefold() < b.casefold()))
    rows = db.execute("select sfld, flds from notes where mid=1813027267").fetchall()

    out = []
    for item, flds in rows:
        fields = flds.split("\x1f")
        stem = O.plain(fields[8])
        q = [t for t in tokens(stem) if t not in STOP]
        if not q:
            out.append((item, 0, 0.0, 0.0, stem[:120], ""))
            continue
        # rarest tokens carry the signal
        q_sorted = sorted(set(q), key=lambda t: len(df.get(t, ())))
        probe = q_sorted[:10]
        cand = defaultdict(int)
        for t in probe:
            for p in df.get(t, ()):
                cand[p] += 1
        if not cand:
            out.append((item, 0, 0.0, 0.0, stem[:120], ""))
            continue
        best_p, best_s, best_cov = 0, 0.0, 0.0
        for p, hits in sorted(cand.items(), key=lambda kv: -kv[1])[:15]:
            page = pages[p]
            cov = sum(1 for t in probe if t in tok_pages[p]) / len(probe)
            ratio = SequenceMatcher(None, page, stem.lower()).find_longest_match(
                0, len(page), 0, len(stem)).size / max(1, len(stem))
            s = 0.6 * cov + 0.4 * ratio
            if s > best_s:
                best_p, best_s, best_cov = p, s, cov
        snippet = ""
        if best_p:
            page = pages[best_p]
            hit = next((page.find(t) for t in probe if t in page), 0)
            snippet = page[max(0, hit - 60):hit + 180]
        out.append((item, best_p, round(best_s, 3), round(best_cov, 3),
                    stem[:120], snippet))

    path = os.path.join(C.OUT, "global_match.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ItemID", "page", "score", "coverage", "stem", "snippet"])
        w.writerows(out)
    good = sum(1 for r in out if r[2] >= 0.55)
    mid = sum(1 for r in out if 0.35 <= r[2] < 0.55)
    bad = sum(1 for r in out if r[2] < 0.35)
    print(f"notes: {len(out)}  score>=0.55: {good}  0.35-0.55: {mid}  <0.35: {bad}")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
