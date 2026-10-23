"""Find the PDF page that actually holds each damaged exercise.

`BookPage` is unreliable for the commentati notes, so each exercise is located by
content: render a window of pages around BookPage, OCR them once (cached), and
score pages by how many distinctive stem words they contain.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

PDF = "/Users/db/Documents/projects/anki/v5repo/Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf"
TESS = "/Users/db/Documents/projects/anki/_tools/tessdata"
TMP = "/tmp/sf_pages"
CACHE = f"{C.OUT}/page_ocr.json"
WINDOW = 14
STOP = set("""della delle degli nella nelle quali quale seguenti seguente sono essere
viene hanno questo questa quello quella nella delle delle della delle più anche
quando perché ogni tutte tutti sullla sulla delle delle""".split())


def words(text):
    out = []
    for w in re.findall(r"[A-Za-zÀ-ÿ]{5,}", text.lower()):
        if w in STOP or "*" in w:
            continue
        out.append(w)
    return out


def render(page):
    os.makedirs(TMP, exist_ok=True)
    base = f"{TMP}/p{page}"
    png = f"{base}-{page:03d}.png"
    if not os.path.exists(png):
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "160",
                        "-png", PDF, base], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    matches = [f for f in os.listdir(TMP) if f.startswith(f"p{page}-") and f.endswith(".png")]
    return os.path.join(TMP, matches[0]) if matches else None


def ocr(page, cache):
    key = str(page)
    if key in cache:
        return cache[key]
    png = render(page)
    if not png:
        cache[key] = ""
        return ""
    out = subprocess.run(["tesseract", png, "stdout", "-l", "ita"],
                         capture_output=True,
                         env=dict(os.environ, TESSDATA_PREFIX=TESS))
    cache[key] = out.stdout.decode("utf-8", "replace")
    return cache[key]


def main() -> None:
    items = json.load(open(f"{C.OUT}/pdf_reextract.json"))
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    located = []
    for it in items:
        base_page = int(it["page"]) if str(it["page"]).isdigit() else 1
        keys = words(it["stem"])[:14]
        best, best_score, best_page = None, 0, None
        for page in range(max(1, base_page - WINDOW), base_page + WINDOW + 1):
            text = ocr(page, cache)
            if not text:
                continue
            low = text.lower()
            score = sum(1 for w in keys if w in low)
            if score > best_score:
                best, best_score, best_page = text, score, page
        located.append({
            "ItemID": it["ItemID"], "book_page": it["page"], "num": it["num"],
            "found_page": best_page, "score": best_score,
            "keys": keys[:8],
            "page_image": f"/tmp/sf_pages/p{best_page}-{best_page:03d}.png" if best_page else None,
        })
        print(f'{it["ItemID"]:22} book={it["page"]:>4}  found={best_page}  score={best_score}/{len(keys)}')
    json.dump(cache, open(CACHE, "w"))
    json.dump(located, open(f"{C.OUT}/located.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
