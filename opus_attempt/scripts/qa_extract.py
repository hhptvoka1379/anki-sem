"""Automatic QA for worker extractions (no model calls).

Usage: qa_extract.py <extracted.jsonl> [--gold build/gold/*.jsonl] [--offset 9] [--qrange 6-50]
Prints one line per flag (id, check, detail) and a summary; exit 1 if any FAIL-level flag.
FAIL = schema/key/gold errors that make a card wrong. WARN = needs a human/agent look at the image.
"""
import argparse, glob, json, re, subprocess, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / "work" / "ocr"
HUNSPELL_DICT = "/Users/db/Documents/projects/anki/_tools/it_IT"
ID_RE = re.compile(r"^(CHIM|BIO|FIS)-C(\d{2})-(COMM|NCOM|COMP)-(\d{3})$")
REQUIRED = ["id", "subject_code", "subject", "chapter", "chapter_title", "quiz_type", "question_num",
            "pdf_page", "printed_page", "stem", "options", "printed_key", "key_page", "printed_reasoning",
            "figure", "figure_side", "question_crop", "solution_crop", "ocr_flags", "worker_notes"]
SUB_SUP = str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789" "0123456789" "-+")


def norm(s):
    """Lowercase, strip accents, map sub/superscripts to plain digits, collapse spaces."""
    s = unicodedata.normalize("NFD", (s or "").translate(SUB_SUP).replace("’", "'"))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", s).strip()


def words(s):
    return set(re.findall(r"[a-z]{4,}", norm(s)))


def ocr_text(pdf_page):
    # The question may continue on the next page, so both pages count as support.
    text = ""
    for p in (pdf_page, pdf_page + 1):
        f = OCR_DIR / ("p%03d.txt" % p)
        if f.exists():
            text += f.read_text(errors="replace") + "\n"
    return text


def hunspell_unknown(text):
    try:
        out = subprocess.run(["hunspell", "-d", HUNSPELL_DICT, "-l"], input=text, capture_output=True,
                             text=True, timeout=30, check=True).stdout
    except (OSError, subprocess.SubprocessError) as e:
        sys.exit("hunspell failed: %s" % e)
    return sorted(set(w for w in out.split() if len(w) > 2 and not re.search(r"\d", w)))


