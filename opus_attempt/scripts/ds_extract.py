"""DeepSeek extraction for one chapter: build page jobs, then parse results into extracted.jsonl records.

  ds_extract.py jobs  --pagemap build/chim_ch1_pagemap.json --workdir work/deepseek/chim01
  deepseek_batch.py   work/deepseek/chim01/jobs.jsonl work/deepseek/chim01/results.jsonl
  ds_extract.py parse --pagemap build/chim_ch1_pagemap.json --workdir work/deepseek/chim01

One job per question page (that page + the next, so a question crossing the page break is complete),
plus one job per key section. Records follow STRUCTURE.md; crops are left null for the crop step.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

SUBJECTS = {"CHIM": "Chimica e Propedeutica Biochimica", "BIO": "Biologia e Genetica", "FIS": "Fisica"}

RULES = """Rules: two columns, read left then right. Ignore all handwriting; printed text only. Copy exactly as printed, no fixes; rejoin words hyphenated at line ends. Plain text with Unicode formulas (H₂SO₄, 10⁻⁹, Na⁺, →, ⇌, ×, °C). Unreadable text: write [?] and list it in "unreadable". Reply with JSON only."""

QUESTION_PROMPT = """This is one page of the section "{label}" of chapter {chapter} ("{title}"). Transcribe every numbered question on it, in order.
If the page starts with the end of a question from the previous page (text before the first number), put that text in "continued_top". If the last question is cut off at the bottom, transcribe what is visible and set "incomplete": true.
{kind}
{rules}
JSON shape: {{"continued_top": null or {{"stem_tail": str, {opt_shape_top}}}, "questions": [{{"question_num": int, "stem": str, {opt_shape}"incomplete": bool, "figure_needed": null or "short description of a needed picture/table", "unreadable": [str]}}]}}"""

MCQ_KIND = 'Each question: number, stem, options A-E.'
MCQ_SHAPE = '"options": {"A": str, "B": str, "C": str, "D": str, "E": str}, '
COMP_KIND = 'Fill-in sentences: write the blank as _____ (one per question), even if a word is handwritten in it.'

KEY_PROMPTS = {
    "COMM": """These images are from the answers section ("RISPOSTE") of the book. Find the solutions to chapter {chapter} ("{title}"), section "Quiz commentati", questions {q0}-{q1}. For each question give the printed answer letter and the printed reasoning text.
{rules}
JSON shape: {{"answers": [{{"question_num": int, "key": "A-E", "reasoning": str, "unreadable": [str]}}]}}""",
    "NCOM": """These images are from the answers section ("RISPOSTE") of the book. Find the answer key of chapter {chapter} ("{title}"), section "Quiz non commentati", questions {q0}-{q1} (usually a table of number + letter). Give every entry.
{rules}
JSON shape: {{"answers": [{{"question_num": int, "key": "A-E", "unreadable": [str]}}]}}""",
    "COMP": """These images are from the answers section ("RISPOSTE") of the book. Find the solutions of chapter {chapter} ("{title}"), section "Quiz a completamento", questions {q0}-{q1} (usually a numbered word list). Give every entry exactly as printed.
{rules}
JSON shape: {{"answers": [{{"question_num": int, "key": str, "unreadable": [str]}}]}}""",
}


def render(pdf_page, workdir):
    out = Path(workdir) / "pages" / ("p%03d.jpg" % pdf_page)
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        prefix = out.with_suffix("")
        subprocess.run(["pdftoppm", "-r", "200", "-gray", "-singlefile", "-jpeg", "-jpegopt", "quality=85", "-f", str(pdf_page),
                        "-l", str(pdf_page), "book.pdf", str(prefix)], check=True)
    return str(out)


def load_map(path):
    m = json.load(open(path))
    m.setdefault("subject", "CHIM")
    return m


def cmd_jobs(a):
    m = load_map(a.pagemap)
    jobs = []
    for sec in m["sections"]:
        qt = sec["quiz_type"]
        p0, p1 = sec["pdf_pages"]
        for p in range(p0, p1 + 1):
            imgs = [render(p, a.workdir)]
            prompt = QUESTION_PROMPT.format(
                label=sec["label"], chapter=m["chapter"], title=m["title"],
                kind=COMP_KIND if qt == "COMP" else MCQ_KIND, rules=RULES,
                opt_shape_top="" if qt == "COMP" else '"options": {letter: str} (only those shown)',
                opt_shape="" if qt == "COMP" else MCQ_SHAPE)
            jobs.append({"id": "q-%s-p%03d" % (qt, p), "prompt": prompt, "images": imgs, "max_tokens": 6000,
                         "reasoning": False})
    for sol in m["solution_pages"]:
        qt = sol["quiz_type"]
        sec = next(s for s in m["sections"] if s["quiz_type"] == qt)
        p0, p1 = sol["pdf_pages"]
        q0, q1 = sec["question_numbers"]
        imgs = [render(p, a.workdir) for p in range(p0, p1 + 1)]
        prompt = KEY_PROMPTS[qt].format(chapter=m["chapter"], title=m["title"], q0=q0, q1=q1, rules=RULES)
        jobs.append({"id": "k-%s" % qt, "prompt": prompt, "images": imgs, "max_tokens": 6000})
    out = Path(a.workdir) / "jobs.jsonl"
    with open(out, "w", encoding="utf-8") as f:
        for j in jobs:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    print("wrote %d jobs to %s" % (len(jobs), out))


def parse_json(content):
    s = content.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    return json.loads(s)


HUNSPELL_DICT = "/Users/db/Documents/projects/anki/_tools/it_IT"
OPTION_LINE = re.compile(r"(?:^|\s)([A-E])\.\s+(.+?)(?=\s+[A-E]\.\s|$)", re.S)


def split_inline_options(text):
    """'stem B. x C. y' -> ('stem', {'B': 'x', 'C': 'y'}); used when a model puts options into the stem tail."""
    m = re.search(r"(?:^|\s)[A-E]\.\s", text)
    if not m:
        return text, {}
    head, rest = text[:m.start()].strip(), text[m.start():]
    return head, {k: re.sub(r"\s+", " ", v).strip() for k, v in OPTION_LINE.findall(rest)}


def known_words(words):
    if not words:
        return set()
    try:
        out = subprocess.run(["hunspell", "-d", HUNSPELL_DICT, "-l"], input="\n".join(words),
                             capture_output=True, text=True, timeout=60, check=True).stdout
    except (OSError, subprocess.SubprocessError) as e:
        sys.exit("hunspell failed: %s" % e)
    return set(words) - set(out.split())


def dehyphenate(records):
    """Rejoin words split at line ends ('polistiro- lo', 'combu-stione'). Joined only if the dictionary
    knows the joined word, so 'mono- o poliatomica' and real compounds stay as printed."""
    def fields(r):
        yield r, "stem"
        for k in (r.get("options") or {}):
            yield r["options"], k
        if r.get("printed_reasoning"):
            yield r, "printed_reasoning"
    split = re.compile(r"(\w+)-\s*(\w+)")
    cands = set()
    for r in records:
        for obj, k in fields(r):
            cands.update(a + b for a, b in split.findall(obj[k]))
    ok = known_words(sorted(cands))
    for r in records:
        for obj, k in fields(r):
            obj[k] = split.sub(lambda m: m.group(1) + m.group(2)
                               if m.group(1) + m.group(2) in ok else m.group(0), obj[k])


def tidy(r):
    """Deterministic repairs of known model habits; each one is noted in worker_notes."""
    key = r.get("printed_key") or ""
    # Fill-in: the model sometimes copies a handwritten answer into the blank.
    if r["quiz_type"] == "COMP" and "_____" not in r["stem"] and key and r["stem"].count(key) == 1:
        r["stem"] = r["stem"].replace(key, "_____")
        r["worker_notes"] += "; blank restored (handwritten answer was transcribed)"
    # Handwriting after the question that repeats one of the options.
    for v in (r.get("options") or {}).values():
        if v and r["stem"].rstrip().endswith(" " + v.strip()) and len(r["stem"]) > len(v) + 5:
            r["stem"] = r["stem"].rstrip()[: -len(v.strip())].rstrip()
            r["worker_notes"] += "; removed option text appended to stem (handwriting)"
            break
    # Printed bullet statements A₁ A₂ A₃ need a separator in plain text.
    r["stem"] = re.sub(r"(?<=[^;:\s]) (A[₁₂₃₄₅₆])(?= )", r"; \1", r["stem"])


def merge_continuation(rec, top, page):
    """Join a question cut at a page bottom with the text that finishes it on the next page."""
    tail = (top.get("stem_tail") or "").strip()
    opts = rec.get("options")
    if opts is not None:
        tail, inline = split_inline_options(tail)
        top = dict(top, options={**inline, **(top.get("options") or {})})
    if tail:
        rec["stem"] = (rec["stem"].rstrip() + " " + tail).strip()
    for letter, text in (top.get("options") or {}).items():
        if opts is not None and (not (opts.get(letter) or "").strip() or "[?]" in opts.get(letter, "")):
            opts[letter] = text
    # Flags raised only because the question was cut off are resolved once nothing is missing.
    if "[?]" not in rec["stem"] and not any("[?]" in (v or "") for v in (opts or {}).values()):
        rec["ocr_flags"] = [f for f in rec["ocr_flags"] if f["page"] != rec["pdf_page"]]
    rec["worker_notes"] += "; continued on pdf %d" % page


def cmd_parse(a):
    m = load_map(a.pagemap)
    subj = m["subject"]
    results = {}
    for line in open(Path(a.workdir) / "results.jsonl"):
        r = json.loads(line)
        if r.get("status") == "ok":
            results[r["id"]] = r  # last ok result wins
    problems = []
    keys = {}
    for qt in ("COMM", "NCOM", "COMP"):
        r = results.get("k-" + qt)
        if not r:
            problems.append("missing key job k-" + qt)
            continue
        try:
            for ans in parse_json(r["content"])["answers"]:
                keys[(qt, ans["question_num"])] = ans
        except (ValueError, KeyError) as e:
            problems.append("k-%s unparsable: %s" % (qt, e))

    records = {}
    for sec in m["sections"]:
        qt = sec["quiz_type"]
        p0, p1 = sec["pdf_pages"]
        key_page = next(s["printed_pages"][0] for s in m["solution_pages"] if s["quiz_type"] == qt)
        pending = None  # last record of the previous page, if it was cut off at the bottom
        for p in range(p0, p1 + 1):
            jid = "q-%s-p%03d" % (qt, p)
            r = results.get(jid)
            if not r:
                problems.append("missing " + jid)
                continue
            if r.get("finish_reason") not in (None, "stop"):
                problems.append("%s finish_reason=%s" % (jid, r.get("finish_reason")))
            try:
                data = parse_json(r["content"])
                qs = data["questions"]
            except (ValueError, KeyError) as e:
                problems.append("%s unparsable: %s" % (jid, e))
                pending = None
                continue
            top = data.get("continued_top")
            m_num = re.match(r"\s*(\d+)\)\s*(.*)", (top or {}).get("stem_tail") or "", re.S)
            if top and not pending and m_num:
                # The model filed a whole numbered question as a continuation; treat it as a question.
                qs = [{"question_num": int(m_num.group(1)), "stem": m_num.group(2), "options": top.get("options"),
                       "unreadable": [], "figure_needed": None}] + qs
                top = None
            if top and pending:
                merge_continuation(pending, top, p)
            elif top:
                problems.append("%s has continued_top but the previous page has no incomplete question" % jid)
            elif pending:
                problems.append("%s incomplete on page %d but page %d has no continued_top" % (pending["id"], p - 1, p))
            pending = None
            for q in qs:
                n = int(q["question_num"])
                rid = "%s-C%02d-%s-%03d" % (subj, m["chapter"], qt, n)
                if rid in records:
                    problems.append("%s seen twice (pages %s and %s)" % (rid, records[rid]["pdf_page"], p))
                    continue
                k = keys.get((qt, n), {})
                flags = [{"span": u, "page": p, "status": "ocr_fallback_needed"} for u in q.get("unreadable") or []]
                flags += [{"span": u, "page": key_page, "status": "ocr_fallback_needed", "where": "key"}
                          for u in k.get("unreadable") or []]
                fig = q.get("figure_needed")
                records[rid] = {
                    "id": rid, "subject_code": subj, "subject": SUBJECTS[subj], "chapter": m["chapter"],
                    "chapter_title": m["title"], "quiz_type": qt, "question_num": n, "pdf_page": p,
                    "printed_page": p - m["offset"], "stem": q["stem"],
                    "options": None if qt == "COMP" else q.get("options"),
                    "printed_key": k.get("key"), "key_page": key_page if k else None,
                    "printed_reasoning": k.get("reasoning") if qt == "COMM" else None,
                    "figure": ("NEEDED: " + fig) if fig else None, "figure_side": "front",
                    "question_crop": None, "solution_crop": None, "ocr_flags": flags,
                    "worker_notes": "deepseek:" + jid}
                if q.get("incomplete"):
                    pending = records[rid]
        q0, q1 = sec["question_numbers"]
        for n in range(q0, q1 + 1):
            if "%s-C%02d-%s-%03d" % (subj, m["chapter"], qt, n) not in records:
                problems.append("not found: %s Q%d" % (qt, n))
    dehyphenate(records.values())
    for r in records.values():
        tidy(r)
    out = Path(a.workdir) / "extracted.jsonl"
    order = sorted(records.values(), key=lambda r: (["COMM", "NCOM", "COMP"].index(r["quiz_type"]), r["question_num"]))
    with open(out, "w", encoding="utf-8") as f:
        for r in order:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("records=%d -> %s" % (len(order), out))
    for p in problems:
        print("PROBLEM", p)
    sys.exit(1 if problems else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["jobs", "parse"])
    ap.add_argument("--pagemap", required=True)
    ap.add_argument("--workdir", required=True)
    a = ap.parse_args()
    {"jobs": cmd_jobs, "parse": cmd_parse}[a.cmd](a)


if __name__ == "__main__":
    main()
