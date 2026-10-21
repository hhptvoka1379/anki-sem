from __future__ import annotations

import json
import multiprocessing
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
try:
    import tesserocr
except ImportError:
    tesserocr = None
from PIL import Image

from extractor.stage1_canonicalize import SUBJECT_CHAPTERS
from extractor.visual_formula_overrides import VISUAL_MCQ_OVERRIDES

SUB_MAP = str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋")
SUP_MAP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶₇⁸⁹⁺⁻")

OPT_LIST = ["A", "B", "C", "D", "E"]

STRONG_OPT = {
    "A": re.compile(r"^(?:A|À)\s*[\.\)\:\-\_,]\s*(.*)$"),
    "B": re.compile(r"^(?:B|8|R)\s*[\.\)\:\-\_,]\s*(.*)$"),
    "C": re.compile(r"^(?:C|Cc|CC|c|€|©|\(|G|CG|GC|\{)\s*[\.\)\:\-\_,]\s*(.*)$"),
    "D": re.compile(r"^(?:D|dD|0)\s*[\.\)\:\-\_,]\s*(.*)$"),
    "E": re.compile(r"^(?:E|F|FE|Ff|£)\s*[\.\)\:\-\_,]\s*(.*)$"),
}

Q_HDR_RE = re.compile(r"^([0-9Il|SsoOQzZ]{1,3})\s*[\)\}\]]\s*(.*)$")

KEEP_HYPHEN_PREFIXES = (
    "cis", "trans", "alfa", "alpha", "beta", "gamma", "delta", "omega",
    "meta", "orto", "para", "endo", "eso", "exo", "anti", "sin", "syn",
    "mono", "bi", "di", "tri", "tetra", "penta", "esa", " non", "co", "sub",
)


def is_running_hdr_or_ftr(txt: str, y0_page: int, y1_page: int, page_h: int) -> bool:
    low = txt.strip().lower()
    if y0_page < max(140, int(page_h * 0.09)):
        if re.match(r"^[\d\$]{1,3}[\.\s]+(chimica|chinuca|chinuica|biologia|fisica)", low):
            return True
        if re.search(r"\bcapitolo\b", low) and (re.search(r"\d{1,3}\s*$", low) or len(low) < 18):
            return True
        if low in ("capit", "capitolo", "commentati", "n commentati") or (low.startswith("quiz ") and len(low) < 40):
            return True
    if "wwwedises" in low or "www.edises" in low or "chimicaepropedeutica" in low:
        return True
    if y1_page > int(page_h * 0.78):
        if re.search(
            r"\b(edises|edlses|ediss|edives|edices|odices|tedises|esses|edison|ediaes|oxices|sases|xiscs|services|saisos|exces|exists)\b",
            low,
        ) or low in (
            "een cs sd",
            "sio |",
            'she is "2',
            'she is "2"',
            "capit",
            "e ee n",
        ):
            return True
    if y0_page > int(page_h * 0.945):
        alpha_only = re.sub(r"[^a-zà-ÿ]", "", low)
        if len(alpha_only) <= 8 and not low.endswith("."):
            return True
    return False


def join_wrapped_italian_lines(lines: List[str]) -> str:
    """Join multi-line text cleanly while resolving Italian syllable line-break hyphens
    and preserving genuine scientific/chemical hyphens (e.g., cis-, D-, C-H, E2F-DP1)."""
    out = ""
    for raw in lines:
        part = raw.strip()
        if not part:
            continue
        if not out:
            out = part
            continue
        if out.endswith("-") and not out.endswith(" -") and len(out) >= 3:
            # Extract trailing token before '-'
            m_prev = re.search(r"([A-Za-zÀ-ÿ0-9]+)-$", out)
            m_next = re.match(r"^([a-zà-ÿ]{2,})", part)
            if m_prev and m_next:
                stem = m_prev.group(1)
                preserve = (
                    len(stem) == 1
                    or any(ch.isdigit() for ch in stem)
                    or stem.isupper()
                    or stem.lower() in KEEP_HYPHEN_PREFIXES
                )
                if not preserve:
                    out = out[:-1] + part
                    continue
        out = out + " " + part
    return re.sub(r"\s{2,}", " ", out).strip()


