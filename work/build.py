#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the answer key JSONL for the 257 flagged cards.

    python3 work/build.py \
        --input-dir   /tmp/answer_key_request \
        --overrides   work/answer_text_fixes.py \
        --parts-dir   work \
        --out         answer_key_output.jsonl \
        --chunks-dir  answer_key_chunks

Output contract
---------------
* one JSON object per line, same ids and same order as NEEDED.jsonl
* MCQ   : id, letter, answer_text, printed_text?, reason, confidence, flags
* cloze : id, answers, reason, confidence, flags

`letter` is the answer. `answer_text` is ALWAYS options[letter] of the matching
NEEDED record, verbatim, so that a consumer which re-derives the text from the
card always agrees with this file. Where the deck's option string is OCR damage
of the page, the restored text goes in the optional `printed_text` field, whose
only source is the override map.
"""
import argparse
import importlib.util
import json
import os
import sys

FLAG_ORDER = [
    "needs_figure", "ambiguous", "no_correct_option",
    "multiple_correct", "typo", "out_of_syllabus",
]


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_answers(parts_dir):
    """Merge the A dict of every answers_part*.py in parts_dir."""
    merged = {}
    names = sorted(
        f[:-3] for f in os.listdir(parts_dir)
        if f.startswith("answers_part") and f.endswith(".py")
    )
    if not names:
        sys.exit(f"no answers_part*.py found in {parts_dir}")
    for name in names:
        mod = load_module(os.path.join(parts_dir, name + ".py"), name)
        merged.update(mod.A)
    return merged, names


def ordered_flags(flags):
    """Deduplicate and sort flags canonically so output is stable."""
    unknown = set(flags) - set(FLAG_ORDER)
    if unknown:
        sys.exit(f"unknown flag(s): {sorted(unknown)}")
    return [f for f in FLAG_ORDER if f in set(flags)]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", required=True,
                    help="directory holding NEEDED.jsonl")
    ap.add_argument("--overrides", required=True,
                    help="answer_text_fixes.py (id -> printed text)")
    ap.add_argument("--parts-dir", default=os.path.dirname(os.path.abspath(__file__)),
                    help="directory holding answers_part*.py (default: next to this script)")
    ap.add_argument("--out", required=True, help="output JSONL path")
    ap.add_argument("--chunks-dir", required=True, help="output directory for chunk_*.jsonl")
    ap.add_argument("--chunk-size", type=int, default=100)
    ap.add_argument("--stats", help="optional path for a JSON stats blob")
    args = ap.parse_args()

    needed = os.path.join(args.input_dir, "NEEDED.jsonl")
    rows = [json.loads(line) for line in open(needed, encoding="utf-8")]
    answers, part_names = load_answers(args.parts_dir)
    fix = load_module(args.overrides, "answer_text_fixes").FIX

    missing = [r["id"] for r in rows if r["id"] not in answers]
    extra = [i for i in answers if i not in {r["id"] for r in rows}]
    if missing or extra:
        sys.exit(f"answer/record mismatch: missing={missing} extra={extra}")

    out, errors, with_printed = [], [], 0
    for rec in rows:
        a = answers[rec["id"]]
        o = {"id": rec["id"]}

        if rec["type"] == "mcq":
            if a["kind"] != "mcq":
                errors.append((rec["id"], "type"))
            opts = rec["options"]
            letter = a["letter"]
            if letter not in opts:
                errors.append((rec["id"], f"letter {letter!r} not in options"))
                continue
            o["letter"] = letter
            # verbatim, never overridden -- a consumer re-derives this from the card
            o["answer_text"] = opts[letter]
            # restored print text, only where the override map has something else
            printed = fix.get(rec["id"])
            if printed is not None and printed != opts[letter]:
                o["printed_text"] = printed
                with_printed += 1
        else:
            if a["kind"] != "cloze":
                errors.append((rec["id"], "type"))
            if len(a["answers"]) != rec["blanks"]:
                errors.append((rec["id"], f"{len(a['answers'])} answers for {rec['blanks']} blanks"))
            o["answers"] = list(a["answers"])

        o["reason"] = a["reason"]
        o["confidence"] = a["conf"]

        # final flags = whole-author flags from the part file
        #             U flags implied by the NEEDED record
        flags = list(a["flags"])
        if "figure" in rec:
            flags.append("needs_figure")
        o["flags"] = ordered_flags(flags)

        out.append(o)

    if errors:
        sys.exit(f"build errors: {errors}")

    # --- full file -------------------------------------------------------
    blob = "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(blob)

    # --- chunks, byte-exact split of the same blob -----------------------
    os.makedirs(args.chunks_dir, exist_ok=True)
    lines = blob.splitlines(keepends=True)
    for i in range(0, len(lines), args.chunk_size):
        part = lines[i:i + args.chunk_size]
        path = os.path.join(args.chunks_dir, f"chunk_{i // args.chunk_size:03d}.jsonl")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("".join(part))

    stats = {
        "rows": len(out),
        "mcq": sum(1 for o in out if "letter" in o),
        "cloze": sum(1 for o in out if "answers" in o),
        "printed_text_rows": with_printed,
        "confidence": {c: sum(1 for o in out if o["confidence"] == c)
                       for c in ("high", "medium", "low")},
        "flags": {f: sum(1 for o in out if f in o["flags"]) for f in FLAG_ORDER},
        "part_modules": part_names,
        "inputs": {"needed": os.path.abspath(needed),
                   "overrides": os.path.abspath(args.overrides),
                   "parts_dir": os.path.abspath(args.parts_dir)},
        "outputs": {"out": os.path.abspath(args.out),
                    "chunks_dir": os.path.abspath(args.chunks_dir)},
    }
    if args.stats:
        with open(args.stats, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
            f.write("\n")

    print(f"wrote {args.out}: {stats['rows']} rows "
          f"({stats['mcq']} mcq, {stats['cloze']} cloze), "
          f"printed_text on {with_printed}, "
          f"confidence {stats['confidence']}")
    print(f"flags: {stats['flags']}")


if __name__ == "__main__":
    main()
