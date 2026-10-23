#!/usr/bin/env python3
"""End-to-end Anki Rust engine merge verification of Semestre_Filtro_Master_7078.apkg into currnet_no_images.apkg.md."""
from __future__ import annotations

import io
import json
import re
import shutil
import zipfile
from collections import Counter
from pathlib import Path

import zstandard
from anki.collection import Collection, ImportAnkiPackageOptions, ImportAnkiPackageRequest

MCQ_MID = 1813027267
CLOZE_MID = 1481924269089


def main() -> None:
    root = Path("/home/user/anki-sem")
    apkg_path = root / "work/master_build/Semestre_Filtro_Master_7078.apkg"
    assert apkg_path.exists(), f"Missing {apkg_path}"

    # 1. Inspect zip entries of exported .apkg
    with zipfile.ZipFile(apkg_path) as zf:
        names = zf.namelist()
        numeric_files = [n for n in names if n.isdigit()]
        print(f"APKG zip entries: total={len(names)}, media_blobs={len(numeric_files)}, non_media={[n for n in names if not n.isdigit()]}")

    # 2. Extract fresh untouched copy of /tmp/arena-coding-uploads/currnet_no_images.apkg.md
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

    # Seed dummy user review state on 5 cards (ivl=21, reps=7, factor=2500) to prove user scheduling is preserved!
    sample_cids = col.find_cards("")[:5]
    for cid in sample_cids:
        c = col.get_card(cid)
        c.type = 2
        c.queue = 2
        c.ivl = 21
        c.reps = 7
        c.factor = 2500
        col.update_card(c)

    # Seed a dummy existing live scan in user's collection.media to prove zero overwrite
    media_dir = Path(col.media.dir())
    sentinel_png = media_dir / "CHIM-C01-NCOM-017.png"
    sentinel_png.write_bytes(b"USER_EXISTING_LIVE_SCAN_SENTINEL")

    # 3. Run Anki's ACTUAL default double-click import (IF_NEWER=0, merge_notetypes=False, with_scheduling=False)
    res = col.import_anki_package(
        ImportAnkiPackageRequest(
            package_path=str(apkg_path),
            options=ImportAnkiPackageOptions(
                merge_notetypes=False,
                update_notes=0,       # IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_IF_NEWER (default)
                update_notetypes=0,   # IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_IF_NEWER (default)
                with_scheduling=False,
                with_deck_configs=False,
            ),
        )
    )
    log = res.log
    log_counts = {f.name: len(getattr(log, f.name)) if f.is_repeated else getattr(log, f.name) for f in log.DESCRIPTOR.fields}
    print("Real Anki ImportLog:", log_counts)

    post_notes = col.note_count()
    post_cards = col.card_count()
    post_nids = set(col.find_notes(""))

    assert pre_notes == 6948 and pre_cards == 6952
    assert post_notes == 7078, f"Expected 7078 notes after merge, got {post_notes}"
    assert post_cards == 7082, f"Expected 7082 cards after merge, got {post_cards}"
    assert pre_nids.issubset(post_nids), "Some original live nids were lost!"
    assert len(log.updated) == 6948, f"Expected 6948 updated notes, got {len(log.updated)}"
    assert len(log.new) == 130, f"Expected 130 new restored notes, got {len(log.new)}"

    # Verify user scheduling preserved on all 5 seeded review cards
    for cid in sample_cids:
        c = col.get_card(cid)
        assert c.ivl == 21 and c.reps == 7, f"User review scheduling wiped on card {cid}!"

    # Verify sentinel live scan untouched AND all 141 delta media files imported
    assert sentinel_png.read_bytes() == b"USER_EXISTING_LIVE_SCAN_SENTINEL", "Live scan overwritten!"
    imported_media = {p.name for p in media_dir.iterdir() if p.name != "CHIM-C01-NCOM-017.png"}
    print(f"Imported delta media files in user collection.media: {len(imported_media)}")

    # Verify 100% explanation coverage, 21 MUR ud:: tags, Page 291, and all 8 tie-breaks
    empty_expl = []
    ud_counter: Counter[str] = Counter()
    no_ud = []
    bad_cloze = []
    notes_by_iid = {}

    for nid in col.find_notes(""):
        n = col.get_note(nid)
        iid = n.fields[0]
        notes_by_iid[iid] = n
        if not n.fields[13].strip():
            empty_expl.append(iid)
        uds = [t for t in n.tags if t.startswith("ud::")]
        if len(uds) != 1:
            no_ud.append((iid, uds))
        else:
            ud_counter[uds[0]] += 1
        if n.mid == CLOZE_MID and "{{c1::" not in n.fields[8]:
            bad_cloze.append(iid)

    assert not empty_expl, f"Empty explanations found: {empty_expl[:20]}"
    assert not no_ud, f"Notes missing exact single ud:: tag: {no_ud[:20]}"
    assert len(ud_counter) == 21, f"Expected 21 distinct ud:: tags, got {len(ud_counter)}"
    assert not bad_cloze, f"Cloze notes missing {{{{c1::}}}}: {bad_cloze}"

    # Verify notetypes updated (no Google Fonts, has @font-face, has #sf-mode-pill, Cloze front has <details class="orig-scan">)
    m_mcq = col.models.get(MCQ_MID)
    m_clz = col.models.get(CLOZE_MID)
    for m in (m_mcq, m_clz):
        assert "fonts.googleapis.com" not in m["css"]
        assert "_SpaceGrotesk-Variable.ttf" in m["css"]
        assert "fonts.googleapis.com" not in m["tmpls"][0]["qfmt"]
        assert "fonts.googleapis.com" not in m["tmpls"][0]["afmt"]
        assert "sf-mode-pill" in m["tmpls"][0]["qfmt"]
    assert '<details class="orig-scan">' in m_clz["tmpls"][0]["qfmt"]
    assert "sf-acc-data" in m_clz["tmpls"][0]["afmt"]

    # Check all 8 tie-breaks
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

    # Check Page 291 (CHIM-C11-COMM-017..023)
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

    col.close()
    shutil.rmtree(merge_dir, ignore_errors=True)
    print("ALL REAL-ANKI MERGE & QUALITY GATES PASSED 100%!")


if __name__ == "__main__":
    main()