def clean_prose_ocr_quirks(txt: str, is_question_stem: bool = False) -> str:
    """Safe, zero-hallucination typography & chemical formula normalizations."""
    s = txt.strip()
    # Never allow decimal commas between digits to stay subscripted if present
    s = re.sub(r"(\d)[₀₁₂₃₄₅₆₇₈₉](\d)", r"\1,\2", s)

    # Join syllable hyphenation across line breaks (including after apostrophes like l'i- potesi, dell'a- tomo, COR- RETTA)
    def _dehyph_inline(m: re.Match) -> str:
        apos_pre, stem, tail = m.group(1) or "", m.group(2), m.group(3)
        full_pre = apos_pre + stem
        if stem.lower() in KEEP_HYPHEN_PREFIXES or full_pre.lower() in KEEP_HYPHEN_PREFIXES:
            return m.group(0)
        if any(c.isdigit() for c in full_pre):
            return m.group(0)
        # Single-letter prefix without apostrophe: keep ('D- glucosio', 'L- alanina', 'p- orbitali', 'C - H')
        if not apos_pre and len(stem) == 1:
            return m.group(0)
        # All-uppercase chemical bond without ALL-CAPS tail (e.g. 'CH - CH'): keep if tail is not uppercase word
        if stem.isupper() and not tail.isupper():
            return m.group(0)
        return full_pre + tail

    s = re.sub(r"((?:[A-Za-zÀ-ÿ]+['’])?)([A-Za-zÀ-ÿ]+)-\s+([A-Za-zÀ-ÿ]{2,})\b", _dehyph_inline, s)

    # Restore elided Italian article before fill-in-the-blank slot ('L _____' -> "L'_____")
    s = re.sub(r"\bL\s+_____", "L'_____", s)
    # Restore 'g eq⁻¹' misread as 'geq!', 'g eq"!', 'g eq”!', 'g eq:!'
    s = re.sub(r"(\d)\s*g\s*eq\s*[\"'’”!:;\-¹1]+", r"\1 g·eq⁻¹", s)
    # Fix OCR capital-I in chlorine compounds (HCIO -> HClO, NaCI -> NaCl, KCI -> KCl, NH₄CI -> NH₄Cl)
    s = re.sub(r"\b(H|K|Na|Li|Ag|Cu|NH₄|NH₃)CI([O₀-₉0-9\b])", r"\1Cl\2", s)
    s = re.sub(r"\b(Ca|Mg|Ba|Zn|Fe|Al)CI([₂₃23\b])", r"\1Cl\2", s)
    s = re.sub(r"\b(Na|K|H|Li|Ag|NH₄)CI\b", r"\1Cl", s)
    # Fix unambiguous chemical formulas
    s = re.sub(r"(?<![A-Za-z0-9,])H,[O0]\b", "H₂O", s)
    s = re.sub(r"\bH₂0\b|\bH30°\b|\bH3O\+\b", lambda m: "H₂O" if "2" in m.group(0) or "₂" in m.group(0) else "H₃O⁺", s)
    s = re.sub(r"\{H,\)", "(H₂)", s)
    s = re.sub(r"\(NH,\}", "(NH₃)", s)
    s = re.sub(r"\bN,\s*\+\s*3\s*H,", "N₂ + 3 H₂", s)
    # Deduplicate any excess repeated blank bars on a single slot
    s = re.sub(r"(?:_____\s*){2,}", "_____ ", s)
    # Clean reaction arrows OCR'd as '—-', '-+', '—+'
    s = re.sub(r"\s*(?:—-|-\+|—\+)\s*", " → ", s)
    # Strip any inline page-break running header/footer fragment
    s = re.sub(
        r"\s*(?:roses\.\s*=\s*DIA\s*|saisos\s+PZ\s+DIN\s*)?(?:\d{2,3}|[A-Z]\d)\s+"
        r"(?:Chimica\s*e\s*Propedeutica\s*Biochimica|Biologia|Fisica)\s+Quiz\s+(?:non\s+)?(?:commentati|a completamento)\b",
        "",
        s,
        flags=re.I,
    )
    if is_question_stem and s.endswith("7") and re.match(r"^(?:Quanti|Quante|Quale|Quali|Qual|Come|Dove|Chi|Che)\b", s):
        s = s[:-1] + "?"
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def repair_word_sub_sup(word_gray: np.ndarray, raw_tok: str, char_api) -> str:
    """Use connected-component geometry + 5x upscaled digit-whitelisted LSTM OCR
    to restore subscript/superscript digits (e.g., H,PO, -> H₃PO₄, sp? -> sp², 1s? -> 1s²)."""
    if word_gray.size == 0 or word_gray.shape[0] < 8 or word_gray.shape[1] < 6:
        return raw_tok
    H, W = word_gray.shape
    _, bw = cv2.threshold(word_gray, 192, 255, cv2.THRESH_BINARY_INV)
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    ccs = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area < 4:
            continue
        ccs.append([x, y, x + w, y + h, area])
    ccs.sort(key=lambda c: c[0])
    if len(ccs) < 2:
        return raw_tok

    merged = [ccs[0]]
    for c in ccs[1:]:
        prev = merged[-1]
        overlap = min(prev[2], c[2]) - max(prev[0], c[0])
        if overlap >= min(prev[2] - prev[0], c[2] - c[0]) * 0.45:
            prev[0] = min(prev[0], c[0])
            prev[1] = min(prev[1], c[1])
            prev[2] = max(prev[2], c[2])
            prev[3] = max(prev[3], c[3])
            prev[4] += c[4]
        else:
            merged.append(c)

    tall = [c for c in merged if (c[3] - c[1]) >= H * 0.40]
    if not tall:
        return raw_tok
    main_h = float(np.median([c[3] - c[1] for c in tall]))
    main_y0 = float(np.median([c[1] for c in tall]))
    main_y1 = float(np.median([c[3] for c in tall]))

    sub_sup_runs: List[Tuple[str, str]] = []
    for x0, y0, x1, y1, _ in merged:
        gh, gw = y1 - y0, x1 - x0
        is_sub = (gh <= main_h * 0.78) and (y1 > main_y1 + 1.0) and (y0 > main_y0 + main_h * 0.25)
        is_sup = (gh <= main_h * 0.78) and (y1 < main_y1 - main_h * 0.16)
        if not (is_sub or is_sup):
            continue
        kind = "sup" if is_sup else "sub"
        if gw >= gh * 2.1 and gh <= 6:
            ch = "⁻" if is_sup else "₋"
        else:
            sub_img = word_gray[max(0, y0 - 1):min(H, y1 + 1), max(0, x0 - 1):min(W, x1 + 1)]
            up = cv2.resize(sub_img, (0, 0), fx=5.0, fy=5.0, interpolation=cv2.INTER_CUBIC)
            up = cv2.copyMakeBorder(up, 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=255)
            char_api.SetImage(Image.fromarray(up))
            d = char_api.GetUTF8Text().strip()[:1]
            if not d:
                return raw_tok
            ch = d.translate(SUP_MAP if is_sup else SUB_MAP)
        sub_sup_runs.append((kind, ch))

    if not sub_sup_runs:
        return raw_tok

    # Check exact 1-to-1 bijection between suspect non-alphanumeric slots inside token and detected sub/sup components!
    # Exclude genuine trailing sentence punctuation (final '?' on a question word when preceded by another suspect slot).
    # Pre-normalize 'y' misread as subscript '8' inside hydrocarbon formulas like 'C,Hy0' -> 'C,H,0'
    core = re.sub(r"(C[,0-9]+H)[yY]", r"\1,", raw_tok)
    trail = ""
    if core.endswith("?") and len(re.findall(r"[,\?\*;']", core)) == len(sub_sup_runs) + 1:
        trail = "?"
        core = core[:-1]
    elif core.endswith((".", ":", ";")) and len(re.findall(r"[,\?\*;']", core[:-1])) == len(sub_sup_runs):
        trail = core[-1]
        core = core[:-1]

    bad_matches = list(re.finditer(r"[,\?\*;']", core))
    if len(bad_matches) == len(sub_sup_runs):
        chars = list(core)
        for bm, (_, repl_ch) in zip(bad_matches, sub_sup_runs):
            chars[bm.start()] = repl_ch
        repaired = "".join(chars)
        repaired = re.sub(r"([A-Z])0([₀₁₂₃₄₅₆₇₈₉\?])", r"\1O\2", repaired)
        repaired = re.sub(r"\b50([₂₃₄])", r"SO\1", repaired)
        return repaired + trail

    return raw_tok


