from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import time
from pathlib import Path
from typing import Dict, List

import cv2
import genanki
import numpy as np
from PIL import Image

from extractor.quality_refiner import normalize_scientific_and_italian_prose
from extractor.stage3_questions import clean_prose_ocr_quirks, join_wrapped_italian_lines

SUBJECT_ORDER = {"CHIM": "01", "BIO": "02", "FIS": "03"}
KIND_ORDER = {
    "commentati": ("1. Quiz commentati", "COMM"),
    "non_commentati": ("2. Quiz non commentati", "NCOM"),
    "completamento": ("3. Quiz a completamento", "COMP"),
}
SUBJECT_TAG_SLUG = {"CHIM": "chimica", "BIO": "biologia", "FIS": "fisica"}


def stable_anki_id(seed_str: str) -> int:
    """Deterministic 31-bit positive integer ID in [1_100_000_000, 2_050_000_000]."""
    h = int(hashlib.sha1(seed_str.encode("utf-8")).hexdigest()[:12], 16)
    return 1_100_000_000 + (h % 950_000_000)


def clean_commentary_explanation(raw_expl: str, answer_letter: str) -> str:
    """Clean OCR line wraps, running headers, and leading answer token from Quiz commentati explanation."""
    if not raw_expl:
        return ""
    lines = []
    for ln in raw_expl.splitlines():
        t = ln.strip()
        if not t:
            continue
        low = t.lower()
        if re.match(r"^\d{1,3}[\.\s]+(chimica|biologia|fisica)", low):
            continue
        if re.search(r"\bcapitolo\b", low) and re.search(r"\d{1,3}\s*$", low):
            continue
        if low.startswith("risposte commentate") or low in ("risposte", "commentate"):
            continue
        if re.search(r"\b(edises|edlses|ediss)\b", low):
            continue
        lines.append(t)
    joined = clean_prose_ocr_quirks(join_wrapped_italian_lines(lines))
    # Normalize leading '1) B. Il ...' or '12. C - ...' to clean prose starting right after answer header
    m_lead = re.match(r"^[0-9Il|SsoOQBzZ]{1,3}\s*[\.\)\-\:]?\s*[A-E8€©]\s*[\.\)\-\:]?\s*(.*)$", joined)
    if m_lead and len(m_lead.group(1).strip()) >= 8:
        joined = m_lead.group(1).strip()
    return normalize_scientific_and_italian_prose(joined, is_stem=False)


FIXED_4GRAY_PALETTE = [
    0, 0, 0,
    85, 85, 85,
    170, 170, 170,
    255, 255, 255,
] + [255, 255, 255] * 252


