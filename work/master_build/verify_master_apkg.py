#!/usr/bin/env python3
"""End-to-end Anki Rust engine merge + standalone media + symbol/OCR verification for Semestre_Filtro_Master_7078.apkg."""
from __future__ import annotations

import html
import io
import re
import shutil
import struct
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import zstandard
from anki.collection import Collection, ImportAnkiPackageOptions, ImportAnkiPackageRequest
from extract_delta_media import BOGUS_TEXT_ONLY_FIGURES, CLEAN_RECROP_FIGURES

MCQ_MID = 1813027267
CLOZE_MID = 1481924269089

DETECT_CORRUPTIONS: list[tuple[str, re.Pattern]] = [
    ("chem_comma_sub", re.compile(r"\b(?:H,PO,|H,S0,|H,S\b|S0,|C0,|C0₂|H₂0\b|CH,,0,|Al,O,|Hg,Cl,|2H,0|FADH,|NADH₄|K,0\b|250,\s*=|\(NH,C1\)|\(NH\.,?\)|CH,CHO|CH,OCH,|H,COCH,)")),
    ("zero_for_O", re.compile(r"\b(?:Na0H|K0H|H202|H2C03|CH₃C00|R-C0-0|Hg₂0|H₄P₂0₇)\b|\(CH₃CH₂\)₂0")),
    ("ion_garble", re.compile(r"(?:OH[”\"]|\[OH\]|H30[°*]|Ca\*\*|Ca⁴⁺|Ca²⁴|Fe³⁺⁺|Rh[”\"]|ZH’|Ze⁻|\b2\s*e°)")),
    ("greek_garble", re.compile(r"\b(?:DNA polimerasi [6è]|Tubulina y|y-tubulina|Actina [8B]|Importina a|Subunità [aB]|Fattore p|p-dipendente|B-ossidazione|070|NFxB|a5ft1|integrina af|integrine a,8)\b")),
    ("roman_Il", re.compile(r"\b(?:Complesso|polimerasi|pol|Topoisomerasi|profase|metafase|anafase|telofase|meiosi|meiotica|Anafase|Profase|Metafase|Telofase)\s+Il\b")),
    ("svedberg_garble", re.compile(r"(?:5,85|\brRNA (?:55|185|165)\b|23\$|\bfase \$|\bfase GO\b|\bin GO\b|\bda GO\b|fasi G,,|G1,5,\s*M)")),
    ("solo_garble", re.compile(r"\b(?:Solole\d|Solo le\d|Solol\s*e|Salo\s*[12l]|Salo\s+per|Salo\s+la|\bla disposta\b|\bmoti di\b|\bdelia\b)")),
    ("unit_garble", re.compile(r"(?:g/cm[’']|\bohmmetro\b|mol-!|10!°|10s\"!|\bns\"!|\bparia1\b|\bparial\b|m/sin\d)")),
    ("bleed_garble", re.compile(r"(?:SS\s*255|os\s*PZ|acs\s*OZ|uss\s*PP|PAR\s*cs|css\.\s*JP)")),
    ("cloze_init_garble", re.compile(r"(?:^LV\s+\{\{c1|^\[GPCR|^IRTK|^LAPC/C|^GHioni|reticolo\)?\}\}\s+fonico|\bAuoruro\b|«dipendente)")),
    ("thermo_A", re.compile(r"\b(?:AG|AH|AS|AK)\s*(?:[<>]|=\s*0)|\bAG°")),
]


