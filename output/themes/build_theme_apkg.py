#!/usr/bin/env python3
"""Zero-dependency CLI tool to repackage Semestre_Filtro_EdiSES_Complete.apkg
with ANY of the 10 art-directed Anki design systems in ~0.7 seconds.

Usage:
  python3 output/themes/build_theme_apkg.py            # Lists all 10 themes
  python3 output/themes/build_theme_apkg.py 04         # Builds full standalone 7,078-card .apkg for #04
  python3 output/themes/build_theme_apkg.py all        # Builds full standalone .apkg for all 10 themes
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from extractor.anki_themes import (
    THEMES,
    build_lightweight_theme_switcher_apkg,
    repackage_apkg_with_theme,
)


def main() -> None:
    src = ROOT / "output" / "Semestre_Filtro_EdiSES_Complete.apkg"
    out_dir = ROOT / "output" / "themes"
    args = [a.strip() for a in sys.argv[1:]]

    if not args:
        print("Available Semestre Filtro Anki Design Systems:")
        for k, th in THEMES.items():
            print(f"  {th['num']} ({k:28s}) — {th['name']}")
        print("\nRun e.g.: python3 output/themes/build_theme_apkg.py 04")
        return

    targets = list(THEMES.keys()) if "all" in args else [
        k for k, th in THEMES.items() if th["num"] in args or k in args
    ]
    if not targets:
        raise SystemExit(f"No matching theme for {args!r}")

    for key in targets:
        t0 = time.time()
        dest = out_dir / f"Semestre_Filtro_{key}.apkg"
        repackage_apkg_with_theme(
            source_apkg=src,
            dest_apkg=dest,
            theme_key=key,
            instant_grade_front=False,
            show_timer=False,
            type_in_completamento=False,
            auto_open_scan=False,
        )
        mb = dest.stat().st_size / (1024 * 1024)
        print(f"[{time.time()-t0:.2f}s] Built full 7,078-card deck -> {dest.relative_to(ROOT)} ({mb:.2f} MB)")


if __name__ == "__main__":
    main()
