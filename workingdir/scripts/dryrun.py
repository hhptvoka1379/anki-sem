#!/usr/bin/env python3
"""Dry-run GUID comparison: live colpkg (collection.anki21b) vs generated .apkg.

Read-only: every SQLite connection uses mode=ro&immutable=1. Nothing is written
except the report file. No import is performed.
"""
import difflib
import html
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE_PATH = os.path.join(BASE, "colpkg", "collection_anki21b.db")
APKG_PATH = os.path.join(BASE, "apkg", "collection.anki2")
REPORT = os.path.join(BASE, "report.md")
SEED = 20261021

SEP = "\x1f"


def _unicase(a, b):
    ka, kb = a.casefold(), b.casefold()
    return (ka > kb) - (ka < kb)


def connect_ro(path):
    """Open read-only + immutable. Anki's schema uses a custom `unicase`
    collation, which must be registered or schema parsing fails."""
    uri = "file:%s?mode=ro&immutable=1" % path
    conn = sqlite3.connect(uri, uri=True)
    conn.create_collation("unicase", _unicase)
    conn.create_collation("unicase_insensitive", _unicase)
    conn.row_factory = sqlite3.Row
    conn.execute("select count(*) from sqlite_master").fetchone()
    return conn


def tables(conn):
    return {r[0] for r in conn.execute(
        "select name from sqlite_master where type='table'")}


def load_notetypes(conn):
    """Return {mid: {'name': str, 'fields': [names]}} for schema 18 or legacy 11."""
    t = tables(conn)
    nts = {}
    if "notetypes" in t and "fields" in t:
        for r in conn.execute("select id, name from notetypes"):
            nts[r["id"]] = {
                "name": r["name"],
                "fields": [x[0] for x in conn.execute(
                    "select name from fields where ntid=? order by ord", (r["id"],))],
            }
        return nts, "schema18 (notetypes/fields)"
    models = json.loads(conn.execute("select models from col").fetchone()[0])
    for k, v in models.items():
        nts[int(k)] = {"name": v["name"], "fields": [f["name"] for f in v["flds"]]}
    return nts, "legacy col.models JSON"


def load_notes(conn):
    out = []
    cols = {r[1] for r in conn.execute("pragma table_info(notes)")}
    assert {"id", "guid", "mid", "mod", "flds", "tags", "sfld"} <= cols, cols
    for r in conn.execute(
            "select id, guid, mid, mod, flds, tags, sfld from notes"):
        out.append({
            "id": r["id"],
            "guid": r["guid"],
            "mid": r["mid"],
            "mod": r["mod"],
            "flds": r["flds"],
            "fields": r["flds"].split(SEP),
            "tags": r["tags"],
            "sfld": r["sfld"] if r["sfld"] is not None else "",
        })
    return out