def record_text(r):
    return " ".join([r.get("stem") or ""] + list((r.get("options") or {}).values()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("extracted")
    ap.add_argument("--gold", nargs="*", default=[])
    ap.add_argument("--offset", type=int, required=True, help="pdf_page - printed_page for this section")
    ap.add_argument("--qrange", help="expected first-last question numbers, e.g. 6-50")
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.extracted) if l.strip()]
    gold = {}
    for pattern in a.gold:
        for f in glob.glob(pattern):
            for l in open(f):
                if l.strip():
                    g = json.loads(l)
                    gold[g["id"]] = g
    flags = []

    def flag(level, rid, check, detail=""):
        flags.append((level, rid, check, detail))

    ids = [r.get("id") for r in recs]
    for d in sorted(set(i for i in ids if ids.count(i) > 1)):
        flag("FAIL", d, "duplicate-id")
    if a.qrange:
        lo, hi = map(int, a.qrange.split("-"))
        got = sorted(r.get("question_num") for r in recs)
        if got != list(range(lo, hi + 1)):
            missing = sorted(set(range(lo, hi + 1)) - set(got))
            extra = sorted(set(got) - set(range(lo, hi + 1)))
            flag("FAIL", "-", "question-numbers", "missing %s extra %s" % (missing, extra))

    for r in recs:
        rid = r.get("id", "?")
        miss = [k for k in REQUIRED if k not in r]
        if miss:
            flag("FAIL", rid, "schema-missing", ",".join(miss))
        m = ID_RE.match(rid)
        if not m:
            flag("FAIL", rid, "id-format")
        elif (m.group(1), int(m.group(2)), m.group(3), int(m.group(4))) != (
                r.get("subject_code"), r.get("chapter"), r.get("quiz_type"), r.get("question_num")):
            flag("FAIL", rid, "id-fields-mismatch")
        if r.get("pdf_page") is not None and r.get("printed_page") != r["pdf_page"] - a.offset:
            flag("FAIL", rid, "printed-page", "pdf %s printed %s" % (r.get("pdf_page"), r.get("printed_page")))

        opts = r.get("options")
        key = r.get("printed_key")
        if r.get("quiz_type") == "COMP":
            if opts:
                flag("FAIL", rid, "comp-has-options")
            if (r.get("stem") or "").count("_____") != 1:
                flag("FAIL", rid, "comp-blank-count", str((r.get("stem") or "").count("_____")))
            if not key:
                flag("WARN", rid, "no-key")
        else:
            if not isinstance(opts, dict) or sorted(opts) != list("ABCDE"):
                flag("FAIL", rid, "options-not-A-E", str(sorted(opts or {})))
            else:
                empty = [k for k, v in opts.items() if not (v or "").strip()]
                if empty:
                    flag("FAIL", rid, "empty-option", ",".join(empty))
                vals = [norm(v) for v in opts.values()]
                if len(set(vals)) < 5:
                    flag("WARN", rid, "identical-options", "check scan; keep as printed")
            if key is None:
                flag("WARN", rid, "no-key")
            elif key not in "ABCDE" or len(key) != 1:
                flag("FAIL", rid, "key-not-letter", repr(key))

        if r.get("ocr_flags"):
            flag("WARN", rid, "worker-ocr-flag", json.dumps(r["ocr_flags"], ensure_ascii=False)[:120])
        if isinstance(r.get("figure"), str) and r["figure"].startswith("NEEDED"):
            flag("WARN", rid, "figure-needed", r["figure"])

        # OCR support: the transcription should share most long words and every number with
        # Tesseract's text of the page. Low support means a misread, a wrong page, or handwriting.
        ocr = ocr_text(r.get("pdf_page") or 0)
        if not ocr:
            flag("WARN", rid, "no-ocr-text")
        else:
            ow, rw = words(ocr), words(record_text(r))
            if rw:
                support = len(rw & ow) / len(rw)
                if support < 0.7:
                    flag("WARN", rid, "low-ocr-support", "%.2f missing %s" % (support, sorted(rw - ow)[:6]))
            onum = set(re.findall(r"\d+", norm(ocr)))
            lost = sorted(set(re.findall(r"\d+", norm(record_text(r)))) - onum)
            if lost:
                flag("WARN", rid, "number-not-in-ocr", ",".join(lost[:8]))

        unknown = hunspell_unknown(record_text(r))
        if unknown:
            flag("INFO", rid, "unknown-words", ",".join(unknown[:10]))

        g = gold.get(rid)
        if g:
            for f in ("stem", "printed_key", "printed_page", "question_num"):
                if norm(str(g.get(f))).replace(" ", "") != norm(str(r.get(f))).replace(" ", ""):
                    flag("FAIL", rid, "gold-" + f, "gold=%r got=%r" % (g.get(f), r.get(f)))
            for k in "ABCDE":
                gv, rv = (g.get("options") or {}).get(k), (r.get("options") or {}).get(k)
                if norm(str(gv)).replace(" ", "") != norm(str(rv)).replace(" ", ""):
                    flag("FAIL", rid, "gold-option-" + k, "gold=%r got=%r" % (gv, rv))

    for f in flags:
        print("\t".join(map(str, f)))
    n_gold = sum(1 for r in recs if r.get("id") in gold)
    gold_bad = len({f[1] for f in flags if f[2].startswith("gold-")})
    counts = {lvl: sum(1 for f in flags if f[0] == lvl) for lvl in ("FAIL", "WARN", "INFO")}
    print("records=%d gold_controls=%d gold_mismatched=%d FAIL=%d WARN=%d INFO=%d warn_ids=%d" % (
        len(recs), n_gold, gold_bad, counts["FAIL"], counts["WARN"], counts["INFO"],
        len({f[1] for f in flags if f[0] == "WARN"})))
    sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
    main()
