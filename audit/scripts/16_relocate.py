"""Locate exercises by OCR-searching page ranges of the master PDF.

Rendering is serial (concurrent pdftoppm truncates PNGs); OCR runs in parallel.
Results: out/relocate.json  {ItemID: [{page, score, snippet}]}
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O

PDF = ("/Users/db/Documents/projects/anki/"
       "Eserciziario Unico per il Semestre Filtro  2.pdf")   # full-res master, 902 pp, no text layer
OUT = os.path.join(C.OUT, "pages3")
TESS = "/opt/homebrew/bin/tesseract"
TESSDATA = "/Users/db/Documents/projects/anki/_tools/tessdata"
DPI = 200

TARGETS = {
    "CHIM-C10-NCOM-019": (148, 172, "formula dell'acido solforico"),
    "CHIM-C11-COMM-038": (168, 194, "minima concentrazione ioni"),
    "BIO-C06-COMM-030": (512, 562, "recettore nicotinico acetilcolina"),
    "CHIM-C11-NCOM-097": (168, 194, "soluzione pH"),
    "CHIM-C12-COMM-032": (196, 220, "composti organici doppio legame"),
}


def render(page):
    png = os.path.join(OUT, f"p{page}.png")
    if not os.path.exists(png):
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(DPI),
                        "-png", "-singlefile", PDF, png[:-4]], check=True)
    return png


def ocr(png):
    txt = png.replace(".png", ".txt")
    if not os.path.exists(txt):
        subprocess.run([TESS, png, txt[:-4], "-l", "ita", "--tessdata-dir", TESSDATA,
                        "--psm", "1"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return open(txt, encoding="utf-8", errors="ignore").read()


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):          # drop renders from any other source PDF
        if f.endswith((".png", ".txt")):
            os.remove(os.path.join(OUT, f))
    pages = sorted({p for a, b, _ in TARGETS.values() for p in range(a, b + 1)})
    for p in pages:                      # serial renders
        render(p)
    print(f"rendered {len(pages)} pages", flush=True)
    with ThreadPoolExecutor(max_workers=6) as ex:
        texts = dict(zip(pages, ex.map(lambda p: ocr(os.path.join(OUT, f"p{p}.png")), pages)))
    print("ocr done", flush=True)
    res = {}
    for item, (a, b, key) in TARGETS.items():
        kw = key.lower().split()
        hits = []
        for p in range(a, b + 1):
            t = " ".join(texts[p].lower().split())
            score = SequenceMatcher(None, t, key.lower()).find_longest_match(
                0, len(t), 0, len(key.lower())).size if key else 0
            if all(w in t for w in kw):
                score = max(score, 60)
            if score >= 8:
                i = t.find(kw[0])
                hits.append({"page": p, "score": round(score, 1),
                             "snippet": t[max(0, i - 40):i + 160]})
        res[item] = sorted(hits, key=lambda h: -h["score"])[:5]
        print(item, [(h["page"], h["score"]) for h in res[item]], flush=True)
    json.dump(res, open(os.path.join(C.OUT, "relocate.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
