#!/usr/bin/env python3
"""Textual mistake taxonomy: count OCR/notation defect classes in the live
collection and in the candidate .apkg (read-only). No images involved."""
import html
import json
import os
import re
import sqlite3
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = os.path.join(BASE, "colpkg", "collection_anki21b.db")
APKG = os.path.join(BASE, "apkg", "collection.anki2")
SEP = "\x1f"
TAG = re.compile(r"<[^>]+>")
OUT = os.path.join(BASE, "out", "patterns.json")

ROMAN_OK = (r"(?:gruppo|ordine|periodo|livello|anno|anni|legge|leggi|classe|grado|guerra|"
            r"tipo|serie|parte|punto|capitolo|cap|divisione|mondo|principio|fase|stadio|"
            r"semestre|anno|a\.c|d\.c|secolo|millennio|piano|universo|onda|esperimento)")

PATTERNS = [
    ("bracket-I noise (I] / fl] / l])", r"\b(?:fl|I|l|ii|II)\]\s"),
    ("II where Il expected", r"\bII\s+(?!" + ROMAN_OK + r"\b)[a-zàèéìòù]"),
    ("ll / l1 / 1l inside word", r"\b(?:ll|l1|1l|I1|1I)\s*[a-zàèéìòù]|\b[a-zàèéìòù]+1[a-zàèéìòù]{2,}\b"),
    ("0 written for o", r"\b[A-Za-z]{2,}0\b|\b0[A-Za-z]{2,}\b"),
    ("period inside formula", r"\b[A-Z][a-z]?\.[A-Za-z]|\b[A-Z]{1,2}\d?\.[,)]"),
    ("euro sign for 'e'", r"€"),
    ("hyphen-space inside word", r"[a-zàèéìòù]- [a-zàèéìòù]|[A-Z]{2,}- [A-Z]{2,}"),
    ("dangling operator at end", r"[+\-*/×·=≠<>]\s*$"),
    ("superscript/subscript lost as plain digit", r"\b(?:cm|mm|dm|km|m|kg|mg|g|L|ml|s|K|J|Pa|mol|Hz|W|V)\d\b"),
    ("leftover table pipe / checkbox", r"\||\|_\|"),
    ("stray bracket before word", r"\[[a-zàèéìòù]"),
]


def ro(path):
    c = sqlite3.connect("file:%s?mode=ro&immutable=1" % path, uri=True)
    c.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                       - (a.casefold() < b.casefold()))
    return c


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", s))).strip()


def load(path, restrict_semestre):
    conn = ro(path)
    q = "select flds from notes"
    if restrict_semestre:
        q = ("select flds from notes n join notetypes t on t.id=n.mid "
             "where t.name like 'Semestre%'")
    out = []
    for (flds,) in conn.execute(q):
        f = flds.split(SEP)
        if len(f) < 14:
            continue
        text = " ".join([f[8], f[10], f[12], f[13] if len(f) > 13 else ""])
        out.append({"id": f[0], "qtype": f[5], "stem": plain(f[8]),
                    "text": plain(text), "raw_stem": f[8],
                    "raw_options": f[10], "banner": plain(f[12]),
                    "has_sol": "<img" in (f[16] if len(f) > 16 else "")})
    return out


live = load(LIVE, True)
apkg = load(APKG, False)


def scan(rows):
    res = {}
    for name, rx in PATTERNS:
        rxc = re.compile(rx)
        res[name] = [r for r in rows if rxc.search(r["text"])]
    # structural checks that a regex cannot express
    res["completamento card with no visible blank"] = [
        r for r in rows if "completamento" in r["qtype"].lower()
        and "blank-slot" not in r["raw_stem"] and "___" not in r["stem"]]
    dup, badkey, noopt = [], [], []
    for r in rows:
        opts = re.findall(
            r'<span class="opt-letter">([A-E])</span>\s*<span class="opt-body">(.*?)</span>',
            r["raw_options"], re.S)
        texts = [plain(t) for _, t in opts]
        if len(texts) != len(set(texts)):
            dup.append(r)
        if not opts and "completamento" not in r["qtype"].lower():
            noopt.append(r)
        m = re.search(r"Risposta corretta:\s*([A-E])", r["banner"])
        if m and m.group(1) not in [c for c, _ in opts] and opts:
            badkey.append(r)
    res["duplicate option text in same card"] = dup
    res["answer letter not among options"] = badkey
    res["no parseable options (MCQ)"] = noopt
    return res


live_res = scan(live)
apkg_res = scan(apkg)

report = {}
for name in live_res:
    report[name] = {
        "live": len(live_res[name]),
        "apkg": len(apkg_res[name]),
        "live_ids": [r["id"] for r in live_res[name][:25]],
        "apkg_ids": [r["id"] for r in apkg_res[name][:25]],
    }

print("%-46s %6s %6s" % ("pattern", "live", "apkg"))
for name in live_res:
    print("%-46s %6d %6d" % (name, report[name]["live"], report[name]["apkg"]))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"live_n": len(live), "apkg_n": len(apkg), "patterns": report},
          open(OUT, "w"), indent=1, ensure_ascii=False)
print("\nwrote", OUT)
