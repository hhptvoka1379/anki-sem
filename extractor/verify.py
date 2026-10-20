from __future__ import annotations

import csv
import json
import re
import sqlite3
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Dict

import numpy as np
from PIL import Image

from extractor.stage1_canonicalize import SUBJECT_CHAPTERS

EXPECTED_GROUND_TRUTH = {
    ("CHIM", 1): (10, 121, 47),
    ("CHIM", 2): (40, 42, 46),
    ("CHIM", 3): (25, 181, 38),
    ("CHIM", 4): (20, 92, 31),
    ("CHIM", 5): (25, 44, 42),
    ("CHIM", 6): (25, 100, 41),
    ("CHIM", 7): (30, 55, 41),
    ("CHIM", 8): (8, 19, 29),
    ("CHIM", 9): (6, 130, 44),
    ("CHIM", 10): (30, 103, 38),
    ("CHIM", 11): (40, 173, 42),
    ("CHIM", 12): (40, 309, 88),
    ("CHIM", 13): (30, 178, 66),
    ("BIO", 1): (50, 264, 122),
    ("BIO", 2): (30, 129, 58),
    ("BIO", 3): (55, 246, 153),
    ("BIO", 4): (88, 224, 80),
    ("BIO", 5): (147, 308, 225),
    ("BIO", 6): (50, 192, 95),
    ("BIO", 7): (74, 214, 110),
    ("FIS", 1): (25, 93, 29),
    ("FIS", 2): (20, 78, 60),
    ("FIS", 3): (50, 185, 196),
    ("FIS", 4): (10, 88, 30),
    ("FIS", 5): (40, 127, 77),
    ("FIS", 6): (50, 197, 138),
    ("FIS", 7): (15, 54, 50),
    ("FIS", 8): (10, 19, 54),
}

# Exact verbatim publisher duplicate-option typos verified directly on the 300-DPI EdiSES textbook pages:
VERBATIM_BOOK_DUPLICATE_IDS = {
    "CHIM-C01-NCOM-010",  # Book p.6: printed C. Ne and E. Ne identically
    "CHIM-C01-NCOM-069",  # Book p.12: printed A. solo dai neutroni and E. solo dai neutroni identically
    "CHIM-C02-NCOM-028",  # Book p.30: printed A. 6 and D. 6 identically
    "CHIM-C10-NCOM-038",  # Book p.155: printed B. idrogeno + non metallo and D. idrogeno + non metallo identically
    "CHIM-C12-NCOM-157",  # Book p.210: printed A. 2 and D. 2 identically
    "FIS-C01-NCOM-046",   # Book p.677: printed D. 10⁶ m and E. 10⁶ m identically
    "FIS-C03-NCOM-023",   # Book p.712: printed A. 5 m/s² and D. 5 m/s² identically
}

HDR_LEAK_RE = re.compile(
    r"(chimicaepropedeutica|wwwedises|www\.edises|\bedises\b|\bedlses\b|\bedives\b|\bedices\b|"
    r"\bodices\b|\btedises\b|\besses\b|\b2dises\b|cases\s*\|\s*_|"
    r"quiz a completamento|quiz non commentati|quiz commentati|risposte commentate)",
    re.I,
)


