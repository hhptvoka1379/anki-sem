#!/usr/bin/env python3
"""Build chunk-by-chunk handoff dataset (<=45 cards/chunk, 196 chunks, 7,078 items) merging:
1. Exact live Anki identity & templates from currnet_no_images.apkg.md (6,948 notes / 6,952 cards,
   notetypes 1813027267 [MCQ] & 1481924269089 [Cloze], 117 deck IDs, random Anki GUIDs)
2. Full 7,078-item corpus from origin/arena/6d93039e-anki-sem (restoring the 130 deduplicated items)
3. Remediated 6,948-item corpus, issues.csv (1,764 fixes), and duplicates.csv (375 pairs) from origin/arena/dbe933e6-anki-sem
4. Uncommented explanations & flags from arena/cc130265-anki-sem (4,905 done / 997 flagged) and arena/0c53ca03-anki-sem (5,464 done / 438 flagged)
5. 257-item answer-key adjudications from arena/9d2e065b-anki-sem & arena/0c0900a2-anki-sem (including Page 291 CHIM-C11-COMM-017..023)
6. CHIM-C01 Opus pilot verification/adjudications/corrections & MUR 2026 ud:: tags from origin/opus-rebuild/semestre-filtro
"""
from __future__ import annotations

import csv
import ctypes
import ctypes.util
import hashlib
import io
import json
import sqlite3
import subprocess
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path("/home/user/anki-sem")
OUT = ROOT / "work" / "opus_handoff"
APKG_UPLOAD = Path("/tmp/arena-coding-uploads/currnet_no_images.apkg.md")
CHUNK_SIZE = 45

BASE91_ANKI = list(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    "!#$%&()*+,-./:;<=>?@[]^_`{|}~"
)

UD_MAP = {
    ("CHIM", 1): "chim-struttura-atomo",
    ("CHIM", 2): "chim-struttura-atomo",
    ("CHIM", 3): "chim-struttura-atomo",
    ("CHIM", 4): "chim-struttura-atomo",
    ("CHIM", 5): "chim-struttura-atomo",
    ("CHIM", 6): "chim-soluzioni",
    ("CHIM", 7): "chim-cinetica-equilibrio",
    ("CHIM", 8): "chim-cinetica-equilibrio",
    ("CHIM", 9): "chim-acidi-basi-redox",
    ("CHIM", 10): "chim-struttura-atomo",
    ("CHIM", 11): "chim-acidi-basi-redox",
    ("CHIM", 12): "chim-idrocarburi",
    ("CHIM", 13): "chim-biomolecole",
    ("BIO", 1): "bio-organizzazione-vita",
    ("BIO", 2): "bio-genoma-epigenetica",
    ("BIO", 3): "bio-flusso-informazione",
    ("BIO", 4): "bio-genetica-mutazioni",
    ("BIO", 5): "bio-strutture-cellulari",
    ("BIO", 6): "bio-segnalazione",
    ("BIO", 7): "bio-ciclo-cellulare",
    ("FIS", 1): "fis-metodi",
    ("FIS", 2): "fis-meccanica",
    ("FIS", 3): "fis-meccanica",
    ("FIS", 4): "fis-fluidi",
    ("FIS", 5): "fis-termodinamica",
    ("FIS", 6): "fis-elettromagnetismo",
    ("FIS", 7): "fis-radiazioni",
    ("FIS", 8): "fis-radiazioni",
}

SUBJECT_ORDER = {"CHIM": 1, "BIO": 2, "FIS": 3}
QT_ORDER = {"commentati": 1, "non_commentati": 2, "completamento": 3}
QT_SHORT = {"commentati": "COMM", "non_commentati": "NCOM", "completamento": "COMP"}


