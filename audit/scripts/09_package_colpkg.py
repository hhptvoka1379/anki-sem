"""Repackage the .colpkg with the converted collection and verify the result.

Only `collection.anki21b` is replaced: every media entry is copied with its
original compression method, so the media mapping and the files stay intact.
"""
import hashlib
import json
import os
import subprocess
import sys
import zipfile

sys.path.insert(0, os.path.dirname(__file__))
import common as C

SRC = "/Users/db/Documents/projects/anki/ankicup_21-10.colpkg"
OUTDIR = f"{C.OUT}/cloze"
DB = f"{OUTDIR}/collection_patched.db"
ZST = f"{OUTDIR}/collection.anki21b"
DST = f"{OUTDIR}/ankicup_21-10-cloze.colpkg"
META = f"{OUTDIR}/collection.anki2"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    subprocess.run(["zstd", "-19", "-f", "-q", DB, "-o", ZST], check=True)
    print("compressed:", os.path.getsize(DB), "->", os.path.getsize(ZST))

    with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, "w",
                                                      allowZip64=True) as zout:
        names = zin.namelist()
        assert names[:3] == ["meta", "collection.anki21b", "collection.anki2"], names[:3]
        for info in zin.infolist():
            payload = (open(ZST, "rb").read()
                       if info.filename == "collection.anki21b"
                       else zin.read(info.filename))
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zout.writestr(zi, payload)
        print("entries written:", len(zin.namelist()))

    subprocess.run(["unzip", "-p", DST, "collection.anki21b"], check=True,
                   stdout=open(f"{OUTDIR}/check.anki21b", "wb"))
    subprocess.run(["zstd", "-d", "-f", "-q", f"{OUTDIR}/check.anki21b",
                    "-o", f"{OUTDIR}/check.db"], check=True)
    assert sha(f"{OUTDIR}/check.db") == sha(DB), "round-trip hash mismatch"
    print("round-trip sha256 OK:", sha(DB)[:16])

    subprocess.run(["unzip", "-p", DST, "meta"], check=True,
                   stdout=open(f"{OUTDIR}/check.meta", "wb"))
    with zipfile.ZipFile(SRC) as a, zipfile.ZipFile(DST) as b:
        assert a.namelist() == b.namelist(), "entry list changed"
    print("entry list identical; colpkg size:", os.path.getsize(DST))
    json.dump({"colpkg": DST, "sha256": sha(DST),
               "db_sha256": sha(DB), "bytes": os.path.getsize(DST)},
              open(f"{OUTDIR}/package.json", "w"), indent=2)


if __name__ == "__main__":
    main()
