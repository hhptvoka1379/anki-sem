#!/bin/bash
# Merge every finished chapter (work/deepseek/<key>/ with a verification.jsonl) into build/,
# build the package and run the gates. No model calls.
#
#   scripts/merge_build.sh <version e.g. 1.0> <pagemap.json for gate 1>
set -euo pipefail
cd "$(dirname "$0")/.."
VERSION="$1"; MAP="$2"; PY=.venv/bin/python

done_dirs=()
for d in work/deepseek/*/; do
  [ -s "$d/verification.jsonl" ] && [ -s "$d/extracted_crops.jsonl" ] && done_dirs+=("$d")
done
[ ${#done_dirs[@]} -gt 0 ] || { echo "no finished chapters"; exit 1; }

rm -rf build/media && mkdir -p build/media
: > build/extracted.jsonl; : > build/verification.jsonl
for d in "${done_dirs[@]}"; do
  cat "$d/extracted_crops.jsonl" >> build/extracted.jsonl
  cat "$d/verification.jsonl" >> build/verification.jsonl
  cp "$d"/media/*.png build/media/
done
# Chapter keys (e.g. CHIM-C01) present in this build, for the per-chapter gate checks.
CHAPTERS=$($PY -c "import json; print(' '.join(sorted({'-'.join(r['id'].split('-')[:2]) for r in map(json.loads, open('build/extracted.jsonl'))})))")
echo "chapters: $CHAPTERS"

OUT="build/Semestre_Filtro_v$VERSION.apkg"
$PY scripts/build.py --extracted build/extracted.jsonl --verification build/verification.jsonl \
  --templates templates/ --media build/media --ids build/ids.json --version "$VERSION" --out "$OUT" --chapters $CHAPTERS
$PY scripts/gates/run_gates.py "$OUT" --extracted build/extracted.jsonl --verification build/verification.jsonl \
  --page-map "$MAP" --unverified UNVERIFIED.md --out build/verification_report.md --chapters $CHAPTERS
