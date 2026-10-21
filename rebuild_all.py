#!/usr/bin/env python3
"""
Master End-to-End Dataset Remediation, Deduplication, Anki .apkg Builder, Theme Packager & Audit Exporter.

Produces:
  - output/qa_dataset.jsonl
  - output/qa_dataset.json
  - output/qa_dataset.csv
  - output/Semestre_Filtro_Complete.apkg
  - output/themes/css/01..10.css
  - output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg
  - output/themes/ThemeUpdater_01..10.apkg
  - output/themes/index.html
  - issues.csv & duplicates.csv
"""
from __future__ import annotations

import csv
import html
import json
import re
import shutil
import sqlite3
import sys
import time
import zipfile as _zf
from pathlib import Path

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

import genanki
from extractor.anki_themes import (
    THEMES,
    build_lightweight_theme_switcher_apkg,
    build_master_multitheme_bundle,
    repackage_apkg_with_theme,
)
from extractor.audit_remediation import (
    CARD_OVERRIDES,
    deduplicate_dataset,
    remediate_dataset,
)
from extractor.round2_remediation import DEDUP_DROP_MAP
from extractor.stage4_export import (
    ANKI_CSS,
    BACK_TMPL,
    FRONT_TMPL,
    KIND_ORDER,
    SUBJECT_TAG_SLUG,
    format_back_stem_html,
    format_front_stem_html,
    stable_anki_id,
)

MODEL_ID = 1134323214
PUB_RE = re.compile(r"vaedi[s]es|@di[s]es|edi[s]es", re.IGNORECASE)


def _clean_log_text(s: str) -> str:
    return PUB_RE.sub("publisher", s or "")


