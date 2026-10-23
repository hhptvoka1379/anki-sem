#!/usr/bin/env python3
"""Verification gates 1-9 for the Semestre Filtro .apkg (PROMPT.md section 7).

Usage:
  run_gates.py <apkg> --extracted build/extracted.jsonl --verification build/verification.jsonl \
      --page-map build/page_map.json --unverified UNVERIFIED.md --out build/verification_report.md \
      [--chapters CHIM-C01 ...] [--sample 3] [--no-render] [--keep-test-collection]

Exit code 0 only when no gate is FAIL. Gates 5 (formulas) and 9 (visual) need a human and
are reported MANUAL, so the report never says "all passed" unless every gate is PASS.
Never launches Anki.app and never touches ~/Library/Application Support/Anki2.
"""
import argparse
import collections
import datetime
import html
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unicodedata
import urllib.parse
import zipfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # opus_attempt/
HUNSPELL_BASE = "/Users/db/Documents/projects/anki/_tools/it_IT"

MODEL_NAME = "Semestre Filtro — Quiz & Completamento"
FRONTED_FIELDS = ["ItemID", "Subject", "SubjectCode", "ChapterNum", "ChapterTitle", "QuizTypeLabel",
                  "QuestionNum", "BookPage", "FrontStemHTML", "BackStemHTML", "FrontOptionsHTML",
                  "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML", "FigureHTML",
                  "QuestionScanHTML", "SolutionScanHTML", "TypedAnswer", "AcceptedAnswers", "NoteHTML"]
FONTS = ["_SpaceGrotesk-Variable.ttf", "_SpaceMono-Regular.ttf", "_SpaceMono-Bold.ttf", "_Syne-Variable.ttf"]
STATUSES = ["verified", "book-corrected", "derived", "unverified"]
REASONS = ["ocr", "no-key", "figure", "ambiguous", "disputed"]
ID_RE = re.compile(r"\b[A-Z]{3,4}-C\d{2}-(?:COMM|NCOM|COMP)-\d{3}\b")
MCQ_TYPES = ("COMM", "NCOM")

PASS, FAIL, MANUAL = "PASS", "FAIL", "MANUAL"


# ----------------------------------------------------------------------------- helpers
class Gate:
    def __init__(self, num, title, check):
        self.num, self.title, self.check = num, title, check
        self.lines = []
        self.problems = 0
        self.status = None  # set by finish()

    def out(self, msg):
        self.lines.append(msg)

    def bad(self, msg):
        self.problems += 1
        if self.problems <= 30:
            self.lines.append("FAIL: " + msg)
        elif self.problems == 31:
            self.lines.append("FAIL: ... further problems not listed (counted in the total)")

    def finish(self, manual_note=None):
        if self.problems:
            self.status = FAIL
            self.lines.append(f"{self.problems} problem(s).")
        elif manual_note:
            self.status = MANUAL
            self.lines.append(manual_note)
        else:
            self.status = PASS
        return self.status


TAG_RE = re.compile(r"<[^>]*>")
WELLFORMED_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>|<!--.*?-->", re.S)


def strip_scripts(h):
    h = re.sub(r"<script\b.*?</script\s*>", "", h, flags=re.S | re.I)
    h = re.sub(r"<script\b[^>]*/>", "", h, flags=re.I)
    return h


def plain(h):
    """Tags removed without inserting spaces (for spacing checks)."""
    return html.unescape(TAG_RE.sub("", strip_scripts(h or "")))


def spaced(h):
    """Tags replaced by a space (for word extraction and visible-text checks)."""
    return html.unescape(TAG_RE.sub(" ", strip_scripts(h or "")))


