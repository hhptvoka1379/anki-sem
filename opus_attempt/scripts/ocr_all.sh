#!/bin/bash
# Full-book Italian OCR, 6 parallel processes (leaves 2 for the page-map agent; cap is 8). Skips pages already done, so it can be re-run.
set -euo pipefail
cd "$(dirname "$0")/.."
TESSDATA=/Users/db/Documents/projects/anki/_tools/tessdata
ocr_page() {
  n=$(printf %03d "$1"); out=work/ocr/p$n
  [ -s "$out.txt" ] && return 0
  tmp=$(mktemp -d work/ocr/tmp.XXXX)
  pdftoppm -r 300 -f "$1" -l "$1" -gray -png book.pdf "$tmp/p"
  img=$(ls "$tmp"/p*.png)
  tesseract "$img" "$out" -l ita --tessdata-dir "$TESSDATA" txt tsv >/dev/null 2>&1
  rm -rf "$tmp"
}
export -f ocr_page; export TESSDATA
seq 1 902 | xargs -P 6 -I{} bash -c 'ocr_page {}'
echo "OCR done: $(ls work/ocr/*.txt | wc -l) pages"
