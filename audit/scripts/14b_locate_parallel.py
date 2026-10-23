"""Locate exercises by content, OCRing pages in parallel.

Same idea as 14_locate_exercises.py but renders/OCRs the union of candidate
pages once, with a process pool, then scores every note against the cached text.
"""
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

PDF = ("/Users/db/Documents/projects/anki/v5repo/"
       "Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf")
TESS = "/Users/db/Documents/projects/anki/_tools/tessdata"
TMP = f"{C.OUT}/pages"
WINDOW = 16
STOP = set("""della delle degli nella nelle quali quale seguenti seguente sono essere
viene hanno questo questa quello quella delle più anche quando perché ogni tutte
tutti sulla sullla delle""".split())


def words(text):
    return [w for w in re.findall(r"[A-Za-zÀ-ÿ]{5,}", text.lower())
            if w not in STOP and "*" not in w]


def page_png(page):
    os.makedirs(TMP, exist_ok=True)
    base = f"{TMP}/p{page}"
    png = f"{base}-{page:03d}.png"
    if not os.path.exists(png):
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "160",
                        "-png", PDF, base], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png if os.path.exists(png) else None


def ocr_only(page):
    png = f"{TMP}/p{page}-{page:03d}.png"
    if not os.path.exists(png):
        return page, ""
    out = subprocess.run(["tesseract", png, "stdout", "-l", "ita"],
                         capture_output=True,
                         env=dict(os.environ, TESSDATA_PREFIX=TESS))
    return page, out.stdout.decode("utf-8", "replace")


def ocr_page(page):
    png = page_png(page)
    if not png:
        return page, ""
    out = subprocess.run(["tesseract", png, "stdout", "-l", "ita"],
                         capture_output=True,
                         env=dict(os.environ, TESSDATA_PREFIX=TESS))
    return page, out.stdout.decode("utf-8", "replace")


def main() -> None:
    items = json.load(open(f"{C.OUT}/pdf_reextract.json"))
    pages = set()
    for it in items:
        base = int(it["page"]) if str(it["page"]).isdigit() else 1
        pages.update(range(max(1, base - WINDOW), base + WINDOW + 1))
    print("pages to OCR:", len(pages))
    # render serially: concurrent pdftoppm on the same PDF truncates PNGs
    from PIL import Image
    bad = 0
    for page in sorted(pages):
        png = page_png(page)
        try:
            Image.open(png).load()
        except Exception:
            bad += 1
            if png and os.path.exists(png):
                os.remove(png)
            page_png(page)
    print("re-rendered corrupted pages:", bad)
    texts = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for page, text in ex.map(ocr_only, sorted(pages)):
            texts[page] = text
    print("ocr done:", sum(1 for t in texts.values() if t))
    low = {p: t.lower() for p, t in texts.items()}
    located = []
    for it in items:
        base = int(it["page"]) if str(it["page"]).isdigit() else 1
        keys = words(it["stem"])[:14]
        best, best_page, best_score = None, None, 0
        for page in range(max(1, base - WINDOW), base + WINDOW + 1):
            t = low.get(page, "")
            if not t:
                continue
            score = sum(1 for w in keys if w in t)
            if score > best_score:
                best, best_page, best_score = it["stem"], page, score
        located.append({
            "ItemID": it["ItemID"], "book_page": it["page"], "num": it["num"],
            "found_page": best_page, "score": best_score, "keys": keys[:8],
        })
        print(f'{it["ItemID"]:22} book={it["page"]:>4} found={best_page} score={best_score}/{len(keys)}')
    json.dump(located, open(f"{C.OUT}/located.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
