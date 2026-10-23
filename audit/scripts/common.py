"""Shared read-only helpers for the v5 audit."""
import html
import re
import sqlite3
import unicodedata

LIVE_DB = "/Users/db/Documents/projects/anki/workingdir/colpkg/collection_anki21b.db"
V5_DB = "/Users/db/Documents/projects/anki/workingdir/tmp/v5apkg/collection.anki2"
V5_MEDIA = "/Users/db/Documents/projects/anki/workingdir/tmp/v5apkg/media"
AUDIT_MEDIA = "/Users/db/Documents/projects/anki/audit/media"
OUT = "/Users/db/Documents/projects/anki/audit/out"
LIVE_MODEL = 1813027267


def _unicase(a: str, b: str) -> int:
    """Anki registers a custom `unicase` collation; without it, preparing any
    query touching fields(name)/notetypes(name) fails with 'no query solution'."""
    fa, fb = a.casefold(), b.casefold()
    return (fa > fb) - (fa < fb)


def connect(path: str) -> sqlite3.Connection:
    """Open read-only. mode=ro trips over the extracted colpkg's missing journal,
    immutable=1 is required and still guarantees no writes."""
    con = sqlite3.connect(f"file:{path}?immutable=1", uri=True)
    con.text_factory = str
    con.create_collation("unicase", _unicase)
    return con


TAG_RE = re.compile(r"<[^>]+>")
IMG_RE = re.compile(r"<img[^>]*src=\"([^\"]+)\"", re.I)
SOUND_RE = re.compile(r"\[sound:([^\]]+)\]", re.I)
WS_RE = re.compile(r"\s+")

SUP_MAP = {
    "\u2070": "0", "\u00b9": "1", "\u00b2": "2", "\u00b3": "3", "\u2074": "4",
    "\u2075": "5", "\u2076": "6", "\u2077": "7", "\u2078": "8", "\u2079": "9",
    "\u207a": "+", "\u207b": "-", "\u207f": "n", "\u2071": "i",
}
SUB_MAP = {
    "\u2080": "0", "\u2081": "1", "\u2082": "2", "\u2083": "3", "\u2084": "4",
    "\u2085": "5", "\u2086": "6", "\u2087": "7", "\u2088": "8", "\u2089": "9",
    "\u208a": "+", "\u208b": "-",
}


def strip_html(text: str) -> str:
    """HTML -> plain text: MathJax delimiters removed, entities unescaped."""
    if not text:
        return ""
    t = re.sub(r"\\\((.*?)\\\)", r"\1", text, flags=re.S)
    t = re.sub(r"\\\[(.*?)\\\]", r"\1", t, flags=re.S)
    t = re.sub(r"\$\$(.*?)\$\$", r"\1", t, flags=re.S)
    t = TAG_RE.sub(" ", t)
    t = html.unescape(t)
    return t


def norm_ws(text: str) -> str:
    return WS_RE.sub(" ", strip_html(text).replace("\u00a0", " ")).strip()


def norm_sup(text: str) -> str:
    """Flatten superscript/subscript encoding to plain characters."""
    t = norm_ws(text)
    t = re.sub(r"<sup>(.*?)</sup>", r"\1", t, flags=re.I | re.S)
    t = re.sub(r"<sub>(.*?)</sub>", r"\1", t, flags=re.I | re.S)
    t = re.sub(r"\^\{([^}]*)\}", r"\1", t)
    t = t.replace("^", "")
    for src, dst in SUP_MAP.items():
        t = t.replace(src, dst)
    for src, dst in SUB_MAP.items():
        t = t.replace(src, dst)
    return WS_RE.sub(" ", t).strip()


def norm_roots(text: str) -> str:
    t = norm_sup(text)
    t = t.replace("\u221a", "").replace("\u221b", "").replace("\u221c", "")
    return t.replace("\\sqrt", "")


def alnum_only(text: str) -> str:
    t = norm_sup(text)
    return "".join(ch for ch in t if ch.isalnum() or ch.isspace())


def symbols_only(text: str) -> str:
    t = norm_sup(text)
    return "".join(ch for ch in t if not ch.isalnum() and not ch.isspace())


def images(text: str) -> list:
    return IMG_RE.findall(text or "")


def sounds(text: str) -> list:
    return SOUND_RE.findall(text or "")


def fields(text: str) -> list:
    return (text or "").split("\x1f")


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def live_notes():
    """[(note_id, ItemID, [17 fields])] for the in-scope note type."""
    con = connect(LIVE_DB)
    rows = con.execute(
        "select id, flds from notes where mid=? order by id", (LIVE_MODEL,)
    ).fetchall()
    out = []
    for nid, flds in rows:
        f = fields(flds)
        out.append((nid, f[0].strip(), f))
    return out


def v5_notes():
    con = connect(V5_DB)
    rows = con.execute("select id, guid, flds from notes order by id").fetchall()
    out = []
    for nid, guid, flds in rows:
        f = fields(flds)
        out.append((nid, guid, f[0].strip(), f))
    return out


FIELD_NAMES = [
    "ItemID", "Subject", "SubjectCode", "ChapterNum", "ChapterTitle",
    "QuizTypeLabel", "QuestionNum", "BookPage", "FrontStemHTML", "BackStemHTML",
    "FrontOptionsHTML", "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML",
    "FigureHTML", "QuestionScanHTML", "SolutionScanHTML",
]
