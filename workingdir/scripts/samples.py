#!/usr/bin/env python3
"""Pick a stratified sample of live cards *with* their crops and write per-agent
briefs (markdown) for image-vs-card verification. Read-only on the DBs."""
import html
import json
import os
import random
import re
import sqlite3

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(BASE, "colpkg", "collection_anki21b.db")
MEDIA = os.path.join(BASE, "samples", "media")
SEP = "\x1f"
SEED = 20261021
NOTE_RX = re.compile(r"[\u2070\u00b9\u00b2\u00b3\u2074-\u2079\u207a\u207b\u2080-\u2089"
                     r"\u221a\u2260\u00d7\u00b7\u22c5]|<sup|<sub|\^")
TAG_RX = re.compile(r"<[^>]+>")


def ro(path):
    c = sqlite3.connect("file:%s?mode=ro&immutable=1" % path, uri=True)
    c.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                       - (a.casefold() < b.casefold()))
    return c


def plain(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(TAG_RX.sub(" ", s))).strip()


def options(s):
    out = []
    for m in re.finditer(r'<span class="opt-letter">([A-E])</span>\s*'
                         r'<span class="opt-body">(.*?)</span>', s, re.S):
        out.append((m.group(1), plain(m.group(2))))
    return out


def img(s):
    m = re.search(r'<img[^>]*src="([^"]+)"', s)
    return m.group(1) if m else None


conn = ro(LIVE)
cards = []
for r in conn.execute(
        "select n.id, n.flds, n.tags from notes n join notetypes t on t.id=n.mid "
        "where t.name like 'Semestre%'"):
    f = r[1].split(SEP)
    cards.append({
        "id": f[0], "subject": f[2], "chapter": f[3], "chapter_title": f[4],
        "qtype": f[5], "qnum": f[6], "page": f[7],
        "stem": plain(f[8]), "options": options(f[10]),
        "answer": plain(f[12]), "explanation": plain(f[13]),
        "q_img": img(f[15]), "sol_img": img(f[16]),
        "notation": bool(NOTE_RX.search(f[8] + f[10] + f[12] + f[13])),
    })

by_key = {c["id"]: c for c in cards}
rnd = random.Random(SEED)


def pick(pool, n, exclude):
    pool = [c for c in pool if c["id"] not in exclude]
    rnd.shuffle(pool)
    chosen = pool[:n]
    exclude |= {c["id"] for c in chosen}
    return chosen


used = set()
notation = [c for c in cards if c["notation"]]
plain_pool = [c for c in cards if not c["notation"]]
sol = [c for c in cards if c["sol_img"]]
sol_notation = [c for c in sol if c["notation"]]

plan = []
plan.append(("agent1", "CHIM notation", pick([c for c in notation if c["subject"] == "CHIM"], 5, used)))
plan.append(("agent2", "CHIM notation", pick([c for c in notation if c["subject"] == "CHIM"], 5, used)))
plan.append(("agent3", "CHIM notation", pick([c for c in notation if c["subject"] == "CHIM"], 5, used)))
plan.append(("agent4", "CHIM random", pick([c for c in cards if c["subject"] == "CHIM"], 5, used)))
plan.append(("agent5", "FIS", pick([c for c in cards if c["subject"] == "FIS"], 5, used)))
plan.append(("agent6", "BIO", pick([c for c in cards if c["subject"] == "BIO"], 5, used)))
plan.append(("agent7", "solution crops + notation", pick(sol_notation, 5, used)))
plan.append(("agent8", "solution crops", pick(sol, 5, used)))

outdir = os.path.join(BASE, "samples")
os.makedirs(outdir, exist_ok=True)
manifest = {}
for name, label, chosen in plan:
    manifest[name] = {"label": label, "cards": chosen}
    lines = ["# Card/image sample - %s (%s)" % (name, label), "",
             "%d cards. Compare each card text with its crop(s)." % len(chosen), ""]
    for c in chosen:
        lines.append("## %s" % c["id"])
        lines.append("")
        lines.append("- subject: %s | chapter %s %s | %s | book page %s"
                     % (c["subject"], c["chapter"], c["chapter_title"], c["qtype"], c["page"]))
        lines.append("- question crop: %s" % os.path.join(MEDIA, c["q_img"])
                     if c["q_img"] else "- question crop: (none)")
        if c["sol_img"]:
            lines.append("- solution crop: %s" % os.path.join(MEDIA, c["sol_img"]))
        lines.append("")
        lines.append("**Card stem (OCR text):** %s" % c["stem"])
        lines.append("")
        for letter, text in c["options"]:
            lines.append("- %s. %s" % (letter, text))
        lines.append("")
        lines.append("**Answer banner:** %s" % c["answer"])
        lines.append("")
        lines.append("**Explanation (book commentary, OCR):** %s" % c["explanation"])
        lines.append("")
    with open(os.path.join(outdir, name + ".md"), "w") as fh:
        fh.write("\n".join(lines))

json.dump(manifest, open(os.path.join(outdir, "manifest.json"), "w"), indent=1, ensure_ascii=False)

names = set()
for _, _, chosen in plan:
    for c in chosen:
        if c["q_img"]:
            names.add(c["q_img"])
        if c["sol_img"]:
            names.add(c["sol_img"])
print("cards:", sum(len(x[2]) for x in plan), "images:", len(names))
print("per agent:", [(n, len(ch)) for n, _, ch in plan])
open(os.path.join(outdir, "media_list.txt"), "w").write("\n".join(sorted(names)))
