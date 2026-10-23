#!/usr/bin/env python3
"""Extract named media from the colpkg/apkg zips into workingdir/samples/media.

Read-only: the zips are only opened for reading.
"""
import json
import os
import subprocess
import sys
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "samples", "media")
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"


def maybe_decompress(blob):
    """colpkg v3 stores each media file zstd-compressed."""
    if blob[:4] != ZSTD_MAGIC:
        return blob
    p = subprocess.run(["zstd", "-dc"], input=blob, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[:200])
    return p.stdout


def colpkg_map(base):
    from dryrun import read_colpkg_media  # reuse the parser
    entries = read_colpkg_media(os.path.join(base, "colpkg", "input.colpkg"))
    return {e["name"]: str(i) for i, e in enumerate(entries)}


def extract(names, which="colpkg"):
    os.makedirs(OUT, exist_ok=True)
    if which == "colpkg":
        zpath = os.path.join(BASE, "colpkg", "input.colpkg")
        mapping = colpkg_map(BASE)
    else:
        zpath = os.path.join(BASE, "apkg", "input.apkg")
        m = json.loads(zipfile.ZipFile(zpath).read("media"))
        mapping = {name: entry for entry, name in m.items()}
    z = zipfile.ZipFile(zpath)
    done, missing = [], []
    for name in names:
        entry = mapping.get(name)
        if entry is None:
            missing.append(name)
            continue
        dest = os.path.join(OUT, name)
        with z.open(entry) as src:
            blob = maybe_decompress(src.read())
        with open(dest, "wb") as dst:
            dst.write(blob)
        done.append(name)
    return done, missing


if __name__ == "__main__":
    which = sys.argv[1]
    names = sys.argv[2:]
    done, missing = extract(names, which)
    print("extracted", len(done), "missing", missing)