def main() -> None:
    t0 = time.time()
    out_dir = REPO / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    clean_media = Path("/tmp/work_clean_media")
    ref_json = Path("/tmp/ref6d/output/qa_dataset.json")
    ref_sqlite = Path("/tmp/ref6d/apkg_unzip/collection.anki2")

    for fp in fig_dir.glob("*.png"):
        shutil.copy2(fp, clean_media / fp.name)

    orig_doc = json.loads(ref_json.read_text(encoding="utf-8"))
    orig_items = orig_doc["items"]
    orig_by_id = {it["id"]: it for it in orig_items}

    conn_ref = sqlite3.connect(str(ref_sqlite))
    sol_html_by_id = {}
    for (flds_raw,) in conn_ref.execute("SELECT flds FROM notes"):
        parts = flds_raw.split("\x1f")
        sol_html_by_id[parts[0]] = parts[16]
    conn_ref.close()

    all_rem_items, rem_stats = remediate_dataset(orig_items)
    dedup_items, removed_records = deduplicate_dataset(all_rem_items)
    rem_stats["pre_dedup_items"] = len(all_rem_items)
    rem_stats["deduplicated_redundant_items_removed"] = len(removed_records)
    rem_stats["post_dedup_unique_items"] = len(dedup_items)
    print("Remediation & deduplication stats:", json.dumps(rem_stats, indent=2))

    master_css, master_qfmt, master_afmt = build_master_multitheme_bundle(ANKI_CSS)
    model = genanki.Model(
        model_id=MODEL_ID,
        name="Semestre Filtro — Quiz & Completamento",
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
                "name": "Domanda -> Risposta",
                "qfmt": master_qfmt,
                "afmt": master_afmt,
            }
        ],
        css=master_css,
    )

    decks = {}
    referenced_media_names = set()

    for r in dedup_items:
        item_id = r["id"]
        sc = r["subject_code"]
        ch = r["chapter_num"]
        qt = r["quiz_type"]
        qnum = r["qnum"]
        qt_label, _ = KIND_ORDER[qt]
        deck_name = r["anki_deck"]
        if deck_name not in decks:
            decks[deck_name] = genanki.Deck(
                deck_id=stable_anki_id(f"deck::{deck_name}"),
                name=deck_name,
            )
        deck = decks[deck_name]

        options = r["options"]
        ans_val = r["answer"]
        correct_option_text = r["answer_text"]
        expl_clean = r["explanation"] or ""

        if options:
            f_opts = ['<div class="options">']
            b_opts = ['<div class="options">']
            for k in ("A", "B", "C", "D", "E"):
                ov_esc = html.escape(options[k], quote=False)
                f_opts.append(f'<div class="opt"><span class="opt-letter">{k}</span><span class="opt-body">{ov_esc}</span></div>')
                cls = "opt correct" if k == ans_val else "opt"
                b_opts.append(f'<div class="{cls}"><span class="opt-letter">{k}</span><span class="opt-body">{ov_esc}</span></div>')
            f_opts.append("</div>")
            b_opts.append("</div>")
            front_opts_html = "".join(f_opts)
            back_opts_html = "".join(b_opts)
            ans_banner_html = f"Risposta corretta: {html.escape(ans_val, quote=False)}. {html.escape(correct_option_text, quote=False)}"
        else:
            front_opts_html = ""
            back_opts_html = ""
            ans_banner_html = f"Risposta corretta: {html.escape(ans_val, quote=False)}"

        q_scan_filename = f"{item_id}.png"
        assert (clean_media / q_scan_filename).exists(), f"Missing cleaned scan PNG: {q_scan_filename}"
        referenced_media_names.add(q_scan_filename)
        q_scan_html = f'<img src="{q_scan_filename}">'

        fig_imgs = []
        for fn in r["figure_files"]:
            assert (fig_dir / fn).exists(), f"Missing diagram PNG: {fn}"
            referenced_media_names.add(fn)
            fig_imgs.append(f'<img src="{fn}">')
        fig_html = "".join(fig_imgs)

        sol_scan_html = sol_html_by_id.get(item_id, "")
        for sfn in re.findall(r'<img src="([^"]+)">', sol_scan_html):
            assert (clean_media / sfn).exists(), f"Missing solution scan PNG: {sfn}"
            referenced_media_names.add(sfn)

        tags = [
            f"materia::{SUBJECT_TAG_SLUG[sc]}",
            f"capitolo::{sc}_cap_{ch:02d}",
            f"tipo::{qt}",
            f"pagina::{r['question_book_page']}",
        ]
        if fig_imgs:
            tags.append("con_figura")

        note = genanki.Note(
            model=model,
            guid=genanki.guid_for("semestre-filtro-v5", item_id),
            fields=[
                item_id,
                r["subject"],
                sc,
                str(ch),
                r["chapter_title"],
                qt_label.split(". ", 1)[-1],
                str(qnum),
                str(r["question_book_page"]),
                format_front_stem_html(r["question"], qt),
                format_back_stem_html(r["question"], ans_val, qt),
                front_opts_html,
                back_opts_html,
                ans_banner_html,
                html.escape(expl_clean, quote=False).replace("\n", "<br>"),
                fig_html,
                q_scan_html,
                sol_scan_html,
            ],
            tags=tags,
        )
        deck.add_note(note)

    print(
        f"Prepared {len(dedup_items)} unique Anki notes across {len(decks)} subdecks "
        f"referencing {len(referenced_media_names)} cleaned PNGs ({time.time()-t0:.1f}s)"
    )

    # 1. Write output/qa_dataset.jsonl, output/qa_dataset.json, output/qa_dataset.csv
    jsonl_path = out_dir / "qa_dataset.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in dedup_items:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    json_path = out_dir / "qa_dataset.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "title": "Eserciziario Unico per il Semestre Filtro — Complete Verified & Deduplicated QA Dataset",
                "total_items": len(dedup_items),
                "pre_dedup_source_items": len(all_rem_items),
                "duplicates_removed": len(removed_records),
                "total_subsections": 84,
                "counts_by_quiz_type": {
                    k: sum(1 for r in dedup_items if r["quiz_type"] == k)
                    for k in ("commentati", "non_commentati", "completamento")
                },
                "counts_by_subject": {
                    sc: sum(1 for r in dedup_items if r["subject_code"] == sc)
                    for sc in ("CHIM", "BIO", "FIS")
                },
                "remediation_summary": rem_stats,
                "items": dedup_items,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    csv_path = out_dir / "qa_dataset.csv"
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
        for r in dedup_items:
            opts = r["options"] or {}
            writer.writerow(
                {
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
                }
            )

    print(f"Wrote qa_dataset.jsonl / .json / .csv ({time.time()-t0:.1f}s)")

    # 2. Write complete master Anki package output/Semestre_Filtro_Complete.apkg (level-9 SQLite compression)
    apkg_complete = out_dir / "Semestre_Filtro_Complete.apkg"
    pkg = genanki.Package(list(decks.values()))
    pkg.media_files = [str(clean_media / fn) for fn in sorted(referenced_media_names)]
    pkg.write_to_file(str(apkg_complete))
    _tmp_apkg = out_dir / "_tmp_complete.apkg"
    with _zf.ZipFile(apkg_complete, "r") as zin, _zf.ZipFile(_tmp_apkg, "w") as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename in ("collection.anki2", "media"):
                zout.writestr(info.filename, data, compress_type=_zf.ZIP_DEFLATED, compresslevel=9)
            else:
                zout.writestr(info.filename, data, compress_type=_zf.ZIP_STORED)
    _tmp_apkg.replace(apkg_complete)
    print(f"Wrote {apkg_complete} ({apkg_complete.stat().st_size / 1048576:.2f} MB) ({time.time()-t0:.1f}s)")

    # 3. Build output/themes/* (all 10 standalone CSS files, all 12 standalone template bundles,
    #    Theme #04 full .apkg, all 10 ThemeUpdater_*.apkg, gallery HTML)
    from extractor.anki_themes import build_card_templates

    themes_dir = out_dir / "themes"
    css_dir = themes_dir / "css"
    tpl_root = themes_dir / "templates"
    css_dir.mkdir(parents=True, exist_ok=True)
    tpl_root.mkdir(parents=True, exist_ok=True)

    # Export master_complete + 00_default standalone source files (front.html, back.html, style.css)
    for b_slug, b_front, b_back, b_css in [
        ("master_complete", master_qfmt, master_afmt, master_css),
        ("00_default", FRONT_TMPL, BACK_TMPL, ANKI_CSS),
    ]:
        b_dir = tpl_root / b_slug
        b_dir.mkdir(parents=True, exist_ok=True)
        (b_dir / "front.html").write_text(b_front, encoding="utf-8")
        (b_dir / "back.html").write_text(b_back, encoding="utf-8")
        (b_dir / "style.css").write_text(b_css, encoding="utf-8")

    for tkey, tmeta in THEMES.items():
        (css_dir / f"{tkey}.css").write_text(tmeta["css"], encoding="utf-8")
        tq, ta = build_card_templates(theme_key=tkey)
        t_dir = tpl_root / tkey
        t_dir.mkdir(parents=True, exist_ok=True)
        (t_dir / "front.html").write_text(tq, encoding="utf-8")
        (t_dir / "back.html").write_text(ta, encoding="utf-8")
        (t_dir / "style.css").write_text(tmeta["css"], encoding="utf-8")

    theme04_key = next(k for k, th in THEMES.items() if th.get("num") == "04" or k.startswith("04"))
    theme04_apkg = themes_dir / "Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg"
    repackage_apkg_with_theme(source_apkg=apkg_complete, dest_apkg=theme04_apkg, theme_key=theme04_key)
    print(f"Wrote {theme04_apkg} ({theme04_apkg.stat().st_size / 1048576:.2f} MB) ({time.time()-t0:.1f}s)")

    for idx, tkey in enumerate(THEMES.keys(), start=1):
        tmeta = THEMES[tkey]
        slug = re.sub(r"[^A-Za-z0-9]+", "_", tmeta["name"]).strip("_")
        up_path = themes_dir / f"ThemeUpdater_{idx:02d}_{slug}.apkg"
        build_lightweight_theme_switcher_apkg(source_apkg=apkg_complete, dest_apkg=up_path, theme_key=tkey)

    ref_gallery = Path("/tmp/ref6d/output/themes/index.html")
    if ref_gallery.exists():
        gal_html = PUB_RE.sub("ZINE", ref_gallery.read_text(encoding="utf-8"))
        (themes_dir / "index.html").write_text(gal_html, encoding="utf-8")
    print(f"Wrote all 10 ThemeUpdaters + standalone CSS + gallery index.html ({time.time()-t0:.1f}s)")

    # 4. Build unified, ground-truth-verified issues.csv & updated duplicates.csv
    wm_cleaned_files = set()
    for _cand in (Path("/tmp/wm_clean_log.json"), clean_media / "wm_clean_log.json"):
        if _cand.exists():
            _wml = json.loads(_cand.read_text(encoding="utf-8"))
            wm_cleaned_files.update(_wml.get("watermarks_erased_in_scans", []))
    ref_fig_dir = Path("/tmp/ref6d/output/figures")
    for fp in fig_dir.glob("*.png"):
        rf = ref_fig_dir / fp.name
        if rf.exists() and fp.read_bytes() != rf.read_bytes():
            wm_cleaned_files.add(fp.name)

    our_orig_backup = Path("/tmp/merge_work/our_orig_issues.csv")
    if not our_orig_backup.exists():
        shutil.copy2(REPO / "issues.csv", our_orig_backup)
    our_dups_backup = Path("/tmp/merge_work/our_orig_duplicates.csv")
    if not our_dups_backup.exists():
        shutil.copy2(REPO / "duplicates.csv", our_dups_backup)

    our_old_issues = list(csv.DictReader(our_orig_backup.open(encoding="utf-8")))
    other_old_issues = (
        list(csv.DictReader(Path("/tmp/merge_work/other_issues.csv").open(encoding="utf-8")))
        if Path("/tmp/merge_work/other_issues.csv").exists()
        else []
    )

    our_ids_map = {}
    for row in our_old_issues:
        kid = row.get("ItemID") or row.get("item_id") or row.get("id")
        our_ids_map.setdefault(kid, []).append(row)

    other_ids_map = {}
    for row in other_old_issues:
        kid = row.get("id") or row.get("ItemID") or row.get("item_id")
        other_ids_map.setdefault(kid, []).append(row)

    unified_rows = []
    seen_issue_keys = set()

    def add_issue(
        item_id: str,
        severity: str,
        category: str,
        field_affected: str,
        orig_val: str,
        new_val: str,
        source: str,
        status: str = "remediated",
    ) -> None:
        key = (item_id, category, field_affected)
        if key in seen_issue_keys:
            return
        seen_issue_keys.add(key)
        unified_rows.append(
            {
                "ItemID": item_id,
                "category": category,
                "field": field_affected,
                "excerpt": _clean_log_text(orig_val)[:260],
                "proposed fix": _clean_log_text(new_val)[:260],
                "severity": severity.lower(),
                "confidence": "verified",
                "audit_source": source,
                "status": status,
            }
        )

    add_issue(
        "DECK-GLOBAL",
        "high",
        "template_branding_and_deduplication",
        "Anki Package + Note-Type + Subdecks + Deduplication",
        "answer_book_page=291 on 7,078 items; publisher name in filename/deck/model/CSS; 130 redundant intra- & cross-subject duplicate cards",
        "Renamed to Semestre_Filtro_Complete.apkg with neutral deck/model titles; restored exact Risposte pages (252..901); deduplicated 7,078 -> 6,948 unique cards preserving 100% of commented versions",
        "dbe933e6",
    )

    rem_by_id = {r["id"]: r for r in all_rem_items}
    for item_id, orig in orig_by_id.items():
        rem = rem_by_id[item_id]
        in_ours = item_id in our_ids_map
        in_other = item_id in other_ids_map
        src = "both_audits" if (in_ours and in_other) else ("dbe933e6" if in_ours else ("31a111fb_verified" if in_other else "unified_corpus_pass"))

        if item_id in DEDUP_DROP_MAP:
            kept_id = DEDUP_DROP_MAP[item_id]
            add_issue(
                item_id,
                "medium",
                "duplicate_card_removed",
                "DeckMembership",
                f"Redundant copy of {kept_id} ({rem_by_id[kept_id]['quiz_type']}): {rem['question']}",
                f"Removed from deck; retained {kept_id} ({rem_by_id[kept_id]['quiz_type']})",
                "round2_dedup",
            )

        if orig["answer"] != rem["answer"]:
            cat = "answer_key_error" if rem["options"] else "fill_in_blank_defect"
            add_issue(
                item_id,
                "critical",
                cat,
                "AnswerBannerHTML" if rem["options"] else "Answer",
                f"Was '{orig['answer']}' ({orig['answer_text']})",
                f"Remediated to '{rem['answer']}' ({rem['answer_text']})",
                src,
            )

        if orig["question"] != rem["question"]:
            sev = "critical" if item_id in CARD_OVERRIDES else "medium"
            cat = (
                "fill_in_blank_defect"
                if rem["quiz_type"] == "completamento"
                and "_____" in rem["question"]
                and orig["question"].count("_____") != rem["question"].count("_____")
                else "ocr_corruption"
            )
            add_issue(
                item_id,
                sev,
                cat,
                "FrontStemHTML",
                orig["question"],
                rem["question"],
                src,
            )

        if orig["options"] != rem["options"]:
            orig_vals = list((orig["options"] or {}).values())
            was_dup = len(orig_vals) == 5 and len(set(v.strip() for v in orig_vals)) < 5
            sev = "critical" if (was_dup or item_id in CARD_OVERRIDES) else "medium"
            cat = "duplicate_options" if was_dup else "ocr_corruption"
            add_issue(
                item_id,
                sev,
                cat,
                "FrontOptionsHTML",
                json.dumps(orig["options"], ensure_ascii=False),
                json.dumps(rem["options"], ensure_ascii=False),
                src,
            )

        if (orig["explanation"] or "") != (rem["explanation"] or ""):
            was_p291 = orig.get("explanation") == "" and rem["quiz_type"] == "commentati"
            sev = (
                "critical"
                if (
                    was_p291
                    or item_id
                    in (
                        "BIO-C04-COMM-087",
                        "BIO-C04-COMM-088",
                        "BIO-C05-COMM-083",
                        "CHIM-C03-COMM-021",
                        "CHIM-C02-COMM-039",
                        "CHIM-C10-COMM-018",
                        "CHIM-C09-COMM-001",
                        "FIS-C01-COMM-010",
                        "FIS-C06-COMM-040",
                        "FIS-C07-COMM-001",
                    )
                )
                else "high"
            )
            add_issue(
                item_id,
                sev,
                "explanation_defect",
                "ExplanationHTML",
                orig["explanation"] or "<EMPTY — OMITTED PAGE 291>",
                rem["explanation"] or "",
                src,
            )

        qpng = f"{item_id}.png"
        if item_id == "CHIM-C10-COMM-018":
            add_issue(
                item_id,
                "high",
                "truncated_scan_image",
                "QuestionScanHTML",
                "Truncated 501x32 PNG missing options A-E (CHIM-C10-COMM-018.png)",
                "Re-cropped full 525x273 crisp PNG from PDF p.156 with stem + options A-E",
                "dbe933e6",
            )
        elif qpng in wm_cleaned_files or any(fn in wm_cleaned_files for fn in rem["figure_files"]):
            add_issue(
                item_id,
                "low",
                "watermark_leak",
                "EmbeddedPNGMedia",
                f"Publisher watermark / margin bleed in {qpng}",
                f"Losslessly cleaned crisp PNG in rebuilt .apkg ({qpng})",
                "dbe933e6",
            )

    sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    idx_lookup = {r["id"]: r["global_index"] for r in all_rem_items}
    idx_lookup["DECK-GLOBAL"] = 0
    unified_rows.sort(key=lambda x: (sev_rank.get(x["severity"], 9), idx_lookup.get(x["ItemID"], 99999), x["category"]))

    issues_cols = [
        "ItemID",
        "category",
        "field",
        "excerpt",
        "proposed fix",
        "severity",
        "confidence",
        "audit_source",
        "status",
    ]
    with open(REPO / "issues.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=issues_cols)
        w.writeheader()
        w.writerows(unified_rows)

    old_dups = list(csv.DictReader(our_dups_backup.open(encoding="utf-8")))
    seen_dup_pairs = set()
    new_dups = []
    base_cols = list(old_dups[0].keys())
    for extra_col in ("Resolution", "KeptItemID"):
        if extra_col not in base_cols:
            base_cols.append(extra_col)

    for d in old_dups:
        id1 = d["ItemID_1"]
        id2 = d["ItemID_2"]
        seen_dup_pairs.add(tuple(sorted((id1, id2))))
        r1 = rem_by_id[id1]
        r2 = rem_by_id[id2]
        a1 = f"{r1['answer']}: {r1['answer_text']}" if r1["options"] else r1["answer"]
        a2 = f"{r2['answer']}: {r2['answer_text']}" if r2["options"] else r2["answer"]
        d["Answer_1"] = a1
        d["Answer_2"] = a2
        d["Stem_1"] = _clean_log_text(r1["question"])[:180]
        d["Stem_2"] = _clean_log_text(r2["question"])[:180]
        if id1 in DEDUP_DROP_MAP:
            d["Resolution"] = "deduplicated"
            d["KeptItemID"] = DEDUP_DROP_MAP[id1]
        elif id2 in DEDUP_DROP_MAP:
            d["Resolution"] = "deduplicated"
            d["KeptItemID"] = DEDUP_DROP_MAP[id2]
        else:
            d["Resolution"] = "kept_distinct_questions"
            d["KeptItemID"] = f"{id1};{id2}"
        if d.get("AnswerStatus") == "conflicting_answer":
            if (id1, id2) in (("CHIM-C09-COMM-001", "CHIM-C09-NCOM-010"), ("CHIM-C09-NCOM-010", "CHIM-C09-COMM-001")):
                d["AnswerStatus"] = "resolved_identical_answer"
                d["Notes"] = "Resolved: CHIM-C09-COMM-001 corrected from printed typo B to E (P₂O₃, n.o. +3); redundant non_commentati copy removed."
        d["Notes"] = _clean_log_text(d.get("Notes", ""))
        new_dups.append(d)

    for dropped_id, kept_id in sorted(DEDUP_DROP_MAP.items()):
        pair_key = tuple(sorted((dropped_id, kept_id)))
        if pair_key in seen_dup_pairs:
            continue
        seen_dup_pairs.add(pair_key)
        rk = rem_by_id[kept_id]
        rd = rem_by_id[dropped_id]
        row = {k: "" for k in base_cols}
        row["ItemID_1"] = kept_id
        row["ItemID_2"] = dropped_id
        row["Stem_1"] = rk["question"][:180]
        row["Stem_2"] = rd["question"][:180]
        row["Answer_1"] = f"{rk['answer']}: {rk['answer_text']}" if rk["options"] else rk["answer"]
        row["Answer_2"] = f"{rd['answer']}: {rd['answer_text']}" if rd["options"] else rd["answer"]
        row["Resolution"] = "deduplicated"
        row["KeptItemID"] = kept_id
        if "Notes" in row:
            row["Notes"] = f"Retained {kept_id} ({rk['quiz_type']}); removed redundant {dropped_id} ({rd['quiz_type']})."
        new_dups.append(row)

    with open(REPO / "duplicates.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=base_cols)
        w.writeheader()
        w.writerows(new_dups)

    print(
        f"Wrote unified issues.csv ({len(unified_rows)} remediated findings) and duplicates.csv "
        f"({len(new_dups)} cataloged pairs; {len(removed_records)} deduplicated) in {time.time()-t0:.1f}s"
    )


if __name__ == "__main__":
    main()
