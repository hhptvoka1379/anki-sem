#!/bin/bash
# One chapter end to end: DeepSeek extraction -> crops -> hand corrections -> QA -> blind derivation
# -> verification -> explanations. Every model step is resumable (finished request ids are skipped),
# so a rerun costs nothing for work already done.
#
#   scripts/run_chapter.sh <work-key e.g. chim01> <pagemap.json> <ud-slug> [budget-usd-per-step]
#
# Stops (exit 1) when verification has pending cards: adjudicate them into
# work/deepseek/<key>/adjudications.jsonl and rerun. Hand fixes go in corrections.jsonl and
# explain/explanations_manual.jsonl in the same folder. Merging into build/ is scripts/merge_build.sh.
set -euo pipefail
cd "$(dirname "$0")/.."

KEY="$1"; MAP="$2"; UD="$3"; BUDGET="${4:-0.30}"
W="work/deepseek/$KEY"; PY=.venv/bin/python
BATCH_PRICES=(--price-in 0.112 --price-out 0.336)   # deepseek-v4.1-flash:batch on deepinfra/fp8
mkdir -p "$W"

echo "== 1. extraction (live: the Batch API rejects embedded images)"
$PY scripts/ds_extract.py jobs --pagemap "$MAP" --workdir "$W"
$PY scripts/deepseek_batch.py "$W/jobs.jsonl" "$W/results.jsonl" --mode live --budget "$BUDGET"
$PY scripts/ds_extract.py parse --pagemap "$MAP" --workdir "$W"

echo "== 2. crops + hand corrections"
cp "$W/extracted.jsonl" "$W/extracted_crops.jsonl"
rm -rf "$W/media"
$PY scripts/crop.py --extracted "$W/extracted_crops.jsonl" --pagemap "$MAP" --out "$W/media" --report "$W/crop_report.tsv"
[ -s "$W/corrections.jsonl" ] && $PY scripts/apply_corrections.py "$W/extracted_crops.jsonl" "$W/corrections.jsonl"

echo "== 3. extraction QA (warnings are for review; failures stop the run)"
OFFSET=$($PY -c "import json,sys; print(json.load(open(sys.argv[1]))['offset'])" "$MAP")
$PY scripts/qa_extract.py "$W/extracted_crops.jsonl" --offset "$OFFSET" > "$W/qa.tsv" || { grep '^FAIL' "$W/qa.tsv"; exit 1; }
tail -1 "$W/qa.tsv"

echo "== 4. blind derivation (batch)"
$PY scripts/ds_derive.py jobs --extracted "$W/extracted_crops.jsonl" --workdir "$W/derive"
$PY scripts/deepseek_batch.py "$W/derive/jobs.jsonl" "$W/derive/results.jsonl" --mode batch "${BATCH_PRICES[@]}" --budget "$BUDGET"
$PY scripts/ds_derive.py parse --extracted "$W/extracted_crops.jsonl" --workdir "$W/derive"

VERIFY=(--extracted "$W/extracted_crops.jsonl" --derived "$W/derive/derived.jsonl" --ud "$UD"
        --adjudications "$W/adjudications.jsonl" --out "$W/verification.jsonl" --pending "$W/pending.jsonl")
touch "$W/adjudications.jsonl"

echo "== 5. verification (stops here if cards need adjudication)"
$PY scripts/verify.py "${VERIFY[@]}"

echo "== 6. explanations: draft, independent check, collect (batch)"
E="$W/explain"
$PY scripts/ds_explain.py draft-jobs --extracted "$W/extracted_crops.jsonl" --verification "$W/verification.jsonl" --workdir "$E"
$PY scripts/deepseek_batch.py "$E/draft_jobs.jsonl" "$E/draft_results.jsonl" --mode batch "${BATCH_PRICES[@]}" --budget "$BUDGET"
$PY scripts/ds_explain.py check-jobs --extracted "$W/extracted_crops.jsonl" --verification "$W/verification.jsonl" --workdir "$E"
$PY scripts/deepseek_batch.py "$E/check_jobs.jsonl" "$E/check_results.jsonl" --mode batch "${BATCH_PRICES[@]}" --budget "$BUDGET"
$PY scripts/ds_explain.py collect --workdir "$E"
touch "$E/explanations_manual.jsonl"
$PY scripts/verify.py "${VERIFY[@]}" --explanations "$E/explanations.jsonl" "$E/explanations_manual.jsonl"
echo "chapter $KEY done: $W/verification.jsonl; rejected explanations in $E/rejected.tsv"