def zstd_decompress(data: bytes) -> bytes:
    libname = ctypes.util.find_library("zstd") or "libzstd.so.1"
    zstd = ctypes.CDLL(libname)
    zstd.ZSTD_getFrameContentSize.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    zstd.ZSTD_getFrameContentSize.restype = ctypes.c_ulonglong
    zstd.ZSTD_decompress.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_size_t]
    zstd.ZSTD_decompress.restype = ctypes.c_size_t
    sz = zstd.ZSTD_getFrameContentSize(data, len(data))
    if sz in (0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFE):
        sz = len(data) * 25
    buf = ctypes.create_string_buffer(sz)
    out_sz = zstd.ZSTD_decompress(buf, sz, data, len(data))
    return buf.raw[:out_sz]


def parse_pb(buf: bytes):
    i, out = 0, []
    while i < len(buf):
        key = shift = 0
        while True:
            b = buf[i]; i += 1
            key |= (b & 0x7F) << shift; shift += 7
            if not (b & 0x80): break
        field, wt = key >> 3, key & 7
        if wt == 0:
            val = shift = 0
            while True:
                b = buf[i]; i += 1
                val |= (b & 0x7F) << shift; shift += 7
                if not (b & 0x80): break
        elif wt == 2:
            n = shift = 0
            while True:
                b = buf[i]; i += 1
                n |= (b & 0x7F) << shift; shift += 7
                if not (b & 0x80): break
            val = buf[i:i + n]; i += n
        elif wt == 5:
            val = buf[i:i + 4]; i += 4
        elif wt == 1:
            val = buf[i:i + 8]; i += 8
        out.append((field, wt, val))
    return out


def deterministic_new_guid(item_id: str, used_guids: set[str]) -> str:
    salt_idx = 0
    while True:
        payload = f"semestre-filtro-restored-130-v1::{salt_idx}::{item_id}".encode("utf-8")
        val = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
        chars = []
        while val > 0:
            val, rem = divmod(val, 91)
            chars.append(BASE91_ANKI[rem])
        cand = ("".join(reversed(chars)) or "a")[:10]
        if cand not in used_guids:
            used_guids.add(cand)
            return cand
        salt_idx += 1


def git_show(spec: str) -> str:
    return subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def load_sqlite_from_git(spec: str) -> bytes:
    return subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True, check=True).stdout


