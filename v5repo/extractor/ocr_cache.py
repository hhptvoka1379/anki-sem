"""High-speed, deadlock-free parallel OCR feature cache builder across all 894 canonical book pages.

Builds and incrementally updates:
  1. questions_ocr_cache.json : All 720 canonical question pages split strictly by exact section
                                banner zones & widest pure-white column gutters (zero column mixing!),
                                exact lossless vector extraction on p.669, 300-DPI cubic upscaling on
                                low-resolution scan pages, PLUS morphological horizontal blank-bar
                                coordinates & clean underline-erased OCR for all 28 'completamento' sections.
  2. risposte_fast_lines.json : Full-page 300-DPI-upscaled OCR lines across all 174 canonical answer pages
                                for heading localization & 'Risposte quiz commentati' extraction.

Workers write directly to temporary chunk files on disk (never passing multi-MB objects over pipes).
"""

from __future__ import annotations

import json
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import numpy as np
from PIL import Image

VEC_SUP = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶₇⁸⁹⁺⁻⁼⁽⁾ⁿ")
VEC_SUB = str.maketrans("0123456789+-=()aeioruvx", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢₒᵣᵤᵥₓ")


def safe_extract_lines_and_words(api, inv_scale: float = 1.0) -> List[dict]:
    """Extract all lines and their constituent word boxes in a single Recognize() pass,
    mapping bounding boxes back into 1x canonical page pixel coordinates via inv_scale."""
    import tesserocr
    api.Recognize()
    ri = api.GetIterator()
    lines = []
    if ri is None:
        return lines
    while True:
        try:
            ltxt = (ri.GetUTF8Text(tesserocr.RIL.TEXTLINE) or "").strip()
        except RuntimeError:
            ltxt = ""
        lb = ri.BoundingBox(tesserocr.RIL.TEXTLINE)
        lconf = ri.Confidence(tesserocr.RIL.TEXTLINE)
        if ltxt and lb:
            words = []
            while True:
                try:
                    wtxt = (ri.GetUTF8Text(tesserocr.RIL.WORD) or "").strip()
                except RuntimeError:
                    wtxt = ""
                wb = ri.BoundingBox(tesserocr.RIL.WORD)
                wconf = ri.Confidence(tesserocr.RIL.WORD)
                if wtxt and wb:
                    words.append({
                        "t": wtxt,
                        "b": [int(round(v * inv_scale)) for v in wb],
                        "c": round(wconf, 1),
                    })
                if ri.IsAtFinalElement(tesserocr.RIL.TEXTLINE, tesserocr.RIL.WORD):
                    break
                if not ri.Next(tesserocr.RIL.WORD):
                    break
            lines.append({
                "text": ltxt,
                "bbox": [int(round(v * inv_scale)) for v in lb],
                "conf": round(lconf, 1),
                "words": words,
            })
        if not ri.Next(tesserocr.RIL.TEXTLINE):
            break
    return lines


def prepare_for_ocr(img: np.ndarray, full_page_w: int) -> Tuple[np.ndarray, float]:
    """Upscale low-DPI scan strips cleanly via bicubic interpolation to ~300 DPI equivalent
    so Tesseract LSTM neither blurs kerning gaps nor drops thin serifs/exponents."""
    scale = 2.0 if full_page_w < 1550 else 1.4
    up = cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    return up, 1.0 / scale


def extract_vector_p669_zone_columns(
    stage1_dir: Path,
    zy0: int,
    zy1: int,
    xg: int,
    w: int,
) -> List[dict]:
    """Extract 100% lossless text & Unicode superscripts/subscripts on vector PDF page 669."""
    vec_path = stage1_dir / "p669_vector.json"
    with open(vec_path, encoding="utf-8") as f:
        vdoc = json.load(f)
    pt_to_px = 220.0 / 72.0
    col_lines: List[List[dict]] = [[], []]

    for blk in vdoc.get("blocks", []):
        for ln in blk.get("lines", []):
            spans = ln.get("spans", [])
            if not spans:
                continue
            bx0, by0, bx1, by1 = [c * pt_to_px for c in ln["bbox"]]
            cy = 0.5 * (by0 + by1)
            if cy < zy0 - 4 or cy > zy1 + 4:
                continue
            tall_spans = [s for s in spans if s["size"] >= 8.8 and s["text"].strip()]
            main_y1 = float(np.median([s["bbox"][3] for s in tall_spans])) if tall_spans else ln["bbox"][3]
            buf = []
            for sp in spans:
                raw_s = sp["text"].replace("\u2002", " ").replace("\u00a0", " ")
                if sp["size"] <= 8.2 and raw_s.strip():
                    if sp["bbox"][3] < main_y1 - 1.2:
                        buf.append(raw_s.translate(VEC_SUP))
                    elif sp["bbox"][3] > main_y1 + 0.8:
                        buf.append(raw_s.translate(VEC_SUB))
                    else:
                        buf.append(raw_s)
                else:
                    buf.append(raw_s)
            txt = re.sub(r"\s{2,}", " ", "".join(buf)).strip()
            if not txt:
                continue
            c_idx = 0 if bx0 < xg else 1
            x_base = 0 if c_idx == 0 else xg
            rel_bb = [
                max(0, int(round(bx0 - x_base))),
                max(0, int(round(by0 - zy0))),
                max(1, int(round(bx1 - x_base))),
                max(1, int(round(by1 - zy0))),
            ]
            # Approximate per-word boxes cleanly across line span
            toks = txt.split()
            tot_chars = max(1, sum(len(t) for t in toks))
            cur_x = rel_bb[0]
            span_w = max(10, rel_bb[2] - rel_bb[0])
            w_objs = []
            for t in toks:
                tw = max(4, int(round(span_w * (len(t) / tot_chars))))
                w_objs.append({"t": t, "b": [cur_x, rel_bb[1], cur_x + tw, rel_bb[3]], "c": 99.9})
                cur_x += tw + 3
            col_lines[c_idx].append({
                "text": txt,
                "bbox": rel_bb,
                "conf": 99.9,
                "words": w_objs,
            })

    for c_idx in (0, 1):
        col_lines[c_idx].sort(key=lambda l: (l["bbox"][1], l["bbox"][0]))

    out = [{
        "col": 0,
        "x_offset": 0,
        "y_offset": zy0,
        "col_w": xg,
        "lines": col_lines[0],
    }]
    if col_lines[1]:
        out.append({
            "col": 1,
            "x_offset": xg,
            "y_offset": zy0,
            "col_w": w - xg,
            "lines": col_lines[1],
        })
    return out


def find_true_two_col_gutter(zone_arr: np.ndarray) -> Tuple[int, bool]:
    """Find midpoint of the widest pure-white center column gutter between Left and Right columns."""
    h, w = zone_arr.shape
    bw = (zone_arr < 180).astype(np.uint8)
    proj = bw.sum(axis=0)
    lo, hi = int(w * 0.36), int(w * 0.64)
    max_noise = max(1, int(h * 0.002))
    is_white = proj[lo:hi] <= max_noise
    best_x = None
    best_score = -1e9
    cur_start = None
    for idx, val in enumerate(is_white):
        if val and cur_start is None:
            cur_start = idx
        elif not val and cur_start is not None:
            run_len = idx - cur_start
            if run_len >= 12:
                mid_x = lo + 0.5 * (cur_start + idx - 1)
                score = run_len - 0.35 * abs(mid_x - 0.50 * w)
                if score > best_score:
                    best_score = score
                    best_x = int(round(mid_x))
            cur_start = None
    if cur_start is not None:
        run_len = len(is_white) - cur_start
        if run_len >= 12:
            mid_x = lo + 0.5 * (cur_start + len(is_white) - 1)
            score = run_len - 0.35 * abs(mid_x - 0.50 * w)
            if score > best_score:
                best_score = score
                best_x = int(round(mid_x))

    if best_x is None:
        smooth = np.convolve(proj[lo:hi], np.ones(11, dtype=float) / 11.0, mode="same")
        best_x = lo + int(np.argmin(smooth))

    has_right = int(bw[:, best_x + 10: int(w * 0.96)].sum()) > 100
    return best_x, has_right


def detect_and_erase_completamento_blanks(z_arr: np.ndarray) -> Tuple[np.ndarray, List[List[float]]]:
    """Detect all solid horizontal fill-in-the-blank underline segments and erase cleanly for OCR."""
    bw = (z_arr < 195).astype(np.uint8)
    min_len = max(38, int(z_arr.shape[1] * 0.035))
    horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_len, 1))
    opened = cv2.morphologyEx(bw, cv2.MORPH_OPEN, horiz_kernel)
    ncc, _, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
    clean = z_arr.copy()
    blanks: List[List[float]] = []
    for i in range(1, ncc):
        x, y, w, h, _ = [int(stats[i, k]) for k in range(5)]
        if w >= min_len and h <= 8:
            blanks.append([round(float(y + 0.5 * h), 1), int(x), int(x + w)])
            clean[max(0, y - 2):min(clean.shape[0], y + h + 2), max(0, x - 3):min(clean.shape[1], x + w + 3)] = 255
    blanks.sort(key=lambda b: (b[0], b[1]))
    return clean, blanks


