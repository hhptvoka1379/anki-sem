"""Clean the raw OCR flags.

Three problems with the raw comparison:
  * crops where Tesseract returned nothing produced "OTHER" rows (empty window);
  * CHAR_SWAP fired on Tesseract misreads (ciclo -> cicto), not card errors;
  * NUMBER_FOR_WORD fired on ordinary numbers mid-sentence.
Direction filter: a swap is kept only if the card word is not a valid Italian
word while the OCR word is (or both are invalid, i.e. a technical term typo).
"""
import collections
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import common as C

HUNSPELL = ["hunspell", "-d", "/Users/db/Documents/projects/anki/_tools/it_IT"]


def valid_words(words):
    res = subprocess.run(HUNSPELL + ["-l"], text=True, capture_output=True,
                         input="\n".join(sorted(words)) + "\n")
    bad = {w for w in res.stdout.split() if w}
    return {w: w not in bad for w in words}


def main() -> None:
    flags = json.load(open(f"{C.OUT}/ocr_flags.json"))
    swaps = {f["detail"].split(" -> ")[0] for f in flags
             if f["category"] == "CHAR_SWAP" and "detail" in f}
    swaps |= {f["detail"].split(" -> ")[1] for f in flags
              if f["category"] == "CHAR_SWAP" and "detail" in f}
    ok = valid_words({w.lower() for w in swaps if w})

    kept, dropped = [], collections.Counter()
    for f in flags:
        if f["category"] == "OTHER" and not f.get("ocr", "").strip():
            dropped["OCR_EMPTY"] += 1
            continue
        if f["category"] == "CHAR_SWAP" and "detail" in f:
            x, y = f["detail"].split(" -> ")
            card_ok = ok.get(x.lower(), False)
            ocr_ok = ok.get(y.lower(), False)
            if card_ok and not ocr_ok:
                dropped["SWAP_OCR_SIDE"] += 1        # Tesseract was wrong
                continue
            if card_ok and ocr_ok:
                dropped["SWAP_BOTH_VALID"] += 1      # cannot tell; usually OCR
                continue
        if f["category"] == "NUMBER_FOR_WORD" and "detail" in f:
            x, y = f["detail"].split(" -> ")
            import re as _re
            if not _re.match(r"^\s*[0-9]{1,2}\s+<BLANK>", f["card"].strip()):
                dropped["NUMBER_NOT_A_STEM_LEAD"] += 1
                continue
        kept.append(f)

    json.dump(kept, open(f"{C.OUT}/ocr_flags.json", "w"), ensure_ascii=False)
    print("kept:", len(kept), collections.Counter(f["category"] for f in kept))
    print("dropped:", dict(dropped))


if __name__ == "__main__":
    main()
