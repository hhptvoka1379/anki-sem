#!/usr/bin/env python3
"""Extract complete standalone + merge-safe media pack (8,230 PNGs + 4 offline Risoprint Zine .ttf fonts = 8,234 files)."""
from __future__ import annotations

import io
import json
import re
import sqlite3
import subprocess
import zipfile
from pathlib import Path

FONTS = [
    "_SpaceGrotesk-Variable.ttf",
    "_SpaceMono-Regular.ttf",
    "_SpaceMono-Bold.ttf",
    "_Syne-Variable.ttf",
]

# 34 false-positive pure-text duplicate crops removed from FigureHTML
BOGUS_TEXT_ONLY_FIGURES: set[str] = {
    "CHIM_C01_comm_Q002.png",
    "CHIM_C01_non__Q058.png",
    "CHIM_C01_non__Q070.png",
    "CHIM_C01_non__Q107.png",
    "CHIM_C02_comm_Q003.png",
    "CHIM_C02_comm_Q005.png",
    "CHIM_C03_non__Q136_p1.png",
    "CHIM_C06_comm_Q016.png",
    "CHIM_C07_non__Q024.png",
    "CHIM_C07_non__Q035.png",
    "CHIM_C07_non__Q041_p1.png",
    "CHIM_C09_non__Q086.png",
    "CHIM_C09_non__Q091.png",
    "CHIM_C10_non__Q064.png",
    "CHIM_C11_comm_Q026.png",
    "CHIM_C11_non__Q045.png",
    "CHIM_C11_non__Q050_p2.png",
    "CHIM_C11_non__Q054_p1.png",
    "CHIM_C11_non__Q110.png",
    "CHIM_C12_non__Q034.png",
    "CHIM_C12_non__Q041.png",
    "CHIM_C12_non__Q046.png",
    "CHIM_C12_non__Q101.png",
    "CHIM_C12_non__Q115.png",
    "CHIM_C12_non__Q160.png",
    "CHIM_C12_non__Q163.png",
    "BIO_C03_non__Q024.png",
    "BIO_C04_comm_Q048_p1.png",
    "BIO_C04_non__Q035_p1.png",
    "BIO_C05_comm_Q037_p1.png",
    "BIO_C07_non__Q014_p1.png",
    "FIS_C03_non__Q184_p1.png",
    "FIS_C06_non__Q123_p1.png",
    "FIS_C07_non__Q051.png",
}

# 12 tightly re-cropped / restored diagrams (renamed to clean_fig_<name> to avoid SHA-1 collisions with older untrimmed files)
CLEAN_RECROP_FIGURES: dict[str, str] = {
    fn: f"clean_fig_{fn}"
    for fn in [
        "BIO_C04_comm_Q063.png",
        "BIO_C04_non__Q035_p2.png",
        "BIO_C07_non__Q044.png",
        "BIO_C07_non__Q055.png",
        "CHIM_C02_comm_Q025_p2.png",
        "CHIM_C12_non__Q161.png",
        "FIS_C01_comm_Q025.png",
        "FIS_C01_non__Q090.png",
        "FIS_C04_comm_Q007.png",
        "FIS_C06_comm_Q034_p1.png",
        "FIS_C06_comm_Q042_p1.png",
        "FIS_C06_non__Q186.png",
    ]
}


def clean_live_figure_html(fig_html: str) -> str:
    """Strip 34 bogus text-only <img src> tags and upgrade 12 tightly cropped diagrams to clean_fig_* names."""
    if not fig_html or not fig_html.strip():
        return ""
    srcs = re.findall(r'src="([^"]+)"', fig_html)
    kept: list[str] = []
    for s in srcs:
        if s in BOGUS_TEXT_ONLY_FIGURES:
            continue
        s_out = CLEAN_RECROP_FIGURES.get(s, s)
        kept.append(f'<img src="{s_out}">')
    return "".join(kept)


import shutil


