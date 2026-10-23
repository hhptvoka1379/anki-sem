#!/usr/bin/env python3
"""Extract collision-free delta media (130 restored question scans, 2 solution scans, any restored figures, + 4 offline Risoprint Zine .ttf fonts)."""
from __future__ import annotations

import io
import json
import re
import sqlite3
import subprocess
import tempfile
import zipfile
from pathlib import Path

FONTS = [
    "_SpaceGrotesk-Variable.ttf",
    "_SpaceMono-Regular.ttf",
    "_SpaceMono-Bold.ttf",
    "_Syne-Variable.ttf",
]


def extract_all_delta_media(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    restored_ids = [
        json.loads(ln)["id"]
        for ln in Path("work/opus_handoff/special_sets/missing_130_restored.jsonl").read_text().splitlines()
    ]
    restored_set = set(restored_ids)

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

        # Check 6d93039e SQLite notes for FigureHTML / SolutionScanHTML on the 130 restored items
        db_tmp = Path("work/.cache/6d93039e_col.anki2")
        db_tmp.write_bytes(zf.read("collection.anki2"))
        con = sqlite3.connect(db_tmp)
        for (flds,) in con.execute("SELECT flds FROM notes"):
            p = flds.split("\x1f")
            iid = p[0]
            if iid not in restored_set:
                continue
            # Question scan
            q_orig = f"{iid}.png"
            assert q_orig in name_to_zipkey, f"Missing {q_orig} in 6d93039e media"
            q_dest = f"restored_{iid}.png"
            (out_dir / q_dest).write_bytes(zf.read(name_to_zipkey[q_orig]))
            q_count += 1

            # FigureHTML (field 14 if 17-field, or scan <img src="...">)
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

            # SolutionScanHTML (field 16 if 17-field)
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

    # Extract 4 offline .ttf fonts from origin/opus-rebuild/semestre-filtro
    for font_name in FONTS:
        font_bytes = subprocess.check_output(
            ["git", "show", f"origin/opus-rebuild/semestre-filtro:opus_attempt/assets/fonts/{font_name}"]
        )
        (out_dir / font_name).write_bytes(font_bytes)

    manifest = {
        "question_scans": q_count,
        "figure_crops": f_count,
        "solution_scans": s_count,
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
    m = extract_all_delta_media(Path("work/.cache/delta_media"))
    print(json.dumps(m, ensure_ascii=False, indent=2))