# ---------------------------------------------------------------- text helpers
TAG_RE = re.compile(r"<[^>]+>")
MEDIA_RE = re.compile(r"\[sound:[^\]]+\]|<img[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
SUP_CHARS = "\u00b2\u00b3\u00b9\u2070\u2074\u2075\u2076\u2077\u2078\u2079"
EXP_RE = re.compile(r"\^|<sup|[" + SUP_CHARS + r"]|(?:\*\*|×10|10\^)", re.I)
ROOT_RE = re.compile(r"√|\\sqrt|<msqrt|radice|surd", re.I)
MULT_RE = re.compile(r"\bper\b|×|⋅|·|\u00b7|\u2219|\u22c5|\*")
SUB_RE = re.compile(r"<sub|_\{|\b[A-Za-z]\d(?![0-9])")


def strip_html(s):
    return TAG_RE.sub(" ", s)


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def squash(s):
    """HTML/whitespace-insensitive form."""
    return norm_ws(strip_html(html.unescape(s)))


def media_refs(s):
    refs = set()
    for m in MEDIA_RE.finditer(s):
        refs.add(m.group(1) if m.group(1) else m.group(0))
    return refs


# --- systematic symbol detectors: counts per side, so direction is visible ---
DETECTOR_RX = {
    "o-vs-zero": (re.compile(r"(?<=[A-Za-z])0|0(?=[A-Za-z])"), "squash"),
    "comma": (re.compile(r","), "squash"),
    "period": (re.compile(r"\."), "squash"),
    "mult-dot": (re.compile(r"[×·⋅∙]"), "squash"),
    "neq": (re.compile("\u2260"), "squash"),
    "sqrt": (re.compile("√"), "squash"),
    "sup": (re.compile(r"<sup|\^|[" + SUP_CHARS + "]"), "raw"),
    "sub": (re.compile(r"<sub"), "raw"),
    "minus-sign": (re.compile("\u2212"), "squash"),
    "arrow": (re.compile(r"→|⇌|⇄|⟶"), "squash"),
}


def detect(a, b):
    """{detector: (live_count, apkg_count)} for detectors that disagree."""
    sa, sb = squash(a), squash(b)
    out = {}
    for name, (rx, src) in DETECTOR_RX.items():
        if src == "raw":
            ca, cb = len(rx.findall(a)), len(rx.findall(b))
        else:
            ca, cb = len(rx.findall(sa)), len(rx.findall(sb))
        if ca != cb:
            out[name] = (ca, cb)
    return out


def smart_trunc(a, b, width=110):
    """Window around the first difference, so samples stay readable."""
    a_s, b_s = squash(a), squash(b)
    i = 0
    n = min(len(a_s), len(b_s))
    while i < n and a_s[i] == b_s[i]:
        i += 1
    lo = max(0, i - width // 2)
    fa = a_s[lo:lo + width] + ("…" if len(a_s) > lo + width else "")
    fb = b_s[lo:lo + width] + ("…" if len(b_s) > lo + width else "")
    pre = "…" if lo else ""
    return pre + fa, pre + fb


def changed_fragments(a, b):
    """Inserted/deleted text fragments (HTML-insensitive view)."""
    a_s, b_s = squash(a), squash(b)
    sm = difflib.SequenceMatcher(None, a_s, b_s, autojunk=False)
    ins, dele = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            dele.append(a_s[i1:i2])
        if tag in ("replace", "insert"):
            ins.append(b_s[j1:j2])
    return "".join(dele), "".join(ins)


def classify_field(a, b):
    """Return list of categories for a changed field pair."""
    if a == b:
        return ["identical"]
    if squash(a) == squash(b):
        return ["whitespace-html"]
    dele, ins = changed_fragments(a, b)
    delta = dele + " " + ins
    cats = []
    if "\u2260" in dele or "\u2260" in ins or ("\u2260" in b) != ("\u2260" in a):
        cats.append("neq")
    if EXP_RE.search(delta) or (EXP_RE.search(a) != EXP_RE.search(b)):
        cats.append("exponents")
    if ROOT_RE.search(delta) or (ROOT_RE.search(a) != ROOT_RE.search(b)):
        cats.append("roots")
    if not cats:
        cats.append("other")
    return cats


def primary(cats):
    for c in ("neq", "exponents", "roots", "whitespace-html", "other"):
        if c in cats:
            return c
    return "other"


def norm_key(s):
    return norm_ws(strip_html(html.unescape(s))).lower()


def esc(s):
    return html.escape(s, quote=False).replace("|", "\\|")


def md_row(cells):
    return "| " + " | ".join(cells) + " |"


# ------------------------------------------------------------------ media maps
def _varint(b, i):
    r = s = 0
    while True:
        x = b[i]
        i += 1
        r |= (x & 0x7F) << s
        if not x & 0x80:
            return r, i
        s += 7


def read_colpkg_media(path):
    """colpkg v3 keeps a zstd-compressed protobuf media index in `media`:
    repeated { 1: name, 2: size, 3: sha1 }. We reuse the decompressed copy."""
    p = os.path.join(BASE, "tmp", "media.pb")
    raw = open(p, "rb").read()
    entries, i = [], 0
    while i < len(raw):
        key, i = _varint(raw, i)
        fnum, wt = key >> 3, key & 7
        if wt != 2:
            raise ValueError("unexpected wiretype %d at %d" % (wt, i))
        ln, i = _varint(raw, i)
        body = raw[i:i + ln]
        i += ln
        j, cur = 0, {}
        while j < len(body):
            k2, j = _varint(body, j)
            f2, w2 = k2 >> 3, k2 & 7
            if w2 == 0:
                v, j = _varint(body, j)
                if f2 == 2:
                    cur["size"] = v
            elif w2 == 2:
                l2, j = _varint(body, j)
                val = body[j:j + l2]
                j += l2
                if f2 == 1:
                    cur["name"] = val.decode("utf-8", "replace")
                elif f2 == 3:
                    cur["sha1"] = val.hex()
        entries.append(cur)
    return entries


def read_apkg_media(path):
    z = zipfile.ZipFile(path)
    m = json.loads(z.read("media"))
    return {name: entry for entry, name in m.items()}


COLPKG_ZIP = os.path.join(BASE, "colpkg", "input.colpkg")
APKG_ZIP = os.path.join(BASE, "apkg", "input.apkg")
colpkg_entries = read_colpkg_media(COLPKG_ZIP)
colpkg_media = {e["name"]: str(i) for i, e in enumerate(colpkg_entries)}
colpkg_media_sizes_ok = None
try:
    _z = zipfile.ZipFile(COLPKG_ZIP)
    _names = set(_z.namelist())
    _rnd = random.Random(SEED)
    _idx = [i for i in range(len(colpkg_entries)) if str(i) in _names]
    _sample = _rnd.sample(_idx, min(60, len(_idx)))
    _bad = []
    for i in _sample:
        blob = _z.read(str(i))
        if blob[:4] == b"\x28\xb5\x2f\xfd":
            blob = subprocess.run(["zstd", "-dc"], input=blob,
                                  capture_output=True).stdout
        if len(blob) != colpkg_entries[i].get("size"):
            _bad.append(i)
    colpkg_media_sizes_ok = (len(_bad) == 0, len(_bad), len(_sample))
except Exception as exc:                      # pragma: no cover
    colpkg_media_sizes_ok = ("error", str(exc)[:80], 0)
apkg_media = read_apkg_media(APKG_ZIP)


# ------------------------------------------------------------------ load data
live_conn = connect_ro(LIVE_PATH)
apkg_conn = connect_ro(APKG_PATH)

live_nts, live_src = load_notetypes(live_conn)
apkg_nts, apkg_src = load_notetypes(apkg_conn)

live_notes = load_notes(live_conn)
apkg_notes = load_notes(apkg_conn)

live_by_guid = defaultdict(list)
for n in live_notes:
    live_by_guid[n["guid"]].append(n)
apkg_by_guid = defaultdict(list)
for n in apkg_notes:
    apkg_by_guid[n["guid"]].append(n)

live_guids = set(live_by_guid)
apkg_guids = set(apkg_by_guid)
matched_guids = live_guids & apkg_guids
live_only = live_guids - apkg_guids
apkg_only = apkg_guids - live_guids

dup_live = {g: v for g, v in live_by_guid.items() if len(v) > 1}
dup_apkg = {g: v for g, v in apkg_by_guid.items() if len(v) > 1}

L = []          # report lines
def w(s=""):
    L.append(s)


# ---------------------------------------------------------- per-pair comparison
def compare(ln, an):
    """Build a comparison record for one (live, apkg) note pair.

    Fields are aligned by *name* when the two note types share names (the live
    type has an extra QuestionScanHTML field), otherwise by position.
    """
    lnt = live_nts.get(ln["mid"], {"name": "?", "fields": []})
    ant = apkg_nts.get(an["mid"], {"name": "?", "fields": []})
    lmap = {n: i for i, n in enumerate(lnt["fields"])}
    amap = {n: i for i, n in enumerate(ant["fields"])}
    shared = [n for n in ant["fields"] if n in lmap]
    if shared:
        alignment = "name"
        pairs_idx = [(n, lmap[n], amap[n]) for n in shared]
    else:
        alignment = "position"
        k = min(len(ln["fields"]), len(an["fields"]))
        pairs_idx = [("field%d" % i, i, i) for i in range(k)]
    used_l = {i for _, i, _ in pairs_idx}
    used_a = {j for _, _, j in pairs_idx}
    field_diffs = []
    for name, i, j in pairs_idx:
        a, b = ln["fields"][i], an["fields"][j]
        if a != b:
            field_diffs.append({
                "idx": j, "live_idx": i, "name": name, "live_name": name,
                "a": a, "b": b, "cats": classify_field(a, b),
                "detectors": detect(a, b),
            })
    lt = set(ln["tags"].split())
    at = set(an["tags"].split())
    return {
        "guid": ln["guid"], "apkg_guid": an["guid"],
        "live": ln, "apkg": an,
        "live_nt": lnt, "apkg_nt": ant,
        "alignment": alignment,
        "field_diffs": field_diffs,
        "extra_live": [ln["fields"][i] for i in range(len(ln["fields"])) if i not in used_l],
        "extra_apkg": [an["fields"][j] for j in range(len(an["fields"])) if j not in used_a],
        "extra_live_names": [n for i, n in enumerate(lnt["fields"]) if i not in used_l],
        "extra_apkg_names": [n for j, n in enumerate(ant["fields"]) if j not in used_a],
        "tags_added": sorted(at - lt), "tags_removed": sorted(lt - at),
        "nt_name_differs": lnt["name"] != ant["name"],
        "field_count_differs": len(lnt["fields"]) != len(ant["fields"]),
    }


def is_changed(p):
    return bool(p["field_diffs"] or p["extra_live"] or p["extra_apkg"])


pairs = [compare(live_by_guid[g][0], apkg_by_guid[g][0]) for g in sorted(matched_guids)]
changed_pairs = [p for p in pairs if is_changed(p)]
identical_pairs = [p for p in pairs if not is_changed(p)]
tag_pairs = [p for p in pairs if p["tags_added"] or p["tags_removed"]]

# destructive flags
def destructive(pairs_in):
    out = []
    for p in pairs_in:
        for d in p["field_diffs"]:
            a, b = d["a"], d["b"]
            flags = []
            if squash(a) and not squash(b):
                flags.append("field emptied")
            ra, rb = media_refs(a), media_refs(b)
            dropped, added = ra - rb, rb - ra
            if ra and not rb:
                flags.append("apkg has no image (%s dropped)" % sorted(ra)[0])
            elif dropped or added:
                flags.append("image refs changed (-%d/+%d)"
                             % (len(dropped), len(added)))
            bad_b = sorted(r for r in rb if r not in apkg_media)
            bad_a = sorted(r for r in ra if r not in colpkg_media)
            if bad_b:
                flags.append("BROKEN ref in apkg: " + ", ".join(bad_b[:2]))
            if bad_a:
                flags.append("BROKEN ref in live: " + ", ".join(bad_a[:2]))
            la, lb = len(squash(a)), len(squash(b))
            if max(la, lb) > 0 and abs(la - lb) / max(la, lb) > 0.5 and abs(la - lb) > 3:
                flags.append("length %d→%d (%d%% change)"
                             % (la, lb, round(100 * abs(la - lb) / max(la, lb))))
            if flags:
                out.append({"pair": p, "diff": d, "flags": flags})
    return out


def categorise(pairs_in):
    cf, cn, samples = Counter(), Counter(), defaultdict(list)
    total = 0
    for p in pairs_in:
        for d in p["field_diffs"]:
            total += 1
            for c in d["cats"]:
                cf[c] += 1
                samples[c].append((p, d))
        if p["field_diffs"]:
            union = set()
            for d in p["field_diffs"]:
                union |= set(d["cats"])
            cn[primary(union)] += 1
    return cf, cn, samples, total


dest = destructive(changed_pairs)
cat_field, cat_note, cat_samples, diff_fields_total = categorise(changed_pairs)
nt_mismatch = [p for p in pairs if p["nt_name_differs"]]
fc_mismatch = [p for p in pairs if p["field_count_differs"]]
mid_sets = Counter((p["apkg_nt"]["name"], p["live_nt"]["name"]) for p in pairs)

# ------------------------------------------------------------ sfld fallback
def key_index(notes):
    idx = defaultdict(list)
    for n in notes:
        k = norm_key(n["sfld"])
        if k:
            idx[k].append(n)
    return idx

live_key = key_index(live_notes)
apkg_key = key_index(apkg_notes)
common_keys = set(live_key) & set(apkg_key)
fallback_pairs = 0
fallback_ambiguous = 0
fallback_ambiguous_examples = []
for k in sorted(common_keys):
    if len(live_key[k]) == 1 and len(apkg_key[k]) == 1:
        fallback_pairs += 1
    else:
        fallback_ambiguous += 1
        if len(fallback_ambiguous_examples) < 5:
            fallback_ambiguous_examples.append((k, len(live_key[k]), len(apkg_key[k])))

# natural-key (ItemID = field 0) check, independent evidence
live_itemid = defaultdict(list)
for n in live_notes:
    if n["fields"] and n["fields"][0].strip():
        live_itemid[n["fields"][0].strip()].append(n)
apkg_only_notes = [apkg_by_guid[g][0] for g in apkg_only]
apkg_only_itemid_hits = [n for n in apkg_only_notes
                         if n["fields"] and n["fields"][0].strip() in live_itemid]
apkg_itemid_conflicts = [
    p for p in pairs
    if p["apkg"]["fields"] and p["live"]["fields"]
    and p["apkg"]["fields"][0].strip() != p["live"]["fields"][0].strip()]

# ------------------------------------- ItemID pairing (natural key, fallback)
itemid_pairs = []
itemid_ambiguous = 0
apkg_unpaired = []
for n in apkg_notes:
    iid = n["fields"][0].strip() if n["fields"] else ""
    hits = live_itemid.get(iid, [])
    if len(hits) == 1:
        itemid_pairs.append(compare(hits[0], n))
    elif len(hits) > 1:
        itemid_ambiguous += 1
    else:
        apkg_unpaired.append(n)

ip_changed = [p for p in itemid_pairs if is_changed(p)]
ip_identical = [p for p in itemid_pairs if not is_changed(p)]
ip_tag = [p for p in itemid_pairs if p["tags_added"] or p["tags_removed"]]
ip_dest = destructive(ip_changed)
ip_cat_field, ip_cat_note, ip_samples, ip_diff_fields = categorise(ip_changed)
ip_nt_names = Counter((p["apkg_nt"]["name"], p["live_nt"]["name"]) for p in itemid_pairs)
ip_fc = [p for p in itemid_pairs if p["field_count_differs"]]

# per-field "changed" counts, so mass renames (e.g. media filenames) are visible
ip_field_names = defaultdict(Counter)
ip_field_changed = Counter()
ip_identical_field = Counter()
for p in itemid_pairs:
    changed_names = {d["name"] for d in p["field_diffs"]}
    for name in p["apkg_nt"]["fields"]:
        ip_field_names[name][1] = 1
        if name in changed_names:
            ip_field_changed[name] += 1
        else:
            ip_identical_field[name] += 1

# review history that GUID-based import would or would not touch
live_ids_itemid = [p["live"]["id"] for p in itemid_pairs]
if live_ids_itemid:
    q = ",".join("?" * len(live_ids_itemid))
    ip_live_cards = live_conn.execute(
        "select count(*) from cards where nid in (%s)" % q, live_ids_itemid).fetchone()[0]
    ip_live_revlog = live_conn.execute(
        "select count(*) from revlog where cid in (select id from cards where nid in (%s))"
        % q, live_ids_itemid).fetchone()[0]
else:
    ip_live_cards = ip_live_revlog = 0
live_semestre_cards = live_conn.execute(
    "select count(*) from cards c join notes n on n.id=c.nid join notetypes t on t.id=n.mid "
    "where t.name like 'Semestre%'").fetchone()[0]
live_semestre_revlog = live_conn.execute(
    "select count(*) from revlog r where r.cid in (select c.id from cards c join notes n on "
    "n.id=c.nid join notetypes t on t.id=n.mid where t.name like 'Semestre%')").fetchone()[0]

# ------------------------------------------------------------------ scheduling
apkg_card_stats = Counter()
for r in apkg_conn.execute("select type, queue, count(*) c from cards group by type, queue"):
    apkg_card_stats[(r["type"], r["queue"])] += r["c"]
apkg_cards_total = sum(apkg_card_stats.values())
apkg_reps_nonzero = apkg_conn.execute("select count(*) from cards where reps > 0").fetchone()[0]
apkg_type_nonzero = apkg_conn.execute("select count(*) from cards where type != 0").fetchone()[0]
apkg_queue_nonzero = apkg_conn.execute("select count(*) from cards where queue != 0").fetchone()[0]
apkg_ivl_nonzero = apkg_conn.execute("select count(*) from cards where ivl > 0").fetchone()[0]
apkg_revlog = apkg_conn.execute("select count(*) from revlog").fetchone()[0]
if matched_guids:
    live_cards_matched = live_conn.execute(
        "select count(*) from cards where nid in (select id from notes where guid in (%s))"
        % ",".join("?" * len(matched_guids)), tuple(matched_guids)).fetchone()[0]
else:
    live_cards_matched = 0
live_cards_total = live_conn.execute("select count(*) from cards").fetchone()[0]
live_nt_names = Counter(live_nts.get(n["mid"], {"name": "?"})["name"] for n in live_notes)
apkg_nt_names = Counter(apkg_nts.get(n["mid"], {"name": "?"})["name"] for n in apkg_notes)


CONTENT_FIELDS = ("FrontStemHTML", "BackStemHTML", "FrontOptionsHTML",
                  "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML")


def _sample_entry(p, d):
    a, b = smart_trunc(d["a"], d["b"], 220)
    return {"id": p["apkg"]["fields"][0], "field": d["name"],
            "live": a, "apkg": b, "cats": d["cats"],
            "detectors": {k: list(v) for k, v in d["detectors"].items()}}


def cosmetic(a, b):
    """True when two fields differ only in punctuation/markup/marks (A vs A., ✓, —)."""
    norm = lambda s: re.sub(r"[^0-9a-zàèéìòù]", "", squash(s).lower())
    return norm(a) == norm(b)


def dump_summary():
    rnd = random.Random(SEED)
    content = [(p, d) for p in ip_changed for d in p["field_diffs"]
               if d["name"] in CONTENT_FIELDS and not cosmetic(d["a"], d["b"])]
    general = rnd.sample(content, min(15, len(content)))
    cats = {}
    for c in ("neq", "exponents", "roots", "whitespace-html", "other"):
        pool = [x for x in content if c in x[1]["cats"]]
        cats[c] = [_sample_entry(*x) for x in rnd.sample(pool, min(5, len(pool)))]
    summary = {
        "live_path": LIVE_PATH, "apkg_path": APKG_PATH,
        "live_notes": len(live_notes), "apkg_notes": len(apkg_notes),
        "live_cards": live_cards_total, "apkg_cards": apkg_cards_total,
        "live_guids": len(live_guids), "apkg_guids": len(apkg_guids),
        "guid_matched": len(matched_guids), "live_only": len(live_only),
        "apkg_only": len(apkg_only),
        "dup_guid_live": len(dup_live), "dup_guid_apkg": len(dup_apkg),
        "guid_overlap_pct": 100 * len(matched_guids) / max(1, len(apkg_guids)),
        "live_nt_count": len(live_nts), "apkg_nt_count": len(apkg_nts),
        "live_nt_names": live_nt_names.most_common(),
        "apkg_nt_names": apkg_nt_names.most_common(),
        "live_schema_src": live_src, "apkg_schema_src": apkg_src,
        "sfld_pairs": fallback_pairs, "sfld_ambiguous": fallback_ambiguous,
        "sfld_common_keys": len(common_keys),
        "itemid_pairs": len(itemid_pairs), "itemid_ambiguous": itemid_ambiguous,
        "itemid_unpaired": len(apkg_unpaired),
        "itemid_unpaired_ids": [n["fields"][0] for n in apkg_unpaired],
        "itemid_changed": len(ip_changed), "itemid_identical": len(ip_identical),
        "itemid_diff_fields": ip_diff_fields,
        "itemid_nt_pairs": ip_nt_names.most_common(),
        "itemid_fc_mismatch": len(ip_fc),
        "cat_field": dict(ip_cat_field), "cat_note": dict(ip_cat_note),
        "field_changed": dict(ip_field_changed),
        "field_identical": dict(ip_identical_field),
        "destructive_n": len(ip_dest),
        "destructive": [{"id": x["pair"]["apkg"]["fields"][0],
                         "field": x["diff"]["name"], "flags": x["flags"]}
                        for x in ip_dest],
        "tag_pairs": len(ip_tag),
        "tag_added_only": sum(1 for p in ip_tag if p["tags_added"] and not p["tags_removed"]),
        "tag_removed_only": sum(1 for p in ip_tag if p["tags_removed"] and not p["tags_added"]),
        "tag_both": sum(1 for p in ip_tag if p["tags_removed"] and p["tags_added"]),
        "tag_added_vocab": Counter(t for p in ip_tag for t in p["tags_added"]).most_common(10),
        "tag_removed_vocab": Counter(t for p in ip_tag for t in p["tags_removed"]).most_common(10),
        "apkg_card_stats": {str(k): v for k, v in apkg_card_stats.items()},
        "apkg_reps_nonzero": apkg_reps_nonzero,
        "apkg_type_nonzero": apkg_type_nonzero,
        "apkg_queue_nonzero": apkg_queue_nonzero,
        "apkg_ivl_nonzero": apkg_ivl_nonzero,
        "apkg_revlog": apkg_revlog,
        "live_cards_itemid": ip_live_cards, "live_revlog_itemid": ip_live_revlog,
        "live_semestre_cards": live_semestre_cards,
        "live_semestre_revlog": live_semestre_revlog,
        "colpkg_media": len(colpkg_media), "apkg_media": len(apkg_media),
        "colpkg_media_sizes_ok": colpkg_media_sizes_ok,
        "extra_live_field_names": sorted({n for p in itemid_pairs
                                          for n in p["extra_live_names"]}),
        "extra_apkg_field_names": sorted({n for p in itemid_pairs
                                          for n in p["extra_apkg_names"]}),
        "samples_general": [_sample_entry(*x) for x in general],
        "samples_by_cat": cats,
    }
    os.makedirs(os.path.join(BASE, "out"), exist_ok=True)
    json.dump(summary, open(os.path.join(BASE, "out", "summary.json"), "w"),
              indent=1, ensure_ascii=False)
    return summary


def diag():
    print("live schema:", live_src, "| apkg schema:", apkg_src)
    print("live notes:", len(live_notes), "apkg notes:", len(apkg_notes))
    print("matched:", len(matched_guids), "live-only:", len(live_only), "apkg-only:", len(apkg_only))
    print("overlap of apkg:", round(100 * len(matched_guids) / max(1, len(apkg_guids)), 2), "%")
    print("dup guids live/apkg:", len(dup_live), len(dup_apkg))
    print("changed pairs:", len(changed_pairs), "identical:", len(identical_pairs))
    print("diff fields:", diff_fields_total, "cat_field:", dict(cat_field), "cat_note:", dict(cat_note))
    print("tag pairs:", len(tag_pairs), "destructive:", len(dest))
    print("nt mismatch:", len(nt_mismatch), "field-count mismatch:", len(fc_mismatch))
    print("mid sets:", mid_sets.most_common(5))
    print("fallback pairs:", fallback_pairs, "ambiguous:", fallback_ambiguous,
          "common keys:", len(common_keys))
    print("apkg-only with ItemID in live:", len(apkg_only_itemid_hits), "/", len(apkg_only_notes))
    print("itemid conflicts among pairs:", len(apkg_itemid_conflicts))
    print("apkg cards:", apkg_cards_total, "stats:", dict(apkg_card_stats))
    print("reps>0:", apkg_reps_nonzero, "type!=0:", apkg_type_nonzero,
          "queue!=0:", apkg_queue_nonzero, "ivl>0:", apkg_ivl_nonzero, "revlog:", apkg_revlog)
    print("live cards:", live_cards_total, "cards of matched notes:", live_cards_matched)
    print("live nt names:", live_nt_names.most_common(3))
    print("apkg nt names:", apkg_nt_names.most_common(3))
    print()
    print("== ItemID pairing ==")
    print("itemid pairs:", len(itemid_pairs), "ambiguous:", itemid_ambiguous,
          "apkg unpaired:", len(apkg_unpaired))
    print("changed:", len(ip_changed), "identical:", len(ip_identical), "tag diffs:", len(ip_tag))
    print("diff fields:", ip_diff_fields)
    print("cat_field:", dict(ip_cat_field))
    print("cat_note:", dict(ip_cat_note))
    print("destructive:", len(ip_dest))
    print("nt names:", ip_nt_names.most_common(3), "fc mismatch:", len(ip_fc))
    print("field changed counts:", {k: ip_field_changed.get(k, 0) for k in sorted(ip_field_changed)})
    print("field identical counts:", {k: ip_identical_field.get(k, 0) for k in sorted(ip_identical_field)})
    print("live cards of paired notes:", ip_live_cards, "revlog:", ip_live_revlog)
    print("live Semestre cards:", live_semestre_cards, "revlog:", live_semestre_revlog)
    print("unpaired samples:", [n["fields"][0] for n in apkg_unpaired[:10]])


if __name__ == "__main__":
    diag()
    s = dump_summary()
    print("\nsummary.json written:", len(s), "keys")