def run_verification(output_dir: Path = Path("/home/user/anki-sem/output")) -> Dict:
    jsonl_path = output_dir / "qa_dataset.jsonl"
    json_path = output_dir / "qa_dataset.json"
    csv_path = output_dir / "qa_dataset.csv"
    apkg_path = output_dir / "Semestre_Filtro_EdiSES_Complete.apkg"
    fig_dir = output_dir / "figures"

    jsonl_rows = [json.loads(line) for line in open(jsonl_path, encoding="utf-8") if line.strip()]
    json_payload = json.load(open(json_path, encoding="utf-8"))
    csv_rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))

    checks: Dict[str, Dict] = {}

    # 1. Exact Grand Total & Cross-Format Parity
    checks["exact_total_7078_parity"] = {
        "passed": len(jsonl_rows) == 7078 and len(json_payload["items"]) == 7078 and len(csv_rows) == 7078,
        "jsonl_count": len(jsonl_rows),
        "json_count": len(json_payload["items"]),
        "csv_count": len(csv_rows),
    }

    # 2. Exact 84 Subsection Ground-Truth Bijection & Contiguous 1..N Sequencing
    subsection_mismatches = []
    for _, sc, ch, _, _, _ in SUBJECT_CHAPTERS:
        exp_comm, exp_ncom, exp_comp = EXPECTED_GROUND_TRUTH[(sc, ch)]
        for qt, exp_n in (("commentati", exp_comm), ("non_commentati", exp_ncom), ("completamento", exp_comp)):
            sub_items = [r for r in jsonl_rows if r["subject_code"] == sc and r["chapter_num"] == ch and r["quiz_type"] == qt]
            qnums = [r["qnum"] for r in sub_items]
            if len(sub_items) != exp_n or qnums != list(range(1, exp_n + 1)):
                subsection_mismatches.append({"section": f"{sc}-C{ch:02d}-{qt}", "got": len(sub_items), "expected": exp_n})

    checks["all_84_subsections_exact_bijection"] = {
        "passed": len(subsection_mismatches) == 0,
        "verified_subsections": 84 - len(subsection_mismatches),
        "mismatches": subsection_mismatches,
    }

    # 3. Unique IDs & Global Index 1..7078
    ids = [r["id"] for r in jsonl_rows]
    g_idxs = [r["global_index"] for r in jsonl_rows]
    checks["unique_ids_and_global_indexing"] = {
        "passed": len(set(ids)) == 7078 and g_idxs == list(range(1, 7078 + 1)),
        "unique_ids": len(set(ids)),
    }

    # 4. Complete Stems & Book Pages on All 7,078 Items
    empty_stems = [r["id"] for r in jsonl_rows if not r["question"] or len(r["question"].strip()) < 4]
    missing_pages = [r["id"] for r in jsonl_rows if not r["question_book_page"] or not r["answer_book_page"]]
    checks["non_empty_stems_and_page_provenance"] = {
        "passed": len(empty_stems) == 0 and len(missing_pages) == 0,
        "empty_stems": empty_stems,
        "missing_pages": missing_pages,
    }

    # 5. Complete 5 Options A..E & Answer Key Validity Across All 5,008 MCQs
    bad_mcq_opts = []
    bad_mcq_ans = []
    unstripped_opt_prefixes = []
    ocr_duplicate_opts = []
    for r in jsonl_rows:
        if r["quiz_type"] in ("commentati", "non_commentati"):
            opts = r["options"]
            if not isinstance(opts, dict) or list(opts.keys()) != ["A", "B", "C", "D", "E"] or any(not opts[k].strip() for k in "ABCDE"):
                bad_mcq_opts.append(r["id"])
            if r["answer"] not in ("A", "B", "C", "D", "E") or r["answer_text"] != opts.get(r["answer"]):
                bad_mcq_ans.append(r["id"])
            for k in "ABCDE":
                if re.match(r"^[ABCDE][\.\)]\s+\S", opts[k]):
                    unstripped_opt_prefixes.append((r["id"], k))
            vals = [opts[k].strip() for k in "ABCDE"]
            if len(set(vals)) < 5 and r["id"] not in VERBATIM_BOOK_DUPLICATE_IDS:
                ocr_duplicate_opts.append(r["id"])

    checks["all_5008_mcqs_complete_and_distinct"] = {
        "passed": (
            len(bad_mcq_opts) == 0
            and len(bad_mcq_ans) == 0
            and len(unstripped_opt_prefixes) == 0
            and len(ocr_duplicate_opts) == 0
        ),
        "total_mcqs": 5008,
        "bad_options": bad_mcq_opts,
        "bad_answers": bad_mcq_ans,
        "unstripped_prefixes": unstripped_opt_prefixes,
        "unexpected_duplicate_options": ocr_duplicate_opts,
        "documented_verbatim_book_typos": sorted(VERBATIM_BOOK_DUPLICATE_IDS),
    }

    # 6. Complete Blank Markers & Unmerged Answers Across All 2,070 Completamento Items
    missing_blanks = []
    bad_comp_answers = []
    for r in jsonl_rows:
        if r["quiz_type"] == "completamento":
            if "_____" not in r["question"]:
                missing_blanks.append(r["id"])
            if not r["answer"].strip() or re.search(r"(?:^|\s)\d{1,3}[\.\)]\s+[A-Za-zÀ-ÿ]", r["answer"]):
                bad_comp_answers.append((r["id"], r["answer"]))

    checks["all_2070_completamento_blanks_and_answers"] = {
        "passed": len(missing_blanks) == 0 and len(bad_comp_answers) == 0,
        "total_completamento": 2070,
        "missing_blanks": missing_blanks,
        "bad_answers": bad_comp_answers,
    }

    # 7. Complete Step-by-Step Explanations Across All 1,043 Quiz Commentati Items
    bad_explanations = [
        r["id"]
        for r in jsonl_rows
        if r["quiz_type"] == "commentati" and (not r["explanation"] or len(r["explanation"].strip()) < 12)
    ]
    checks["all_1043_commentati_explanations"] = {
        "passed": len(bad_explanations) == 0,
        "total_commentati": 1043,
        "missing_or_short_explanations": bad_explanations,
    }

    # 8. Zero Running Header / Footer / Watermark Leakage Across All 7,078 Items
    header_leaks = []
    for r in jsonl_rows:
        pool = [r["question"], r["answer"], r["explanation"] or ""]
        if r["options"]:
            pool.extend(r["options"].values())
        if any(HDR_LEAK_RE.search(t) for t in pool):
            header_leaks.append(r["id"])

    checks["zero_running_header_footer_leakage"] = {
        "passed": len(header_leaks) == 0,
        "leaked_ids": header_leaks,
    }

    # 9. Zero Decimal-Comma Subscript Corruptions ('0₄2' -> '0,2') Across All Fields
    dec_sub_corruptions = []
    # 10. Zero Unjoined Line-Break Hyphenations ('di- viene' -> 'diviene') Across All Fields
    unjoined_hyphens = []
    # 11. Zero Adjacent-Column Option Bleeds ('... B. ...') Across All 25,040 MCQ Options
    option_bleeds = []
    # 12. Zero Unconverted Ohm ('Ω' misread as '0') Options on Resistance Questions
    ohm_corruptions = []
    # 13. Zero Mixed Subscript-7 inside Superscript Exponents ('10⁻₇') Across All Fields
    mixed_sup7 = []

    for r in jsonl_rows:
        fields = [("Q", r["question"]), ("Ans", r["answer"]), ("Expl", r["explanation"] or "")]
        if r["options"]:
            for k, v in r["options"].items():
                fields.append((f"Opt.{k}", v))
                if re.search(r"\s[A-E][\.\)]\s*\S", v):
                    option_bleeds.append((r["id"], k, v))
                if re.search(r"\b(?:resistenz|resistor|ohm)\w*", r["question"].lower()) and re.match(r"^\d+0$", v.strip()):
                    ohm_corruptions.append((r["id"], k, v))
        for fn, txt in fields:
            if re.search(r"\d[₀₁₂₃₄₅₆₇₈₉]\d", txt):
                dec_sub_corruptions.append((r["id"], fn, txt[:80]))
            if re.search(r"[A-Za-zÀ-ÿ]-\s+[a-zà-ÿ]{2,}", txt):
                unjoined_hyphens.append((r["id"], fn, txt[:80]))
            if re.search(r"[⁰¹²³⁴⁵⁶⁸⁹⁻⁺]₇|₇[⁰¹²³⁴⁵⁶⁸⁹]|\b10₇\b", txt):
                mixed_sup7.append((r["id"], fn, txt[:80]))

    checks["zero_decimal_comma_subscript_corruptions"] = {
        "passed": len(dec_sub_corruptions) == 0,
        "count": len(dec_sub_corruptions),
        "samples": dec_sub_corruptions[:10],
    }
    checks["zero_unjoined_linebreak_hyphenations"] = {
        "passed": len(unjoined_hyphens) == 0,
        "count": len(unjoined_hyphens),
        "samples": unjoined_hyphens[:10],
    }
    checks["zero_adjacent_option_bleeds"] = {
        "passed": len(option_bleeds) == 0,
        "count": len(option_bleeds),
        "samples": option_bleeds[:10],
    }
    checks["zero_resistance_ohm_misreads"] = {
        "passed": len(ohm_corruptions) == 0,
        "count": len(ohm_corruptions),
        "samples": ohm_corruptions[:10],
    }
    checks["zero_mixed_superscript_glyphs"] = {
        "passed": len(mixed_sup7) == 0,
        "count": len(mixed_sup7),
        "samples": mixed_sup7[:10],
    }

    # 14. Genuine Non-Text Diagram Figure Verification + 100% Explicit Visual Stem Coverage
    on_disk_pngs = sorted(p.name for p in fig_dir.glob("*.png"))
    ref_in_dataset = sorted({fn for r in jsonl_rows for fn in r["figure_files"]})
    explicit_vis_re = re.compile(
        r"\b(?:in\s+figura|nella\s+figura|della\s+figura|seguente\s+figura|\(figura\)|"
        r"lo\s+schema|nello\s+schema|seguente\s+schema|il\s+grafico\s+(?:riporta|mostra|rappresenta|seguente)|"
        r"come\s+riporta\s+il\s+grafico|nel\s+grafico|seguenti\s+grafici|seguenti\s+disegni|"
        r"albero\s+genealogico\s+(?:riportato|mostrato|in\s+figura|seguente)|"
        r"mostrato\s+in\s+figura|rappresentat[oaie]\s+in\s+figura|"
        r"nella\s+tabella|seguente\s+tabella|tabella\s+seguente)\b"
    )
    missing_explicit_vis = [
        r["id"] for r in jsonl_rows if explicit_vis_re.search(r["question"].lower()) and not r["figure_files"]
    ]
    checks["clean_true_diagrams_and_all_explicit_visuals_covered"] = {
        "passed": on_disk_pngs == ref_in_dataset and 65 <= len(on_disk_pngs) <= 260 and len(missing_explicit_vis) == 0,
        "figure_count": len(on_disk_pngs),
        "missing_explicit_visual_ids": missing_explicit_vis,
        "orphan_files_on_disk": sorted(set(on_disk_pngs) - set(ref_in_dataset)),
        "missing_files_on_disk": sorted(set(ref_in_dataset) - set(on_disk_pngs)),
    }

    # 14b. Complete 1-to-1 Question Scan PNG Bijection Across All 7,078 QA Pairs
    q_img_dir = output_dir / "question_images"
    q_imgs_on_disk = sorted(p.name for p in q_img_dir.glob("*.png"))
    expected_q_imgs = sorted(f"{r['id']}.png" for r in jsonl_rows)
    missing_q_img_field = [r["id"] for r in jsonl_rows if r.get("question_image") != f"question_images/{r['id']}.png"]
    checks["all_7078_question_images_1to1_bijection"] = {
        "passed": (
            len(q_imgs_on_disk) == 7078
            and q_imgs_on_disk == expected_q_imgs
            and len(missing_q_img_field) == 0
        ),
        "question_images_on_disk": len(q_imgs_on_disk),
        "expected_count": 7078,
        "missing_field_ids": missing_q_img_field[:10],
    }

    # 15. Anki .apkg Structural, SQLite & Media Integrity Check
    with tempfile.TemporaryDirectory() as tmpd:
        tmp_path = Path(tmpd)
        with zipfile.ZipFile(apkg_path, "r") as zf:
            names = set(zf.namelist())
            db_entry = "collection.anki21" if "collection.anki21" in names else "collection.anki2"
            zf.extract(db_entry, tmp_path)
            zf.extract("media", tmp_path)
            media_map = json.loads((tmp_path / "media").read_text(encoding="utf-8"))
            missing_zip_media = [k for k in media_map.keys() if k not in names]
            dark_or_blank_media = []
            for k, orig_name in media_map.items():
                if k in names:
                    arr_m = np.asarray(Image.open(BytesIO(zf.read(k))).convert("L"), dtype=np.float32)
                    if float(arr_m.mean()) < 130.0 or float(np.percentile(arr_m, 90)) < 220.0 or float(arr_m.min()) > 150.0:
                        dark_or_blank_media.append((orig_name, round(float(arr_m.mean()), 1), round(float(arr_m.min()), 1)))

        conn = sqlite3.connect(str(tmp_path / db_entry))
        cur = conn.cursor()
        note_count = cur.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        card_count = cur.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
        distinct_dids = cur.execute("SELECT COUNT(DISTINCT did) FROM cards").fetchone()[0]
        flds_all = [row[0] for row in cur.execute("SELECT flds FROM notes").fetchall()]
        conn.close()

        referenced_imgs = set()
        for fstr in flds_all:
            referenced_imgs.update(re.findall(r'<img src="([^"]+)">', fstr))
        media_filenames = set(media_map.values())
        missing_ref_imgs = sorted(referenced_imgs - media_filenames)

    checks["anki_apkg_and_media_integrity"] = {
        "passed": (
            note_count == 7078
            and card_count == 7078
            and distinct_dids == 84
            and len(missing_zip_media) == 0
            and len(missing_ref_imgs) == 0
            and len(media_map) == len(referenced_imgs)
            and set(on_disk_pngs).issubset(media_filenames)
        ),
        "apkg_size_bytes": apkg_path.stat().st_size,
        "apkg_size_mb": round(apkg_path.stat().st_size / (1024 * 1024), 2),
        "sqlite_notes": note_count,
        "sqlite_cards": card_count,
        "distinct_subdecks": distinct_dids,
        "embedded_media_files": len(media_map),
        "referenced_card_images": len(referenced_imgs),
        "missing_zip_media": missing_zip_media,
        "missing_referenced_images": missing_ref_imgs,
    }

    checks["zero_dark_or_blank_embedded_pngs"] = {
        "passed": len(dark_or_blank_media) == 0,
        "inspected_png_count": len(media_map),
        "bad_pngs": dark_or_blank_media[:15],
    }

    overall_passed = all(c["passed"] for c in checks.values())
    report = {
        "overall_passed": overall_passed,
        "verified_total_qa_pairs": len(jsonl_rows),
        "subject_totals": {
            sc: sum(1 for r in jsonl_rows if r["subject_code"] == sc)
            for sc in ("CHIM", "BIO", "FIS")
        },
        "quiz_type_totals": {
            qt: sum(1 for r in jsonl_rows if r["quiz_type"] == qt)
            for qt in ("commentati", "non_commentati", "completamento")
        },
        "checks": checks,
    }

    report_path = output_dir / "verification_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=================================================================")
    print(f"OVERALL VERIFICATION PASSED: {overall_passed} ({sum(c['passed'] for c in checks.values())} / {len(checks)} checks)")
    for name, res in checks.items():
        status = "PASS" if res["passed"] else "FAIL"
        print(f"  [{status}] {name}")
    print("=================================================================")
    if not overall_passed:
        raise AssertionError(f"Verification failed: {json.dumps(report, ensure_ascii=False, indent=2)}")
    return report


if __name__ == "__main__":
    run_verification()