def main() -> None:
    (OUT / "target_schema" / "current_templates").mkdir(parents=True, exist_ok=True)
    (OUT / "special_sets").mkdir(parents=True, exist_ok=True)
    (OUT / "chunks").mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(APKG_UPLOAD, "r") as z:
        raw_db = zstd_decompress(z.read("collection.anki21b"))

    with tempfile.NamedTemporaryFile(dir=str(ROOT / "work"), suffix=".sqlite", delete=True) as tf:
        tf.write(raw_db); tf.flush()
        con = sqlite3.connect(f"file:{tf.name}?immutable=1", uri=True)
        con.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold()) - (a.casefold() < b.casefold()))

        max_note_mod = con.execute("SELECT max(mod) FROM notes").fetchone()[0]
        max_card_mod = con.execute("SELECT max(mod) FROM cards").fetchone()[0]

        notetypes_info = {}
        for ntid in (1813027267, 1481924269089):
            name, mtime, cfg = con.execute("SELECT name, mtime_secs, config FROM notetypes WHERE id=?", (ntid,)).fetchone()
            pb_int = {f: v for f, wt, v in parse_pb(cfg) if wt == 0}
            pb_bytes = {f: v for f, wt, v in parse_pb(cfg) if wt == 2}
            css = pb_bytes.get(3, b"").decode("utf-8", "replace")
            flds = [r[0] for r in con.execute("SELECT name FROM fields WHERE ntid=? ORDER BY ord", (ntid,)).fetchall()]
            tname, tcfg = con.execute("SELECT name, config FROM templates WHERE ntid=? ORDER BY ord LIMIT 1", (ntid,)).fetchone()
            tpb = {f: v for f, wt, v in parse_pb(tcfg) if wt == 2}
            qfmt = tpb.get(1, b"").decode("utf-8", "replace")
            afmt = tpb.get(2, b"").decode("utf-8", "replace")
            notetypes_info[str(ntid)] = {
                "id": ntid,
                "name": name,
                "kind": pb_int.get(1, 0),
                "mtime_secs": mtime,
                "fields": flds,
                "template_name": tname,
            }
            slug = "mcq_1813027267" if ntid == 1813027267 else "cloze_1481924269089"
            tdir = OUT / "target_schema" / "current_templates" / slug
            tdir.mkdir(parents=True, exist_ok=True)
            (tdir / "front.html").write_text(qfmt, encoding="utf-8")
            (tdir / "back.html").write_text(afmt, encoding="utf-8")
            (tdir / "style.css").write_text(css, encoding="utf-8")

        decks_by_id = {}
        decks_by_name = {}
        subdeck_lookup = {}
        for did, dname in con.execute("SELECT id, name FROM decks ORDER BY name").fetchall():
            canon_name = dname.replace("\x1f", "::")
            decks_by_id[str(did)] = canon_name
            decks_by_name[canon_name] = did

        cards_by_nid = defaultdict(list)
        for cid, nid, did, cord in con.execute("SELECT id, nid, did, ord FROM cards ORDER BY nid, ord").fetchall():
            cards_by_nid[nid].append({"cid": cid, "did": did, "ord": cord})

        live_notes = {}
        used_guids = set()
        for nid, guid, mid, mod, tags, flds in con.execute("SELECT id, guid, mid, mod, tags, flds FROM notes").fetchall():
            fl = flds.split("\x1f")
            iid = fl[0]
            used_guids.add(guid)
            c_list = cards_by_nid[nid]
            did = c_list[0]["did"]
            dname = decks_by_id[str(did)]
            parts = iid.split("-")
            subdeck_lookup[(parts[0], int(parts[1][1:]), parts[2])] = (did, dname)
            live_notes[iid] = {
                "nid": nid,
                "guid": guid,
                "mid": mid,
                "did": did,
                "deck_name": dname,
                "mod": mod,
                "card_count": len(c_list),
                "tags": [t for t in tags.strip().split() if t],
                "essential_html": {
                    "FrontStemHTML": fl[8],
                    "AnswerBannerHTML": fl[12],
                    "ExplanationHTML": fl[13],
                    "FigureHTML": fl[14],
                    "QuestionScanHTML": fl[15],
                    "SolutionScanHTML": fl[16],
                },
            }
        con.close()

    qa_7078 = {
        r["id"]: r
        for r in (json.loads(ln) for ln in git_show("origin/arena/6d93039e-anki-sem:output/qa_dataset.jsonl").splitlines() if ln.strip())
    }
    qa_6948 = {
        r["id"]: r
        for r in (json.loads(ln) for ln in git_show("origin/arena/dbe933e6-anki-sem:output/qa_dataset.jsonl").splitlines() if ln.strip())
    }

    issues_by_id = defaultdict(list)
    for row in csv.DictReader(io.StringIO(git_show("origin/arena/dbe933e6-anki-sem:issues.csv"))):
        issues_by_id[row["ItemID"]].append({
            "cat": row["category"],
            "field": row["field"],
            "fix": row["proposed fix"],
            "status": row["status"],
        })

    dup_pairs_by_id = defaultdict(list)
    twin_kept_map = {}
    for row in csv.DictReader(io.StringIO(git_show("origin/arena/dbe933e6-anki-sem:duplicates.csv"))):
        i1, i2 = row["ItemID_1"], row["ItemID_2"]
        dup_pairs_by_id[i1].append({"other_id": i2, "type": row["DuplicateType"], "resolution": row["Resolution"], "kept": row["KeptItemID"]})
        dup_pairs_by_id[i2].append({"other_id": i1, "type": row["DuplicateType"], "resolution": row["Resolution"], "kept": row["KeptItemID"]})
        if row["Resolution"] == "deduplicated":
            kept = row["KeptItemID"]
            dropped = i2 if i1 == kept else i1
            twin_kept_map[dropped] = kept

    con_cc1 = sqlite3.connect(f"file:{ROOT / 'work/uncommented_questions_workpack/questions.db'}?immutable=1", uri=True)
    cc1_map = {
        r[0]: {"status": r[1], "reason": r[2], "flags": json.loads(r[3]) if r[3] else []}
        for r in con_cc1.execute("SELECT id, status, reason, flags FROM questions")
    }
    con_cc1.close()

    raw_0c5 = load_sqlite_from_git("origin/arena/0c53ca03-anki-sem:work/questions.db")
    with tempfile.NamedTemporaryFile(dir=str(ROOT / "work"), suffix=".sqlite", delete=True) as tf2:
        tf2.write(raw_0c5); tf2.flush()
        con_0c5 = sqlite3.connect(f"file:{tf2.name}?immutable=1", uri=True)
        c05_map = {
            r[0]: {"status": r[1], "reason": r[2], "flags": json.loads(r[3]) if r[3] else []}
            for r in con_0c5.execute("SELECT id, status, reason, flags FROM questions")
        }
        con_0c5.close()

    ak_9d2 = {r["id"]: r for r in (json.loads(ln) for ln in git_show("origin/arena/9d2e065b-anki-sem:answer_key_output.jsonl").splitlines() if ln.strip())}
    ak_0c0 = {r["id"]: r for r in (json.loads(ln) for ln in git_show("origin/arena/0c0900a2-anki-sem:answers.jsonl").splitlines() if ln.strip())}

    opus_ver = {
        r["id"]: r
        for r in (json.loads(ln) for ln in git_show("origin/opus-rebuild/semestre-filtro:opus_attempt/build/verification.jsonl").splitlines() if ln.strip())
    }
    opus_corr = {
        r["id"]: r
        for r in (json.loads(ln) for ln in git_show("origin/opus-rebuild/semestre-filtro:opus_attempt/work/deepseek/chim01/corrections.jsonl").splitlines() if ln.strip())
    }

    (OUT / "target_schema" / "ids_and_decks.json").write_text(
        json.dumps(
            {
                "source_package": "currnet_no_images.apkg.md",
                "existing_notes_count": len(live_notes),
                "full_book_items_count": len(qa_7078),
                "restored_duplicates_count": len(qa_7078) - len(live_notes),
                "max_existing_note_mod": max_note_mod,
                "max_existing_card_mod": max_card_mod,
                "required_min_mod_for_update": max(max_note_mod, max_card_mod) + 60,
                "notetypes": notetypes_info,
                "decks_by_name": decks_by_name,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    all_ids_sorted = sorted(
        qa_7078.keys(),
        key=lambda iid: (
            SUBJECT_ORDER[qa_7078[iid]["subject_code"]],
            int(qa_7078[iid]["chapter_num"]),
            QT_ORDER[qa_7078[iid]["quiz_type"]],
            int(qa_7078[iid]["qnum"]),
        ),
    )

    guid_map_7078 = {}
    restored_130_records = []
    page_291_records = []
    adjudicated_257_records = []
    open_defects_records = []
    by_subsection = defaultdict(list)

    for iid in all_ids_sorted:
        base_7078 = qa_7078[iid]
        rem_6948 = qa_6948.get(iid)
        sc = base_7078["subject_code"]
        ch = int(base_7078["chapter_num"])
        qt = base_7078["quiz_type"]
        qt_s = QT_SHORT[qt]
        qnum = int(base_7078["qnum"])

        in_live = iid in live_notes
        if in_live:
            ln = live_notes[iid]
            guid = ln["guid"]
            mid = ln["mid"]
            did = ln["did"]
            dname = ln["deck_name"]
        else:
            guid = deterministic_new_guid(iid, used_guids)
            mid = 1481924269089 if qt == "completamento" else 1813027267
            did, dname = subdeck_lookup[(sc, ch, qt_s)]

        twin_id = twin_kept_map.get(iid)
        guid_map_7078[iid] = {
            "guid": guid,
            "mid": mid,
            "did": did,
            "deck_name": dname,
            "in_current_apkg": in_live,
            "kept_twin_id": twin_id,
        }

        cc1_entry = cc1_map.get(iid)
        c05_entry = c05_map.get(iid)
        twin_info = None
        if not in_live and twin_id:
            twin_src = qa_6948.get(twin_id) or qa_7078[twin_id]
            twin_reason = None
            if cc1_map.get(twin_id, {}).get("status") == "done":
                twin_reason = cc1_map[twin_id]["reason"]
            elif c05_map.get(twin_id, {}).get("status") == "done":
                twin_reason = c05_map[twin_id]["reason"]
            elif twin_id in live_notes and live_notes[twin_id]["essential_html"]["ExplanationHTML"]:
                twin_reason = live_notes[twin_id]["essential_html"]["ExplanationHTML"]
            twin_info = {
                "twin_id": twin_id,
                "twin_answer": twin_src["answer"],
                "twin_answer_text": twin_src["answer_text"],
                "same_answer_letter_as_twin": (base_7078["answer"] == twin_src["answer"]),
                "twin_explanation": twin_reason,
                "caution": (
                    "6d93039e record is pre-remediation OCR; clean OCR against scan crop, "
                    "verify key against twin_answer_text, and remap any option-letter references in twin_explanation!"
                ),
            }

        ak_info = None
        if iid in ak_9d2:
            r9 = ak_9d2[iid]
            r0 = ak_0c0.get(iid, {})
            v9 = r9.get("letter") or r9.get("answers")
            v0 = r0.get("letter") or r0.get("answers") or r0.get("answer")
            ak_info = {
                "answer_9d2e065b": v9,
                "answer_0c0900a2": v0,
                "unanimous_with_0c0900a2": (v9 == v0),
                "answer_text": r9.get("answer_text"),
                "printed_text": r9.get("printed_text"),
                "reason": r9.get("reason"),
                "confidence": r9.get("confidence"),
                "flags": r9.get("flags", []),
            }
            adjudicated_257_records.append({"id": iid, **ak_info})

        src_struct = rem_6948 if rem_6948 is not None else base_7078

        review_reasons = []
        if iid == "CHIM-C10-NCOM-080":
            review_reasons.append("residual_banner_typo: banner reads 'Risposta corretta: A. C,' in currnet_no_images")
        if iid == "FIS-C04-COMM-007":
            review_reasons.append("residual_ocr_explanation: Bernoulli formula garbled in currnet_no_images; also needs_figure")
        if cc1_entry and cc1_entry["status"] == "flagged":
            for flg in cc1_entry["flags"]:
                review_reasons.append(f"cc130265_{flg}")
        if ak_info and (not ak_info["unanimous_with_0c0900a2"] or ak_info["flags"] or ak_info["confidence"] != "high"):
            review_reasons.append(f"ak257_review: conf={ak_info['confidence']} flags={ak_info['flags']} unanimous={ak_info['unanimous_with_0c0900a2']}")
        if not in_live:
            review_reasons.append(
                f"restored_duplicate_130: twin={twin_id} same_letter={twin_info['same_answer_letter_as_twin'] if twin_info else None}"
            )

        rec = {
            "id": iid,
            "in_current_apkg": in_live,
            "guid": guid,
            "mid": mid,
            "did": did,
            "deck_name": dname,
            "subject_code": sc,
            "subject": src_struct["subject"],
            "chapter_num": ch,
            "chapter_title": src_struct["chapter_title"],
            "quiz_type": qt,
            "qnum": qnum,
            "question_book_page": src_struct["question_book_page"],
            "answer_book_page": src_struct.get("answer_book_page"),
            "ud_tag": f"ud::{UD_MAP[(sc, ch)]}",
            "dup_tags": sorted({f"dup::{d['other_id']}" for d in dup_pairs_by_id.get(iid, [])}),
            "remediated_card": {
                "question": src_struct["question"],
                "options": src_struct["options"],
                "answer": src_struct["answer"],
                "answer_text": src_struct["answer_text"],
                "explanation_comm": src_struct.get("explanation"),
                "question_image": f"{iid}.png",
                "figure_files": src_struct.get("figure_files", []),
            },
            "live_anki": live_notes[iid]["essential_html"] if in_live else None,
            "live_tags": live_notes[iid]["tags"] if in_live else [],
            "solved_work": {
                "cc130265": cc1_entry,
                "0c53ca03": c05_entry,
                "restored_twin_ref": twin_info,
                "ak257": ak_info,
                "opus_chim01": opus_ver.get(iid),
                "opus_chim01_scan_fix": opus_corr.get(iid),
            },
            "issues_fixed_log": issues_by_id.get(iid, []),
            "needs_attention": review_reasons,
        }

        if not in_live:
            restored_130_records.append(rec)
        if sc == "CHIM" and ch == 11 and qt == "commentati" and 17 <= qnum <= 23:
            page_291_records.append(rec)
        if review_reasons:
            open_defects_records.append({
                "id": iid,
                "in_current_apkg": in_live,
                "quiz_type": qt,
                "question_book_page": src_struct["question_book_page"],
                "needs_attention": review_reasons,
            })

        by_subsection[(sc, ch, qt_s, QT_ORDER[qt])].append(rec)

    assert len({v["guid"] for v in guid_map_7078.values()}) == 7078, "GUID collision detected!"

    (OUT / "target_schema" / "guid_map_7078.json").write_text(
        json.dumps(guid_map_7078, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    def write_jsonl(path: Path, rows: list) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    write_jsonl(OUT / "special_sets" / "missing_130_restored.jsonl", restored_130_records)
    write_jsonl(OUT / "special_sets" / "page_291_chim_c11_comm_17_23.jsonl", page_291_records)
    write_jsonl(OUT / "special_sets" / "adjudicated_257_keys.jsonl", adjudicated_257_records)
    write_jsonl(OUT / "special_sets" / "items_needing_scan_or_key_check.jsonl", open_defects_records)

    chunk_manifest = []
    sorted_subs = sorted(by_subsection.keys(), key=lambda k: (SUBJECT_ORDER[k[0]], k[1], k[3]))
    global_chunk_idx = 0

    for sc, ch, qt_s, _ in sorted_subs:
        rows = by_subsection[(sc, ch, qt_s, _)]
        ch_dir = OUT / "chunks" / f"{sc}-C{ch:02d}"
        ch_dir.mkdir(parents=True, exist_ok=True)
        for start in range(0, len(rows), CHUNK_SIZE):
            batch = rows[start:start + CHUNK_SIZE]
            global_chunk_idx += 1
            q_first, q_last = batch[0]["qnum"], batch[-1]["qnum"]
            fname = f"chunk_{global_chunk_idx:03d}_{sc}-C{ch:02d}_{qt_s}_{q_first:03d}-{q_last:03d}.jsonl"
            rel_path = f"chunks/{sc}-C{ch:02d}/{fname}"
            write_jsonl(ch_dir / fname, batch)
            n_attn = sum(1 for r in batch if r["needs_attention"])
            n_restored = sum(1 for r in batch if not r["in_current_apkg"])
            chunk_manifest.append({
                "chunk_num": global_chunk_idx,
                "path": rel_path,
                "chapter_key": f"{sc}-C{ch:02d}",
                "quiz_type_short": qt_s,
                "qnum_range": [q_first, q_last],
                "total_items": len(batch),
                "in_current_apkg": len(batch) - n_restored,
                "restored_130_items": n_restored,
                "items_needing_attention": n_attn,
                "clean_ready_items": len(batch) - n_attn,
            })

    (OUT / "chunk_manifest.json").write_text(
        json.dumps(
            {
                "chunk_size_cap": CHUNK_SIZE,
                "total_chunks": len(chunk_manifest),
                "total_items": len(all_ids_sorted),
                "live_existing_items": len(live_notes),
                "restored_130_items": len(restored_130_records),
                "items_needing_attention": len(open_defects_records),
                "chunks": chunk_manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Built {len(chunk_manifest)} chunks across 28 chapters ({len(all_ids_sorted)} total items).")


if __name__ == "__main__":
    main()