def extract_all_delta_media(out_dir: Path, include_full_live_media: bool = True) -> dict:
    """Extract all 137 restored_* PNGs + 4 fonts (+ all 8,093 clean live PNGs when include_full_live_media=True)."""
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    restored_ids = [
        json.loads(ln)["id"]
        for ln in Path("work/opus_handoff/special_sets/missing_130_restored.jsonl").read_text().splitlines()
    ]
    restored_set = set(restored_ids)

    live_png_count = 0
    recrop_count = 0
    if include_full_live_media:
        dbe_bytes = subprocess.check_output(
            ["git", "show", "origin/arena/dbe933e6-anki-sem:output/Semestre_Filtro_Complete.apkg"]
        )
        with zipfile.ZipFile(io.BytesIO(dbe_bytes)) as dzf:
            d_media: dict[str, str] = json.loads(dzf.read("media").decode("utf-8"))
            for num_key, fn in d_media.items():
                if fn in BOGUS_TEXT_ONLY_FIGURES:
                    continue
                dest_name = CLEAN_RECROP_FIGURES.get(fn, fn)
                (out_dir / dest_name).write_bytes(dzf.read(num_key))
                if fn in CLEAN_RECROP_FIGURES:
                    recrop_count += 1
                else:
                    live_png_count += 1

    apkg_bytes = subprocess.check_output(
        ["git", "show", "origin/arena/6d93039e-anki-sem:output/Semestre_Filtro_EdiSES_Complete.apkg"]
    )
    restored_fig_html: dict[str, str] = {}
    restored_sol_html: dict[str, str] = {}
    q_count = 0
    s_count = 0
    f_count = 0

    with zipfile.ZipFile(io.BytesIO(apkg_bytes)) as zf:
        media_map: dict[str, str] = json.loads(zf.read("media").decode("utf-8"))
        name_to_zipkey = {v: k for k, v in media_map.items()}

        db_tmp = Path("work/.cache/6d93039e_col.anki2")
        db_tmp.write_bytes(zf.read("collection.anki2"))
        con = sqlite3.connect(db_tmp)
        for (flds,) in con.execute("SELECT flds FROM notes"):
            p = flds.split("\x1f")
            iid = p[0]
            if iid not in restored_set:
                continue
            q_orig = f"{iid}.png"
            assert q_orig in name_to_zipkey, f"Missing {q_orig} in 6d93039e media"
            q_dest = f"restored_{iid}.png"
            (out_dir / q_dest).write_bytes(zf.read(name_to_zipkey[q_orig]))
            q_count += 1

            fig_field = p[14] if len(p) > 14 else ""
            if fig_field.strip():
                srcs = re.findall(r'src="([^"]+)"', fig_field)
                new_imgs = []
                for idx, src in enumerate(srcs, 1):
                    if src in name_to_zipkey:
                        f_dest = f"restored_fig_{iid}_{idx}.png"
                        (out_dir / f_dest).write_bytes(zf.read(name_to_zipkey[src]))
                        new_imgs.append(f'<img src="{f_dest}">')
                        f_count += 1
                if new_imgs:
                    restored_fig_html[iid] = "".join(new_imgs)

            sol_field = p[16] if len(p) > 16 else ""
            if sol_field.strip():
                srcs = re.findall(r'src="([^"]+)"', sol_field)
                new_sols = []
                for idx, src in enumerate(srcs, 1):
                    if src in name_to_zipkey:
                        s_dest = f"restored_sol_{iid}_{idx}.png"
                        (out_dir / s_dest).write_bytes(zf.read(name_to_zipkey[src]))
                        new_sols.append(f'<img src="{s_dest}">')
                        s_count += 1
                if new_sols:
                    restored_sol_html[iid] = "".join(new_sols)
        con.close()
        db_tmp.unlink(missing_ok=True)

    for font_name in FONTS:
        font_bytes = subprocess.check_output(
            ["git", "show", f"origin/opus-rebuild/semestre-filtro:opus_attempt/assets/fonts/{font_name}"]
        )
        (out_dir / font_name).write_bytes(font_bytes)

    manifest = {
        "live_sha1_identical_pngs": live_png_count,
        "clean_recropped_figure_pngs": recrop_count,
        "restored_question_scans": q_count,
        "restored_figure_crops": f_count,
        "restored_solution_scans": s_count,
        "fonts": len(FONTS),
        "total_files": len(list(out_dir.iterdir())),
        "restored_fig_html": restored_fig_html,
        "restored_sol_html": restored_sol_html,
    }
    Path("work/.cache/delta_media_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    return manifest


if __name__ == "__main__":
    m = extract_all_delta_media(Path("work/.cache/full_media"), include_full_live_media=True)
    print(json.dumps({k: v for k, v in m.items() if not isinstance(v, dict)}, ensure_ascii=False, indent=2))