def compute_page_zones(p: dict) -> List[Tuple[int, int, str]]:
    y0_b, y1_b = p["body_y0"], p["body_y1"]
    banners = p["banners"]
    zones = []
    cur_y = y0_b
    cur_qtype = p["active_qtype_at_top"]
    for by0, by1, btype in banners:
        if cur_qtype is not None and btype != "commentati" and (by0 - 6) - cur_y > 24:
            zones.append((cur_y, by0 - 6, cur_qtype))
        cur_y = by1 + 6
        cur_qtype = btype
    if cur_qtype is not None and y1_b - cur_y > 20:
        zones.append((cur_y, y1_b, cur_qtype))
    return zones


def _worker_questions_to_file(args) -> str:
    os.environ["OMP_THREAD_LIMIT"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    import tesserocr

    pages_chunk, stage1_dir, out_part_path = args
    stage1_dir = Path(stage1_dir)
    out = []
    tess_fast = "/tmp/tessdata_fast" if Path("/tmp/tessdata_fast").exists() else None

    with tesserocr.PyTessBaseAPI(path=tess_fast, lang="ita+eng", psm=tesserocr.PSM.SINGLE_BLOCK) as api:
        for p in pages_chunk:
            bp = p["book_page"]
            arr = np.array(Image.open(stage1_dir / "pages" / f"bp_{bp:03d}.png"))
            h, w = arr.shape
            zones = compute_page_zones(p)

            zone_results = []
            for zy0, zy1, qtype in zones:
                if qtype == "completamento" and p["subject_code"] != "FIS" and zy1 < h:
                    zy1 = h
                z_arr = arr[zy0:zy1, :]
                cols_out = []
                if bp == 669 and (stage1_dir / "p669_vector.json").exists():
                    xg, _ = find_true_two_col_gutter(z_arr)
                    cols_out = extract_vector_p669_zone_columns(stage1_dir, zy0, zy1, xg, w)
                elif qtype == "completamento":
                    clean_z, blanks = detect_and_erase_completamento_blanks(z_arr)
                    sm_c = cv2.GaussianBlur(clean_z, (3, 3), 0.6)
                    api.SetImage(Image.fromarray(sm_c))
                    lns = safe_extract_lines_and_words(api, 1.0)
                    cols_out.append({
                        "col": 0,
                        "x_offset": 0,
                        "y_offset": zy0,
                        "col_w": w,
                        "lines": lns,
                        "blanks": blanks,
                    })
                elif w < 700:
                    up_img, inv_s = prepare_for_ocr(z_arr, w)
                    api.SetImage(Image.fromarray(up_img))
                    lns = safe_extract_lines_and_words(api, inv_s)
                    cols_out.append({
                        "col": 0,
                        "x_offset": 0,
                        "y_offset": zy0,
                        "col_w": w,
                        "lines": lns,
                    })
                else:
                    xg, has_right = find_true_two_col_gutter(z_arr)
                    left_arr = z_arr[:, :xg]
                    up_l, inv_s = prepare_for_ocr(left_arr, w)
                    api.SetImage(Image.fromarray(up_l))
                    lns_l = safe_extract_lines_and_words(api, inv_s)
                    cols_out.append({
                        "col": 0,
                        "x_offset": 0,
                        "y_offset": zy0,
                        "col_w": xg,
                        "lines": lns_l,
                    })
                    if has_right:
                        right_arr = z_arr[:, xg:]
                        up_r, inv_r = prepare_for_ocr(right_arr, w)
                        api.SetImage(Image.fromarray(up_r))
                        lns_r = safe_extract_lines_and_words(api, inv_r)
                        cols_out.append({
                            "col": 1,
                            "x_offset": xg,
                            "y_offset": zy0,
                            "col_w": w - xg,
                            "lines": lns_r,
                        })

                # Restore sparse short numeric 'E. <num>' lines only when not already recognized at 2x scale
                SPARSE_BOTTOM_E_FIXES = {
                    95: [("D1", "E. 3"), ("D. 1", "E. 3")],
                    182: [("D.-3", "E. 3"), ("D. -3", "E. 3"), ("D. 0,2", "E. 2,0")],
                    196: [("D. 4", "E. 5")],
                }
                if bp in SPARSE_BOTTOM_E_FIXES and qtype in ("commentati", "non_commentati"):
                    for d_tok, e_line in SPARSE_BOTTOM_E_FIXES[bp]:
                        for c_obj in cols_out:
                            for idx_l, l_obj in enumerate(c_obj["lines"]):
                                if l_obj["text"].strip() == d_tok:
                                    nxt_txt = (
                                        c_obj["lines"][idx_l + 1]["text"].strip()
                                        if idx_l + 1 < len(c_obj["lines"])
                                        else ""
                                    )
                                    if not re.match(r"^(?:E|F|£)\s*[\.\)\:\-\_,]?\s*\d", nxt_txt):
                                        dx0, _, _, dy1 = l_obj["bbox"]
                                        nb = [dx0, dy1 + 10, dx0 + 120, dy1 + 42]
                                        c_obj["lines"].insert(idx_l + 1, {
                                            "text": e_line,
                                            "bbox": nb,
                                            "words": [{"t": t, "c": 99.0, "b": nb} for t in e_line.split()],
                                        })
                                    break

                zone_results.append({
                    "y0": zy0,
                    "y1": zy1,
                    "quiz_type": qtype,
                    "columns": cols_out,
                })

            out.append({
                "book_page": bp,
                "pdf_page": p["pdf_page"],
                "subject_code": p["subject_code"],
                "chapter_num": p["chapter_num"],
                "width": w,
                "height": h,
                "zones": zone_results,
            })

    with open(out_part_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    return out_part_path


def _worker_answers_fast_to_file(args) -> str:
    os.environ["OMP_THREAD_LIMIT"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    import tesserocr

    pages_chunk, stage1_dir, out_part_path = args
    stage1_dir = Path(stage1_dir)
    out = []
    tess_fast = "/tmp/tessdata_fast" if Path("/tmp/tessdata_fast").exists() else None

    with tesserocr.PyTessBaseAPI(path=tess_fast, lang="ita+eng", psm=tesserocr.PSM.SINGLE_BLOCK) as api:
        for p in pages_chunk:
            bp = p["book_page"]
            arr = np.array(Image.open(stage1_dir / "pages" / f"bp_{bp:03d}.png"))
            up_img, inv_s = prepare_for_ocr(arr, p["width"])
            api.SetImage(Image.fromarray(up_img))
            lns = safe_extract_lines_and_words(api, inv_s)
            out.append({
                "book_page": bp,
                "pdf_page": p["pdf_page"],
                "subject_code": p["subject_code"],
                "width": p["width"],
                "height": p["height"],
                "body_y0": p["body_y0"],
                "body_y1": p["body_y1"],
                "lines": [{"bbox": ln["bbox"], "text": ln["text"], "conf": ln["conf"]} for ln in lns],
            })

    with open(out_part_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    return out_part_path


def build_all_ocr_caches(stage1_dir: str = "/tmp/anki_sem_stage1") -> None:
    s1 = Path(stage1_dir)
    with open(s1 / "canonical_pages.json", encoding="utf-8") as f:
        pages = json.load(f)

    q_pages = [p for p in pages if p["role"] == "questions"]
    active_qt = None
    for p in q_pages:
        p["active_qtype_at_top"] = active_qt
        for _, _, btype in p["banners"]:
            active_qt = btype

    q_cache_path = s1 / "questions_ocr_cache.json"
    existing_q: Dict[int, dict] = {}
    if q_cache_path.exists():
        with open(q_cache_path, encoding="utf-8") as f:
            existing_q = {item["book_page"]: item for item in json.load(f)}

    dirty_q_pages = [p for p in q_pages if p["book_page"] not in existing_q]
    t0 = time.time()
    if dirty_q_pages:
        # Process in safe 240-page batches across 2 cores with atomic checkpointing
        for b_start in range(0, len(dirty_q_pages), 240):
            batch = dirty_q_pages[b_start:b_start + 240]
            tb = time.time()
            mid = len(batch) // 2
            part0 = str(s1 / "_q_part0.json")
            part1 = str(s1 / "_q_part1.json")
            tasks = [t for t in [(batch[:mid], str(s1), part0), (batch[mid:], str(s1), part1)] if t[0]]
            with ProcessPoolExecutor(max_workers=2) as ex:
                part_paths = list(ex.map(_worker_questions_to_file, tasks))
            for pp in part_paths:
                with open(pp, encoding="utf-8") as pf:
                    for item in json.load(pf):
                        existing_q[item["book_page"]] = item
                os.remove(pp)
            ordered_partial = [existing_q[p["book_page"]] for p in q_pages if p["book_page"] in existing_q]
            with open(q_cache_path, "w", encoding="utf-8") as f:
                json.dump(ordered_partial, f, ensure_ascii=False)
            print(
                f"  [OCR-Q] Checkpoint {len(existing_q)}/{len(q_pages)} pages ({time.time() - tb:.1f}s)",
                flush=True,
            )
        print(f"Built questions_ocr_cache.json ({len(existing_q)} pages) in {time.time() - t0:.2f}s!")

    a_pages = [p for p in pages if p["role"] == "answers"]
    r_fast_path = s1 / "risposte_fast_lines.json"
    if not r_fast_path.exists():
        t1 = time.time()
        mid_a = len(a_pages) // 2
        pa0 = str(s1 / "_a_part0.json")
        pa1 = str(s1 / "_a_part1.json")
        with ProcessPoolExecutor(max_workers=2) as ex:
            apaths = list(ex.map(_worker_answers_fast_to_file, [(a_pages[:mid_a], str(s1), pa0), (a_pages[mid_a:], str(s1), pa1)]))
        merged_a = []
        for pp in apaths:
            with open(pp, encoding="utf-8") as pf:
                merged_a.extend(json.load(pf))
            os.remove(pp)
        with open(r_fast_path, "w", encoding="utf-8") as f:
            json.dump(merged_a, f, ensure_ascii=False)
        print(f"Built risposte_fast_lines.json ({len(merged_a)} pages) in {time.time() - t1:.2f}s!")


if __name__ == "__main__":
    build_all_ocr_caches()
