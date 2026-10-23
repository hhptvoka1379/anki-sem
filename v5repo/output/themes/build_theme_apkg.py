#!/usr/bin/env python3
"""100% Zero-Dependency CLI tool (pure Python 3 stdlib — NO `pip install` needed!)
to generate full standalone 6,948-card `.apkg` packages for ANY or ALL of the 10 themes
directly from `output/Semestre_Filtro_Complete.apkg` in ~0.8s per deck.

Every generated `.apkg` includes:
  - Full 6,948 deduplicated cards + all 8,127 embedded figures & scan PNGs
  - Top-left `DARK` / `LIGHT` toggle button (`#sf-theme-toggle` inside `.sf-canvas`, persisted in `localStorage['sf-theme']`)
  - Isolated Anki Note Type ID, subdeck IDs, and note GUIDs (never skipped or collided in Anki!)
  - Self-contained Anki media: after importing into Anki, you can safely delete this cloned repository (`rm -rf anki-sem`)!

Usage:
  python3 output/themes/build_theme_apkg.py            # Lists all 10 themes
  python3 output/themes/build_theme_apkg.py 04         # Builds standalone .apkg for theme #04
  python3 output/themes/build_theme_apkg.py 01 05 10   # Builds standalone .apkg for themes #01, #05, #10
  python3 output/themes/build_theme_apkg.py all        # Builds ALL 10 standalone full .apkg decks!
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from extractor.anki_themes import THEMES, repackage_apkg_with_theme


def _friendly_filename(theme_key: str, theme_obj: dict) -> str:
    if theme_obj["num"] == "04":
        return "Semestre_Filtro_04_NeoBrutalist_Risoprint_Zine.apkg"
    clean_name = re.sub(r"[^A-Za-z0-9]+", "_", theme_obj["name"]).strip("_")
    return f"Semestre_Filtro_{theme_obj['num']}_{clean_name}.apkg"


def main() -> None:
    src = ROOT / "output" / "Semestre_Filtro_Complete.apkg"
    out_dir = ROOT / "output" / "themes"
    args = [a.strip() for a in sys.argv[1:] if a.strip() and not a.startswith("-")]

    if not args or "--list" in sys.argv or "-h" in sys.argv or "--help" in sys.argv:
        print("Available Semestre Filtro Standalone Anki Design Systems (with DARK/LIGHT toggle):")
        for k, th in THEMES.items():
            print(f"  {th['num']} ({k:26s}) -> output/themes/{_friendly_filename(k, th)}")
        print("\nExamples (uses standard macOS/Linux/Windows python3 — zero pip packages required):")
        print("  python3 output/themes/build_theme_apkg.py all")
        print("  python3 output/themes/build_theme_apkg.py 01 04 06 10")
        return

    targets = (
        list(THEMES.keys())
        if "all" in args
        else [k for k, th in THEMES.items() if th["num"] in args or k in args]
    )
    if not targets:
        raise SystemExit(f"No matching theme for {args!r}")

    for key in targets:
        t0 = time.time()
        th = THEMES[key]
        dest = out_dir / _friendly_filename(key, th)
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
        print(f"[{time.time()-t0:.2f}s] Built full 6,948-card deck -> {dest.relative_to(ROOT)} ({mb:.2f} MB)")


if __name__ == "__main__":
    main()