def maybe_repair_line_formulas(
    ln: dict,
    page_gray: Optional[np.ndarray],
    x_off: int,
    y_off: int,
    char_api,
) -> str:
    if page_gray is None or not ln.get("words"):
        return ln["text"].strip()
    changed = False
    rebuilt: List[str] = []
    words = ln["words"]
    wi = 0
    while wi < len(words):
        w = words[wi]
        wt = w["t"]
        # Join detached raised exponent tokens right after a unit/number (e.g. 'pascal/m' + '?' -> 'pascal/m²')
        if wi + 1 < len(words):
            wn = words[wi + 1]
            nt = wn["t"].strip()
            w_h = max(8, w["b"][3] - w["b"][1])
            gap_x = wn["b"][0] - w["b"][2]
            if (
                0 <= gap_x <= 16
                and nt in ("?", "!", "'", "2", "3", "4", "-1", "-2", "-3")
                and wn["b"][3] < w["b"][3] - 0.16 * w_h
                and re.search(r"[A-Za-z0-9]$", wt)
            ):
                if nt.lstrip("-").isdigit():
                    sup_str = nt.translate(SUP_MAP)
                else:
                    sx0 = max(0, x_off + wn["b"][0] - 2)
                    sx1 = min(page_gray.shape[1], x_off + wn["b"][2] + 3)
                    sy0 = max(0, y_off + wn["b"][1] - 3)
                    sy1 = min(page_gray.shape[0], y_off + wn["b"][3] + 3)
                    scrop = page_gray[sy0:sy1, sx0:sx1]
                    if scrop.size > 0:
                        up = cv2.resize(scrop, (0, 0), fx=5.0, fy=5.0, interpolation=cv2.INTER_CUBIC)
                        up = cv2.copyMakeBorder(up, 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=255)
                        char_api.SetImage(Image.fromarray(up))
                        d = char_api.GetUTF8Text().strip()[:2]
                        sup_str = d.translate(SUP_MAP) if d else ""
                    else:
                        sup_str = ""
                if sup_str:
                    rebuilt.append(wt + sup_str)
                    changed = True
                    wi += 2
                    continue

        if re.search(r"[A-Za-z0-9][,\?\*;']", wt) and len(wt) <= 18:
            # NEVER corrupt decimal commas ('0,2', '346,05', '3,5,2'), apostrophe words, phase labels ('G1,'), or prose commas!
            if re.search(r"\d,\d", wt):
                rebuilt.append(wt)
                wi += 1
                continue
            if re.match(r"^[A-Za-zÀ-ÿ]+['’][A-Za-zÀ-ÿ0-9]+[\.,\?\:\;]?$", wt):
                rebuilt.append(wt)
                wi += 1
                continue
            if re.match(r"^[A-ZÀ-Ý]?[a-zà-ÿ]{2,}[,;]$", wt) or re.match(r"^[A-Za-z]+\d+[,;\.\?\:]$", wt):
                rebuilt.append(wt)
                wi += 1
                continue
            if wt[0].islower() and not re.match(r"^(?:[spdf]|sp|cm|mm|km|kg|mol)[,\?\*;0-9]", wt):
                rebuilt.append(wt)
                wi += 1
                continue
            wx0 = max(0, x_off + w["b"][0] - 2)
            wx1 = min(page_gray.shape[1], x_off + w["b"][2] + 4)
            wy0 = max(0, y_off + w["b"][1] - 4)
            wy1 = min(page_gray.shape[0], y_off + w["b"][3] + 5)
            nw = repair_word_sub_sup(page_gray[wy0:wy1, wx0:wx1], wt, char_api)
            if nw != wt:
                changed = True
            rebuilt.append(nw)
        else:
            rebuilt.append(wt)
        wi += 1
    return " ".join(rebuilt).strip() if changed else ln["text"].strip()


def reocr_option_after_prefix_valley(
    page_gray: np.ndarray,
    x_off: int,
    y_off: int,
    bbox: List[int],
    line_api,
    char_api,
) -> str:
    """Slice strictly to the right of the printed 'A.'..'E.' label pixel valley at 4x cubic upscale!
    Prevents short chemical symbol options like 'A. I', 'A. F', 'C. K', 'D. B', 'C. P' from fusing."""
    lx0, ly0, lx1, ly1 = bbox
    ax0 = max(0, x_off + lx0 - 2)
    ax1 = min(page_gray.shape[1], x_off + lx1 + 14)
    ay0 = max(0, y_off + ly0 - 5)
    ay1 = min(page_gray.shape[0], y_off + ly1 + 6)
    crop = page_gray[ay0:ay1, ax0:ax1]
    if crop.size == 0 or crop.shape[1] < 24:
        return ""
    # Locate the white gap right after 'A.' (typically at offset 20..52 px from lx0)
    dark_col = (crop < 190).sum(axis=0)
    search_lo = min(18, crop.shape[1] - 4)
    search_hi = min(56, crop.shape[1] - 2)
    cut_x = None
    in_letter = False
    for xi in range(0, search_hi):
        if dark_col[xi] >= 2:
            in_letter = True
        elif in_letter and xi >= search_lo:
            # Find end of white gap after dot '.' if a dot follows within 12 px
            dot_end = xi
            for xj in range(xi, min(xi + 16, search_hi)):
                if dark_col[xj] >= 2:
                    dot_end = xj + 1
            cut_x = dot_end
            break
    if cut_x is None or cut_x >= crop.shape[1] - 3:
        return ""
    rhs = crop[:, cut_x:]
    if (rhs < 195).sum() < 6:
        return ""
    up = cv2.resize(rhs, (0, 0), fx=4.0, fy=4.0, interpolation=cv2.INTER_CUBIC)
    up = cv2.copyMakeBorder(up, 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=255)
    line_api.SetImage(Image.fromarray(up))
    val = line_api.GetUTF8Text().strip()
    # Also repair subscript/superscript if present on short ion/formula
    rep = repair_word_sub_sup(rhs, val, char_api) if val else ""
    return rep if rep else val