def write_compact_gray_png(gray_arr: np.ndarray, dest: Path) -> None:
    """Save crisp contrast-normalized 8-bit grayscale PNG (16 quantized levels for tiny zlib size).
    Avoids Pillow's Palette.ADAPTIVE octree bug which writes all-black palettes on bilevel images!"""
    lo = min(float(np.percentile(gray_arr, 2)), 75.0)
    hi = max(float(np.percentile(gray_arr, 97)), 235.0)
    span = max(80.0, hi - lo)
    norm = np.clip((gray_arr.astype(np.float32) - lo) * (255.0 / span), 0, 255).astype(np.uint8)
    q16 = ((norm // 16) * 17).astype(np.uint8)
    im = Image.fromarray(q16, mode="L")
    im.save(str(dest), format="PNG", optimize=True, compress_level=9)


def write_crisp_2bit_png(gray_arr: np.ndarray, dest: Path) -> None:
    """Save ultra-compact (~2.7 KB), high-contrast 4-level grayscale PNG with an explicit
    fixed RGB palette [0, 85, 170, 255] so 0 images can ever invert or turn black."""
    lo = min(float(np.percentile(gray_arr, 2)), 75.0)
    hi = max(float(np.percentile(gray_arr, 97)), 235.0)
    span = max(80.0, hi - lo)
    norm = np.clip((gray_arr.astype(np.float32) - lo) * (255.0 / span), 0, 255)
    idx4 = np.clip(np.rint(norm / 85.0), 0, 3).astype(np.uint8)
    im = Image.fromarray(idx4, mode="P")
    im.putpalette(FIXED_4GRAY_PALETTE)
    im.save(str(dest), format="PNG", bits=2, optimize=True)


def stitch_question_slices_clean(slices: List[dict], get_page_gray) -> np.ndarray:
    """Crop every slice of a question from its 300-DPI canonical page, strip any black
    EdiSES footer rectangle at column bottoms, and stitch vertically with clean white padding."""
    parts: List[np.ndarray] = []
    for sl in slices:
        pgray = get_page_gray(int(sl["book_page"]))
        if pgray is None:
            continue
        H_p, W_p = pgray.shape
        x0, y0, x1, y1 = [int(v) for v in sl["bbox"]]
        crop = pgray[max(0, y0 - 4):min(H_p, y1 + 8), max(0, x0 - 6):min(W_p, x1 + 6)].copy()
        ch, cw = crop.shape
        # Remove solid black rectangular EdiSES footer logo band if present at bottom of column slice
        bw = (crop < 90).astype(np.uint8)
        n_lbl, _, stats, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
        for li in range(1, n_lbl):
            bx, by, bw_box, bh_box, b_area = stats[li]
            if bw_box >= 55 and 12 <= bh_box <= 52 and (b_area / float(max(1, bw_box * bh_box))) >= 0.62:
                crop[max(0, by - 4):min(ch, by + bh_box + 5), max(0, bx - 6):min(cw, bx + bw_box + 6)] = 255
        # Trim trailing pure-white dead space at bottom/top of slice
        row_dark = (crop < 220).sum(axis=1)
        non_empty = np.where(row_dark > 1)[0]
        if len(non_empty) > 0:
            crop = crop[max(0, int(non_empty[0]) - 4):min(ch, int(non_empty[-1]) + 6), :]
        parts.append(crop)

    if not parts:
        return np.full((60, 480), 255, dtype=np.uint8)
    max_w = max(p.shape[1] for p in parts)
    padded = [
        cv2.copyMakeBorder(p, 0, 6 if i < len(parts) - 1 else 0, 0, max_w - p.shape[1], cv2.BORDER_CONSTANT, value=255)
        for i, p in enumerate(parts)
    ]
    stitched = cv2.vconcat(padded) if len(padded) > 1 else padded[0]
    return cv2.copyMakeBorder(stitched, 10, 10, 12, 12, cv2.BORDER_CONSTANT, value=255)


ANKI_CSS = """
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 16.5px;
  line-height: 1.55;
  color: #1e293b;
  background-color: #f8fafc;
  margin: 0;
  padding: 16px 14px 28px 14px;
  text-align: left;
}
.nightMode.card, .night_mode .card {
  color: #f1f5f9;
  background-color: #0f172a;
}
.wrap {
  max-width: 740px;
  margin: 0 auto;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}
.nightMode .wrap, .night_mode .wrap {
  background: #1e293b;
  border-color: #334155;
  box-shadow: none;
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  margin-bottom: 14px;
  font-size: 12px;
  font-weight: 600;
}
.badge {
  padding: 3px 9px;
  border-radius: 999px;
  letter-spacing: 0.02em;
}
.subj-CHIM { background: #dbeafe; color: #1d4ed8; }
.subj-BIO  { background: #dcfce7; color: #15803d; }
.subj-FIS  { background: #fef3c7; color: #b45309; }
.nightMode .subj-CHIM, .night_mode .subj-CHIM { background: #1e3a8a; color: #bfdbfe; }
.nightMode .subj-BIO,  .night_mode .subj-BIO  { background: #14532d; color: #bbf7d0; }
.nightMode .subj-FIS,  .night_mode .subj-FIS  { background: #78350f; color: #fde68a; }
.meta-dim {
  color: #64748b;
  font-weight: 500;
}
.nightMode .meta-dim, .night_mode .meta-dim { color: #94a3b8; }
.stem {
  font-size: 17.5px;
  font-weight: 600;
  margin-bottom: 14px;
  color: #0f172a;
}
.nightMode .stem, .night_mode .stem { color: #f8fafc; }
.blank-slot {
  display: inline-block;
  min-width: 84px;
  border-bottom: 2.5px solid #2563eb;
  color: #2563eb;
  text-align: center;
  font-weight: 700;
  padding: 0 6px;
  margin: 0 2px;
}
.blank-filled {
  display: inline-block;
  background: #dcfce7;
  color: #166534;
  border-bottom: 2.5px solid #16a34a;
  border-radius: 5px;
  padding: 1px 8px;
  font-weight: 700;
}
.nightMode .blank-filled, .night_mode .blank-filled {
  background: #14532d;
  color: #bbf7d0;
  border-bottom-color: #4ade80;
}
.opts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}
.opt {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 9px;
  background: #f8fafc;
  cursor: pointer;
}
.nightMode .opt, .night_mode .opt {
  background: #0f172a;
  border-color: #334155;
}
.opt.user-picked {
  border-color: #3b82f6;
  background: #eff6ff;
}
.nightMode .opt.user-picked, .night_mode .opt.user-picked {
  border-color: #60a5fa;
  background: #1e3a8a;
}
.opt-correct {
  border: 2px solid #16a34a !important;
  background: #f0fdf4 !important;
  font-weight: 600;
}
.nightMode .opt-correct, .night_mode .opt-correct {
  border-color: #4ade80 !important;
  background: #14532d !important;
  color: #f0fdf4 !important;
}
.opt-key {
  font-weight: 700;
  min-width: 22px;
  color: #475569;
}
.nightMode .opt-key, .night_mode .opt-key { color: #cbd5e1; }
.opt-correct .opt-key { color: #15803d; }
.nightMode .opt-correct .opt-key, .night_mode .opt-correct .opt-key { color: #86efac; }
.ans-banner {
  margin-top: 16px;
  padding: 12px 15px;
  border-radius: 10px;
  background: #dcfce7;
  border-left: 4px solid #16a34a;
  color: #14532d;
  font-weight: 700;
  font-size: 16.5px;
}
.nightMode .ans-banner, .night_mode .ans-banner {
  background: #14532d;
  border-left-color: #4ade80;
  color: #f0fdf4;
}
.expl-box {
  margin-top: 14px;
  padding: 13px 15px;
  border-radius: 10px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  font-size: 15px;
  line-height: 1.55;
}
.nightMode .expl-box, .night_mode .expl-box {
  background: #0f172a;
  border-color: #334155;
}
.fig-box {
  margin-top: 12px;
  text-align: center;
}
.fig-box img, details.orig-scan img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  padding: 4px;
}
details.orig-scan {
  margin-top: 12px;
  font-size: 13px;
  color: #64748b;
}
details.orig-scan summary {
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 6px;
}
"""

FRONT_TMPL = """
<div class="wrap">
  <div class="meta">
    <span class="badge subj-{{SubjectCode}}">{{Subject}}</span>
    <span class="meta-dim">Cap. {{ChapterNum}} — {{ChapterTitle}}</span>
    <span class="meta-dim">• {{QuizTypeLabel}} #{{QuestionNum}} (p. {{BookPage}})</span>
  </div>
  <div class="stem">{{FrontStemHTML}}</div>
  {{#FigureHTML}}<div class="fig-box">{{FigureHTML}}</div>{{/FigureHTML}}
  {{FrontOptionsHTML}}
  {{#QuestionScanHTML}}<details class="orig-scan"><summary>Scansione originale della domanda (p. {{BookPage}})</summary>{{QuestionScanHTML}}</details>{{/QuestionScanHTML}}
</div>
<script>
document.querySelectorAll('.opt').forEach(function(el) {
  el.addEventListener('click', function() {
    el.classList.toggle('user-picked');
  });
});
</script>
"""

BACK_TMPL = """
<div class="wrap">
  <div class="meta">
    <span class="badge subj-{{SubjectCode}}">{{Subject}}</span>
    <span class="meta-dim">Cap. {{ChapterNum}} — {{ChapterTitle}}</span>
    <span class="meta-dim">• {{QuizTypeLabel}} #{{QuestionNum}} (p. {{BookPage}})</span>
  </div>
  <div class="stem">{{BackStemHTML}}</div>
  {{#FigureHTML}}<div class="fig-box">{{FigureHTML}}</div>{{/FigureHTML}}
  {{BackOptionsHTML}}
  <div class="ans-banner">{{AnswerBannerHTML}}</div>
  {{#ExplanationHTML}}<div class="expl-box"><strong>Spiegazione:</strong> {{ExplanationHTML}}</div>{{/ExplanationHTML}}
  {{#QuestionScanHTML}}<details class="orig-scan"><summary>Scansione originale della domanda (p. {{BookPage}})</summary>{{QuestionScanHTML}}</details>{{/QuestionScanHTML}}
  {{#SolutionScanHTML}}<details class="orig-scan"><summary>Risoluzione grafica originale del libro</summary>{{SolutionScanHTML}}</details>{{/SolutionScanHTML}}
</div>
"""


def format_front_stem_html(question_text: str, quiz_type: str) -> str:
    esc = html.escape(question_text)
    if quiz_type == "completamento":
        esc = esc.replace("^[_____]", '<sup><span class="blank-slot">&nbsp;&nbsp;&nbsp;</span></sup>')
        esc = esc.replace("_____", '<span class="blank-slot">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>')
    return esc


def format_back_stem_html(question_text: str, answer_str: str, quiz_type: str) -> str:
    esc = html.escape(question_text)
    if quiz_type != "completamento":
        return esc
    parts = [p.strip() for p in re.split(r"\s*[/;]\s*|\s*,\s*(?=[a-zA-ZÀ-ÿ])", answer_str) if p.strip()]
    blank_count = esc.count("_____")
    if blank_count == 1:
        fill = f'<span class="blank-filled">{html.escape(answer_str)}</span>'
        esc = esc.replace("^[_____]", f"<sup>{fill}</sup>", 1)
        esc = esc.replace("_____", fill, 1)
        return esc
    if len(parts) == blank_count and blank_count > 1:
        for p in parts:
            fill = f'<span class="blank-filled">{html.escape(p)}</span>'
            if "^[_____]" in esc:
                esc = esc.replace("^[_____]", f"<sup>{fill}</sup>", 1)
            else:
                esc = esc.replace("_____", fill, 1)
        return esc
    fill_all = f'<span class="blank-filled">{html.escape(answer_str)}</span>'
    return esc.replace("^[_____]", f"<sup>{fill_all}</sup>").replace("_____", fill_all)


def run_stage4(
    stage1_dir: Path = Path("/tmp/anki_sem_stage1"),
    output_dir: Path = Path("/home/user/anki-sem/output"),
) -> Dict[str, str]:
    t0 = time.time()
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    q_img_dir = output_dir / "question_images"
    q_img_dir.mkdir(parents=True, exist_ok=True)
    sol_media_dir = stage1_dir / "anki_sol_media"
    sol_media_dir.mkdir(parents=True, exist_ok=True)

    with open(stage1_dir / "stage2_answers.json", encoding="utf-8") as f:
        s2_list = json.load(f)
    with open(stage1_dir / "stage3_questions.json", encoding="utf-8") as f:
        s3_list = json.load(f)

    s2_map = {(b["subject_code"], b["chapter_num"], b["kind"]): b for b in s2_list}
    s3_map = {(b["subject_code"], b["chapter_num"], b["kind"]): b for b in s3_list}

    assert set(s2_map.keys()) == set(s3_map.keys()) and len(s2_map) == 84, "Expected exact 84 subsections"

    model = genanki.Model(
        model_id=stable_anki_id("SemestreFiltroEdiSES-Model-v1"),
        name="Semestre Filtro EdiSES — Studio & Esame",
        fields=[
            {"name": "ItemID"},
            {"name": "Subject"},
            {"name": "SubjectCode"},
            {"name": "ChapterNum"},
            {"name": "ChapterTitle"},
            {"name": "QuizTypeLabel"},
            {"name": "QuestionNum"},
            {"name": "BookPage"},
            {"name": "FrontStemHTML"},
            {"name": "BackStemHTML"},
            {"name": "FrontOptionsHTML"},
            {"name": "BackOptionsHTML"},
            {"name": "AnswerBannerHTML"},
            {"name": "ExplanationHTML"},
            {"name": "FigureHTML"},
            {"name": "QuestionScanHTML"},
            {"name": "SolutionScanHTML"},
        ],
        templates=[
            {
                "name": "Domanda → Risposta",
                "qfmt": FRONT_TMPL,
                "afmt": BACK_TMPL,
            }
        ],
        css=ANKI_CSS,
    )

    decks: Dict[str, genanki.Deck] = {}
    media_files_set: Dict[str, str] = {}
    page_cache: Dict[int, np.ndarray] = {}

    def get_page_gray(bp_num: int) -> np.ndarray:
        if bp_num not in page_cache:
            if len(page_cache) > 20:
                page_cache.clear()
            page_cache[bp_num] = cv2.imread(str(stage1_dir / f"pages/bp_{bp_num:03d}.png"), cv2.IMREAD_GRAYSCALE)
        return page_cache[bp_num]

    dataset_rows: List[dict] = []

    # Iterate in canonical workbook order (CHIM C01..13, BIO C01..07, FIS C01..08 x commentati, non_commentati, completamento)
    sorted_keys = sorted(
        s3_map.keys(),
        key=lambda k: (SUBJECT_ORDER[k[0]], k[1], KIND_ORDER[k[2]][0]),
    )

    for sc, ch, qt in sorted_keys:
        qb = s3_map[(sc, ch, qt)]
        ab = s2_map[(sc, ch, qt)]
        assert qb["count"] == ab["count"], f"Count mismatch on {(sc, ch, qt)}"

        qt_label, qt_short = KIND_ORDER[qt]
        subj_prefix = f"{SUBJECT_ORDER[sc]} {qb['subject']}"
        deck_name = f"Semestre Filtro EdiSES::{subj_prefix}::Cap. {ch:02d} - {qb['chapter_title']}::{qt_label}"
        if deck_name not in decks:
            decks[deck_name] = genanki.Deck(
                deck_id=stable_anki_id(f"deck::{deck_name}"),
                name=deck_name,
            )
        deck = decks[deck_name]

        for q_item, a_item in zip(qb["items"], ab["items"]):
            qnum = q_item["qnum"]
            assert qnum == a_item["qnum"], f"qnum alignment mismatch on {(sc, ch, qt, qnum)}"

            item_id = f"{sc}-C{ch:02d}-{qt_short}-{qnum:03d}"
            ans_val = a_item["answer"].strip()
            answer_bp = (
                (a_item.get("slices", [{}])[0].get("bp") if a_item.get("slices") else None)
                or a_item.get("bp")
                or ab.get("start_bp")
                or ab.get("p_start")
                or (ab.get("pages", [None])[0] if ab.get("pages") else None)
                or 291  # CHIM C11 Q17..Q23 publisher-omitted page 291
            )

            options = q_item["options"]
            correct_option_text = options[ans_val] if options else ans_val

            expl_clean = ""
            sol_scan_html = ""
            if qt == "commentati":
                expl_clean = clean_commentary_explanation(a_item.get("explanation", ""), ans_val)
                sol_imgs = []
                if a_item.get("slices"):
                    for s_idx, sl in enumerate(a_item.get("slices", [])):
                        sbp = sl["bp"]
                        pgray = get_page_gray(sbp)
                        if pgray is not None:
                            y0 = max(0, int(sl["y0"]) - 4)
                            y1 = min(pgray.shape[0], int(sl["y1"]) + 6)
                            if y1 > y0 + 14:
                                sol_name = f"sol_{sc}_C{ch:02d}_Q{qnum:03d}_{s_idx+1}.png"
                                sol_dest = sol_media_dir / sol_name
                                write_compact_gray_png(pgray[y0:y1, :], sol_dest)
                                media_files_set[sol_name] = str(sol_dest)
                                sol_imgs.append(f'<img src="{sol_name}">')
                else:
                    # Re-encode pre-extracted commentary scan PNGs as crisp 2-bit fixed-palette PNGs
                    for pre_sol in sorted(sol_media_dir.glob(f"sol_{sc}_C{ch:02d}_Q{qnum:03d}_*.png")):
                        sg = cv2.imread(str(pre_sol), cv2.IMREAD_GRAYSCALE)
                        if sg is not None:
                            write_crisp_2bit_png(sg, pre_sol)
                        media_files_set[pre_sol.name] = str(pre_sol)
                        sol_imgs.append(f'<img src="{pre_sol.name}">')
                sol_scan_html = "".join(sol_imgs)

            # Export 1-to-1 full stitched question scan PNG for EVERY question (1..7,078)
            q_scan_filename = f"{item_id}.png"
            q_scan_dest = q_img_dir / q_scan_filename
            stitched_q_arr = stitch_question_slices_clean(q_item.get("q_slices", []), get_page_gray)
            write_crisp_2bit_png(stitched_q_arr, q_scan_dest)
            media_files_set[q_scan_filename] = str(q_scan_dest)
            q_scan_html = f'<img src="{q_scan_filename}">'

            fig_imgs = []
            for fname in q_item.get("figure_files", []):
                fpath = fig_dir / fname
                if fpath.exists():
                    # Re-save compact 4-bit grayscale PNG in place so output/figures & apkg stay sleek!
                    g_im = cv2.imread(str(fpath), cv2.IMREAD_GRAYSCALE)
                    if g_im is not None:
                        write_compact_gray_png(g_im, fpath)
                    media_files_set[fname] = str(fpath)
                    fig_imgs.append(f'<img src="{fname}">')
            fig_html = "".join(fig_imgs)

            if options:
                f_opts = ['<div class="opts">']
                b_opts = ['<div class="opts">']
                for k in ("A", "B", "C", "D", "E"):
                    ov_esc = html.escape(options[k])
                    f_opts.append(f'<div class="opt"><span class="opt-key">{k}.</span><span>{ov_esc}</span></div>')
                    cls = "opt opt-correct" if k == ans_val else "opt"
                    prefix_mark = "✓ " if k == ans_val else ""
                    b_opts.append(
                        f'<div class="{cls}"><span class="opt-key">{prefix_mark}{k}.</span><span>{ov_esc}</span></div>'
                    )
                f_opts.append("</div>")
                b_opts.append("</div>")
                front_opts_html = "".join(f_opts)
                back_opts_html = "".join(b_opts)
                ans_banner_html = f"Risposta corretta: {html.escape(ans_val)} — {html.escape(correct_option_text)}"
            else:
                front_opts_html = ""
                back_opts_html = ""
                ans_banner_html = f"Risposta corretta: {html.escape(ans_val)}"

            record = {
                "id": item_id,
                "global_index": len(dataset_rows) + 1,
                "subject": qb["subject"],
                "subject_code": sc,
                "chapter_num": ch,
                "chapter_title": qb["chapter_title"],
                "quiz_type": qt,
                "qnum": qnum,
                "question_book_page": q_item["book_page"],
                "answer_book_page": answer_bp,
                "question": q_item["question_text"],
                "options": options,
                "answer": ans_val,
                "answer_text": correct_option_text,
                "explanation": expl_clean if qt == "commentati" else None,
                "question_image": f"question_images/{q_scan_filename}",
                "figure_files": q_item.get("figure_files", []),
                "anki_deck": deck_name,
            }
            dataset_rows.append(record)

            tags = [
                f"materia::{SUBJECT_TAG_SLUG[sc]}",
                f"capitolo::{sc}_cap_{ch:02d}",
                f"tipo::{qt}",
                f"pagina::{q_item['book_page']}",
            ]
            if fig_imgs:
                tags.append("con_figura")

            note = genanki.Note(
                model=model,
                guid=genanki.guid_for("anki-sem-edises-v1", item_id),
                fields=[
                    item_id,
                    qb["subject"],
                    sc,
                    f"{ch:02d}",
                    qb["chapter_title"],
                    qt_label,
                    str(qnum),
                    str(q_item["book_page"]),
                    format_front_stem_html(q_item["question_text"], qt),
                    format_back_stem_html(q_item["question_text"], ans_val, qt),
                    front_opts_html,
                    back_opts_html,
                    ans_banner_html,
                    html.escape(expl_clean),
                    fig_html,
                    q_scan_html,
                    sol_scan_html,
                ],
                tags=tags,
            )
            deck.add_note(note)

    # 1. Write JSONL
    jsonl_path = output_dir / "qa_dataset.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for row in dataset_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # 2. Write structured JSON
    json_path = output_dir / "qa_dataset.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "title": "Eserciziario Unico per il Semestre Filtro — EdiSES (Complete Verified QA Dataset)",
                "total_items": len(dataset_rows),
                "total_subsections": len(sorted_keys),
                "counts_by_quiz_type": {
                    k: sum(1 for r in dataset_rows if r["quiz_type"] == k)
                    for k in ("commentati", "non_commentati", "completamento")
                },
                "counts_by_subject": {
                    sc: sum(1 for r in dataset_rows if r["subject_code"] == sc)
                    for sc in ("CHIM", "BIO", "FIS")
                },
                "items": dataset_rows,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # 3. Write flat UTF-8 CSV for spreadsheet / pandas inspection
    csv_path = output_dir / "qa_dataset.csv"
    csv_cols = [
        "id",
        "global_index",
        "subject_code",
        "subject",
        "chapter_num",
        "chapter_title",
        "quiz_type",
        "qnum",
        "question_book_page",
        "answer_book_page",
        "question",
        "option_A",
        "option_B",
        "option_C",
        "option_D",
        "option_E",
        "answer",
        "answer_text",
        "explanation",
        "question_image",
        "figure_files",
        "anki_deck",
    ]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_cols)
        writer.writeheader()
        for r in dataset_rows:
            opts = r["options"] or {}
            writer.writerow({
                "id": r["id"],
                "global_index": r["global_index"],
                "subject_code": r["subject_code"],
                "subject": r["subject"],
                "chapter_num": r["chapter_num"],
                "chapter_title": r["chapter_title"],
                "quiz_type": r["quiz_type"],
                "qnum": r["qnum"],
                "question_book_page": r["question_book_page"],
                "answer_book_page": r["answer_book_page"],
                "question": r["question"],
                "option_A": opts.get("A", ""),
                "option_B": opts.get("B", ""),
                "option_C": opts.get("C", ""),
                "option_D": opts.get("D", ""),
                "option_E": opts.get("E", ""),
                "answer": r["answer"],
                "answer_text": r["answer_text"],
                "explanation": r["explanation"] or "",
                "question_image": r["question_image"],
                "figure_files": ";".join(r["figure_files"]),
                "anki_deck": r["anki_deck"],
            })

    # 4. Write Anki .apkg package with all 84 hierarchical subdecks + embedded media (deflate SQLite & media JSON)
    import zipfile as _zipfile

    apkg_path = output_dir / "Semestre_Filtro_EdiSES_Complete.apkg"
    raw_apkg = output_dir / "_tmp_raw.apkg"
    pkg = genanki.Package(list(decks.values()))
    pkg.media_files = list(media_files_set.values())
    pkg.write_to_file(str(raw_apkg))
    with _zipfile.ZipFile(str(raw_apkg), "r") as zin, _zipfile.ZipFile(str(apkg_path), "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            ctype = _zipfile.ZIP_STORED if info.filename.isdigit() else _zipfile.ZIP_DEFLATED
            zout.writestr(info.filename, data, compress_type=ctype, compresslevel=9 if ctype == _zipfile.ZIP_DEFLATED else None)
    raw_apkg.unlink(missing_ok=True)

    elapsed = time.time() - t0
    print(
        f"[Stage 4 DONE in {elapsed:.2f}s] Exported {len(dataset_rows)} QA pairs across {len(decks)} Anki decks "
        f"({len(pkg.media_files)} media PNGs) -> {apkg_path} ({apkg_path.stat().st_size / (1024*1024):.2f} MB)"
    )
    return {
        "jsonl": str(jsonl_path),
        "json": str(json_path),
        "csv": str(csv_path),
        "apkg": str(apkg_path),
    }


if __name__ == "__main__":
    run_stage4()
