#!/usr/bin/env python3
"""
Deterministic End-to-End QA Extractor & Anki .apkg Exporter
for 'Eserciziario Unico per il Semestre Filtro' (902 PDF pages -> 6,948 unique QA pairs).

Usage:
    .venv/bin/python extract_all.py
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from extractor.ocr_cache import build_all_ocr_caches
from extractor.quality_refiner import run_quality_refiner
from extractor.stage1_canonicalize import run_stage1
from extractor.stage2_answers import run_stage2
from extractor.stage3_questions import run_stage3
from extractor.stage4_export import run_stage4
from extractor.verify import run_verification


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract all 7,078 verified QA pairs & export Anki .apkg")
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path("/home/user/anki-sem/Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf"),
    )
    parser.add_argument("--cache-dir", type=Path, default=Path("/tmp/anki_sem_stage1"))
    parser.add_argument("--output-dir", type=Path, default=Path("/home/user/anki-sem/output"))
    args = parser.parse_args()

    t0 = time.time()
    if not (args.cache_dir / "canonical_pages.json").exists():
        run_stage1(args.pdf, args.cache_dir)
    if not (args.cache_dir / "questions_ocr_cache.json").exists() or not (args.cache_dir / "risposte_fast_lines.json").exists():
        build_all_ocr_caches(args.cache_dir)
    if not (args.cache_dir / "stage2_answers.json").exists():
        run_stage2(args.cache_dir)
    run_stage3(args.cache_dir, args.output_dir / "figures")
    run_quality_refiner(args.cache_dir, args.output_dir / "figures")
    run_stage4(args.cache_dir, args.output_dir)
    run_verification(args.output_dir)
    print(f"Complete pipeline verified cleanly in {time.time() - t0:.2f}s.")


if __name__ == "__main__":
    main()