def detect_and_save_figure_crop(
    page_gray: np.ndarray,
    col_x_off: int,
    col_w: int,
    z_y0: int,
    lines_in_col: List[dict],
    fig_path: Path,
) -> Optional[str]:
    """Mask all OCR word boxes to white inside the question's column span and check
    whether genuine non-text graphic ink (diagram, chemical ring, pedigree, circuit, table) remains."""
    if not lines_in_col:
        return None
    min_ly0 = min(l["bbox"][1] for l in lines_in_col)
    max_ly1 = max(l["bbox"][3] for l in lines_in_col)
    rx0 = max(0, col_x_off - 4)
    rx1 = min(page_gray.shape[1], col_x_off + col_w + 4)
    ry0 = max(0, z_y0 + min_ly0 - 8)
    ry1 = min(page_gray.shape[0], z_y0 + max_ly1 + 10)
    if ry1 - ry0 < 48 or rx1 - rx0 < 80:
        return None

    region = page_gray[ry0:ry1, rx0:rx1].copy()
    masked = region.copy()
    word_hs = [w["b"][3] - w["b"][1] for l in lines_in_col for w in l.get("words", []) if (w["b"][3] - w["b"][1]) > 4]
    med_wh = float(np.median(word_hs)) if word_hs else 24.0
    max_text_h = max(56.0, 2.25 * med_wh)
    for l in lines_in_col:
        for w in l.get("words", []):
            # Only leave unmasked genuine tall multi-line diagram boxes (> max_text_h) or ultra-low-conf diagram noise (< 40)!
            if (w["b"][3] - w["b"][1]) > max_text_h or w.get("c", 90.0) < 40.0:
                continue
            wx0 = max(0, col_x_off + w["b"][0] - rx0 - 7)
            wx1 = min(masked.shape[1], col_x_off + w["b"][2] - rx0 + 7)
            wy0 = max(0, z_y0 + w["b"][1] - ry0 - 7)
            wy1 = min(masked.shape[0], z_y0 + w["b"][3] - ry0 + 7)
            masked[wy0:wy1, wx0:wx1] = 255

    _, bw = cv2.threshold(masked, 185, 255, cv2.THRESH_BINARY_INV)
    num_l, _, stats, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    big_graphic = False
    total_residual_ink = 0
    for i in range(1, num_l):
        _, _, w, h, area = stats[i]
        if area >= 40:
            total_residual_ink += int(area)
        if (w >= 42 and h >= 38 and area >= 220) or (area >= 480 and h >= 26):
            big_graphic = True
            break

    if not big_graphic and total_residual_ink < 950:
        return None

    fig_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(fig_path), region)
    return str(fig_path.name)


def split_inline_segs(ln: dict, repaired_line_text: str) -> List[Tuple[int, int, str, List[int]]]:
    words = ln.get("words", [])
    if not words:
        return [(ln["bbox"][0], ln["bbox"][1], repaired_line_text.strip(), ln["bbox"])]
    segs = []
    cur = [words[0]]
    for w in words[1:]:
        gap_x = w["b"][0] - cur[-1]["b"][2]
        tc = w["t"].strip()
        if gap_x >= 14 and re.match(r"^(?:[ABCDEabcde]|Cc|FE|Ff)[\.\)\:](\S*)$", tc):
            sb = [cur[0]["b"][0], min(x["b"][1] for x in cur), cur[-1]["b"][2], max(x["b"][3] for x in cur)]
            segs.append((cur[0]["b"][0], cur[0]["b"][1], " ".join(x["t"] for x in cur).strip(), sb))
            cur = [w]
        else:
            cur.append(w)
    if len(segs) == 0:
        return [(ln["bbox"][0], ln["bbox"][1], repaired_line_text.strip(), ln["bbox"])]
    sb = [cur[0]["b"][0], min(x["b"][1] for x in cur), cur[-1]["b"][2], max(x["b"][3] for x in cur)]
    segs.append((cur[0]["b"][0], cur[0]["b"][1], " ".join(x["t"] for x in cur).strip(), sb))
    return segs


def strip_known_opt_prefix(letter: str, txt: str) -> Tuple[str, bool]:
    """Return (clean_option_body, matched_clean_separator)."""
    t = txt.strip()
    m_clean = re.match(rf"^{letter}\s*[\.\)\:\,]\s*(.*)$", t)
    if m_clean and m_clean.group(1).strip():
        return m_clean.group(1).strip(), True
    rx = STRONG_OPT[letter]
    m_s = rx.match(t)
    if m_s and m_s.group(1).strip():
        return m_s.group(1).strip(), True
    # Space-separated without dot: 'Cc 5 moli', 'E +2', 'A Ba'
    m_sp = re.match(r"^(?:[ABCDEabcde]|Cc|CC|GC|CG|FE|Ff|dD)\s+(\S.*)$", t)
    if m_sp:
        return m_sp.group(1).strip(), True
    return t, False


