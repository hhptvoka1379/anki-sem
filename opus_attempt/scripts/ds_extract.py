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

RULES = """Rules:
- The page is a scan of an Italian quiz book. Pages have two columns: read the left column top to bottom, then the right column.
- Students wrote on the scans (circles, ticks, crosses, handwritten words or letters). Ignore all handwriting completely. Transcribe only printed text. Never use handwriting as an answer.
- Transcribe exactly as printed, including mistakes. Do not correct, translate or summarise.
- Plain text. Write chemistry and maths with Unicode: subscripts (H₂SO₄), superscripts (10⁻⁹, Na⁺, m²), →, ⇌, ×, ·, °C, ≤, ≥. Join words hyphenated across a line break.
- If any printed text is unreadable, put the exact place in "unreadable" and write [?] in the text. Do not guess.
- Answer with JSON only, no comments, no code fences."""

QUESTION_PROMPT = """Image 1 is a page of the section "{label}" of chapter {chapter} ("{title}").{next_note}
Transcribe every question whose number STARTS on image 1. Ignore text at the top of image 1 that finishes a question begun on an earlier page.{cont_note}
{kind}
{rules}
JSON shape: {{"questions": [{{"question_num": int, "stem": str, {opt_shape}"figure_needed": null or "short description of a picture/diagram/table the question needs that is not text", "unreadable": [str]}}]}}"""

MCQ_KIND = 'Each question has a number, a stem and five options A-E. Put the options in "options".'
MCQ_SHAPE = '"options": {"A": str, "B": str, "C": str, "D": str, "E": str}, '
COMP_KIND = ('These are fill-in-the-blank sentences. Write the blank as exactly five underscores _____ '
             '(one blank per question). Handwritten words in the blank must be ignored: the blank stays _____.')

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
            has_next = p < p1
            if has_next:
                imgs.append(render(p + 1, a.workdir))
            prompt = QUESTION_PROMPT.format(
                label=sec["label"], chapter=m["chapter"], title=m["title"],
                next_note=" Image 2 is the next page." if has_next else "",
                cont_note=" If the last question on image 1 continues on image 2, complete it from image 2. Do not transcribe questions that start on image 2." if has_next else "",
                kind=COMP_KIND if qt == "COMP" else MCQ_KIND, rules=RULES,
                opt_shape="" if qt == "COMP" else MCQ_SHAPE)
            jobs.append({"id": "q-%s-p%03d" % (qt, p), "prompt": prompt, "images": imgs, "max_tokens": 12000})
    for sol in m["solution_pages"]:
        qt = sol["quiz_type"]
        sec = next(s for s in m["sections"] if s["quiz_type"] == qt)
        p0, p1 = sol["pdf_pages"]
        q0, q1 = sec["question_numbers"]
        imgs = [render(p, a.workdir) for p in range(p0, p1 + 1)]
        prompt = KEY_PROMPTS[qt].format(chapter=m["chapter"], title=m["title"], q0=q0, q1=q1, rules=RULES)
        jobs.append({"id": "k-%s" % qt, "prompt": prompt, "images": imgs, "max_tokens": 12000})
    out = Path(a.workdir) / "jobs.jsonl"
    with open(out, "w", encoding="utf-8") as f:
        for j in jobs:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    print("wrote %d jobs to %s" % (len(jobs), out))


def parse_json(content):
    s = content.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    return json.loads(s)


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
        for p in range(p0, p1 + 1):
            jid = "q-%s-p%03d" % (qt, p)
            r = results.get(jid)
            if not r:
                problems.append("missing " + jid)
                continue
            if r.get("finish_reason") not in (None, "stop"):
                problems.append("%s finish_reason=%s" % (jid, r.get("finish_reason")))
            try:
                qs = parse_json(r["content"])["questions"]
            except (ValueError, KeyError) as e:
                problems.append("%s unparsable: %s" % (jid, e))
                continue
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
        q0, q1 = sec["question_numbers"]
        for n in range(q0, q1 + 1):
            if "%s-C%02d-%s-%03d" % (subj, m["chapter"], qt, n) not in records:
                problems.append("not found: %s Q%d" % (qt, n))
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
