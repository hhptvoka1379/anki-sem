"""Question / solution crops from Tesseract word boxes (no model calls).

  crop.py --extracted X.jsonl --pagemap build/chim_ch1_pagemap.json --out DIR [--report R.tsv]

For each record: <id>_q.png = the question from its number to the next number in the same column,
with any part that runs into the next column or page stacked below. COMM records also get
<id>_s.png, the same cut on the RISPOSTE pages. NCOM/COMP keys are a table / word list, so they
get no solution crop. Records with a needed figure get figure = their question crop.
A question whose number cannot be found is reported as needs_manual and gets no crop.
Updates the records in place (question_crop, solution_crop, figure) and rewrites X.jsonl.
"""
import argparse, csv, json, re, sys
from pathlib import Path

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / "work" / "ocr"
OCR_DPI = 300
PAGE_W = 2481
MID = PAGE_W // 2
HEADER_MAX_Y = 450   # running header ("6 | Chimica ... | Quiz ...") sits above this
NUMBER_MIN_Y = 400   # but a first question number can sit at y≈437, just inside that band
OUT_DPI = 170        # ~830 px per column: readable on a phone, small files

_words = {}


def words(page):
    if page not in _words:
        rows = []
        with open(OCR_DIR / ("p%03d.tsv" % page)) as f:
            for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
                if r["level"] == "5" and r["text"].strip():
                    rows.append({k: int(r[k]) for k in ("left", "top", "width", "height")}
                                | {"text": r["text"].strip(), "conf": float(r["conf"])})
        _words[page] = rows
    return _words[page]


_split = {}