def process_subject_questions_to_file(args) -> str:
    subj_code, pages_subset, s2_lookup, stage1_dir_str, fig_dir_str, out_path_str = args
    s1_dir = Path(stage1_dir_str)
    fig_dir = Path(fig_dir_str)
    page_img_cache: Dict[int, np.ndarray] = {}

    def get_page_gray(bp_num: int) -> np.ndarray:
        if bp_num not in page_img_cache:
            # Keep bounded cache per worker
            if len(page_img_cache) > 24:
                page_img_cache.clear()
            page_img_cache[bp_num] = cv2.imread(str(s1_dir / f"pages/bp_{bp_num:03d}.png"), cv2.IMREAD_GRAYSCALE)
        return page_img_cache[bp_num]

    chapters = [c for c in SUBJECT_CHAPTERS if c[1] == subj_code]
    blocks_out = []

    tess_dir = "/tmp/tessdata_best" if Path("/tmp/tessdata_best").exists() else "/tmp/tessdata_fast"
    with (
        tesserocr.PyTessBaseAPI(path=tess_dir, lang="eng", psm=tesserocr.PSM.SINGLE_CHAR) as char_api,
        tesserocr.PyTessBaseAPI(path=tess_dir, lang="ita+eng", psm=tesserocr.PSM.SINGLE_LINE) as line_api,
    ):
        char_api.SetVariable("tessedit_char_whitelist", "0123456789+-")

        for subj_name, code, ch, ch_title, _, _ in chapters:
            ch_pages = [p for p in pages_subset if p["chapter_num"] == ch]

            # 1 & 2: Multiple-choice subsections ('commentati' and 'non_commentati')
            for qt in ("commentati", "non_commentati"):
                exp = s2_lookup[(code, ch, qt)]["count"]
                col_stream = []
                for p in ch_pages:
                    for z in p["zones"]:
                        if z["quiz_type"] != qt:
                            continue
                        zy0 = z["y0"]
                        for col in z["columns"]:
                            lns = [
                                ln for ln in col["lines"]
                                if not is_running_hdr_or_ftr(ln["text"], zy0 + ln["bbox"][1], zy0 + ln["bbox"][3], p["height"])
                            ]
                            if not lns:
                                continue
                            x_m = int(sorted(l["bbox"][0] for l in lns)[max(0, len(lns) // 10)])
                            prev_y1 = None
                            for l in lns:
                                gap = 999 if prev_y1 is None else (l["bbox"][1] - prev_y1)
                                prev_y1 = l["bbox"][3]
                                col_stream.append((
                                    p["book_page"],
                                    col["col"],
                                    col["x_offset"],
                                    col["col_w"],
                                    zy0,
                                    x_m,
                                    gap,
                                    l["bbox"],
                                    l["text"].strip(),
                                    l,
                                ))

                found: List[Tuple[int, int]] = []
                for idx_i, item in enumerate(col_stream):
                    _, _, _, _, _, x_m, gap, bb, txt, _ = item
                    if bb[0] <= x_m + 34:
                        m = Q_HDR_RE.match(txt)
                        if m:
                            dn = m.group(1).translate(str.maketrans("Il|SsoOQzZ", "1115500022"))
                            if dn.isdigit():
                                n = int(dn)
                                exp_n = len(found) + 1
                                if n == exp_n and (exp_n == 1 or gap >= 15):
                                    found.append((n, idx_i))
                                elif exp_n < n <= min(exp, exp_n + 4) and gap >= 15:
                                    ahead = []
                                    for k in range(idx_i + 1, min(len(col_stream), idx_i + 55)):
                                        mk = Q_HDR_RE.match(col_stream[k][8])
                                        if mk and col_stream[k][7][0] <= col_stream[k][5] + 34 and col_stream[k][6] >= 15:
                                            dnk = mk.group(1).translate(str.maketrans("Il|SsoOQzZ", "1115500022"))
                                            if dnk.isdigit():
                                                ahead.append(int(dnk))
                                    if (n + 1) in ahead or n == exp:
                                        miss_cnt = n - exp_n
                                        prev_idx = found[-1][1] if found else -1
                                        cands_between = [
                                            (col_stream[u][6], u)
                                            for u in range(prev_idx + 1, idx_i)
                                            if col_stream[u][7][0] <= col_stream[u][5] + 38
                                            and col_stream[u][6] >= 16
                                            and not re.match(r"^[ABCDEabcde][\.\)]\s", col_stream[u][8])
                                        ]
                                        cands_between.sort(reverse=True)
                                        for m_off, u_pos in enumerate(sorted(u for _, u in cands_between[:miss_cnt])):
                                            found.append((exp_n + m_off, u_pos))
                                        found.append((n, idx_i))

                while len(found) < exp:
                    prev_idx = found[-1][1] if found else -1
                    cands_after = [
                        (col_stream[u][6], u)
                        for u in range(prev_idx + 1, len(col_stream))
                        if col_stream[u][7][0] <= col_stream[u][5] + 38
                        and col_stream[u][6] >= 18
                        and not re.match(r"^[ABCDEabcde][\.\)]\s", col_stream[u][8])
                    ]
                    cands_after.sort(reverse=True)
                    found.append((len(found) + 1, cands_after[0][1]))

                assert len(found) == exp, f"{code} C{ch:02d} {qt}: got {len(found)} vs {exp}"

                q_records = []
                for qi in range(exp):
                    qnum = qi + 1
                    s_i = found[qi][1]
                    e_i = found[qi + 1][1] if qi + 1 < exp else len(col_stream)
                    q_slice = col_stream[s_i:e_i]

                    # Build segment list with formula subscript/superscript repair!
                    segs = []
                    for li_idx, (bp, cidx, x_off, col_w, zy0, x_m, gap, bb, raw_txt, lobj) in enumerate(q_slice):
                        pgray = get_page_gray(bp)
                        rep_txt = maybe_repair_line_formulas(lobj, pgray, x_off, zy0, char_api)
                        if li_idx == 0:
                            m0 = Q_HDR_RE.match(rep_txt)
                            stem0 = m0.group(2).strip() if m0 else rep_txt
                            segs.append((bp, cidx, x_off, col_w, zy0, bb[0], x_m, gap, stem0, bb, lobj))
                        else:
                            for sub_i, (sx0, _, stxt, sbb) in enumerate(split_inline_segs(lobj, rep_txt)):
                                segs.append((bp, cidx, x_off, col_w, zy0, sx0, x_m, gap if sub_i == 0 else 99, stxt, sbb, lobj))

                    # Pass 1: Monotonic strong anchor match with remaining-slot guard (len(segs) - 1 - si >= 4 - oi)
                    anchors: Dict[str, int] = {}
                    last_si = 0
                    for oi, L in enumerate(OPT_LIST):
                        rx = STRONG_OPT[L]
                        for si in range(last_si + 1, len(segs) - (4 - oi)):
                            sx0, x_m, stxt = segs[si][5], segs[si][6], segs[si][8]
                            if sx0 <= x_m + 220 and rx.match(stxt):
                                anchors[L] = si
                                last_si = si
                                break

                    # Pass 2: Exact pigeonhole interpolation between adjacent anchor indices
                    if len(anchors) < 5:
                        oi = 0
                        while oi < 5:
                            if OPT_LIST[oi] in anchors:
                                oi += 1
                                continue
                            oj = oi
                            while oj < 5 and OPT_LIST[oj] not in anchors:
                                oj += 1
                            left_si = anchors[OPT_LIST[oi - 1]] if oi > 0 else 0
                            right_si = anchors[OPT_LIST[oj]] if oj < 5 else len(segs)
                            need = oj - oi
                            margin_cands = [
                                si for si in range(left_si + 1, right_si)
                                if segs[si][5] <= segs[si][6] + 24
                            ]
                            if oi == 0 and len(margin_cands) >= need:
                                chosen = margin_cands[-need:]
                            elif len(margin_cands) >= need:
                                chosen = margin_cands[:need]
                            else:
                                chosen = list(range(left_si + 1, right_si))[:need]
                            for k_off, si_pick in enumerate(chosen):
                                anchors[OPT_LIST[oi + k_off]] = si_pick
                            oi = oj

                    assert len(anchors) >= 1 or len(segs) >= 1, f"Empty question on {code} C{ch} {qt} Q{qnum}"

                    valid_opt_sis = sorted(anchors.values())
                    first_opt_si = valid_opt_sis[0] if valid_opt_sis else len(segs)
                    stem_lines = [segs[si][8] for si in range(0, first_opt_si)]
                    stem_text = clean_prose_ocr_quirks(join_wrapped_italian_lines(stem_lines), is_question_stem=True)

                    options_dict: Dict[str, str] = {}
                    graphical_opt = False
                    for oi, L in enumerate(OPT_LIST):
                        if L not in anchors:
                            graphical_opt = True
                            options_dict[L] = f"[Opzione grafica {L} — vedi figura]"
                            continue
                        si_start = anchors[L]
                        nxt_anchored = [anchors[OPT_LIST[u]] for u in range(oi + 1, 5) if OPT_LIST[u] in anchors]
                        si_end = nxt_anchored[0] if nxt_anchored else len(segs)
                        bp_o, _, x_off_o, _, zy0_o, _, _, _, head_txt, sbb_o, _ = segs[si_start]
                        body0, was_clean = strip_known_opt_prefix(L, head_txt)
                        if not was_clean:
                            re_rhs = reocr_option_after_prefix_valley(
                                get_page_gray(bp_o), x_off_o, zy0_o, sbb_o, line_api, char_api
                            )
                            if re_rhs:
                                body0 = re_rhs
                            elif len(body0) >= 2 and body0[0].upper() == L:
                                body0 = body0[1:].lstrip(".,:)_ ")
                        opt_lines = [body0] + [segs[u][8] for u in range(si_start + 1, si_end)]
                        opt_text = clean_prose_ocr_quirks(join_wrapped_italian_lines(opt_lines))
                        if not opt_text:
                            graphical_opt = True
                            opt_text = f"[Opzione grafica {L} — vedi figura]"
                        options_dict[L] = opt_text

                    # Context-disambiguate standalone vertical-bar OCR 'I'/'1' and 'Cl' halogen symbol across sibling options!
                    others = {k: v for k, v in options_dict.items() if v not in ("|", "l")}
                    all_numeric_siblings = len(others) >= 3 and all(re.match(r"^[\+\-]?\d+(?:[,\./]\d+)?$", v) for v in others.values())
                    all_element_siblings = len(others) >= 3 and all(re.match(r"^[A-Z][a-z]?$", v) for v in others.values())
                    for k, v in list(options_dict.items()):
                        if v in ("|", "l"):
                            options_dict[k] = "1" if all_numeric_siblings else ("I" if all_element_siblings else "1")
                        elif v == "CI" and all_element_siblings:
                            options_dict[k] = "Cl"

                    # Strip any residual duplicated leading option prefix like 'E. Bloccano...' inside option E
                    for k, v in list(options_dict.items()):
                        m_dup_pref = re.match(rf"^{k}[\.\)]\s+(\S.*)$", v)
                        if m_dup_pref:
                            options_dict[k] = m_dup_pref.group(1).strip()

                    # Apply 100%-visually-verified exact typeset formula/exponent overrides where applicable
                    ov = VISUAL_MCQ_OVERRIDES.get((code, ch, qt, qnum))
                    if ov:
                        if "stem" in ov:
                            stem_text = ov["stem"]
                        if "options" in ov:
                            options_dict = dict(ov["options"])

                    mentions_visual = bool(re.search(
                        r"\b(?:figura|schema|grafico|tabella|circuito|diagramma|immagine)\b",
                        stem_text.lower(),
                    ))

                    # Detect embedded figure/diagram/chemical structure across the column span(s) of this question
                    fig_files = []
                    by_col: Dict[Tuple[int, int], Tuple[int, int, int, List[dict]]] = {}
                    for bp_l, cidx_l, x_off_l, col_w_l, zy0_l, _, _, _, _, lobj_l in q_slice:
                        key_c = (bp_l, cidx_l)
                        if key_c not in by_col:
                            by_col[key_c] = (x_off_l, col_w_l, zy0_l, [])
                        if lobj_l not in by_col[key_c][3]:
                            by_col[key_c][3].append(lobj_l)

                    for part_idx, ((bp_c, _), (xo_c, cw_c, zy_c, col_lns)) in enumerate(by_col.items()):
                        sfx = "" if len(by_col) == 1 else f"_p{part_idx+1}"
                        fpath = fig_dir / f"{code}_C{ch:02d}_{qt[:4]}_Q{qnum:03d}{sfx}.png"
                        saved_name = detect_and_save_figure_crop(get_page_gray(bp_c), xo_c, cw_c, zy_c, col_lns, fpath)
                        if not saved_name and (graphical_opt or (mentions_visual and part_idx == 0)):
                            # Always save full visual crop if any option is pure structural formula/graphic!
                            pgray_c = get_page_gray(bp_c)
                            ry0 = max(0, zy_c + min(l["bbox"][1] for l in col_lns) - 8)
                            ry1 = min(pgray_c.shape[0], zy_c + max(l["bbox"][3] for l in col_lns) + 28)
                            rx0 = max(0, xo_c - 4)
                            rx1 = min(pgray_c.shape[1], xo_c + cw_c + 4)
                            fpath.parent.mkdir(parents=True, exist_ok=True)
                            cv2.imwrite(str(fpath), pgray_c[ry0:ry1, rx0:rx1])
                            saved_name = fpath.name
                        if saved_name:
                            fig_files.append(saved_name)

                    # Store exact pixel slice boxes too for lossless rendering
                    q_slices_meta = [
                        {
                            "book_page": bp_c,
                            "bbox": [
                                max(0, xo_c - 4),
                                max(0, zy_c + min(l["bbox"][1] for l in col_lns) - 8),
                                xo_c + cw_c + 4,
                                zy_c + max(l["bbox"][3] for l in col_lns) + 10,
                            ],
                        }
                        for (bp_c, _), (xo_c, cw_c, zy_c, col_lns) in by_col.items()
                    ]

                    q_records.append({
                        "qnum": qnum,
                        "book_page": q_slice[0][0],
                        "question_text": stem_text,
                        "options": options_dict,
                        "has_figure": len(fig_files) > 0,
                        "figure_files": fig_files,
                        "q_slices": q_slices_meta,
                    })

                blocks_out.append({
                    "subject": subj_name,
                    "subject_code": code,
                    "chapter_num": ch,
                    "chapter_title": ch_title,
                    "kind": qt,
                    "count": len(q_records),
                    "items": q_records,
                })

            # 3: Fill-in-the-blank subsection ('completamento')
            exp_c = s2_lookup[(code, ch, "completamento")]["count"]
            paras = []
            for p in ch_pages:
                for z in p["zones"]:
                    if z["quiz_type"] != "completamento":
                        continue
                    col = z["columns"][0]
                    zy0 = z["y0"]
                    pgray = get_page_gray(p["book_page"])
                    raw_lines = [
                        ln for ln in col["lines"]
                        if not is_running_hdr_or_ftr(ln["text"], zy0 + ln["bbox"][1], zy0 + ln["bbox"][3], p["height"])
                    ]
                    if not raw_lines:
                        continue
                    page_x_margin = int(sorted(l["bbox"][0] for l in raw_lines)[max(0, len(raw_lines) // 10)])
                    max_blank_y = int(p["height"] * (0.945 if code != "FIS" else 0.93))
                    blanks = [b for b in col.get("blanks", []) if zy0 + b[0] < max_blank_y]

                    # Assign each detected blank bar UNIQUELY (1-to-1) to its closest vertical text line within [-11, +13] px!
                    line_blanks: List[List[Tuple[int, int, float]]] = [[] for _ in raw_lines]
                    standalone_blanks: List[Tuple[float, int, int]] = []
                    for by, bx0, bx1 in blanks:
                        best_li = None
                        best_dist = 999.0
                        for li_idx, ln in enumerate(raw_lines):
                            ly0, ly1 = ln["bbox"][1], ln["bbox"][3]
                            if ly0 - 11 <= by <= ly1 + 13:
                                dist = abs(by - (ly1 - 2.0))
                                if dist < best_dist:
                                    best_dist = dist
                                    best_li = li_idx
                        if best_li is not None:
                            line_blanks[best_li].append((int(bx0), int(bx1), float(by)))
                        else:
                            standalone_blanks.append((float(by), int(bx0), int(bx1)))

                    unified = []
                    for li_idx, ln in enumerate(raw_lines):
                        lx0, ly0, lx1, ly1 = ln["bbox"]
                        rep_line = maybe_repair_line_formulas(ln, pgray, col["x_offset"], zy0, char_api)
                        rep_words = rep_line.split()
                        orig_words = ln.get("words", [])
                        toks = []
                        if len(rep_words) == len(orig_words):
                            for w, rw in zip(orig_words, rep_words):
                                toks.append((w["b"][0], w["b"][2], rw))
                        else:
                            for w in orig_words:
                                toks.append((w["b"][0], w["b"][2], w["t"]))
                        for bx0, bx1, by in line_blanks[li_idx]:
                            marker = "^[_____]" if by < ly0 + 0.45 * max(14, ly1 - ly0) else "_____"
                            toks.append((bx0, bx1, marker))
                        toks.sort(key=lambda t: t[0])
                        unified.append((
                            ly0,
                            ly1,
                            lx0,
                            " ".join(t[2] for t in toks).strip(),
                            True,
                            p["book_page"],
                            orig_words,
                            [col["x_offset"] + lx0, zy0 + ly0, col["x_offset"] + lx1, zy0 + ly1],
                        ))
                    for by, bx0, bx1 in standalone_blanks:
                        unified.append((
                            int(by - 12),
                            int(by + 2),
                            bx0,
                            "_____",
                            False,
                            p["book_page"],
                            [],
                            [col["x_offset"] + bx0, int(zy0 + by - 14), col["x_offset"] + bx1, int(zy0 + by + 4)],
                        ))
                    unified.sort(key=lambda u: u[0])

                    prev_y1 = None
                    for ly0, ly1, lx0, txt, has_words, bp_u, wds, abs_bb in unified:
                        expl = (
                            has_words
                            and lx0 <= page_x_margin + 22
                            and bool(re.match(r"^[0-9BSOIl]{1,3}[\.\),](?:\s+\S|[0-9Il]+\s)", txt))
                        )
                        if prev_y1 is None:
                            sn = (
                                not paras
                                or expl
                                or paras[-1]["lines"][-1].rstrip().endswith(".")
                                or (has_words and lx0 <= page_x_margin + 18)
                            )
                            if sn:
                                paras.append({"bp": bp_u, "gap": 999, "expl": expl, "lines": [txt], "words": [wds], "bboxes": [(bp_u, abs_bb)]})
                            else:
                                paras[-1]["lines"].append(txt)
                                paras[-1]["words"].append(wds)
                                paras[-1]["bboxes"].append((bp_u, abs_bb))
                        else:
                            vgap = ly0 - prev_y1
                            if has_words and (vgap >= 24 or expl):
                                paras.append({"bp": bp_u, "gap": vgap, "expl": expl, "lines": [txt], "words": [wds], "bboxes": [(bp_u, abs_bb)]})
                            else:
                                paras[-1]["lines"].append(txt)
                                paras[-1]["words"].append(wds)
                                paras[-1]["bboxes"].append((bp_u, abs_bb))
                        prev_y1 = ly1

            while len(paras) > exp_c:
                cands_merge = [
                    (paras[idx]["gap"] + (1000 if paras[idx]["expl"] else 0) + (80 if paras[idx - 1]["lines"][-1].rstrip().endswith(".") else 0), idx)
                    for idx in range(1, len(paras))
                ]
                cands_merge.sort()
                _, m_idx = cands_merge[0]
                paras[m_idx - 1]["lines"].extend(paras[m_idx]["lines"])
                paras[m_idx - 1]["words"].extend(paras[m_idx]["words"])
                paras[m_idx - 1]["bboxes"].extend(paras[m_idx]["bboxes"])
                paras.pop(m_idx)

            while len(paras) < exp_c:
                best_split = (-999999, -1, -1)
                for p_i, pr_item in enumerate(paras):
                    for l_i in range(1, len(pr_item["lines"])):
                        prev_l = pr_item["lines"][l_i - 1].rstrip()
                        cur_l = pr_item["lines"][l_i].lstrip()
                        score_s = (100 if prev_l.endswith(".") else 0) + (250 if re.match(r"^\d{1,3}[\.\),]", cur_l) else 0) + (pr_item["bboxes"][l_i][1][1] - pr_item["bboxes"][l_i - 1][1][3])
                        if score_s > best_split[0]:
                            best_split = (score_s, p_i, l_i)
                _, sp_p, sp_l = best_split
                orig_p = paras[sp_p]
                new_p = {
                    "bp": orig_p["bboxes"][sp_l][0],
                    "gap": 25,
                    "expl": False,
                    "lines": orig_p["lines"][sp_l:],
                    "words": orig_p["words"][sp_l:],
                    "bboxes": orig_p["bboxes"][sp_l:],
                }
                orig_p["lines"] = orig_p["lines"][:sp_l]
                orig_p["words"] = orig_p["words"][:sp_l]
                orig_p["bboxes"] = orig_p["bboxes"][:sp_l]
                paras.insert(sp_p + 1, new_p)

            assert len(paras) == exp_c, f"{code} C{ch:02d} completamento: got {len(paras)} vs {exp_c}"

            comp_records = []
            for qi, pr in enumerate(paras):
                qnum = qi + 1
                merged_lines = list(pr["lines"])
                # Restore '-__' suffix blanks (e.g. CHIM C04 Q8/Q9) or horizontal word-gap blanks (>= 100 px) if needed!
                joined_check = " ".join(merged_lines)
                if "_____" not in joined_check:
                    if "__" in joined_check:
                        merged_lines = [re.sub(r"_{2,}", "_____", s) for s in merged_lines]
                    else:
                        best_gap = (0, -1, -1)
                        for li_i, wds in enumerate(pr["words"]):
                            for wi in range(len(wds) - 1):
                                gx = wds[wi + 1]["b"][0] - wds[wi]["b"][2]
                                if gx > best_gap[0]:
                                    best_gap = (gx, li_i, wi)
                        if best_gap[0] >= 95:
                            _, li_i, wi = best_gap
                            wds = pr["words"][li_i]
                            merged_lines[li_i] = (
                                " ".join(w["t"] for w in wds[: wi + 1])
                                + " _____ "
                                + " ".join(w["t"] for w in wds[wi + 1 :])
                            )

                full_raw = join_wrapped_italian_lines(merged_lines)
                # Strip leading printed item number (e.g., '1. ', '91 ', 'Lu ', 'S1. ', '70 ') cleanly!
                s_clean = full_raw
                m_num_dot = re.match(r"^[0-9Il|SsoOQBzZ\$]{1,3}[\.\),]\s*(.*)$", s_clean)
                if m_num_dot:
                    s_clean = m_num_dot.group(1).strip()
                else:
                    # Handle fused prefix like '7.1 _____' -> 'I _____', '91 _____' -> 'I _____', '70 _____' -> 'Il _____', 'Lu _____' -> "L'equilibrio _____"
                    m_fused_art = re.match(rf"^{qnum}[\.\s]*([01Il|])\s+(.*)$", s_clean)
                    if m_fused_art:
                        art = "Il" if m_fused_art.group(1) == "0" else "I"
                        s_clean = f"{art} {m_fused_art.group(2).strip()}"
                    else:
                        m_any_num = re.match(r"^\d{1,3}\s+(.*)$", s_clean)
                        if m_any_num:
                            s_clean = m_any_num.group(1).strip()
                        elif code == "CHIM" and ch == 8 and qnum == 1 and s_clean.startswith("Lu "):
                            s_clean = "L'equilibrio " + s_clean[3:].strip()
                        elif code == "CHIM" and ch == 5 and qnum == 21 and s_clean.startswith("zi. "):
                            s_clean = "_____ " + s_clean[4:].lstrip("_ ").strip()

                s_clean = clean_prose_ocr_quirks(s_clean)
                # Strip any trailing page-footer horizontal rule misdetected after sentence-ending punctuation
                if s_clean.count("_____") >= 2:
                    s_clean = re.sub(r"([\.\?\!])\s*_____\s*$", r"\1", s_clean).strip()
                if code == "BIO" and ch == 7 and qnum == 1 and s_clean.startswith("_____ cellulare"):
                    s_clean = "Il " + s_clean
                elif code == "CHIM" and ch == 13 and qnum == 1 and re.match(r"^it\s+_____", s_clean, re.I):
                    s_clean = re.sub(r"^it\s+", "I ", s_clean, flags=re.I)
                elif code == "FIS" and ch == 1 and qnum == 29:
                    s_clean = "La distanza media Terra-Sole è circa 1,50 × 10^[_____] metri."
                # Group bounding boxes per page
                by_p: Dict[int, List[List[int]]] = {}
                for bp_b, bb_b in pr["bboxes"]:
                    by_p.setdefault(bp_b, []).append(bb_b)
                q_slices_meta = [
                    {
                        "book_page": bp_b,
                        "bbox": [
                            max(0, min(b[0] for b in bbs) - 8),
                            max(0, min(b[1] for b in bbs) - 8),
                            max(b[2] for b in bbs) + 8,
                            max(b[3] for b in bbs) + 8,
                        ],
                    }
                    for bp_b, bbs in by_p.items()
                ]
                comp_records.append({
                    "qnum": qnum,
                    "book_page": pr["bp"],
                    "question_text": s_clean,
                    "options": None,
                    "has_figure": False,
                    "figure_files": [],
                    "q_slices": q_slices_meta,
                })

            blocks_out.append({
                "subject": subj_name,
                "subject_code": code,
                "chapter_num": ch,
                "chapter_title": ch_title,
                "kind": "completamento",
                "count": len(comp_records),
                "items": comp_records,
            })
            print(
                f"  [Stage3-{subj_code}] Cap {ch:02d}: "
                f"comm={blocks_out[-3]['count']} | non_comm={blocks_out[-2]['count']} | compl={blocks_out[-1]['count']}",
                flush=True,
            )

    with open(out_path_str, "w", encoding="utf-8") as f:
        json.dump(blocks_out, f, ensure_ascii=False)
    return out_path_str


def run_stage3(
    stage1_dir: Path = Path("/tmp/anki_sem_stage1"),
    fig_dir: Path = Path("/home/user/anki-sem/output/figures"),
) -> Path:
    t0 = time.time()
    with open(stage1_dir / "questions_ocr_cache.json", encoding="utf-8") as f:
        qc = json.load(f)
    qc.sort(key=lambda x: x["book_page"])

    with open(stage1_dir / "stage2_answers.json", encoding="utf-8") as f:
        s2_list = json.load(f)
    s2_lookup = {(b["subject_code"], b["chapter_num"], b["kind"]): b for b in s2_list}

    fig_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for sc in ("CHIM", "BIO", "FIS"):
        sub_pages = [p for p in qc if p["subject_code"] == sc]
        sub_s2 = {k: {"count": v["count"]} for k, v in s2_lookup.items() if k[0] == sc}
        tasks.append((
            sc,
            sub_pages,
            sub_s2,
            str(stage1_dir),
            str(fig_dir),
            str(stage1_dir / f"_stage3_part_{sc}.json"),
        ))

    with ProcessPoolExecutor(max_workers=2, mp_context=multiprocessing.get_context("spawn")) as ex:
        part_files = list(ex.map(process_subject_questions_to_file, tasks))

    all_blocks = []
    for pf in part_files:
        with open(pf, encoding="utf-8") as f:
            all_blocks.extend(json.load(f))
        os.remove(pf)

    out_path = stage1_dir / "stage3_questions.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_blocks, f, ensure_ascii=False, indent=2)

    tot_q = sum(b["count"] for b in all_blocks)
    tot_fig = sum(1 for b in all_blocks for it in b["items"] if it["has_figure"])
    no_blank = sum(
        1
        for b in all_blocks
        if b["kind"] == "completamento"
        for it in b["items"]
        if "_____" not in it["question_text"]
    )
    print(
        f"[Stage 3 DONE in {time.time() - t0:.2f}s] "
        f"Subsections={len(all_blocks)}/84 | Total Questions={tot_q}/7078 | "
        f"Embedded Figures Cropped={tot_fig} | Missing Completamento Blanks={no_blank}"
    )
    return out_path


if __name__ == "__main__":
    run_stage3()
