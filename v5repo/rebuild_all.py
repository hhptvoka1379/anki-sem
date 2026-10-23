#!/usr/bin/env python3
"""
Master End-to-End Self-Contained Dataset Remediation, Deduplication, Anki .apkg Builder,
Theme Packager & Audit Exporter (zero `/tmp` dependency — runs cleanly from repo state).

Produces:
  - output/figures/*.png (cleaned & tightly cropped 79 genuine diagrams)
  - output/qa_dataset.jsonl
  - output/qa_dataset.json
  - output/qa_dataset.csv
  - output/Semestre_Filtro_Complete.apkg
  - output/themes/css/01..10.css
  - output/themes/templates/{master_complete,00_default,01..10}/{front.html,back.html,style.css}
  - output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg
  - output/themes/ThemeUpdater_01..10.apkg
  - issues.csv & duplicates.csv
"""
from __future__ import annotations

import csv
import html
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import zipfile as _zf
from pathlib import Path

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

import genanki
from extractor.anki_themes import (
    THEMES,
    build_card_templates,
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
from extractor.round3_remediation import clean_figures_on_disk
from extractor.stage4_export import (
    ANKI_CSS,
    BACK_TMPL,
    FRONT_TMPL,
    KIND_ORDER,
    SUBJECT_TAG_SLUG,
    format_back_stem_html,
    format_explanation_html,
    format_front_stem_html,
    format_inline_html,
    stable_anki_id,
)

MODEL_ID = 1134323214
BASE_MAIN_COMMIT = "e652f27"
PUB_RE = re.compile(r"vaedi[s]es|@di[s]es|edi[s]es", re.IGNORECASE)


def _clean_log_text(s: str) -> str:
    return PUB_RE.sub("publisher", s or "")


def _load_baseline_items(out_dir: Path) -> list[dict]:
    """Load pre-dedup raw baseline items from git object store when available so `issues.csv`
    & `duplicates.csv` capture the complete historical delta; fall back to `output/qa_dataset.json`."""
    try:
        raw = subprocess.check_output(
            ["git", "show", f"{BASE_MAIN_COMMIT}:output/qa_dataset.json"],
            cwd=str(REPO),
            stderr=subprocess.DEVNULL,
        )
        return json.loads(raw.decode("utf-8"))["items"]
    except Exception:
        return json.loads((out_dir / "qa_dataset.json").read_text(encoding="utf-8"))["items"]


def main() -> None:
    t0 = time.time()
    out_dir = REPO / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    apkg_complete = out_dir / "Semestre_Filtro_Complete.apkg"

    with tempfile.TemporaryDirectory() as work_tmp:
        clean_media = Path(work_tmp) / "media"
        clean_media.mkdir(parents=True, exist_ok=True)
        ref_sqlite = Path(work_tmp) / "collection.anki2"

        # Hydrate all scan PNGs + solution scan HTML straight from existing `Semestre_Filtro_Complete.apkg`
        with _zf.ZipFile(apkg_complete, "r") as zin:
            media_map = json.loads(zin.read("media").decode("utf-8"))
            ref_sqlite.write_bytes(zin.read("collection.anki2"))
            for zkey, fname in media_map.items():
                if zkey in zin.namelist():
                    (clean_media / fname).write_bytes(zin.read(zkey))

        # Clean bogus text-only figures and apply exact y-band crops cleanly & idempotently
        fig_stats = clean_figures_on_disk(fig_dir, clean_media)
        for fp in fig_dir.glob("*.png"):
            shutil.copy2(fp, clean_media / fp.name)
        print("Figure remediation stats:", fig_stats)

        conn_ref = sqlite3.connect(str(ref_sqlite))
        sol_html_by_id = {}
        for (flds_raw,) in conn_ref.execute("SELECT flds FROM notes"):
            parts = flds_raw.split("\x1f")
            sol_html_by_id[parts[0]] = parts[16]
        conn_ref.close()

        orig_items = _load_baseline_items(out_dir)
        orig_by_id = {it["id"]: it for it in orig_items}

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
                {"name": "QuestionType_Unused" if False else "QuizTypeLabel"},
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
                    ov_esc = format_inline_html(options[k])
                    f_opts.append(f'<div class="opt"><span class="opt-letter">{k}</span><span class="opt-body">{ov_esc}</span></div>')
                    cls = "opt correct" if k == ans_val else "opt"
                    b_opts.append(f'<div class="{cls}"><span class="opt-letter">{k}</span><span class="opt-body">{ov_esc}</span></div>')
                f_opts.append("</div>")
                b_opts.append("</div>")
                front_opts_html = "\n".join(f_opts)
                back_opts_html = "\n".join(b_opts)
                ans_banner_html = f"Risposta corretta: {html.escape(ans_val, quote=False)}. {format_inline_html(correct_option_text)}"
            else:
                front_opts_html = ""
                back_opts_html = ""
                ans_banner_html = f"Risposta corretta: {format_inline_html(ans_val)}"

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
                    format_explanation_html(expl_clean),
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
                    "pre_dedup_source_items": 7078,
                    "duplicates_removed": len(DEDUP_DROP_MAP),
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
        #    Theme #04 full .apkg, all 10 ThemeUpdater_*.apkg)
        themes_dir = out_dir / "themes"
        css_dir = themes_dir / "css"
        tpl_root = themes_dir / "templates"
        css_dir.mkdir(parents=True, exist_ok=True)
        tpl_root.mkdir(parents=True, exist_ok=True)

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
        print(f"Wrote all 10 ThemeUpdaters + 12 template bundles + standalone CSS ({time.time()-t0:.1f}s)")

        # 4. Build unified, ground-truth-verified issues.csv & updated duplicates.csv
        existing_issues_path = REPO / "issues.csv"
        our_old_issues = (
            list(csv.DictReader(existing_issues_path.open(encoding="utf-8")))
            if existing_issues_path.exists()
            else []
        )
        our_ids_map = {}
        for row in our_old_issues:
            kid = row.get("ItemID") or row.get("item_id") or row.get("id")
            our_ids_map.setdefault(kid, []).append(row)

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
            "Anki Package + Note-Type + Subdecks + Deduplication + Figure Clean",
            "answer_book_page=291 on 7,078 items; publisher name in filename/deck/model/CSS; 130 duplicates; 34 text-duplicate figures; inline scan disclosure collision",
            "Renamed to Semestre_Filtro_Complete.apkg with neutral deck/model titles; restored exact Risposte pages (252..901); deduplicated 7,078 -> 6,948 unique cards; cleaned 113 -> 79 diagrams; stacked .scan-stack accordions & multi-line bullets across all 12 themes",
            "dbe933e6",
        )

        rem_by_id = {r["id"]: r for r in all_rem_items}
        for item_id, orig in orig_by_id.items():
            rem = rem_by_id[item_id]
            prev_src = our_ids_map[item_id][0].get("audit_source", "dbe933e6") if item_id in our_ids_map else "round3_scan_verified"

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
                    prev_src,
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
                add_issue(item_id, sev, cat, "FrontStemHTML", orig["question"], rem["question"], prev_src)

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
                    prev_src,
                )

            if (orig["explanation"] or "") != (rem["explanation"] or ""):
                was_p291 = orig.get("explanation") == "" and rem["quiz_type"] == "commentati"
                sev = "critical" if was_p291 else "high"
                add_issue(
                    item_id,
                    sev,
                    "explanation_defect",
                    "ExplanationHTML",
                    orig["explanation"] or "<EMPTY — OMITTED PAGE 291>",
                    rem["explanation"] or "",
                    prev_src,
                )

            if orig.get("figure_files") != rem.get("figure_files"):
                add_issue(
                    item_id,
                    "medium",
                    "bogus_duplicate_text_figure_removed",
                    "FigureHTML",
                    json.dumps(orig.get("figure_files"), ensure_ascii=False),
                    json.dumps(rem.get("figure_files"), ensure_ascii=False),
                    "round3_scan_verified",
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

        old_dups = list(csv.DictReader((REPO / "duplicates.csv").open(encoding="utf-8")))
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
            r1 = rem_by_id.get(id1) or rem_by_id[DEDUP_DROP_MAP[id1]]
            r2 = rem_by_id.get(id2) or rem_by_id[DEDUP_DROP_MAP[id2]]
            d["Answer_1"] = f"{r1['answer']}: {r1['answer_text']}" if r1["options"] else r1["answer"]
            d["Answer_2"] = f"{r2['answer']}: {r2['answer_text']}" if r2["options"] else r2["answer"]
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
            d["Notes"] = _clean_log_text(d.get("Notes", ""))
            new_dups.append(d)

        with open(REPO / "duplicates.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=base_cols)
            w.writeheader()
            w.writerows(new_dups)

        write_live_html_showcases(out_dir)

        print(
            f"Wrote unified issues.csv ({len(unified_rows)} remediated findings) and duplicates.csv "
            f"({len(new_dups)} cataloged pairs) in {time.time()-t0:.1f}s"
        )


def write_live_html_showcases(out_dir: Path) -> None:
    """Keep both root `index.html` and `output/themes/theme_showcase.html` 100% synced
    with the live rebuilt `.apkg` models, CSS, and clean Round-3 cards."""
    import base64
    import sqlite3
    import zipfile

    master_apkg = out_dir / "Semestre_Filtro_Complete.apkg"
    riso_apkg = out_dir / "themes" / "Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg"
    showcase_ids = [
        "CHIM-C01-COMM-002",
        "FIS-C06-COMM-034",
        "FIS-C06-COMM-031",
        "CHIM-C01-NCOM-033",
        "BIO-C01-COMM-034",
        "BIO-C06-COMP-095",
    ]
    field_names = [
        "ItemID", "Subject", "SubjectCode", "ChapterNum", "ChapterTitle",
        "QuizTypeLabel", "QuestionNum", "BookPage", "FrontStemHTML", "BackStemHTML",
        "FrontOptionsHTML", "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML",
        "FigureHTML", "QuestionScanHTML", "SolutionScanHTML",
    ]

    def _load_bundle(apkg_path: Path):
        with zipfile.ZipFile(apkg_path, "r") as zf, tempfile.TemporaryDirectory() as td:
            zf.extract("collection.anki2", td)
            media_map = json.loads(zf.read("media").decode("utf-8"))
            rev_media = {fname: zkey for zkey, fname in media_map.items()}
            conn = sqlite3.connect(str(Path(td) / "collection.anki2"))
            models = json.loads(conn.execute("SELECT models FROM col").fetchone()[0])
            mobj = next(iter(models.values()))
            notes = {}
            for (flds_str,) in conn.execute("SELECT flds FROM notes"):
                parts = flds_str.split("\x1f")
                if parts[0] in showcase_ids:
                    notes[parts[0]] = parts
            conn.close()

            def _inline_imgs(html_frag: str) -> str:
                def _rep(m):
                    fn = m.group(1)
                    zk = rev_media[fn]
                    b64 = base64.b64encode(zf.read(zk)).decode("ascii")
                    return f'<img src="data:image/png;base64,{b64}">'

                return re.sub(r'<img src="([^"]+)">', _rep, html_frag)

            cards = []
            for cid in showcase_ids:
                parts = notes[cid]
                d = dict(zip(field_names, parts))
                for k in ("FigureHTML", "QuestionScanHTML", "SolutionScanHTML"):
                    d[k] = _inline_imgs(d[k])
                cards.append(d)

            return {
                "name": mobj["name"],
                "css": mobj["css"],
                "qfmt": mobj["tmpls"][0]["qfmt"],
                "afmt": mobj["tmpls"][0]["afmt"],
            }, cards

    master_bundle, showcase_cards = _load_bundle(master_apkg)
    riso_bundle, _ = _load_bundle(riso_apkg)
    data_json = json.dumps(
        {"master": master_bundle, "riso": riso_bundle, "cards": showcase_cards},
        ensure_ascii=False,
    ).replace("</script>", "<\\/script>")

    root_html = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Semestre Filtro — Live Anki .apkg Reviewer Simulator</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; background: #0b1120; color: #f8fafc; }}
  .topbar {{
    display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between;
    padding: 12px 18px; background: #111827; border-bottom: 1px solid #1f2937;
  }}
  .btn-group {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }}
  button {{
    border: 1px solid #374151; background: #1f2937; color: #e5e7eb; padding: 7px 12px;
    border-radius: 8px; font-size: 12.5px; font-weight: 600; cursor: pointer;
  }}
  button.active {{ background: #facc15; color: #111111; border-color: #facc15; font-weight: 800; }}
  .hint {{ font-size: 12px; color: #9ca3af; padding: 8px 18px; background: #0f172a; border-bottom: 1px solid #1e293b; }}
  iframe {{ width: 100%; height: calc(100vh - 96px); border: none; background: #fff; display: block; }}
  a.sc-link {{ color: #fde047; font-size: 12px; font-weight: 700; text-decoration: none; padding: 6px 10px; border: 1px solid #854d0e; border-radius: 8px; }}
</style>
</head>
<body>
<div class="topbar">
  <div class="btn-group">
    <button id="deck-riso" class="active" onclick="setDeck('riso')">04_NeoBrutalist_Risoprint_Zine.apkg (Standalone v5)</button>
    <button id="deck-master" onclick="setDeck('master')">Semestre_Filtro_Complete.apkg (00–10 Corner Switcher)</button>
    <a class="sc-link" href="/output/themes/theme_showcase.html" target="_blank">Open 10-Theme Showcase ↗</a>
  </div>
  <div class="btn-group">
    <button id="side-front" class="active" onclick="setSide('front')">Fronte (Domanda)</button>
    <button id="side-back" onclick="setSide('back')">Retro (Soluzione)</button>
    <button id="next-card-btn" onclick="nextCard()">Prossima Carta (1/6)</button>
    <button id="anki-dark" class="active" onclick="toggleNight()">Anki Host Chrome: Dark Mode ON</button>
  </div>
</div>
<div class="hint" id="status-bar"></div>
<iframe id="card-frame"></iframe>
<script>
const DATA = {data_json};
let curDeck = 'riso';
let curSide = 'front';
let cardIdx = 0;
let night = true;

function renderTemplate(tpl, fields) {{
  let out = tpl.replace(/\\{{\\{{#(\\w+)\\}}\\}}([\\s\\S]*?)\\{{\\{{\\/\\1\\}}\\}}/g, (_, k, inner) => fields[k] ? inner : '');
  out = out.replace(/\\{{\\{{(\\w+)\\}}\\}}/g, (_, k) => (fields[k] !== undefined ? fields[k] : ''));
  return out;
}}

function refresh() {{
  const d = DATA[curDeck];
  const c = DATA.cards[cardIdx];
  const bodyHtml = renderTemplate(curSide === 'front' ? d.qfmt : d.afmt, c);
  const frame = document.getElementById('card-frame');
  const cls = night ? 'card card1 isMac nightMode night_mode' : 'card card1 isMac';
  frame.srcdoc = '<!doctype html><html><head><meta charset="utf-8"><style>' + d.css + '</style></head><body class="' + cls + '"><div id="qa">' + bodyHtml + '</div></body></html>';
  document.getElementById('status-bar').textContent =
    (curDeck === 'master'
      ? 'Deck attivo: output/Semestre_Filtro_Complete.apkg — clicca il numerino in alto a destra (00..10) per cambiare tema in tempo reale!'
      : 'Deck attivo: output/themes/Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg — standalone v5 con toggle DARK/LIGHT e accordions impilati!') +
    '  •  Carta (' + (cardIdx + 1) + '/' + DATA.cards.length + '): ' + c.ItemID;
}}

function setDeck(k) {{
  curDeck = k;
  document.getElementById('deck-master').classList.toggle('active', k === 'master');
  document.getElementById('deck-riso').classList.toggle('active', k === 'riso');
  refresh();
}}
function setSide(s) {{
  curSide = s;
  document.getElementById('side-front').classList.toggle('active', s === 'front');
  document.getElementById('side-back').classList.toggle('active', s === 'back');
  refresh();
}}
function nextCard() {{
  cardIdx = (cardIdx + 1) % DATA.cards.length;
  document.getElementById('next-card-btn').textContent = 'Prossima Carta (' + (cardIdx + 1) + '/' + DATA.cards.length + ')';
  refresh();
}}
function toggleNight() {{
  night = !night;
  const b = document.getElementById('anki-dark');
  b.classList.toggle('active', night);
  b.textContent = night ? 'Anki Host Chrome: Dark Mode ON' : 'Anki Host Chrome: Light Mode';
  refresh();
}}
refresh();
</script>
</body>
</html>
"""
    (REPO / "index.html").write_text(root_html, encoding="utf-8")

    # Sync output/themes/theme_showcase.html with live templates, CSS, dark toggle, and clean Round-3 cards
    themes_payload = []
    for k, t in THEMES.items():
        q_full, a_full = build_card_templates(theme_key=k)
        # Strip inline <script> blocks for ShadowDOM gallery mounting
        q_clean = re.sub(r"<script>[\s\S]*?</script>", "", q_full)
        a_clean = re.sub(r"<script>[\s\S]*?</script>", "", a_full)
        safe = re.sub(r"[^A-Za-z0-9]+", "_", t["name"]).strip("_")
        themes_payload.append({
            "key": k,
            "num": t["num"],
            "name": t["name"],
            "tagline": t.get("tagline", ""),
            "accent": t.get("accent", "#facc15"),
            "defaultDark": bool(t.get("default_dark")),
            "css": t["css"],
            "qfmt": q_clean,
            "afmt": a_clean,
            "fullApkg": "Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg" if k == "04_neobrutalist_bauhaus" else None,
            "updaterApkg": f"ThemeUpdater_{t['num']}_{safe}.apkg",
        })

    cards_payload = []
    for c in showcase_cards:
        m = re.search(r"Risposta corretta:\s*([A-E])", c["AnswerBannerHTML"])
        ans = m.group(1) if m else c["AnswerBannerHTML"].split(":", 1)[-1].strip()
        cards_payload.append({
            "id": c["ItemID"],
            "ans": ans,
            "label": f"{c['ItemID']} • {c['QuizTypeLabel']} #{c['QuestionNum']}",
            "fields": c,
        })

    sc_html = (out_dir / "themes" / "theme_showcase.html").read_text(encoding="utf-8")
    sc_html = re.sub(
        r"const THEMES = \[[\s\S]*?\];\nconst CARDS = \[[\s\S]*?\];",
        "const THEMES = "
        + json.dumps(themes_payload, ensure_ascii=False).replace("</script>", "<\\/script>")
        + ";\nconst CARDS = "
        + json.dumps(cards_payload, ensure_ascii=False).replace("</script>", "<\\/script>")
        + ";",
        sc_html,
        count=1,
    )
    if 'const cv = sr.querySelector(".sf-canvas")' not in sc_html:
        sc_html = sc_html.replace(
            """sr.innerHTML = `<style>:host{display:block;}${th.css}</style><div class="${useDark ? 'card nightMode' : 'card'}">${htmlBody}</div>`;""",
            """sr.innerHTML = `<style>:host{display:block;}${th.css}</style><div class="${useDark ? 'card nightMode' : 'card'}">${htmlBody}</div>`;
  const cv = sr.querySelector(".sf-canvas");
  const tb = sr.querySelector("#sf-theme-toggle");
  const applyDark = (d) => {
    if (cv) cv.classList.toggle("sf-dark", d);
    if (tb) {
      tb.textContent = d ? "LIGHT" : "DARK";
      tb.style.background = d ? "#18181b" : "#fef08a";
      tb.style.color = d ? "#fafafa" : "#111";
      tb.style.borderColor = d ? "#fafafa" : "#111";
    }
  };
  applyDark(useDark);
  if (tb && cv) {
    tb.addEventListener("click", () => applyDark(!cv.classList.contains("sf-dark")));
  }""",
        )
    (out_dir / "themes" / "theme_showcase.html").write_text(sc_html, encoding="utf-8")


if __name__ == "__main__":
    main()