def main() -> None:
    root = Path("/home/user/anki-sem")
    apkg_path = root / "work/master_build/Semestre_Filtro_Master_7078.apkg"
    assert apkg_path.exists(), f"Missing {apkg_path}"
    size_mb = apkg_path.stat().st_size / (1024 * 1024)
    print(f"Checking {apkg_path.name} ({size_mb:.2f} MB)...")

    # 1. Inspect zip entries of exported .apkg
    with zipfile.ZipFile(apkg_path) as zf:
        names = zf.namelist()
        numeric_files = [n for n in names if n.isdigit()]
        non_media = [n for n in names if not n.isdigit()]
        print(f"APKG zip entries: total={len(names)}, media_blobs={len(numeric_files)}, non_media={non_media}")
        assert len(numeric_files) == 8234, f"Expected 8234 bundled media blobs, got {len(numeric_files)}"

    # 2. Real Anki Merge Test into untouched /tmp/arena-coding-uploads/currnet_no_images.apkg.md
    merge_dir = root / "work/.cache/real_anki_merge_test"
    shutil.rmtree(merge_dir, ignore_errors=True)
    merge_dir.mkdir(parents=True, exist_ok=True)
    target_db = merge_dir / "user_live.anki2"

    with zipfile.ZipFile("/tmp/arena-coding-uploads/currnet_no_images.apkg.md") as zf:
        with zstandard.ZstdDecompressor().stream_reader(io.BytesIO(zf.read("collection.anki21b"))) as sr:
            target_db.write_bytes(sr.read())

    col = Collection(str(target_db))
    pre_notes = col.note_count()
    pre_cards = col.card_count()
    pre_nids = set(col.find_notes(""))

    # Seed user review state on 5 cards (ivl=21, reps=7, factor=2500) to prove scheduling preservation
    sample_cids = col.find_cards("")[:5]
    for cid in sample_cids:
        c = col.get_card(cid)
        c.type = 2
        c.queue = 2
        c.ivl = 21
        c.reps = 7
        c.factor = 2500
        col.update_card(c)

    # Pre-seed an authentic live scan from audit/media to prove zero SHA-1 collision / zero hash-renaming
    media_dir = Path(col.media.dir())
    real_live_png = subprocess.check_output(
        ["git", "show", "origin/import/full-anki-folder:audit/media/BIO-C01-COMM-001.png"]
    )
    (media_dir / "BIO-C01-COMM-001.png").write_bytes(real_live_png)

    res = col.import_anki_package(
        ImportAnkiPackageRequest(
            package_path=str(apkg_path),
            options=ImportAnkiPackageOptions(
                merge_notetypes=False,
                update_notes=0,       # IF_NEWER (Anki default)
                update_notetypes=0,   # IF_NEWER (Anki default)
                with_scheduling=False,
                with_deck_configs=False,
            ),
        )
    )
    log = res.log
    log_counts = {
        f.name: len(getattr(log, f.name)) if f.is_repeated else getattr(log, f.name)
        for f in log.DESCRIPTOR.fields
    }
    print("Real Anki Merge ImportLog:", log_counts)

    assert pre_notes == 6948 and pre_cards == 6952
    assert col.note_count() == 7078, f"Expected 7078 notes after merge, got {col.note_count()}"
    assert col.card_count() == 7082, f"Expected 7082 cards after merge, got {col.card_count()}"
    assert pre_nids.issubset(set(col.find_notes(""))), "Some original live nids were lost!"
    assert len(log.updated) == 6948, f"Expected 6948 updated notes, got {len(log.updated)}"
    assert len(log.new) == 130, f"Expected 130 new restored notes, got {len(log.new)}"
    assert len(log.duplicate) == 0 and len(log.conflicting) == 0

    for cid in sample_cids:
        c = col.get_card(cid)
        assert c.ivl == 21 and c.reps == 7, f"User review scheduling wiped on card {cid}!"

    merged_media = {p.name for p in media_dir.iterdir() if p.is_file()}
    assert len(merged_media) == 8234, f"Expected 8234 media files without hash-renaming duplicates, got {len(merged_media)}"
    assert (media_dir / "BIO-C01-COMM-001.png").read_bytes() == real_live_png
    col.close()
    shutil.rmtree(merge_dir, ignore_errors=True)

    # 3. Fresh-Profile Standalone Import + Full Media, Entity, Figure, Tag & Symbol Audit
    fresh_dir = root / "work/.cache/real_anki_fresh_test"
    shutil.rmtree(fresh_dir, ignore_errors=True)
    fresh_dir.mkdir(parents=True, exist_ok=True)
    fresh_db = fresh_dir / "fresh.anki2"

    fcol = Collection(str(fresh_db))
    fres = fcol.import_anki_package(
        ImportAnkiPackageRequest(
            package_path=str(apkg_path),
            options=ImportAnkiPackageOptions(with_scheduling=False, with_deck_configs=False),
        )
    )
    assert fcol.note_count() == 7078 and fcol.card_count() == 7082
    assert len(fres.log.new) == 7078

    fmedia_dir = Path(fcol.media.dir())
    fmedia_files = {p.name: p for p in fmedia_dir.iterdir() if p.is_file()}
    assert len(fmedia_files) == 8234, f"Expected 8234 standalone media files, got {len(fmedia_files)}"

    # Verify every PNG file has valid PNG signature & positive dimensions, and all 4 offline fonts exist
    for font_name in ("_SpaceGrotesk-Variable.ttf", "_SpaceMono-Regular.ttf", "_SpaceMono-Bold.ttf", "_Syne-Variable.ttf"):
        assert font_name in fmedia_files and fmedia_files[font_name].stat().st_size > 10000, f"Missing font {font_name}"

    png_count = 0
    for name, p in fmedia_files.items():
        if name.endswith(".png"):
            png_count += 1
            b = p.read_bytes()
            assert len(b) >= 24 and b[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG header: {name}"
            w, h = struct.unpack(">II", b[16:24])
            assert w > 0 and h > 0, f"Zero-dimension PNG: {name} ({w}x{h})"
    assert png_count == 8230, f"Expected 8230 PNGs, got {png_count}"

    # Audit all 7,078 notes
    empty_expl = []
    ud_counter: Counter[str] = Counter()
    no_ud = []
    bad_cloze = []
    double_escaped = []
    missing_imgs = []
    bogus_figs_left = []
    uncropped_figs_left = []
    fig_tag_mismatch = []
    detect_hits = []
    unique_referenced_pngs: set[str] = set()
    total_img_refs = 0
    notes_by_iid = {}

    for nid in fcol.find_notes(""):
        n = fcol.get_note(nid)
        iid = n.fields[0]
        notes_by_iid[iid] = n

        if not n.fields[13].strip():
            empty_expl.append(iid)

        uds = [t for t in n.tags if t.startswith("ud::")]
        if len(uds) != 1:
            no_ud.append((iid, uds))
        else:
            ud_counter[uds[0]] += 1

        if n.mid == CLOZE_MID:
            if "{{c1::" not in n.fields[8]:
                bad_cloze.append(iid)
            if "{{c1::" in n.fields[9] or '<span class="blank-filled">' not in n.fields[9]:
                bad_cloze.append(f"{iid}:bad_back_stem")

        for idx, val in enumerate(n.fields):
            if re.search(r"&amp;(?:lt|gt|amp|quot|#\d+|#x[0-9a-fA-F]+);", val):
                double_escaped.append((iid, idx, val[:100]))

        has_fig = bool(n.fields[14].strip())
        has_cf_tag = "con_figura" in n.tags
        if has_fig != has_cf_tag:
            fig_tag_mismatch.append((iid, n.fields[14], n.tags))

        for src in re.findall(r'src="([^"]+)"', n.fields[14]):
            if src in BOGUS_TEXT_ONLY_FIGURES:
                bogus_figs_left.append((iid, src))
            if src in CLEAN_RECROP_FIGURES:
                uncropped_figs_left.append((iid, src))

        for idx in (14, 15, 16):
            for src in re.findall(r'src="([^"]+)"', n.fields[idx]):
                total_img_refs += 1
                unique_referenced_pngs.add(src)
                if src not in fmedia_files:
                    missing_imgs.append((iid, idx, src))

        plain_text = " || ".join(
            html.unescape(re.sub(r"<[^>]+>", " ", n.fields[i])) for i in (8, 9, 10, 12, 13)
        )
        for rule_name, pat in DETECT_CORRUPTIONS:
            m = pat.search(plain_text)
            if m:
                detect_hits.append((iid, rule_name, m.group(0)))

    assert not empty_expl, f"Empty explanations: {empty_expl[:20]}"
    assert not no_ud, f"Notes without exact single ud:: tag: {no_ud[:20]}"
    assert len(ud_counter) == 21, f"Expected 21 MUR ud:: tags, got {len(ud_counter)}"
    assert not bad_cloze, f"Malformed Cloze notes: {bad_cloze[:20]}"
    assert not double_escaped, f"Double-escaped HTML entities found: {double_escaped[:20]}"
    assert not fig_tag_mismatch, f"FigureHTML vs con_figura tag mismatch: {fig_tag_mismatch[:20]}"
    assert not bogus_figs_left, f"Bogus text-only FigureHTML crops left: {bogus_figs_left}"
    assert not uncropped_figs_left, f"Un-upgraded figure crops left: {uncropped_figs_left}"
    assert not missing_imgs, f"Missing <img src> files: {missing_imgs[:20]}"
    assert total_img_refs == 8230 and len(unique_referenced_pngs) == 8230, (
        f"Expected 8230 total & unique PNG refs, got total={total_img_refs}, unique={len(unique_referenced_pngs)}"
    )
    assert not detect_hits, f"Residual OCR/symbol corruptions detected: {detect_hits[:30]}"

    # Spot-check key remediated items (double-escape Cloze <7/>7, 10^15 superscript, scan-verified options, errata notes)
    assert "Risposta corretta: &lt;7<" in notes_by_iid["CHIM-C11-COMP-028"].fields[12]
    assert "Risposta corretta: &gt;7<" in notes_by_iid["CHIM-C11-COMP-030"].fields[12]
    assert "10<sup>{{c1::15}}</sup>" in notes_by_iid["FIS-C01-COMP-019"].fields[8]
    assert '10<sup><span class="blank-filled">15</span></sup>' in notes_by_iid["FIS-C01-COMP-019"].fields[9]
    assert '<div class="note-box">' in notes_by_iid["CHIM-C11-NCOM-057"].fields[13]
    assert "concentrazione di H⁺ aumenta" in notes_by_iid["CHIM-C11-NCOM-057"].fields[10]

    # Verify notetypes updated (no Google Fonts, has @font-face, has #sf-mode-pill, Cloze front has <details class="orig-scan">)
    m_mcq = fcol.models.get(MCQ_MID)
    m_clz = fcol.models.get(CLOZE_MID)
    for m in (m_mcq, m_clz):
        assert "fonts.googleapis.com" not in m["css"]
        assert "_SpaceGrotesk-Variable.ttf" in m["css"]
        assert "fonts.googleapis.com" not in m["tmpls"][0]["qfmt"]
        assert "fonts.googleapis.com" not in m["tmpls"][0]["afmt"]
        assert "sf-mode-pill" in m["tmpls"][0]["qfmt"]
    assert '<details class="orig-scan">' in m_clz["tmpls"][0]["qfmt"]
    assert "sf-acc-data" in m_clz["tmpls"][0]["afmt"]

    # Check all 8 tie-breaks & Page 291 (CHIM-C11-COMM-017..023)
    expected_ties = {
        "CHIM-C06-NCOM-088": "Risposta corretta: E.",
        "CHIM-C11-NCOM-019": "Risposta corretta: B.",
        "CHIM-C13-NCOM-104": "Risposta corretta: C.",
        "BIO-C01-NCOM-216": "Risposta corretta: A.",
        "BIO-C02-COMP-016": "Risposta corretta: interfasici",
        "BIO-C04-COMM-014": "Risposta corretta: A.",
        "BIO-C04-NCOM-204": "Risposta corretta: C.",
        "FIS-C03-NCOM-185": "Risposta corretta: C.",
    }
    for tid, prefix in expected_ties.items():
        banner = notes_by_iid[tid].fields[12]
        assert banner.startswith(prefix), f"Tie-break mismatch on {tid}: {banner}"

    expected_p291 = {
        "CHIM-C11-COMM-017": "Risposta corretta: C.",
        "CHIM-C11-COMM-018": "Risposta corretta: D.",
        "CHIM-C11-COMM-019": "Risposta corretta: C.",
        "CHIM-C11-COMM-020": "Risposta corretta: A.",
        "CHIM-C11-COMM-021": "Risposta corretta: E.",
        "CHIM-C11-COMM-022": "Risposta corretta: A.",
        "CHIM-C11-COMM-023": "Risposta corretta: B.",
    }
    for pid, prefix in expected_p291.items():
        n = notes_by_iid[pid]
        assert n.fields[12].startswith(prefix), f"Page 291 mismatch on {pid}: {n.fields[12]}"
        assert len(n.fields[13].strip()) > 60, f"Page 291 missing explanation on {pid}"
        assert "0₂" not in n.fields[10], f"Unfixed 0₂ on {pid}"

    fcol.close()
    shutil.rmtree(fresh_dir, ignore_errors=True)
    print(
        "ALL STANDALONE MEDIA (8,234/8,234), PNG INTEGRITY (8,230/8,230), HTML ENTITY, "
        "SYMBOL/OCR, AND REAL-ANKI MERGE GATES PASSED 100%!"
    )


if __name__ == "__main__":
    main()