def collapse(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()


def norm_cmp(s):
    return collapse(s).casefold()


class OptParser(HTMLParser):
    """Collects elements whose class list contains the token 'opt'."""
    VOID = {"br", "img", "hr", "input", "meta", "link", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.opts = []
        self.cur = None
        self.depth = 0
        self.stack = []  # per open tag inside an opt: is_letter

    def handle_starttag(self, tag, attrs):
        tokens = (dict(attrs).get("class") or "").split()
        if self.cur is None:
            if "opt" in tokens:
                self.cur = {"tokens": tokens, "text": [], "letter": []}
                self.opts.append(self.cur)
                self.depth = 1
                self.stack = [False]
            return
        if tag in self.VOID:
            return
        self.depth += 1
        self.stack.append("opt-letter" in tokens)

    def handle_endtag(self, tag):
        if self.cur is None or tag in self.VOID:
            return
        self.depth -= 1
        if self.stack:
            self.stack.pop()
        if self.depth <= 0:
            self.cur = None

    def handle_data(self, data):
        if self.cur is None:
            return
        (self.cur["letter"] if any(self.stack) else self.cur["text"]).append(data)


def parse_options(h):
    p = OptParser()
    p.feed(h or "")
    res = []
    for o in p.opts:
        text = collapse("".join(o["text"]))
        letter = re.sub(r"[()\s.]", "", "".join(o["letter"]))
        if not letter:
            m = re.match(r"\(?([A-E])\)?[.\s]", text)
            if m:
                letter, text = m.group(1), collapse(text[m.end():])
        res.append({"letter": letter, "text": text, "correct": "correct" in o["tokens"]})
    return res


def jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise SystemExit(f"{path}:{n}: invalid JSON: {e}")
    return rows


def id_parts(item_id):
    m = re.match(r"^([A-Z]{3,4})-C(\d{2})-(COMM|NCOM|COMP)-(\d{3})$", item_id or "")
    return (m.group(1), int(m.group(2)), m.group(3)) if m else None


def chapter_of(item_id):
    m = re.match(r"^([A-Z]{3,4}-C\d{2})-", item_id or "")
    return m.group(1) if m else None


# ----------------------------------------------------------------------------- package loading
class Package:
    def __init__(self, apkg, workdir):
        self.dir = Path(workdir)
        with zipfile.ZipFile(apkg) as z:
            self.names = z.namelist()
            z.extractall(self.dir)
        self.db_name = next((n for n in ("collection.anki21b", "collection.anki21", "collection.anki2")
                             if n in self.names), None)
        if not self.db_name:
            raise SystemExit("no collection.* file inside the package")
        db_path = self.dir / self.db_name
        if self.db_name.endswith("21b"):
            if not shutil.which("zstd"):
                raise SystemExit("collection.anki21b needs the zstd binary to decompress; not found")
            raw = self.dir / "collection.decompressed.sqlite"
            subprocess.run(["zstd", "-dqf", str(db_path), "-o", str(raw)], check=True)
            db_path = raw
        self.con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        self.media_map = self._media_map()
        self._load()

    def _media_map(self):
        try:
            return json.loads((self.dir / "media").read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None  # newer protobuf media list; handled by the caller

    def _load(self):
        c = self.con
        tables = {r[0] for r in c.execute("select name from sqlite_master where type='table'")}
        self.notetypes = {}   # mid -> {name, fields[list], css, templates}
        self.decks = {}       # did -> name
        if "notetypes" in tables:
            for mid, name in c.execute("select id, name from notetypes"):
                fields = [r[0] for r in c.execute("select name from fields where ntid=? order by ord", (mid,))]
                tmpl = [(r[0], r[1]) for r in c.execute("select name, config from templates where ntid=? order by ord", (mid,))]
                self.notetypes[mid] = {"name": name, "fields": fields, "css": "", "templates": [], "tmpl_raw": tmpl}
            for did, name in c.execute("select id, name from decks"):
                self.decks[did] = name.replace("\x1f", "::")
        else:
            models, decks = c.execute("select models, decks from col").fetchone()
            for mid, m in json.loads(models).items():
                self.notetypes[int(mid)] = {
                    "name": m["name"], "fields": [f["name"] for f in sorted(m["flds"], key=lambda f: f["ord"])],
                    "css": m.get("css", ""), "templates": [(t["qfmt"], t["afmt"]) for t in m["tmpls"]], "tmpl_raw": []}
            for did, d in json.loads(decks).items():
                self.decks[int(did)] = d["name"]
        self.notes = []
        for nid, guid, mid, tags, flds in c.execute("select id, guid, mid, tags, flds from notes"):
            nt = self.notetypes.get(mid)
            names = nt["fields"] if nt else []
            vals = flds.split("\x1f")
            self.notes.append({"nid": nid, "guid": guid, "mid": mid, "tags": tags.split(),
                               "f": dict(zip(names, vals)), "nvals": len(vals), "nt": nt})
        self.cards = [{"nid": r[0], "did": r[1], "ord": r[2]} for r in c.execute("select nid, did, ord from cards")]


# ----------------------------------------------------------------------------- page map (best effort)
def page_map_combos(pm):
    """Returns set of (subject_code|None, chapter, type) found in page_map.json, or None if the schema is not recognised."""
    found = set()

    def walk(x):
        if isinstance(x, dict):
            ch = x.get("chapter", x.get("cap"))
            ty = x.get("quiz_type", x.get("type"))
            if isinstance(ch, int) and ty in ("COMM", "NCOM", "COMP"):
                found.add((x.get("subject_code"), ch, ty))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(pm)
    return found or None


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("apkg")
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--verification", required=True)
    ap.add_argument("--page-map", required=True)
    ap.add_argument("--unverified", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chapters", nargs="*", default=None, help="e.g. CHIM-C01; limits expected counts and the 84-deck check")
    ap.add_argument("--sample", type=int, default=3, help="fill-in cards used for the typed-answer matrix")
    ap.add_argument("--no-render", action="store_true", help="skip Playwright (gate 9 then FAILs as not run)")
    ap.add_argument("--keep-test-collection", action="store_true")
    args = ap.parse_args()

    out_path = Path(args.out).resolve()
    build_dir = out_path.parent
    build_dir.mkdir(parents=True, exist_ok=True)
    renders = build_dir / "renders"
    html_dir = renders / "html"
    gates = []
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    chapters = set(args.chapters) if args.chapters else None
    keep = (lambda i: chapter_of(i) in chapters) if chapters else (lambda i: True)

    extracted = [r for r in jsonl(args.extracted) if keep(r["id"])]
    verification = {r["id"]: r for r in jsonl(args.verification) if keep(r["id"])}
    expected_ids = {r["id"] for r in extracted}
    exp_combo = collections.Counter(id_parts(r["id"]) for r in extracted)

    tmp = Path(tempfile.mkdtemp(prefix="gates_", dir=HERE))
    try:
        pkg = Package(args.apkg, tmp / "unz")
        run_all(args, pkg, gates, extracted, verification, expected_ids, exp_combo, chapters, keep,
                build_dir, renders, html_dir, stamp, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    write_report(args, gates, out_path, chapters)
    sys.exit(1 if any(g.status == FAIL for g in gates) else 0)


def run_all(args, pkg, gates, extracted, verification, expected_ids, exp_combo, chapters, keep,
            build_dir, renders, html_dir, stamp, tmp):
    from_pkg_notes_all = pkg.notes
    sf_notes = [n for n in from_pkg_notes_all if n["nt"] and n["nt"]["name"] == MODEL_NAME]
    notes = [n for n in sf_notes if keep(n["f"].get("ItemID", ""))]
    outside = len(sf_notes) - len(notes)
    by_id = {n["f"].get("ItemID"): n for n in notes}
    kind_of = lambda iid: (id_parts(iid) or (None, None, None))[2]

    # ------------------------------------------------------------------ gate 1
    g = Gate(1, "Completeness", "sqlite3 on the unzipped collection: note/card counts vs extracted.jsonl, per-chapter/type counts, "
                                 "deck count, note type, every src=/url() media reference and the 4 fonts in the package media map")
    gates.append(g)
    ncards = len(pkg.cards)
    g.out(f"Package collection file: {pkg.db_name}. Scope: {'chapters ' + ', '.join(sorted(chapters)) if chapters else 'all chapters'}.")
    g.out(f"Expected printed questions (extracted.jsonl{' filtered' if chapters else ''}): {len(expected_ids)}")
    g.out(f"Notes found: {len(notes)} (note type '{MODEL_NAME}'); all notes in file: {len(pkg.notes)}; cards in file: {ncards}; "
          f"notes outside the chapter filter: {outside}")
    if len(notes) != len(expected_ids):
        g.bad(f"notes {len(notes)} != expected {len(expected_ids)}")
    if not chapters and ncards != len(pkg.notes):
        g.bad(f"cards {ncards} != notes {len(pkg.notes)}")
    note_cards = collections.Counter(c["nid"] for c in pkg.cards)
    for n in notes:
        if note_cards[n["nid"]] != 1:
            g.bad(f"{n['f'].get('ItemID')}: {note_cards[n['nid']]} cards (expected 1)")
    ids_found = [n["f"].get("ItemID") for n in notes]
    dups = [i for i, c in collections.Counter(ids_found).items() if c > 1]
    for i in dups:
        g.bad(f"duplicate ItemID {i}")
    for i in sorted(expected_ids - set(ids_found))[:30]:
        g.bad(f"missing from deck: {i}")
    for i in sorted(set(ids_found) - expected_ids)[:30]:
        g.bad(f"in deck but not in extracted.jsonl: {i}")
    found_combo = collections.Counter(id_parts(i) for i in ids_found)
    g.out(f"Distinct (subject, chapter, type) groups: expected {len(exp_combo)}, found {len(found_combo)}")
    for k in sorted(set(exp_combo) | set(found_combo), key=str):
        if exp_combo[k] != found_combo[k]:
            g.bad(f"group {k}: expected {exp_combo[k]}, found {found_combo[k]}")
    # page map cross-check
    try:
        pm = json.loads(Path(args.page_map).read_text(encoding="utf-8"))
        pmc = page_map_combos(pm)
    except (OSError, ValueError) as e:
        pm, pmc = None, None
        g.bad(f"page_map.json unreadable: {e}")
    if pm is not None:
        if pmc is None:
            g.out("page_map.json: schema not recognised by the checker (no objects with chapter + quiz_type); "
                  "per-chapter/type counts were checked against extracted.jsonl only.")
        else:
            pm_pairs = {(c, t) for (_, c, t) in pmc if (not chapters or any(int(x.split('-C')[1]) == c for x in chapters))}
            ex_pairs = {(c, t) for (_, c, t) in exp_combo}
            g.out(f"page_map.json (chapter,type) pairs: {len(pm_pairs)}; extracted: {len(ex_pairs)}")
            if pm_pairs != ex_pairs:
                g.bad(f"page_map vs extracted (chapter,type) differ: only in page_map {sorted(pm_pairs - ex_pairs)[:10]}, "
                      f"only in extracted {sorted(ex_pairs - pm_pairs)[:10]}")
    # decks
    sf_decks = {did: name for did, name in pkg.decks.items() if name.startswith("Semestre Filtro::") and name.count("::") == 3}
    used = {c["did"] for c in pkg.cards}
    deck_expected = len(exp_combo) if chapters else 84
    g.out(f"Subdecks 'Semestre Filtro::<Materia>::<Capitolo>::<Tipo>': found {len(sf_decks)}, expected {deck_expected}"
          + (" (filtered run: one per (subject, chapter, type) in extracted.jsonl; full run: 84)" if chapters else "")
          + f"; non-empty: {len(sf_decks.keys() & used)}")
    if len(sf_decks) != deck_expected:
        g.bad(f"subdeck count {len(sf_decks)} != {deck_expected}")
    card_deck = {c["nid"]: pkg.decks.get(c["did"], "?") for c in pkg.cards}
    for n in notes:
        dn = card_deck.get(n["nid"], "?")
        parts = dn.split("::")
        if len(parts) != 4 or parts[0] != "Semestre Filtro":
            g.bad(f"{n['f'].get('ItemID')}: deck '{dn}' is not Semestre Filtro::<Materia>::<Capitolo>::<Tipo>")
        elif parts[1] != n["f"].get("Subject"):
            g.bad(f"{n['f'].get('ItemID')}: deck subject '{parts[1]}' != Subject field '{n['f'].get('Subject')}'")
    # note type
    nts = [nt for nt in pkg.notetypes.values() if nt["name"] == MODEL_NAME]
    g.out(f"Note type '{MODEL_NAME}': {'present' if nts else 'MISSING'}; note types in file: {[nt['name'] for nt in pkg.notetypes.values()]}")
    if not nts:
        g.bad("note type name not found")
    else:
        if nts[0]["fields"] != FRONTED_FIELDS:
            g.bad(f"field list differs from the frozen v1 list: {nts[0]['fields']}")
        else:
            g.out("Field list and order match the frozen 20 fields.")
    for n in notes:
        if n["nvals"] != len(FRONTED_FIELDS):
            g.bad(f"{n['f'].get('ItemID')}: {n['nvals']} field values")
    # media
    media_names = None
    if pkg.media_map is None:
        g.out("Package media list is not JSON (newer format); media-in-package check is done in gate 8 against col.media.dir().")
    else:
        media_names = set(pkg.media_map.values())
        for num, name in pkg.media_map.items():
            if not (pkg.dir / num).exists():
                g.bad(f"media map entry {num} -> {name} has no file in the zip")
        for f in FONTS:
            if f not in media_names:
                g.bad(f"font {f} missing from package media")
        g.out(f"Media entries in package: {len(media_names)} (fonts present: {sum(f in media_names for f in FONTS)}/4)")
    ref_re = re.compile(r"""(?:src\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\))""", re.I)
    refs = collections.defaultdict(set)
    def collect(where, text):
        for m in ref_re.finditer(text or ""):
            r = m.group(1) or m.group(2)
            refs[html.unescape(r.strip())].add(where)
    for n in notes:
        for fname, val in n["f"].items():
            collect(f"{n['f'].get('ItemID')}.{fname}", val)
    for nt in nts:
        collect("note type CSS", nt["css"])
        for i, (q, a) in enumerate(nt["templates"]):
            collect(f"template {i} front", q)
            collect(f"template {i} back", a)
        for name, cfg in nt["tmpl_raw"]:
            collect(f"template {name}", cfg.decode("utf-8", "ignore") if isinstance(cfg, bytes) else str(cfg))
    external = [r for r in refs if re.match(r"^(https?:)?//", r)]
    for r in external:
        g.bad(f"external reference (breaks offline): {r} used in {sorted(refs[r])[:3]}")
    for nt in nts:
        blob = nt["css"] + "".join(q + a for q, a in nt["templates"])
        if "fonts.googleapis" in blob or "fonts.gstatic" in blob:
            g.bad("Google Fonts reference still present in CSS/templates")
    local = {r for r in refs if not r.startswith("data:") and r not in external}
    if media_names is not None:
        for r in sorted(local):
            if r not in media_names and urllib.parse.unquote(r) not in media_names:
                g.bad(f"referenced media not in package: {r} (from {sorted(refs[r])[:2]})")
    g.out(f"Distinct local media references in fields/CSS/templates: {len(local)}; external references: {len(external)}")
    g.finish()

    # ------------------------------------------------------------------ gate 2
    g = Gate(2, "Answers", "Parse BackOptionsHTML: exactly one 'opt correct', same letter/text as the banner and verification final_key; "
                           "fill-in: TypedAnswer set, banner shows it, AcceptedAnswers match verification")
    gates.append(g)
    n_mcq = n_comp = 0
    rec_by_id = {r["id"]: r for r in extracted}
    for n in notes:
        f, iid = n["f"], n["f"].get("ItemID", "")
        kind = kind_of(iid)
        ver = verification.get(iid)
        if kind in MCQ_TYPES:
            n_mcq += 1
            back, front = parse_options(f.get("BackOptionsHTML")), parse_options(f.get("FrontOptionsHTML"))
            correct = [o for o in back if o["correct"]]
            if len(correct) != 1:
                g.bad(f"{iid}: {len(correct)} options marked correct on the back (need exactly 1)")
                continue
            if any(o["correct"] for o in front):
                g.bad(f"{iid}: front options already carry 'correct' (answer leaks)")
            rec = rec_by_id.get(iid)
            want = len(rec["options"]) if rec and rec.get("options") else None
            if want and (len(back) != want or len(front) != want):
                g.bad(f"{iid}: options front/back {len(front)}/{len(back)} != extracted {want}")
            elif len(back) != len(front):
                g.bad(f"{iid}: option count differs front {len(front)} / back {len(back)}")
            m = re.match(r"\s*Risposta corretta:\s*\(?([A-E])\)?[.)]?\s*(.*)$", collapse(plain(f.get("AnswerBannerHTML"))), re.S)
            if not m:
                g.bad(f"{iid}: banner does not match 'Risposta corretta: <lettera>. <testo>': {collapse(plain(f.get('AnswerBannerHTML')))[:80]!r}")
                continue
            if m.group(1) != correct[0]["letter"]:
                g.bad(f"{iid}: banner letter {m.group(1)} != correct option {correct[0]['letter']}")
            if norm_cmp(m.group(2)).rstrip(".") != norm_cmp(correct[0]["text"]).rstrip("."):
                g.bad(f"{iid}: banner text {m.group(2)[:50]!r} != correct option text {correct[0]['text'][:50]!r}")
            if ver and ver.get("final_key") and ver["final_key"] != correct[0]["letter"]:
                g.bad(f"{iid}: correct option {correct[0]['letter']} != verification final_key {ver['final_key']}")
        elif kind == "COMP":
            n_comp += 1
            ta = collapse(plain(f.get("TypedAnswer")))
            if not ta:
                g.bad(f"{iid}: TypedAnswer empty")
                continue
            if norm_cmp(ta) not in norm_cmp(plain(f.get("AnswerBannerHTML"))):
                g.bad(f"{iid}: banner does not contain TypedAnswer {ta!r}")
            if ver:
                if ver.get("final_key") and norm_cmp(ver["final_key"]) != norm_cmp(ta):
                    g.bad(f"{iid}: TypedAnswer {ta!r} != verification final_key {ver['final_key']!r}")
                acc_note = {norm_cmp(x) for x in (f.get("AcceptedAnswers") or "").split("|") if x.strip()}
                acc_ver = {norm_cmp(x) for x in (ver.get("accepted_answers") or [])}
                if acc_note != acc_ver:
                    g.bad(f"{iid}: AcceptedAnswers {sorted(acc_note)} != verification {sorted(acc_ver)}")
            if parse_options(f.get("BackOptionsHTML")):
                g.bad(f"{iid}: fill-in note has option boxes")
        else:
            g.bad(f"{iid!r}: ItemID does not match the id pattern")
    g.out(f"Checked {n_mcq} multiple-choice and {n_comp} fill-in notes.")
    g.finish()

    # ------------------------------------------------------------------ gate 3
    g = Gate(3, "Typos (refusi) and OCR damage", "Regex scan for OCR damage over every field (FAIL on any hit); "
                                                 "hunspell it_IT word check (unknown words listed for review in build/typo_candidates.tsv, not auto-fail)")
    gates.append(g)
    damage = [
        ("0/1 between lowercase letters", re.compile(r"(?<=[a-zà-ÿ])[01](?=[a-zà-ÿ])")),
        ("0/1 at end of lowercase word", re.compile(r"(?<=[a-zà-ÿ]{2})[01]\b")),
        ("capital O or I inside lowercase word", re.compile(r"(?<=[a-zà-ÿ])[OI](?=[a-zà-ÿ])")),
        ("ligature", re.compile(r"[ﬀ-ﬆ]")),
        ("doubled space", re.compile(r"(?<=\S) {2,}(?=\S)")),
        ("mojibake", re.compile(r"Ã[\u0080-¿]|â€|Â[ -¿]|ï¿½|�")),
        ("control character", re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")),
    ]
    raw_damage = [
        ("&#x27; / &#39; entity", re.compile(r"&#x27;|&#39;")),
        ("double-escaped entity", re.compile(r"&amp;(?:#\d+|#x[0-9a-f]+|amp|lt|gt|quot|nbsp);", re.I)),
    ]
    skip_fields = {"ItemID", "SubjectCode", "QuestionScanHTML", "SolutionScanHTML"}
    hits = []
    word_re = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")
    words = collections.defaultdict(lambda: {"count": 0, "ids": [], "ctx": ""})
    acronyms = 0
    for n in notes:
        iid = n["f"].get("ItemID")
        seen_text = set()
        for fname, val in n["f"].items():
            if fname in skip_fields or not val:
                continue
            raw = val
            for label, rx in raw_damage:
                for m in rx.finditer(raw):
                    hits.append((iid, fname, label, raw[max(0, m.start() - 20): m.end() + 20]))
            if "<" in WELLFORMED_TAG_RE.sub("", strip_scripts(raw)):
                m = re.search("<", WELLFORMED_TAG_RE.sub("", strip_scripts(raw)))
                s = WELLFORMED_TAG_RE.sub("", strip_scripts(raw))
                hits.append((iid, fname, "stray '<' outside a tag", s[max(0, m.start() - 20): m.end() + 20]))
            txt = plain(raw)
            for label, rx in damage:
                for m in rx.finditer(txt):
                    hits.append((iid, fname, label, txt[max(0, m.start() - 20): m.end() + 20]))
            sp = collapse(spaced(raw))
            if sp in seen_text:
                continue
            seen_text.add(sp)
            for m in word_re.finditer(sp):
                w = m.group(0)
                if len(w) < 2:
                    continue
                if w.isupper() and len(w) <= 4:
                    acronyms += 1
                    continue
                d = words[w]
                d["count"] += 1
                if iid not in d["ids"]:
                    d["ids"].append(iid)
                if not d["ctx"]:
                    d["ctx"] = sp[max(0, m.start() - 25): m.end() + 25]
    for iid, fname, label, ctx in hits:
        g.bad(f"{iid} {fname}: {label}: …{ctx!r}…")
    (build_dir / "ocr_damage.tsv").write_text(
        "id\tfield\tkind\tcontext\n" + "".join(f"{a}\t{b}\t{c}\t{d!r}\n" for a, b, c, d in hits), encoding="utf-8")
    # dictionary
    unknown, method = dict_check(list(words))
    g.out(f"Dictionary method: {method}")
    g.out(f"Distinct words checked: {len(words)} (all-caps tokens of up to 4 letters skipped as acronyms: {acronyms}); unknown to dictionary: {len(unknown)}")
    rows = sorted(((w, words[w]) for w in unknown), key=lambda x: (-x[1]["count"], x[0]))
    with open(build_dir / "typo_candidates.tsv", "w", encoding="utf-8") as fh:
        fh.write("word\tcount\tnote_ids\tcontext\n")
        for w, d in rows:
            fh.write(f"{w}\t{d['count']}\t{','.join(d['ids'][:15])}\t{d['ctx']}\n")
    g.out(f"Unknown words for the orchestrator to review: build/typo_candidates.tsv ({len(rows)} rows). Top: "
          + ", ".join(f"{w}×{d['count']}" for w, d in rows[:12]))
    g.out(f"OCR-damage hits: {len(hits)} (full list: build/ocr_damage.tsv)")
    g.finish()

    # ------------------------------------------------------------------ gate 4
    g = Gate(4, "Refusal text", "Case-insensitive search of all field text and raw HTML for: I can't, I cannot, I'm sorry, Mi dispiace, non posso, come modello")
    gates.append(g)
    ref_rx = re.compile(r"I can[’']?t|I cannot|I[’']m sorry|Mi dispiace|non posso|come modello", re.I)
    cnt = 0
    for n in notes:
        for fname, val in n["f"].items():
            for m in ref_rx.finditer(collapse(spaced(val))):
                cnt += 1
                g.bad(f"{n['f'].get('ItemID')} {fname}: {m.group(0)!r} in …{collapse(spaced(val))[max(0, m.start()-30): m.end()+30]!r}")
    g.out(f"Hits: {cnt}")
    g.finish()

    # ------------------------------------------------------------------ gate 5
    g = Gate(5, "Formulas and units", "Regex extraction of every field containing number+unit, chemical formula, sub/superscripts or reaction/relation symbols -> build/formula_review.tsv")
    gates.append(g)
    unit_rx = re.compile(r"(?<![A-Za-z])\d+(?:[.,]\d+)?\s?(?:%|‰|°\s?[CFK]?|K|mol|mmol|[μµ]mol|M|mM|g|mg|kg|[μµ]g|L|l|mL|ml|dL|cm|mm|nm|km|m|s|ms|min|h|Hz|N|J|kJ|cal|kcal|W|V|mV|A|mA|Ω|Pa|kPa|atm|mmHg|eV|u|Da|kDa|bar|rad|T|ppm|C)(?![A-Za-z])")
    formula_rx = re.compile(r"[A-Z][a-z]?\d|[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻₀-₉→⇌⇄↔±×÷≈≤≥≠√ΔΔ∆]|\d\s*[x*]\s*10|\d\s*[=/^]\s*\d|\^")
    review_fields = ["FrontStemHTML", "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML", "TypedAnswer", "AcceptedAnswers", "NoteHTML"]
    nrev = 0
    with open(build_dir / "formula_review.tsv", "w", encoding="utf-8") as fh:
        fh.write("id\tpage\tfield\tmatches\ttext\n")
        for n in notes:
            f = n["f"]
            for fname in review_fields:
                t = collapse(spaced(f.get(fname)))
                ms = [m.group(0) for m in unit_rx.finditer(t)] + [m.group(0) for m in formula_rx.finditer(t)]
                if ms:
                    nrev += 1
                    fh.write(f"{f.get('ItemID')}\t{f.get('BookPage')}\t{fname}\t{' | '.join(dict.fromkeys(ms))[:120]}\t{t[:400]}\n")
    g.out(f"{nrev} field(s) with formulas/units listed in build/formula_review.tsv. Checking each against the scan and recomputing "
          "calculated answers is not automatable.")
    g.finish(manual_note="MANUAL — see file build/formula_review.tsv")

    # ------------------------------------------------------------------ gate 6
    g = Gate(6, "Status", "Tags on every note: exactly one verify::<status>, matches verification.jsonl; unverified count vs UNVERIFIED.md; NoteHTML present for unverified/corrected/derived")
    gates.append(g)
    status_count = collections.Counter()
    for n in notes:
        iid, tags, f = n["f"].get("ItemID"), n["tags"], n["f"]
        st = [t[8:] for t in tags if t.startswith("verify::") and t[8:] in STATUSES]
        rs = {t[8:] for t in tags if t.startswith("verify::") and t[8:] in REASONS}
        other = [t for t in tags if t.startswith("verify::") and t[8:] not in STATUSES + REASONS]
        for t in other:
            g.bad(f"{iid}: unknown tag {t}")
        if len(st) != 1:
            g.bad(f"{iid}: {len(st)} status tags {st}")
            continue
        status_count[st[0]] += 1
        ver = verification.get(iid)
        if ver is None:
            g.bad(f"{iid}: no record in verification.jsonl")
        else:
            if ver.get("status") != st[0]:
                g.bad(f"{iid}: tag verify::{st[0]} != verification status {ver.get('status')}")
            if set(ver.get("reason") or []) != rs:
                g.bad(f"{iid}: reason tags {sorted(rs)} != verification reason {sorted(ver.get('reason') or [])}")
            if st[0] == "unverified" and not rs:
                g.bad(f"{iid}: unverified without a reason tag")
            for d in ver.get("dup") or []:
                if f"dup::{d}" not in tags:
                    g.bad(f"{iid}: missing tag dup::{d}")
            if ver.get("ud") and f"ud::{ver['ud']}" not in tags:
                g.bad(f"{iid}: missing tag ud::{ver['ud']}")
        note_plain = collapse(plain(f.get("NoteHTML")))
        need = {"unverified": "non verificata", "derived": "ricavata", "book-corrected": "Il libro indica"}
        if st[0] in need:
            if not note_plain:
                g.bad(f"{iid}: status {st[0]} but NoteHTML empty")
            elif need[st[0]].lower() not in note_plain.lower():
                g.bad(f"{iid}: NoteHTML for {st[0]} lacks '{need[st[0]]}': {note_plain[:60]!r}")
    g.out(f"Status tag counts: {dict(status_count)}")
    try:
        unv_text = Path(args.unverified).read_text(encoding="utf-8")
        unv_ids = {i for i in ID_RE.findall(unv_text) if keep(i)}
    except OSError as e:
        unv_ids = set()
        g.bad(f"cannot read UNVERIFIED.md: {e}")
    tagged_unv = {n["f"].get("ItemID") for n in notes if "verify::unverified" in n["tags"]}
    g.out(f"verify::unverified in deck: {len(tagged_unv)}; ids in UNVERIFIED.md{' (filtered)' if chapters else ''}: {len(unv_ids)}")
    if len(tagged_unv) != len(unv_ids):
        g.bad(f"unverified count {len(tagged_unv)} != UNVERIFIED.md {len(unv_ids)}")
    for i in sorted(tagged_unv ^ unv_ids)[:30]:
        g.bad(f"{i}: {'tagged unverified but not in UNVERIFIED.md' if i in tagged_unv else 'in UNVERIFIED.md but not tagged unverified'}")
    g.finish()

    # ------------------------------------------------------------------ gate 8 (before 7: 7 uses its renders)
    g8 = Gate(8, "Import", "anki library: new Collection under work/anki-test/<timestamp>/, col.import_anki_package(ImportAnkiPackageRequest(... with_scheduling=False)); "
                           "counts, decks, note type, media in col.media.dir(), card.question()/answer() for every card, "
                           "[[type:TypedAnswer]] replaced by col.compare_answer(), typed_answer.js run in Node+jsdom")
    g7 = Gate(7, "No-script fallback", "Back HTML with every <script> removed: banner, accepted answers, TypedAnswer, correct option, NoteHTML, explanation present as text (all cards); "
                                       "then sample cards loaded in Chromium with JavaScript disabled and checked via innerText")
    render_cards = gate8(args, pkg, g8, g7, notes, kind_of, expected_ids, deck_expected, chapters, build_dir, renders, html_dir, stamp)
    gates.append(g7)
    gates.append(g8)

    # ------------------------------------------------------------------ gate 9
    g9 = Gate(9, "Visual", "node work/gates/render.js: MCQ + fill-in card, front/back, light/dark (body.nightMode), 390 px wide, bundled fonts, to build/renders/*.png")
    gates.append(g9)
    gate9(args, g9, g7, render_cards, renders)
    gates.sort(key=lambda x: x.num)


def dict_check(words):
    """Returns (unknown_words, method description)."""
    hs = shutil.which("hunspell")
    if hs and Path(HUNSPELL_BASE + ".dic").exists():
        p = subprocess.run([hs, "-d", HUNSPELL_BASE, "-i", "UTF-8", "-l"], input="\n".join(words) + "\n",
                           capture_output=True, text=True, encoding="utf-8")
        if p.returncode == 0:
            return set(p.stdout.split("\n")) - {""}, f"hunspell binary ({hs}) with {HUNSPELL_BASE}.dic/.aff (full affix rules)"
    # Fallback: plain word list, lowercase lookup, no affix expansion (many false positives).
    known = set()
    with open(HUNSPELL_BASE + ".dic", encoding="utf-8", errors="replace") as fh:
        next(fh, None)
        for line in fh:
            known.add(line.split("/")[0].strip().lower())
    return {w for w in words if w.lower() not in known}, "FALLBACK: lowercase lookup in it_IT.dic stems without affix expansion (hunspell binary not available); expect many false positives"


# ----------------------------------------------------------------------------- gate 8 + 7
def page_wrap(body, css, night=False):
    cls = "card card1" + (" nightMode night_mode" if night else "")
    return ("<!doctype html><html><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<style>{css}</style></head><body class=\"{cls}\">{body}</body></html>")


def gate8(args, pkg, g8, g7, notes, kind_of, expected_ids, deck_expected, chapters, build_dir, renders, html_dir, stamp):
    try:
        from anki.collection import Collection, ImportAnkiPackageOptions, ImportAnkiPackageRequest
    except ImportError as e:
        g8.bad(f"anki library not importable ({e}); run with opus_attempt/.venv/bin/python")
        g8.finish(); g7.bad("depends on gate 8 renders"); g7.finish()
        return []
    test_dir = ROOT / "work" / "anki-test" / stamp
    test_dir.mkdir(parents=True, exist_ok=True)
    col = Collection(str(test_dir / "collection.anki2"))
    render_cards = []
    try:
        req = ImportAnkiPackageRequest(package_path=str(Path(args.apkg).resolve()),
                                       options=ImportAnkiPackageOptions(with_scheduling=False, merge_notetypes=False,
                                                                        with_deck_configs=False))
        log = col.import_anki_package(req)
        lg = log.log
        g8.out(f"Import log: new={len(lg.new)} updated={len(lg.updated)} duplicate={len(lg.duplicate)} conflicting={len(lg.conflicting)} "
               f"first_field_match={len(lg.first_field_match)}")
        n_notes, n_cards = col.note_count(), col.card_count()
        g8.out(f"Collection after import: notes={n_notes}, cards={n_cards} (expected {len(expected_ids)})")
        if n_notes != len(expected_ids):
            g8.bad(f"notes {n_notes} != {len(expected_ids)}")
        if n_cards != len(expected_ids):
            g8.bad(f"cards {n_cards} != {len(expected_ids)}")
        names = [d.name for d in col.decks.all_names_and_ids()]
        subs = [n for n in names if n.startswith("Semestre Filtro::") and n.count("::") == 3]
        g8.out(f"Subdecks: {len(subs)} (expected {deck_expected})")
        if len(subs) != deck_expected:
            g8.bad(f"subdecks {len(subs)} != {deck_expected}")
        nt = col.models.by_name(MODEL_NAME)
        if not nt:
            g8.bad(f"note type '{MODEL_NAME}' missing after import")
            g8.finish(); g7.bad("no note type, nothing rendered"); return []
        fn = col.models.field_names(nt)
        g8.out(f"Note type present, {len(fn)} fields, {len(nt['tmpls'])} template(s): {[t['name'] for t in nt['tmpls']]}")
        if fn != FRONTED_FIELDS:
            g8.bad("imported note type field list differs from the frozen list")
        if [t["name"] for t in nt["tmpls"]] != ["Domanda -> Risposta"]:
            g8.bad("template name is not exactly ['Domanda -> Risposta']")
        mdir = Path(col.media.dir())
        have = {p.name for p in mdir.iterdir()}
        want = set((pkg.media_map or {}).values()) | set(FONTS)
        missing = sorted(want - have)
        g8.out(f"Media: {len(have)} files in col.media.dir(); package lists {len(want - set(FONTS)) if pkg.media_map else '?'} + fonts; missing: {len(missing)}")
        for m in missing[:30]:
            g8.bad(f"media not in collection media folder: {m}")
        for f in FONTS:
            if f not in have:
                g8.bad(f"font {f} not in collection media folder")
        css = nt["css"]

        # render every card
        by_nid = {}
        for n in notes:
            by_nid[n["f"].get("ItemID")] = n
        sample = {"mcq": [], "fill": []}
        issues_before = g7.problems
        n_render = 0
        for cid in col.find_cards(""):
            card = col.get_card(cid)
            fields = dict(card.note().items())
            iid = fields.get("ItemID", "")
            if not keep_id(iid, chapters):
                continue
            q, a = card.question(), card.answer()
            n_render += 1
            kind = kind_of(iid)
            typed_ok = collapse(plain(fields.get("TypedAnswer")))
            if kind == "COMP":
                if "[[type:TypedAnswer]]" not in q or "[[type:TypedAnswer]]" not in a:
                    g8.bad(f"{iid}: [[type:TypedAnswer]] not present in rendered front/back")
                a_ok = a.replace("[[type:TypedAnswer]]", col.compare_answer(typed_ok, typed_ok))
            else:
                a_ok = a
            # gate 7 string checks on the script-free back
            stripped = collapse(spaced(strip_scripts(a_ok)))
            need = [("banner", collapse(plain(fields.get("AnswerBannerHTML"))))]
            if kind == "COMP":
                need.append(("TypedAnswer", typed_ok))
                for acc in (fields.get("AcceptedAnswers") or "").split("|"):
                    if acc.strip():
                        need.append(("accepted answer", collapse(acc)))
            else:
                corr = [o["text"] for o in parse_options(fields.get("BackOptionsHTML")) if o["correct"]]
                if len(corr) == 1:
                    need.append(("correct option", corr[0]))
                if not re.search(r"""class\s*=\s*["'][^"']*\bopt\b[^"']*\bcorrect\b""", strip_scripts(a_ok)):
                    g7.bad(f"{iid}: back HTML has no 'opt correct' element")
            if collapse(plain(fields.get("NoteHTML"))):
                need.append(("NoteHTML", collapse(plain(fields["NoteHTML"]))))
            if collapse(plain(fields.get("ExplanationHTML"))):
                need.append(("explanation", collapse(plain(fields["ExplanationHTML"]))))
            for label, s in need:
                if s and s not in stripped:
                    g7.bad(f"{iid}: {label} text not in script-free back: {s[:60]!r}")
            rank = (bool((fields.get("AcceptedAnswers") or "").strip()), bool(fields.get("NoteHTML")),
                    bool(fields.get("FigureHTML")), bool(fields.get("ExplanationHTML")))
            bucket = sample["fill"] if kind == "COMP" else sample["mcq"]
            bucket.append((rank, iid, fields, q, a, need))
        g8.out(f"Rendered card.question() and card.answer() for {n_render} card(s).")
        g7.out(f"String checks (banner, accepted answers, TypedAnswer, correct option, NoteHTML, explanation) run on the script-free back of {n_render} card(s).")
        if n_render != len(expected_ids):
            g8.bad(f"rendered {n_render} cards, expected {len(expected_ids)}")

        # save samples + typed-answer matrix
        if html_dir.exists():
            shutil.rmtree(html_dir)
        html_dir.mkdir(parents=True, exist_ok=True)
        picked_mcq = sorted(sample["mcq"], key=lambda x: x[0], reverse=True)[:max(args.sample, 1)]
        picked_fill = sorted(sample["fill"], key=lambda x: x[0], reverse=True)[:max(args.sample, 1)]
        copied = set(FONTS)

        def save(name, body, night=False):
            p = html_dir / f"{name}.html"
            p.write_text(page_wrap(body, css, night), encoding="utf-8")
            for m in re.finditer(r"""(?:src\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+)["']?\s*\))""", body + css):
                r = urllib.parse.unquote(html.unescape(m.group(1) or m.group(2)))
                copied.add(r)
            return str(p.resolve())

        cases = []
        for rank, iid, fields, q, a, need in picked_mcq:
            slug = iid.lower()
            fp = save(f"{slug}_front", q)
            bp = save(f"{slug}_back", a)
            render_cards.append({"kind": "mcq", "iid": iid, "front": fp, "back": bp, "must_show": [s for _, s in need if s]})
        for rank, iid, fields, q, a, need in picked_fill:
            slug = iid.lower()
            main = collapse(plain(fields["TypedAnswer"]))
            accs = [collapse(x) for x in (fields.get("AcceptedAnswers") or "").split("|") if x.strip()]
            variant = accs[0] if accs else "il " + main
            variants = [("correct", main, True), ("variant" if accs else "article-prefixed", variant, True), ("wrong", "zzxqj", False)]
            fp = save(f"{slug}_front", q.replace("[[type:TypedAnswer]]", '<input id="typeans" type="text">'))
            first_back = None
            for label, typed, should in variants:
                body = a.replace("[[type:TypedAnswer]]", col.compare_answer(main, typed))
                bp = save(f"{slug}_back_{label}", body)
                first_back = first_back or bp
                cases.append({"name": f"{iid} {label} ({typed!r})", "html": bp, "main": main,
                              "accepted": "|".join(accs), "should_show": should})
            render_cards.append({"kind": "fill", "iid": iid, "front": fp, "back": first_back,
                                 "must_show": [s for _, s in need if s]})
        for r in sorted(copied):
            src = mdir / r
            if src.exists():
                shutil.copy(src, html_dir / r)
            else:
                g8.bad(f"sample HTML references {r} which is not in the collection media folder")
        g8.out(f"Saved {len(list(html_dir.glob('*.html')))} sample HTML file(s) to {html_dir} (media copied alongside).")
        # typed answer matrix in node+jsdom
        if not cases:
            g8.out("No fill-in cards in scope: typed-answer matrix not run.")
        elif not (HERE / "node_modules" / "jsdom").exists():
            g8.bad("jsdom not installed (npm install in work/gates/)")
        else:
            cf = html_dir / "_typed_cases.json"
            cf.write_text(json.dumps(cases), encoding="utf-8")
            pr = subprocess.run(["node", str(HERE / "typed_check.js"), str(cf)], capture_output=True, text=True, cwd=HERE)
            if pr.returncode != 0:
                g8.bad(f"typed_check.js failed: {pr.stderr[:300]}")
            else:
                res = json.loads(pr.stdout.strip().splitlines()[-1])
                g8.out("Typed-answer matrix (typed_answer.js run in jsdom with the card's scripts; 'shown' = 'Risposta accettata' visible):")
                for c, r in zip(cases, res):
                    ok = (r["accepted_shown"] == c["should_show"]) and r["typeans_found"] and not r["script_errors"]
                    g8.out(f"  {'ok ' if ok else 'BAD'} {c['name']}: typed_read={r['typed_read']!r} matcher_accepts={r['matcher_accepts']} "
                           f"shown={r['accepted_shown']} expected_shown={c['should_show']} errors={r['script_errors'][:1]}")
                    if not ok:
                        g8.bad(f"{c['name']}: 'Risposta accettata' shown={r['accepted_shown']}, expected {c['should_show']}"
                               + ("" if r["typeans_found"] else " (no #typeans in comparison HTML)")
                               + (f" script errors {r['script_errors'][:1]}" if r["script_errors"] else ""))
                    if r["matcher_accepts"] != c["should_show"]:
                        g8.bad(f"{c['name']}: assets/typed_answer.js accepted()={r['matcher_accepts']}, expected {c['should_show']}")
        g8.out("Not covered here: AnkiMobile/AnkiDroid/AnkiWeb behaviour and real Anki night-mode class handling; see the manual steps in gate 9.")
    finally:
        col.close()
        if not args.keep_test_collection:
            shutil.rmtree(test_dir, ignore_errors=True)
    g8.finish()
    return render_cards


def keep_id(iid, chapters):
    return (not chapters) or chapter_of(iid) in chapters


# ----------------------------------------------------------------------------- gate 9 (+ no-JS part of gate 7)
def gate9(args, g9, g7, render_cards, renders):
    expected_pngs = [f"{k}_{s}_{t}.png" for k in ("mcq", "fill") for s in ("front", "back") for t in ("light", "dark")]
    kinds = {c["kind"] for c in render_cards}
    if args.no_render:
        g9.bad("render step skipped (--no-render): gate 9 not run")
        g7.out("JavaScript-off browser check not run (--no-render); only the string checks above were done.")
        g9.finish(); g7.finish(); return
    if not render_cards:
        g9.bad("no sample cards from gate 8 to render")
        g9.finish(); g7.finish(); return
    if not (HERE / "node_modules" / "playwright").exists():
        g9.bad("playwright not installed (npm install + npx playwright install chromium in work/gates/)")
        g9.finish(); g7.finish(); return
    all_nojs = [dict(c, screenshots=(c is first)) for c in render_cards for first in [next(x for x in render_cards if x["kind"] == c["kind"])]]
    mf = renders / "_manifest.json"
    renders.mkdir(parents=True, exist_ok=True)
    for old in renders.glob("*.png"):
        old.unlink()
    mf.write_text(json.dumps({"cards": all_nojs}), encoding="utf-8")
    pr = subprocess.run(["node", str(HERE / "render.js"), str(mf), str(renders)], capture_output=True, text=True, cwd=HERE)
    g9.out(f"Command: node work/gates/render.js {mf} {renders}  -> exit {pr.returncode}")
    if pr.returncode != 0:
        g9.bad(f"render.js failed: {pr.stderr[-400:]}")
        g7.bad("JavaScript-off browser check could not run (render.js failed)")
        g9.finish(); g7.finish(); return
    res = json.loads((renders / "render_results.json").read_text(encoding="utf-8"))
    for name in expected_pngs:
        p = renders / name
        if kinds >= {name.split("_")[0]} and (not p.exists() or p.stat().st_size < 1000):
            g9.bad(f"missing or empty render {name}")
    present = [n for n in expected_pngs if (renders / n).exists()]
    g9.out(f"PNGs written: {len(present)}/{len(expected_pngs)} in {renders}")
    unused = set()
    for s in res["screens"]:
        if s["horizontal_overflow"]:
            g9.bad(f"{Path(s['file']).name}: horizontal scroll (scrollWidth {s['scrollWidth']} > 390)")
        fonts = [f for f in s["fonts"]]
        if not any(f.endswith(":loaded") for f in fonts):
            g9.bad(f"{Path(s['file']).name}: no bundled font reached 'loaded' state ({fonts})")
        for f in fonts:
            if f.endswith(":error"):
                g9.bad(f"{Path(s['file']).name}: font failed to load: {f}")
        unused.update(f for f in fonts if f.endswith(":unloaded"))
    if unused:
        g9.out(f"Declared but not used by the rendered cards (status 'unloaded', not an error): {sorted(unused)}")
    g9.out("Checked automatically: PNG exists, no horizontal overflow at 390 px, @font-face fonts reach 'loaded'. "
           "What the cards look like (layout, colours, dark mode contrast) was NOT judged by this script.")
    g9.out("Manual check in Anki desktop: import the .apkg (File > Import), open a CHIM chapter deck, study one multiple-choice and one fill-in card, "
           "tap an option / type an answer, press Show Answer; expect pink-framed yellow dotted card, mint correct option, yellow banner, "
           "the DARK/LIGHT button toggles, and 'Risposta accettata' for an accepted variant. On a phone: sync, repeat, and turn Airplane Mode on to confirm the fonts still load.")
    g9.finish(manual_note="RENDERED — visual review MANUAL (open the PNGs in build/renders/ and follow the steps above)")
    # gate 7 no-JS part
    for r in res["nojs"]:
        if r["missing"]:
            g7.bad(f"{r['kind']} card with JavaScript disabled: not visible in innerText: {[m[:50] for m in r['missing']]}")
    g7.out(f"JavaScript-off Chromium innerText check on {len(res['nojs'])} sample card(s): "
           + ", ".join(f"{r['kind']} missing={len(r['missing'])} of {len(r['checked'])}" for r in res["nojs"]))
    g7.finish()


# ----------------------------------------------------------------------------- report
def write_report(args, gates, out_path, chapters):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    statuses = {g.num: g.status for g in gates}
    if all(s == PASS for s in statuses.values()):
        summary = "All 9 gates PASS."
    else:
        parts = [f"gate {n}: {s}" for n, s in sorted(statuses.items()) if s != PASS]
        summary = "NOT all gates pass — " + "; ".join(parts) + "."
    L = [f"# Verification report", "",
         f"- Package: `{args.apkg}`",
         f"- Run: {ts}; scope: {', '.join(sorted(chapters)) if chapters else 'all chapters'}",
         f"- Command: `{' '.join(sys.argv)}`",
         f"- Summary: **{summary}**", "",
         "| Gate | Name | Result |", "|---|---|---|"]
    for g in gates:
        L.append(f"| {g.num} | {g.title} | {g.status} |")
    for g in gates:
        L += ["", f"## Gate {g.num}: {g.title} — {g.status}", "", f"Check: {g.check}", "", "Output:", "```"]
        L += g.lines or ["(no output)"]
        L += ["```"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{summary}\nReport: {out_path}")


if __name__ == "__main__":
    main()
