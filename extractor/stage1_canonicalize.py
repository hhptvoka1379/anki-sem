"""Stage 1: Lossless De-Annotation & Canonical Book Page Reconstruction.

Transforms the 902-page raw PDF ('Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf')
into the exact sequence of 894 canonical, unannotated book pages:
  - Chimica e Propedeutica Biochimica : Book Pages   3..290, 292..306 (303 pages; p.291 missing in source)
  - Biologia e Genetica               : Book Pages 309..666           (358 pages; zero missing)
  - Fisica                            : Book Pages 669..901           (233 pages; zero missing)

Handles every forensic anomaly present in the raw PDF:
  1. Strips 100% of vector handwriting, circles, highlights & Apple Scribble hidden fonts by
     reconstructing pages directly from raw embedded XObject bitmaps (and filtered vector spans on p.669).
  2. Drops exact duplicate page PDF p.176 (identical to p.175) and repeated XObject xref 1767 on p.132[0].
  3. Distinguishes multi-strip single pages (0.0pt gap, equal width) from 8 two-page vertical collages
     (PDF p. 121, 131, 132, 157, 166, 192, 227, 308 -> >0.5pt gap).
  4. Fixes reversed page order at the end of Biologia answers (PDF p.666 <-> PDF p.667 => Book 665 -> 666).
  5. Crops iOS reader chrome on uncropped screenshot PDF p.866 and removes outer border frames on p.670..901.
  6. Bottom-up EdiSES footer detection & micro-sliver-safe running header stripping (never truncates body lines).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Tuple, Optional

import cv2
import numpy as np
import pymupdf
from PIL import Image

PDF_FILENAME = "Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf"

# Exact publisher Table of Contents from vector INDICE on PDF pages 8-9
SUBJECT_CHAPTERS = [
    # Chimica e Propedeutica Biochimica (13 chapters + Risposte)
    ("Chimica e Propedeutica Biochimica", "CHIM", 1, "La matematica e la chimica", 3, 20),
    ("Chimica e Propedeutica Biochimica", "CHIM", 2, "Il modello atomico: chimica e orbitali", 21, 34),
    ("Chimica e Propedeutica Biochimica", "CHIM", 3, "Ordine tra gli elementi: la tavola periodica", 35, 60),
    ("Chimica e Propedeutica Biochimica", "CHIM", 4, "I legami tra ioni e tra atomi", 61, 75),
    ("Chimica e Propedeutica Biochimica", "CHIM", 5, "I legami tra le molecole e proprietà delle sostanze", 76, 88),
    ("Chimica e Propedeutica Biochimica", "CHIM", 6, "Le soluzioni", 89, 107),
    ("Chimica e Propedeutica Biochimica", "CHIM", 7, "Le trasformazioni chimiche", 108, 122),
    ("Chimica e Propedeutica Biochimica", "CHIM", 8, "La velocità delle reazioni e l'equilibrio", 123, 129),
    ("Chimica e Propedeutica Biochimica", "CHIM", 9, "Le reazioni di ossido-riduzione", 130, 146),
    ("Chimica e Propedeutica Biochimica", "CHIM", 10, "La nomenclatura dei composti inorganici", 147, 163),
    ("Chimica e Propedeutica Biochimica", "CHIM", 11, "Acidità e basicità", 164, 189),
    ("Chimica e Propedeutica Biochimica", "CHIM", 12, "La chimica organica", 190, 227),
    ("Chimica e Propedeutica Biochimica", "CHIM", 13, "Sostanze organiche di interesse biologico", 228, 251),
    # Biologia e Genetica (7 chapters + Risposte)
    ("Biologia e Genetica", "BIO", 1, "Le basi dell'organizzazione biologica e molecolare della vita", 309, 354),
    ("Biologia e Genetica", "BIO", 2, "I meccanismi cellulari di trasmissione e controllo dell'informazione genetica e epigenetica", 355, 376),
    ("Biologia e Genetica", "BIO", 3, "Il flusso dell'informazione", 377, 418),
    ("Biologia e Genetica", "BIO", 4, "I meccanismi cellulari di trasmissione e controllo dei caratteri selvatici e mutati", 419, 466),
    ("Biologia e Genetica", "BIO", 5, "Le strutture cellulari: biogenesi, morfologia e funzioni", 467, 528),
    ("Biologia e Genetica", "BIO", 6, "La cellula e l'ambiente, la segnalazione cellulare e la trasduzione del segnale", 529, 557),
    ("Biologia e Genetica", "BIO", 7, "Il controllo della proliferazione e della sopravvivenza cellulare", 558, 596),
    # Fisica (8 chapters + Risposte)
    ("Fisica", "FIS", 1, "Grandezze fisiche e vettori", 669, 684),
    ("Fisica", "FIS", 2, "Cinematica", 685, 701),
    ("Fisica", "FIS", 3, "Dinamica, lavoro, energia e statica", 702, 744),
    ("Fisica", "FIS", 4, "Meccanica dei fluidi", 745, 760),
    ("Fisica", "FIS", 5, "Termodinamica", 761, 787),
    ("Fisica", "FIS", 6, "Elettricità ed elettromagnetismo", 788, 829),
    ("Fisica", "FIS", 7, "Onde e ottica", 830, 843),
    ("Fisica", "FIS", 8, "Fisica nucleare", 844, 851),
]

RISPOSTE_RANGES = {
    "CHIM": ("Chimica e Propedeutica Biochimica", 252, 306),
    "BIO": ("Biologia e Genetica", 597, 666),
    "FIS": ("Fisica", 852, 901),
}


@dataclass
class CanonicalPage:
    book_page: int
    pdf_page: int
    sub_index: int
    subject: str
    subject_code: str
    role: str  # "questions" or "answers"
    chapter_num: Optional[int]
    chapter_title: Optional[str]
    is_vector: bool
    xrefs: List[int]
    width: int
    height: int
    body_y0: int
    body_y1: int
    banners: List[Tuple[int, int, str]]


def _strip_frame_and_ios_chrome(arr: np.ndarray, pdf_pno: int) -> np.ndarray:
    """Remove iOS screenshot chrome on PDF p.866 and thin rectangular frame lines on Fisica pages."""
    h, w = arr.shape
    if pdf_pno == 866:
        sub = arr[350:2400, :]
        row_edges = (sub < 225).mean(axis=1)
        ys = np.where(row_edges > 0.72)[0]
        y_top = 350 + int(ys[0]) + 6 if len(ys) else 554
        y_bot = 350 + int(ys[-1]) - 6 if len(ys) else 2242
        col_edges = (arr[y_top:y_bot, :] < 225).mean(axis=0)
        xs = np.where(col_edges > 0.72)[0]
        x_left = int(xs[0]) + 6 if len(xs) else 102
        x_right = int(xs[-1]) - 6 if len(xs) else 1188
        arr = arr[y_top:y_bot, x_left:x_right].copy()
        h, w = arr.shape

    if pdf_pno >= 670:
        row_dark = (arr < 160).mean(axis=1)
        col_dark = (arr < 160).mean(axis=0)

        top_cut = 0
        y = 0
        while y < int(h * 0.10):
            if row_dark[y] > 0.65:
                y_end = y
                while y_end < h and row_dark[y_end] > 0.50:
                    y_end += 1
                if (y_end - y) <= 10:
                    top_cut = y_end + 3
                y = y_end + 1
            else:
                y += 1

        bot_cut = h
        y = h - 1
        while y > int(h * 0.90):
            if row_dark[y] > 0.65:
                y_start = y
                while y_start >= 0 and row_dark[y_start] > 0.50:
                    y_start -= 1
                if (y - y_start) <= 10:
                    bot_cut = y_start - 3
                y = y_start - 1
            else:
                y -= 1

        left_cut = 0
        for x in range(int(w * 0.12)):
            if col_dark[x] > 0.65:
                left_cut = x + 3
        right_cut = w
        for x in range(w - 1, int(w * 0.88), -1):
            if col_dark[x] > 0.65:
                right_cut = x - 3
        if top_cut > 0 or bot_cut < h or left_cut > 0 or right_cut < w:
            arr = arr[top_cut:bot_cut, left_cut:right_cut].copy()
    return arr


def render_clean_p669(doc: pymupdf.Document, dpi: int = 220) -> Tuple[np.ndarray, dict]:
    """Reconstruct PDF page 669 cleanly from EdiSES vector fonts only (0% Apple Pencil / Scribble)."""
    src = doc[668]
    raw_dict = src.get_text("dict")
    out_doc = pymupdf.open()
    dst = out_doc.new_page(width=src.rect.width, height=src.rect.height)

    for drw in src.get_drawings():
        fill = drw.get("fill")
        rect = drw.get("rect")
        if fill is not None and rect is not None and rect.width > src.rect.width * 0.5 and rect.height > 15:
            dst.draw_rect(rect, color=None, fill=(0, 0, 0))

    clean_blocks = []
    for blk in raw_dict["blocks"]:
        if blk.get("type") != 0:
            continue
        lines_out = []
        for ln in blk.get("lines", []):
            spans_out = []
            for sp in ln.get("spans", []):
                fname = sp.get("font", "")
                if fname.startswith("."):
                    continue
                spans_out.append({
                    "text": sp["text"],
                    "font": fname,
                    "size": round(sp["size"], 2),
                    "flags": sp["flags"],
                    "bbox": [round(v, 2) for v in sp["bbox"]],
                })
                color_rgb = (1, 1, 1) if sp.get("color") == 16777215 else (0, 0, 0)
                bold = "Bold" in fname or "SemiBold" in fname
                fontname = "tiro" if not bold else "tibo"
                dst.insert_text(
                    pymupdf.Point(sp["origin"][0], sp["origin"][1]),
                    sp["text"],
                    fontname=fontname,
                    fontsize=sp["size"],
                    color=color_rgb,
                )
            if spans_out:
                lines_out.append({"bbox": [round(v, 2) for v in ln["bbox"]], "spans": spans_out})
        if lines_out:
            clean_blocks.append({"bbox": [round(v, 2) for v in blk["bbox"]], "lines": lines_out})

    pix = dst.get_pixmap(dpi=dpi)
    arr = np.array(Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L"))
    out_doc.close()
    return arr, {"width_pt": src.rect.width, "height_pt": src.rect.height, "blocks": clean_blocks}


def detect_banners_header_footer(arr: np.ndarray) -> Tuple[int, int, List[Tuple[int, int]]]:
    """Detect solid dark section banners + strip ONLY genuine top running header & bottom EdiSES footer.

    Critical invariant:
      - Footer strip NEVER cuts body content lines (e.g. double-spaced 'completamento' items near y ~ 0.88*h).
        It inspects ONLY the single bottom-most horizontal ink band (`bot_bands[-1]`) near the bottom edge
        and requires the solid black EdiSES corner bar (or wide bottom-margin isolation >= 72px).
      - Header strip skips micro-border slivers (< 8px tall at top edge) and removes single-line running headers
        cleanly across both full-height and partial-height pages.
    """
    h, w = arr.shape
    row_dark_frac = (arr < 128).mean(axis=1)
    row_ink_pixels = (arr < 180).sum(axis=1)

    # 1. Detect full-width dark section banners ('Quiz commentati', 'Quiz non commentati', 'Quiz a completamento')
    dark_rows = np.where(row_dark_frac > 0.52)[0]
    banner_bands: List[Tuple[int, int]] = []
    if len(dark_rows) >= 15:
        splits = np.where(np.diff(dark_rows) > 6)[0] + 1
        for grp in np.split(dark_rows, splits):
            bh = int(grp[-1]) - int(grp[0]) + 1
            if bh >= max(18, int(h * 0.025)) and int(grp[0]) < int(h * 0.85):
                banner_bands.append((int(grp[0]), int(grp[-1])))

    # 2. Bottom-up EdiSES footer strip: inspect ONLY the single bottom-most ink band on the page!
    body_y1 = h
    bot_scan_top = int(h * 0.80)
    bot_ink_rows = np.where(row_ink_pixels[bot_scan_top:] > 4)[0]
    if len(bot_ink_rows) > 0:
        bsplits = np.where(np.diff(bot_ink_rows) > 10)[0] + 1
        bot_bands = [
            (bot_scan_top + int(g[0]), bot_scan_top + int(g[-1]))
            for g in np.split(bot_ink_rows, bsplits)
            if len(g) >= 6
        ]
        # Skip trailing tiny bottom-border speck band (< 6px) already filtered above
        if bot_bands:
            fy0, fy1 = bot_bands[-1]
            fh = fy1 - fy0 + 1
            # Measure solid black corner bar signature inside [fy0:fy1+1]
            sub_band = arr[fy0:fy1 + 1, :]
            col_black = (sub_band < 55).mean(axis=0)
            has_solid_bar = int((col_black > 0.65).sum()) >= int(w * 0.065)
            # Measure pure white vertical gap directly ABOVE this bottom-most band
            gap_above = 0
            for yy in range(fy0 - 1, max(-1, fy0 - 160), -1):
                if row_ink_pixels[yy] <= 3:
                    gap_above += 1
                else:
                    break
            # Genuine EdiSES footer ALWAYS has the solid black corner bar + whitespace gap above it
            if fh <= 64 and fy0 > int(h * 0.86) and has_solid_bar and gap_above >= 14:
                body_y1 = fy0 - 4

    # 3. Single-line top running header detection (skipping any <8px top border sliver near y < 16)
    body_y0 = 0
    top_limit = int(h * 0.14) if h >= 850 else int(h * 0.24)
    ink_rows = np.where(row_ink_pixels[:top_limit] > 3)[0]
    if len(ink_rows) > 0:
        splits = np.where(np.diff(ink_rows) > 7)[0] + 1
        bands = [
            (int(g[0]), int(g[-1]))
            for g in np.split(ink_rows, splits)
            if not (int(g[0]) < 16 and len(g) < 8) and len(g) >= 5
        ]
        if bands:
            b0_top, b0_bot = bands[0]
            band_h = b0_bot - b0_top + 1
            after_gap = 0
            for y in range(b0_bot + 1, min(h, b0_bot + 130)):
                if row_ink_pixels[y] <= 2:
                    after_gap += 1
                else:
                    break
            max_hdr_h = max(36, int(w * 0.030))
            min_gap = max(18, int(w * 0.020))
            if band_h <= max_hdr_h and after_gap >= min_gap and (not banner_bands or b0_bot < banner_bands[0][0] - 18):
                body_y0 = b0_bot + 4

    return body_y0, body_y1, banner_bands


def classify_banner(arr: np.ndarray, y0: int, y1: int, api_line) -> str:
    """Classify a dark full-width banner as 'commentati', 'non_commentati', or 'completamento'."""
    h, w = arr.shape
    inv = 255 - arr[max(0, y0 - 4):min(h, y1 + 4), int(w * 0.08):]
    up = cv2.resize(inv, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    up = cv2.GaussianBlur(up, (3, 3), 0.7)
    api_line.SetImage(Image.fromarray(up))
    txt = api_line.GetUTF8Text().lower()
    if "complet" in txt or "comp" in txt:
        return "completamento"
    if "non" in txt:
        return "non_commentati"
    return "commentati"


def assign_book_page_metadata(book_page: int) -> Tuple[str, str, str, Optional[int], Optional[str]]:
    for subj, code, ch_num, ch_title, bp_start, bp_end in SUBJECT_CHAPTERS:
        if bp_start <= book_page <= bp_end:
            return subj, code, "questions", ch_num, ch_title
    for code, (subj, bp_start, bp_end) in RISPOSTE_RANGES.items():
        if bp_start <= book_page <= bp_end:
            return subj, code, "answers", None, None
    raise ValueError(f"Unexpected book_page {book_page} outside INDICE ranges!")


def refresh_canonical_geometry_from_cached_pages(cache_dir: str = "/tmp/anki_sem_stage1") -> List[dict]:
    """Recompute exact (body_y0, body_y1, banners) across all 894 already-rendered clean PNGs in ~2s."""
    out_dir = Path(cache_dir)
    meta_path = out_dir / "canonical_pages.json"
    with open(meta_path, encoding="utf-8") as f:
        pages = json.load(f)

    changed_y0 = changed_y1 = 0
    for m in pages:
        bp = m["book_page"]
        arr = np.array(Image.open(out_dir / "pages" / f"bp_{bp:03d}.png"))
        new_y0, new_y1, _ = detect_banners_header_footer(arr)
        if abs(new_y0 - m["body_y0"]) > 2:
            changed_y0 += 1
        if abs(new_y1 - m["body_y1"]) > 2:
            changed_y1 += 1
        m["body_y0_prev"] = m["body_y0"]
        m["body_y1_prev"] = m["body_y1"]
        m["body_y0"] = new_y0
        m["body_y1"] = new_y1

    with open(meta_path, "w", encoding="utf-8") as mf:
        json.dump(pages, mf, ensure_ascii=False, indent=2)
    print(f"Refreshed geometry on all {len(pages)} pages (updated body_y0={changed_y0}, body_y1={changed_y1}).")
    return pages


def run_stage1(pdf_path: str = PDF_FILENAME, cache_dir: str = "/tmp/anki_sem_stage1", force_reextract: bool = False) -> List[CanonicalPage]:
    out_dir = Path(cache_dir)
    if not force_reextract and (out_dir / "canonical_pages.json").exists() and len(list((out_dir / "pages").glob("bp_*.png"))) == 894:
        pages_dicts = refresh_canonical_geometry_from_cached_pages(cache_dir)
        return [
            CanonicalPage(**{k: v for k, v in d.items() if k in CanonicalPage.__dataclass_fields__})
            for d in pages_dicts
        ]

    os.environ["OMP_THREAD_LIMIT"] = "1"
    import tesserocr

    (out_dir / "pages").mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    seen_xrefs = set()
    raw_entries = []

    for pno in range(12, 902):
        if pno in (176, 309, 668):
            continue
        p = doc[pno - 1]
        imgs = p.get_images(full=True)
        if not imgs:
            arr, vec_data = render_clean_p669(doc)
            with open(out_dir / "p669_vector.json", "w", encoding="utf-8") as vf:
                json.dump(vec_data, vf, ensure_ascii=False, indent=2)
            raw_entries.append((pno, 0, True, [], arr))
            continue

        items = []
        for im in imgs:
            xref = im[0]
            r = p.get_image_rects(xref)[0]
            items.append((r.y0, r.y1, xref, im[2], im[3]))
        items.sort(key=lambda x: x[0])

        groups = [[items[0]]]
        for it in items[1:]:
            prev = groups[-1][-1]
            if abs(it[0] - prev[1]) < 0.5 and it[3] == prev[3]:
                groups[-1].append(it)
            else:
                groups.append([it])

        for g_idx, grp in enumerate(groups):
            key_xrefs = tuple(x[2] for x in grp)
            if key_xrefs in seen_xrefs:
                continue
            seen_xrefs.add(key_xrefs)

            strips = []
            for _, _, xref, _, _ in grp:
                pix = pymupdf.Pixmap(doc, xref)
                mode = "L" if pix.n == 1 else ("RGB" if pix.n == 3 else "RGBA")
                pil = Image.frombytes(mode, (pix.width, pix.height), pix.samples).convert("L")
                strips.append(np.array(pil))
            arr = strips[0] if len(strips) == 1 else np.vstack(strips)
            arr = _strip_frame_and_ios_chrome(arr, pno)
            raw_entries.append((pno, g_idx, False, list(key_xrefs), arr))

    idx_666 = next(i for i, e in enumerate(raw_entries) if e[0] == 666)
    idx_667 = next(i for i, e in enumerate(raw_entries) if e[0] == 667)
    raw_entries[idx_666], raw_entries[idx_667] = raw_entries[idx_667], raw_entries[idx_666]

    assert len(raw_entries) == 894, f"Expected 894 canonical pages, got {len(raw_entries)}"

    book_page_numbers = (
        list(range(3, 291))
        + list(range(292, 307))
        + list(range(309, 667))
        + list(range(669, 902))
    )
    assert len(book_page_numbers) == 894

    pages_meta: List[CanonicalPage] = []
    tess_path = "/tmp/tessdata_fast" if Path("/tmp/tessdata_fast").exists() else None
    with tesserocr.PyTessBaseAPI(path=tess_path, lang="ita+eng", psm=tesserocr.PSM.SINGLE_LINE) as api_line:
        for bp, (pno, g_idx, is_vec, xrefs, arr) in zip(book_page_numbers, raw_entries):
            subj, code, role, ch_num, ch_title = assign_book_page_metadata(bp)
            body_y0, body_y1, banner_bands = detect_banners_header_footer(arr)
            classified_banners: List[Tuple[int, int, str]] = []
            for by0, by1 in banner_bands:
                if role == "questions":
                    btype = classify_banner(arr, by0, by1, api_line)
                    classified_banners.append((by0, by1, btype))
            Image.fromarray(arr).save(out_dir / "pages" / f"bp_{bp:03d}.png")
            pages_meta.append(CanonicalPage(
                book_page=bp,
                pdf_page=pno,
                sub_index=g_idx,
                subject=subj,
                subject_code=code,
                role=role,
                chapter_num=ch_num,
                chapter_title=ch_title,
                is_vector=is_vec,
                xrefs=xrefs,
                width=int(arr.shape[1]),
                height=int(arr.shape[0]),
                body_y0=body_y0,
                body_y1=body_y1,
                banners=classified_banners,
            ))

    expected_seq = ["commentati", "non_commentati", "completamento"]
    chap_banner_refs = {}
    for m in pages_meta:
        if m.role == "questions":
            for b_idx in range(len(m.banners)):
                chap_banner_refs.setdefault((m.subject_code, m.chapter_num), []).append((m, b_idx))

    for (code, ch_num), refs in chap_banner_refs.items():
        assert len(refs) == 3, f"Expected 3 section banners in {code} Cap {ch_num}, got {len(refs)}"
        for idx, (m_page, b_idx) in enumerate(refs):
            by0, by1, _ = m_page.banners[b_idx]
            m_page.banners[b_idx] = (by0, by1, expected_seq[idx])

    with open(out_dir / "canonical_pages.json", "w", encoding="utf-8") as mf:
        json.dump([asdict(m) for m in pages_meta], mf, ensure_ascii=False, indent=2)

    return pages_meta


if __name__ == "__main__":
    pages = run_stage1()
    print(f"Stage 1 ready: {len(pages)} canonical book pages.")
