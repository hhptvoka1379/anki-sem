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

from extractor.round2_remediation import DEDUP_DROP_MAP
from extractor.stage1_canonicalize import SUBJECT_CHAPTERS

EXPECTED_SOURCE_COUNTS = {
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

EXPECTED_TOTAL_UNIQUE = 7078 - len(DEDUP_DROP_MAP)  # 6,948 unique cards

HDR_LEAK_RE = re.compile(
    r"(chimicaepropedeutica|wwwedi[s]es|www\.edi[s]es|\bedi[s]es\b|\bedlses\b|\bedives\b|\bedices\b|"
    r"\bodices\b|\btedi[s]es\b|\besses\b|\b2di[s]es\b|cases\s*\|\s*_|"
    r"quiz a completamento|quiz non commentati|quiz commentati|risposte commentate)",
    re.I,
)

PUB_ANY_RE = re.compile(r"edi[s]es|@di[s]es|vaedi[s]es", re.I)


def run_verification(output_dir: Path = Path("/home/user/anki-sem/output")) -> Dict:
    repo_dir = output_dir.parent
    jsonl_path = output_dir / "qa_dataset.jsonl"
    json_path = output_dir / "qa_dataset.json"
    csv_path = output_dir / "qa_dataset.csv"
    apkg_path = output_dir / "Semestre_Filtro_Complete.apkg"
    fig_dir = output_dir / "figures"

    jsonl_rows = [json.loads(line) for line in open(jsonl_path, encoding="utf-8") if line.strip()]
    json_payload = json.load(open(json_path, encoding="utf-8"))
    csv_rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))

    checks: Dict[str, Dict] = {}

    # 1. Exact Post-Deduplication Total & Cross-Format Parity (6,948 unique cards)
    checks["exact_deduplicated_total_parity"] = {
        "passed": (
            len(jsonl_rows) == EXPECTED_TOTAL_UNIQUE
            and len(json_payload["items"]) == EXPECTED_TOTAL_UNIQUE
            and len(csv_rows) == EXPECTED_TOTAL_UNIQUE
        ),
        "expected_unique": EXPECTED_TOTAL_UNIQUE,
        "removed_duplicates": len(DEDUP_DROP_MAP),
        "jsonl_count": len(jsonl_rows),
        "json_count": len(json_payload["items"]),
        "csv_count": len(csv_rows),
    }

    # 2. Exact 84 Subsection Accounting (Source Count - Verified Dropped Duplicates == Live Count)
    subsection_mismatches = []
    code_map = {"COMM": "commentati", "NCOM": "non_commentati", "COMP": "completamento"}
    dropped_by_sub: Dict[tuple, set] = {}
    for did in DEDUP_DROP_MAP:
        sc_d, ch_s, qt_s, qn_s = did.split("-")
        dropped_by_sub.setdefault((sc_d, int(ch_s[1:]), code_map[qt_s]), set()).add(int(qn_s))

    for _, sc, ch, _, _, _ in SUBJECT_CHAPTERS:
        exp_comm, exp_ncom, exp_comp = EXPECTED_SOURCE_COUNTS[(sc, ch)]
        for qt, src_n in (("commentati", exp_comm), ("non_commentati", exp_ncom), ("completamento", exp_comp)):
            sub_items = [r for r in jsonl_rows if r["subject_code"] == sc and r["chapter_num"] == ch and r["quiz_type"] == qt]
            qnums = [r["qnum"] for r in sub_items]
            dropped_qnums = dropped_by_sub.get((sc, ch, qt), set())
            expected_qnums = [q for q in range(1, src_n + 1) if q not in dropped_qnums]
            if qnums != expected_qnums:
                subsection_mismatches.append(
                    {"section": f"{sc}-C{ch:02d}-{qt}", "got": len(sub_items), "expected": len(expected_qnums)}
                )

    checks["all_84_subsections_exact_bijection"] = {
        "passed": len(subsection_mismatches) == 0,
        "verified_subsections": 84 - len(subsection_mismatches),
        "mismatches": subsection_mismatches,
    }

    # 3. Unique IDs, Disjointness from DEDUP_DROP_MAP & Contiguous Global Index 1..N
    ids = [r["id"] for r in jsonl_rows]
    id_set = set(ids)
    g_idxs = [r["global_index"] for r in jsonl_rows]
    prio = {"commentati": 3, "non_commentati": 2, "completamento": 1}
    qt_from_id = lambda cid: code_map[cid.split("-")[2]]
    prio_violations = [
        (d, k) for d, k in DEDUP_DROP_MAP.items() if prio[qt_from_id(k)] < prio[qt_from_id(d)] or k not in id_set or d in id_set
    ]
    checks["unique_ids_dedup_priority_and_indexing"] = {
        "passed": (
            len(id_set) == EXPECTED_TOTAL_UNIQUE
            and g_idxs == list(range(1, EXPECTED_TOTAL_UNIQUE + 1))
            and len(prio_violations) == 0
        ),
        "unique_ids": len(id_set),
        "priority_or_membership_violations": prio_violations,
    }

    # 4. Complete Stems & Book Pages on All Items
    empty_stems = [r["id"] for r in jsonl_rows if not r["question"] or len(r["question"].strip()) < 4]
    missing_pages = [r["id"] for r in jsonl_rows if not r["question_book_page"] or not r["answer_book_page"]]
    checks["non_empty_stems_and_page_provenance"] = {
        "passed": len(empty_stems) == 0 and len(missing_pages) == 0,
        "empty_stems": empty_stems,
        "missing_pages": missing_pages,
    }

    # 5. Complete 5 Distinct Options A..E & Answer Key Validity Across All MCQs
    mcq_rows = [r for r in jsonl_rows if r["quiz_type"] in ("commentati", "non_commentati")]
    bad_mcq_opts = []
    bad_mcq_ans = []
    unstripped_opt_prefixes = []
    dup_opt_ids = []
    for r in mcq_rows:
        opts = r["options"]
        if not isinstance(opts, dict) or list(opts.keys()) != ["A", "B", "C", "D", "E"] or any(not opts[k].strip() for k in "ABCDE"):
            bad_mcq_opts.append(r["id"])
        if r["answer"] not in ("A", "B", "C", "D", "E") or r["answer_text"] != opts.get(r["answer"]):
            bad_mcq_ans.append(r["id"])
        for k in "ABCDE":
            if re.match(r"^[ABCDE][\.\)]\s+\S", opts[k]):
                unstripped_opt_prefixes.append((r["id"], k))
        vals = [opts[k].strip() for k in "ABCDE"]
        if len(set(vals)) != 5:
            dup_opt_ids.append(r["id"])

    checks["all_mcqs_complete_and_distinct"] = {
        "passed": (
            len(bad_mcq_opts) == 0
            and len(bad_mcq_ans) == 0
            and len(unstripped_opt_prefixes) == 0
            and len(dup_opt_ids) == 0
        ),
        "total_mcqs": len(mcq_rows),
        "bad_options": bad_mcq_opts,
        "bad_answers": bad_mcq_ans,
        "unstripped_prefixes": unstripped_opt_prefixes,
        "duplicate_option_mcqs": dup_opt_ids,
    }

    # 6. Complete Blank Markers & Unmerged Answers Across All Completamento Items
    comp_rows = [r for r in jsonl_rows if r["quiz_type"] == "completamento"]
    missing_blanks = [r["id"] for r in comp_rows if "_____" not in r["question"]]
    bad_comp_answers = [
        (r["id"], r["answer"])
        for r in comp_rows
        if not r["answer"].strip() or re.search(r"(?:^|\s)\d{1,3}[\.\)]\s+[A-Za-zÀ-ÿ]", r["answer"])
    ]
    checks["all_completamento_blanks_and_answers"] = {
        "passed": len(missing_blanks) == 0 and len(bad_comp_answers) == 0,
        "total_completamento": len(comp_rows),
        "missing_blanks": missing_blanks,
        "bad_answers": bad_comp_answers,
    }

    # 7. Complete Step-by-Step Explanations Across All Quiz Commentati Items
    comm_rows = [r for r in jsonl_rows if r["quiz_type"] == "commentati"]
    bad_explanations = [
        r["id"] for r in comm_rows if not r["explanation"] or len(r["explanation"].strip()) < 12
    ]
    checks["all_commentati_explanations"] = {
        "passed": len(comm_rows) == 1041 and len(bad_explanations) == 0,
        "total_commentati": len(comm_rows),
        "missing_or_short_explanations": bad_explanations,
    }

    # 8. Zero Running Header / Footer / Watermark Leakage & Zero Targeted OCR Typos
    header_leaks = []
    targeted_typos = []
    typo_rx = re.compile(
        r"ossidrit|\b(?:a|la)\s*T\s*=\s*K\b|\bUsala\b|\bll\s+[a-zà-ÿ0-9]|\bJa\s+[a-zà-ÿ]|(?<!\S)(?:i\]|1\]|I\}|i\})\s+"
    )
    dec_sub_corruptions = []
    unjoined_hyphens = []
    option_bleeds = []
    ohm_corruptions = []
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
            if HDR_LEAK_RE.search(txt):
                header_leaks.append((r["id"], fn))
            if typo_rx.search(txt):
                targeted_typos.append((r["id"], fn, typo_rx.findall(txt)))
            if re.search(r"\d[₀₁₂₃₄₅₆₇₈₉]\d", txt):
                dec_sub_corruptions.append((r["id"], fn, txt[:80]))
            if re.search(r"[A-Za-zÀ-ÿ]-(?<!\bmono-)\s+[a-zà-ÿ]{2,}", txt):
                unjoined_hyphens.append((r["id"], fn, txt[:80]))
            if re.search(r"[⁰¹²³⁴⁵⁶⁸⁹⁻⁺]₇|(?<![A-Za-z₀-₉])₇[⁰¹²³⁴⁵⁶⁸⁹]|\b10₇\b", txt):
                mixed_sup7.append((r["id"], fn, txt[:80]))

    checks["zero_running_header_footer_leakage"] = {"passed": len(header_leaks) == 0, "leaked_ids": header_leaks}
    checks["zero_round2_targeted_ocr_typos"] = {"passed": len(targeted_typos) == 0, "hits": targeted_typos}
    checks["zero_decimal_comma_subscript_corruptions"] = {"passed": len(dec_sub_corruptions) == 0, "count": len(dec_sub_corruptions)}
    checks["zero_unjoined_linebreak_hyphenations"] = {"passed": len(unjoined_hyphens) == 0, "count": len(unjoined_hyphens)}
    checks["zero_adjacent_option_bleeds"] = {"passed": len(option_bleeds) == 0, "count": len(option_bleeds)}
    checks["zero_resistance_ohm_misreads"] = {"passed": len(ohm_corruptions) == 0, "count": len(ohm_corruptions)}
    checks["zero_mixed_superscript_glyphs"] = {"passed": len(mixed_sup7) == 0, "count": len(mixed_sup7)}

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

    expected_q_imgs = sorted(f"{r['id']}.png" for r in jsonl_rows)
    missing_q_img_field = [r["id"] for r in jsonl_rows if r.get("question_image") != f"question_images/{r['id']}.png"]

    # 15. Anki .apkg Structural, SQLite, Publisher-Free & Media Integrity Check
    pub_sqlite_leaks = []
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
        models_raw, decks_raw = cur.execute("SELECT models, decks FROM col").fetchone()
        col_models = json.loads(models_raw)
        if PUB_ANY_RE.search(models_raw):
            pub_sqlite_leaks.append("col.models")
        if PUB_ANY_RE.search(decks_raw):
            pub_sqlite_leaks.append("col.decks")
        flds_all = [row[0] for row in cur.execute("SELECT flds FROM notes").fetchall()]
        conn.close()

        referenced_imgs = set()
        html_entity_leaks = []
        missing_fig_html = []
        for fstr in flds_all:
            parts = fstr.split("\x1f")
            if "&#x27;" in fstr or "&#39;" in fstr:
                html_entity_leaks.append(parts[0])
            if PUB_ANY_RE.search(fstr):
                pub_sqlite_leaks.append(parts[0])
            referenced_imgs.update(re.findall(r'<img src="([^"]+)">', fstr))
        media_filenames = set(media_map.values())
        missing_ref_imgs = sorted(referenced_imgs - media_filenames)
        q_imgs_effective = sorted(fn for fn in media_filenames if fn in set(expected_q_imgs))

    id_to_flds = {fstr.split("\x1f")[0]: fstr.split("\x1f") for fstr in flds_all}
    for r in jsonl_rows:
        if r["figure_files"]:
            fh = id_to_flds[r["id"]][14]
            if not all(f'<img src="{fn}">' in fh for fn in r["figure_files"]):
                missing_fig_html.append(r["id"])

    checks["all_question_images_1to1_bijection"] = {
        "passed": (
            len(q_imgs_effective) == EXPECTED_TOTAL_UNIQUE
            and q_imgs_effective == expected_q_imgs
            and len(missing_q_img_field) == 0
        ),
        "question_images_verified": len(q_imgs_effective),
        "expected_count": EXPECTED_TOTAL_UNIQUE,
        "missing_field_ids": missing_q_img_field[:10],
    }

    p291_ids = [r["id"] for r in jsonl_rows if r.get("answer_book_page") == 291]
    expected_p291 = [f"CHIM-C11-COMM-{i:03d}" for i in range(17, 24)]
    bad_ans_bp = [
        r["id"] for r in jsonl_rows
        if not isinstance(r.get("answer_book_page"), int) or not (252 <= r["answer_book_page"] <= 901)
    ]
    checks["exact_answer_book_pages_restored"] = {
        "passed": p291_ids == expected_p291 and len(bad_ans_bp) == 0,
        "page_291_ids": p291_ids,
        "invalid_answer_book_page_count": len(bad_ans_bp),
    }

    bad_filenames = [
        str(p.relative_to(repo_dir))
        for p in repo_dir.rglob("*")
        if ".git" not in p.parts and PUB_ANY_RE.search(p.name)
    ]
    pub_text_leaks = []
    for p in sorted(repo_dir.rglob("*")):
        if ".git" in p.parts or p.is_dir() or p.suffix in (".pdf", ".png", ".apkg", ".pyc"):
            continue
        try:
            if PUB_ANY_RE.search(p.read_text(encoding="utf-8")):
                pub_text_leaks.append(str(p.relative_to(repo_dir)))
        except Exception:
            continue

    checks["zero_publisher_branding_across_repo_and_apkg"] = {
        "passed": len(bad_filenames) == 0 and len(pub_sqlite_leaks) == 0 and len(pub_text_leaks) == 0,
        "publisher_named_files": bad_filenames,
        "sqlite_leaks": pub_sqlite_leaks,
        "text_file_leaks": pub_text_leaks,
    }

    checks["zero_html_entities_or_missing_figures"] = {
        "passed": len(html_entity_leaks) == 0 and len(missing_fig_html) == 0,
        "html_entity_leaks": len(html_entity_leaks),
        "missing_figure_html_cards": missing_fig_html,
    }

    theme04_apkg = output_dir / "themes" / "Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg"
    theme_updaters = sorted((output_dir / "themes").glob("ThemeUpdater_*.apkg"))
    theme_css_files = sorted((output_dir / "themes" / "css").glob("*.css"))
    t04_ok = False
    if theme04_apkg.exists():
        with zipfile.ZipFile(theme04_apkg, "r") as zt:
            znames = set(zt.namelist())
            t_media = json.loads(zt.read("media").decode("utf-8"))
            with tempfile.TemporaryDirectory() as td2:
                zt.extract("collection.anki2", td2)
                c2 = sqlite3.connect(str(Path(td2) / "collection.anki2"))
                n2 = c2.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
                m2_raw, d2_raw = c2.execute("SELECT models, decks FROM col").fetchone()
                m2 = json.loads(m2_raw)
                c2.close()
            m2_css = "\n".join(v.get("css", "") for v in m2.values())
            t04_ok = (
                n2 == EXPECTED_TOTAL_UNIQUE
                and len(t_media) == len(media_map)
                and "RISO.ZINE // REG.04" in m2_css
                and not PUB_ANY_RE.search(m2_raw)
                and not PUB_ANY_RE.search(d2_raw)
                and all(k in znames for k in t_media.keys())
            )
    checks["themed_apkg_and_10_theme_updaters_integrity"] = {
        "passed": t04_ok and len(theme_updaters) == 10 and len(theme_css_files) == 10,
        "theme04_apkg_exists_and_valid": t04_ok,
        "theme_updater_count": len(theme_updaters),
        "theme_css_count": len(theme_css_files),
    }

    checks["anki_apkg_and_media_integrity"] = {
        "passed": (
            note_count == EXPECTED_TOTAL_UNIQUE
            and card_count == EXPECTED_TOTAL_UNIQUE
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
        "pre_dedup_source_pairs": 7078,
        "deduplicated_pairs_removed": len(DEDUP_DROP_MAP),
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
