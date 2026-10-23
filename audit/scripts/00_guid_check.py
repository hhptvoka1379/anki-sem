"""Check which GUID scheme produced the v5 .apkg GUIDs.

Stage 1 forbids pairing by GUID, so this is only an identity-scheme sanity check
(salt "semestre-filtro-v5" must reproduce the apkg GUIDs). Read-only.
"""
import hashlib
import json
import sqlite3
import sys

V5 = "/Users/db/Documents/projects/anki/workingdir/tmp/v5apkg/collection.anki2"

# standard basE91 alphabet (A-Z then a-z), as used by genanki.util.guid_for
ALPHABET = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            '!#$%&()*+,./:;<=>?@[]^_`{|}~"')


def base91(n: int) -> str:
    if n == 0:
        return ALPHABET[0]
    out = []
    while n:
        n, r = divmod(n, 91)
        out.append(ALPHABET[r])
    return "".join(reversed(out))


def variants(salt: str, item_id: str):
    """Candidate GUID derivations, in the order genanki versions used them."""
    b = (salt + item_id).encode()
    b_join = "\x1f".join([salt, item_id]).encode()
    for label, payload in (("concat", b), ("unit-sep", b_join)):
        h = hashlib.sha1(payload).hexdigest()
        yield f"{label}:sha1hex-int", base91(int(h, 16))[:10]
        d = hashlib.sha1(payload).digest()
        yield f"{label}:sha1digest-int", base91(int.from_bytes(d, "big"))[:10]
        yield f"{label}:sha1hex-trunc", h[:10]
        m = hashlib.md5(payload).hexdigest()
        yield f"{label}:md5hex-int", base91(int(m, 16))[:10]


def main() -> None:
    con = sqlite3.connect(f"file:{V5}?immutable=1", uri=True)
    rows = con.execute("select guid, flds from notes limit 400").fetchall()
    sample = []
    for guid, flds in rows:
        item = flds.split("\x1f")[0].strip()
        sample.append((guid, item))

    hits = {}
    for guid, item in sample:
        for label, cand in variants("semestre-filtro-v5", item):
            if cand == guid:
                hits.setdefault(label, 0)
                hits[label] += 1
    print(json.dumps({
        "rows_tested": len(sample),
        "hits": hits,
        "first": sample[0],
        "candidates_first": list(variants("semestre-filtro-v5", sample[0][1])),
    }, indent=2))


if __name__ == "__main__":
    sys.exit(main())