def split_x(page):
    """x of the gutter between the two columns: the widest empty vertical strip in the middle of the
    text block. Margins differ between odd and even pages, so it is measured per page."""
    if page not in _split:
        ws = [w for w in words(page) if w["top"] > HEADER_MAX_Y and w["conf"] >= 70]
        nums = sorted(w["left"] for w in words(page)
                      if w["top"] > NUMBER_MIN_Y and re.match(r"^\d{1,3}[\).]$", w["text"]))
        if len(nums) >= 3 and nums[-1] - nums[0] < 150:
            # Every number starts at one x: a full-width page (fill-in list, RISPOSTE). No gutter.
            _split[page] = PAGE_W
        elif len(ws) < 20:
            _split[page] = MID
        else:
            lo, hi = pct([w["left"] for w in ws], 0.02), pct([w["left"] + w["width"] for w in ws], 0.98)
            covered = [0] * (PAGE_W // 10 + 1)
            for w in ws:
                for b in range(w["left"] // 10, min(len(covered), (w["left"] + w["width"]) // 10 + 1)):
                    covered[b] += 1
            a, z = (lo + (hi - lo) // 5) // 10, (hi - (hi - lo) // 5) // 10
            best, run, start = (0, MID // 10), 0, a
            for b in range(a, z + 1):
                if covered[b] <= 1:  # one stray word (handwriting, a dash) may cross the gutter
                    if run == 0:
                        start = b
                    run += 1
                    if run > best[0]:
                        best = (run, start + run // 2)
                else:
                    run = 0
            _split[page] = best[1] * 10 if best[0] >= 2 else (lo + hi) // 2
    return _split[page]


def column_of(w, page):
    return 0 if w["left"] < split_x(page) else 1


def pct(vals, q):
    vals = sorted(vals)
    return vals[min(len(vals) - 1, int(q * len(vals)))]


def body(page, col):
    # Confident words only: handwritten margin notes OCR with low confidence and would
    # otherwise drag the column edge (and every crop) out into the margin.
    ws = [w for w in words(page) if column_of(w, page) == col and w["top"] > HEADER_MAX_Y and w["conf"] >= 70]
    if len(ws) < 5:
        return None
    # Right edge = the longest confident line; a percentile clipped full-width lines.
    return {"x0": pct([w["left"] for w in ws], 0.02), "x1": max(w["left"] + w["width"] for w in ws),
            "y0": min(w["top"] for w in ws), "y1": max(w["top"] + w["height"] for w in ws)}


NUM_RE = re.compile(r"^(\d{1,3})[\).]")


def starts(page, col):
    """(number, top) of every number in the current section's format at the column's left edge.
    The format is set per section (NUM_RE) so statement numerals '1.' inside an NCOM question,
    or '14.' wrapped to a line start, are not taken for question starts."""
    b = body(page, col)
    if not b:
        return []
    out = []
    for w in words(page):
        m = NUM_RE.match(w["text"])
        if m and column_of(w, page) == col and w["top"] > NUMBER_MIN_Y and abs(w["left"] - b["x0"]) < 90:
            out.append((int(m.group(1)), w["top"]))
    return sorted(out, key=lambda t: t[1])


def headings(page):
    """Top y of 'Risposte quiz ...' section headings on answer pages."""
    return sorted(w["top"] for w in words(page) if w["text"].lower().startswith("rispost"))


def region_after(page, col, y_from, limits):
    """Text in a column from y_from to the next number (or section heading); returns (y_end, ends_at_number)."""
    nxt = [t for _, t in starts(page, col) if t > y_from + 20] + [h for h in limits if h > y_from + 20]
    b = body(page, col)
    if nxt:
        return min(nxt) - 10, True
    return b["y1"] + 10, False


def cut(doc, page, col, y0, y1):
    b = body(page, col)
    s = 72 / OCR_DPI
    mid = split_x(page)
    x0 = max(0, b["x0"] - 25) if col == 0 else max(mid - 10, b["x0"] - 25)
    x1 = min(mid + 10, b["x1"] + 25) if col == 0 else min(PAGE_W, b["x1"] + 25)
    pix = doc[page - 1].get_pixmap(dpi=OUT_DPI, clip=pymupdf.Rect(x0 * s, y0 * s, x1 * s, y1 * s),
                                   colorspace=pymupdf.csGRAY)
    return Image.frombytes("L", (pix.width, pix.height), pix.samples)


def next_slot(page, col, last_page):
    if col == 0:
        return page, 1
    return (page + 1, 0) if page + 1 <= last_page else None


def crop_one(doc, num, pages, out_path, limits_for, num_re):
    """Find number `num` on `pages`, cut to the next number, follow a spill into the next column/page."""
    global NUM_RE
    NUM_RE = num_re
    for page in pages:
        for col in (0, 1):
            hit = [t for n, t in starts(page, col) if n == num]
            if not hit:
                continue
            y0 = hit[0] - 15
            y1, closed = region_after(page, col, hit[0], limits_for(page))
            parts = [cut(doc, page, col, y0, y1)]
            slot = None if closed else next_slot(page, col, pages[-1])
            # A spill exists when the next column/page starts with text before its first number.
            while slot:
                p2, c2 = slot
                b = body(p2, c2)
                if not b:
                    break
                firsts = [t for _, t in starts(p2, c2)] + [h for h in limits_for(p2) if h > b["y0"]]
                first = min(firsts) if firsts else b["y1"] + 10
                if first - b["y0"] < 40:
                    break
                parts.append(cut(doc, p2, c2, b["y0"] - 10, first - 10))
                slot = None if firsts else next_slot(p2, c2, pages[-1])
            w = max(p.width for p in parts)
            img = Image.new("L", (w, sum(p.height for p in parts)), 255)
            y = 0
            for p in parts:
                img.paste(p, (0, y))
                y += p.height
            img.save(out_path, optimize=True)
            return {"page": page, "col": col, "parts": len(parts)}
    return None


PAREN_NUM = re.compile(r"^(\d{1,3})\)")   # 'Quiz commentati/non commentati' and RISPOSTE entries: '12)'
COMP_NUM = re.compile(r"^(\d{1,3})\.")    # 'Quiz a completamento': '12.'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--pagemap", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    m = json.load(open(a.pagemap))
    recs = [json.loads(l) for l in open(a.extracted) if l.strip()]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(ROOT / "book.pdf")
    sec_pages = {s["quiz_type"]: list(range(s["pdf_pages"][0], s["pdf_pages"][1] + 1)) for s in m["sections"]}
    sol_pages = {s["quiz_type"]: list(range(s["pdf_pages"][0], s["pdf_pages"][1] + 1)) for s in m["solution_pages"]}
    report = []
    for r in recs:
        qt, n, base = r["quiz_type"], r["question_num"], r["id"].lower()
        # Search the record's own page first; the page map range is the fallback.
        pages = [r["pdf_page"]] + [p for p in sec_pages[qt] if p > r["pdf_page"]]
        res = crop_one(doc, n, pages, out / (base + "_q.png"), lambda p: [], COMP_NUM if qt == "COMP" else PAREN_NUM)
        if res:
            r["question_crop"] = base + "_q.png"
            if res["page"] != r["pdf_page"]:
                report.append((r["id"], "page-mismatch", "record pdf %d, number found on %d" % (r["pdf_page"], res["page"])))
            report.append((r["id"], "q-ok", "pdf %d col %d parts %d" % (res["page"], res["col"], res["parts"])))
        else:
            r["question_crop"] = None
            report.append((r["id"], "q-needs_manual", "number %d not found at a column edge" % n))
        if isinstance(r.get("figure"), str) and r["figure"].startswith("NEEDED") and r["question_crop"]:
            # The figure is inside the printed question; showing the question crop on the front
            # gives the student the figure without opening the scan.
            r["figure"] = r["question_crop"]
        if qt == "COMM":
            # Commentati solutions are full-width paragraphs, even on a page that ends in a
            # multi-column key table, so the answer pages are never split into columns.
            for p in sol_pages[qt]:
                _split[p] = PAGE_W
            # Answer pages hold several sections; a 'Risposte ...' heading ends a solution.
            sres = crop_one(doc, n, sol_pages[qt], out / (base + "_s.png"), headings, PAREN_NUM)
            r["solution_crop"] = base + "_s.png" if sres else None
            report.append((r["id"], "s-ok" if sres else "s-needs_manual", str(sres or "")))
    with open(a.extracted, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    if a.report:
        with open(a.report, "w") as f:
            for row in report:
                f.write("\t".join(row) + "\n")
    bad = [x for x in report if "needs_manual" in x[1] or x[1] == "page-mismatch"]
    for x in bad:
        print("\t".join(x))
    print("records=%d question_crops=%d solution_crops=%d problems=%d" % (
        len(recs), sum(1 for r in recs if r.get("question_crop")),
        sum(1 for r in recs if r.get("solution_crop")), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
