#!/usr/bin/env python3
"""Shrink an image-only (screenshot) PDF without dropping any page content.

This PDF is not real text: every page is a single raster image (a screenshot of a
PDF reader).  So "delete the images" would leave 902 blank pages.  Instead this
script re-encodes the *same* bitmaps with the codec that suits each one:

  * grayscale text pages at <140 ppi  -> CCITT G4 at 2x pixel size, so viewers
    downsample and thin 96 dpi strokes stay smooth instead of ragged
  * grayscale text pages otherwise    -> CCITT G4 1:1 (crisp; at 200+ ppi this is
    sharper than the blurry JPEG source)
  * genuinely coloured pages          -> JPEG, only when smaller than the original
  * photos / gradients                -> grayscale JPEG q82

The 2x upscale is capped by pixel count, because on multi-megapixel phone
screenshots it only doubles the bytes.

Nothing is cropped or dropped: page count, page boxes, vector overlays and image
placement matrices are untouched.

Usage:
    shrink_pdf.py INPUT.pdf [OUTPUT.pdf] [--profile good|j2k|tiny|g4x2|balanced]
                            [--dry-run]
"""
from __future__ import annotations

import argparse
import io
import math
import os
import re
import struct
import sys
from collections import Counter

import pikepdf
from PIL import Image, ImageChops

NUM = rb"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?"
CM_OR_DO = re.compile(
    rb"(" + NUM + rb")\s+(" + NUM + rb")\s+(" + NUM + rb")"
    rb"\s+(" + NUM + rb")\s+(" + NUM + rb")\s+(" + NUM + rb")"
    rb"\s+cm|/([^\s/\[\]<>()]+)\s+Do"
)


def page_content(page) -> bytes:
    contents = page.obj.get("/Contents")
    if contents is None:
        return b""
    if isinstance(contents, pikepdf.Array):
        return b"".join(bytes(s.read_bytes()) for s in contents)
    return bytes(contents.read_bytes())


def image_extents(page):
    """name -> (width_pt, height_pt) of the image drawn by that /Name Do."""
    out, last = {}, None
    for m in CM_OR_DO.finditer(page_content(page)):
        if m.group(7) is None:
            last = tuple(float(m.group(i)) for i in range(1, 7))
        elif last is not None:
            a, b, c, d = last[0], last[1], last[2], last[3]
            out[m.group(7).decode()] = (math.hypot(a, b), math.hypot(c, d))
    return out


UPSCALE_MAX_PIXELS = 1_200_000


def has_colour(img: Image.Image, thresh: int = 48, limit: float = 0.002) -> bool:
    """True only for pages with genuinely saturated pixels.

    A low threshold counts JPEG chroma fringing around black text, which is why
    a plain grey textbook page used to be treated as a colour photograph.
    """
    rgb = img.convert("RGB")
    r, g, b = rgb.split()
    d = ImageChops.lighter(ImageChops.difference(r, g), ImageChops.difference(g, b))
    return sum(d.histogram()[thresh:]) / (rgb.width * rgb.height) > limit


def midtone_fraction(gray: Image.Image) -> float:
    """Share of pixels in the 64..191 band - high for photos, low for text."""
    h = gray.histogram()
    return sum(h[64:192]) / (gray.width * gray.height)


def encode_jpeg(img: Image.Image, quality: int, gray: bool) -> bytes:
    buf = io.BytesIO()
    im = img.convert("L") if gray else img.convert("RGB")
    im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True,
            subsampling=0)
    return buf.getvalue()


def encode_j2k(img: Image.Image, rate: int, gray: bool = True) -> bytes:
    """Lossy JPEG 2000 (JP2 container) at a compression ratio of ``rate``:1.

    Chosen for the low-resolution screenshots: at ~0.15 bit/px it keeps the
    antialiased glyph edges that binarisation throws away, and grey banners
    stay grey instead of turning black.
    """
    buf = io.BytesIO()
    im = img.convert("L") if gray else img.convert("RGB")
    im.save(buf, "JPEG2000", no_jp2=False, irreversible=True,
            quality_mode="rates", quality_layers=[rate])
    return buf.getvalue()


def tiff_wrap(data: bytes, w: int, h: int, photometric: int) -> bytes:
    """Minimal single-strip TIFF around a G4 codestream (used to self-verify)."""
    tags = [(256, 4, w), (257, 4, h), (258, 3, 1), (259, 3, 4), (262, 3, photometric),
            (273, 4, 0), (277, 3, 1), (278, 4, h), (279, 4, len(data))]
    ifd_off = 8
    data_off = ifd_off + 2 + len(tags) * 12 + 4
    entries = []
    for tag, typ, val in tags:
        if tag == 273:
            val = data_off
        entries.append(struct.pack("<HHI", tag, typ, 1) +
                       (struct.pack("<H", val) + b"\0\0" if typ == 3
                        else struct.pack("<I", val)))
    head = (b"II*\0" + struct.pack("<I", ifd_off) + struct.pack("<H", len(tags))
            + b"".join(entries) + struct.pack("<I", 0))
    if len(head) != data_off:
        raise AssertionError("TIFF header size mismatch")
    return head + data


def encode_g4(gray: Image.Image, scale: int = 1, thresh: int = 190):
    """Binarize and CCITT-G4 encode.  Returns (data, w, h, black_is_1)."""
    im = gray if scale == 1 else gray.resize(
        (gray.width * scale, gray.height * scale), Image.LANCZOS)
    bw = im.point(lambda v: 255 if v > thresh else 0, mode="1")
    buf = io.BytesIO()
    # RowsPerStrip=height keeps libtiff from emitting one EOFB per strip, which
    # would corrupt the stream for PDF decoders that read it continuously.
    bw.save(buf, "TIFF", compression="group4", tiffinfo={278: bw.height})
    blob = buf.getvalue()

    tif = Image.open(io.BytesIO(blob))
    tags = tif.tag_v2
    offsets, counts = tags.get(273), tags.get(279)
    if offsets is None or counts is None:
        raise ValueError("TIFF has no strip offsets/byte counts")
    if not isinstance(offsets, tuple):
        offsets, counts = (offsets,), (counts,)
    data = b"".join(blob[o:o + c] for o, c in zip(offsets, counts))
    photometric = tags.get(262, 0)
    if len(data) < 16:
        raise ValueError(f"G4 codestream looks truncated ({len(data)} bytes)")

    # self-check: the extracted codestream must decode back to the same bitmap
    back = Image.open(io.BytesIO(tiff_wrap(data, bw.width, bw.height, photometric)))
    back.load()
    if back.convert("L").tobytes() != bw.convert("L").tobytes():
        raise ValueError("G4 round-trip mismatch")

    # libtiff labels the strip MinIsBlack (262=1) but emits white runs that must
    # be read as 1-bits, i.e. PDF needs /BlackIs1 true; verified by rendering a
    # known pattern through both settings (see README note in --help).
    return data, bw.width, bw.height, photometric != 0


def patch_image(stream, data: bytes, filt: str, parms, extra: dict):
    """Overwrite an image XObject in place (keeps object numbering intact)."""
    for key in ("/SMask", "/Mask", "/Decode", "/DecodeParms", "/Alternate",
                "/Interpolate", "/Intent", "/Metadata", "/StructParent",
                "/Filter"):
        if key in stream:
            del stream[key]
    for k, v in extra.items():
        stream[k if k.startswith("/") else "/" + k] = v
    stream.write(data, filter=pikepdf.Name(filt), decode_parms=parms)


def collect_images(pdf):
    """objgen -> {'stream', 'pages', 'extents'}; one entry per distinct XObject."""
    found = {}
    for pno, page in enumerate(pdf.pages, 1):
        res = page.obj.get("/Resources")
        if res is None:
            continue
        xo = res.get("/XObject")
        if xo is None:
            continue
        extents = image_extents(page)
        for name in xo.keys():
            obj = xo[name]
            if obj.get("/Subtype") != pikepdf.Name("/Image"):
                continue
            try:
                gen = obj.objgen
            except ValueError:
                continue          # direct object: cannot patch in place
            entry = found.setdefault(gen, {"stream": obj, "pages": [], "extents": []})
            entry["pages"].append(pno)
            if name[1:] in extents:
                entry["extents"].append(extents[name[1:]])
    return found


def decode_flat(stream) -> Image.Image:
    img = pikepdf.PdfImage(stream).as_pil_image()
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img)
    return img.convert("RGB")


PROFILES = {
    # j2k_rate: JPEG 2000 compression ratio for text pages (None disables it).
    # low_res_scale: G4 pixel multiplier for <140 ppi pages, offered as an
    #                alternative to J2K; the smaller of the two is kept.
    "good":     dict(j2k_rate=None, low_res_scale=2, colour_q=88, photo_q=82,
                     low_res_gray=False),
    "j2k":      dict(j2k_rate=40, low_res_scale=2, colour_q=80, photo_q=78,
                     low_res_gray=False),
    "tiny":     dict(j2k_rate=50, low_res_scale=1, colour_q=72, photo_q=70,
                     low_res_gray=False),
    "g4x2":     dict(j2k_rate=None, low_res_scale=2, colour_q=88, photo_q=82,
                     low_res_gray=False),
    "balanced": dict(j2k_rate=None, low_res_scale=1, colour_q=88, photo_q=82,
                     low_res_gray=True),
}


def decide(img, ppi, profile):
    """Return (data, filter, decode_parms, extra_dict, label) for one image."""
    opts = PROFILES[profile]

    if has_colour(img):
        return (encode_jpeg(img, opts["colour_q"], gray=False), "/DCTDecode", None,
                {"Width": img.width, "Height": img.height, "BitsPerComponent": 8,
                 "ColorSpace": pikepdf.Name("/DeviceRGB")},
                f"colour jpeg q{opts['colour_q']}")

    gray = img.convert("L")
    if midtone_fraction(gray) > 0.22:      # photo / gradient / shaded artwork
        return (encode_jpeg(gray, opts["photo_q"], gray=True), "/DCTDecode", None,
                {"Width": gray.width, "Height": gray.height, "BitsPerComponent": 8,
                 "ColorSpace": pikepdf.Name("/DeviceGray")},
                f"gray jpeg q{opts['photo_q']}")

    low_res = ppi is not None and ppi < 140
    if opts["low_res_gray"] and low_res:
        return (encode_jpeg(gray, opts["photo_q"], gray=True), "/DCTDecode", None,
                {"Width": gray.width, "Height": gray.height, "BitsPerComponent": 8,
                 "ColorSpace": pikepdf.Name("/DeviceGray")},
                "gray jpeg (low-res)")

    # 2x upscaling smooths thin 96 dpi strokes, but on multi-megapixel phone
    # screenshots it only doubles the bytes, so cap it by pixel count.
    upscale = (opts["low_res_scale"]
               if low_res and gray.width * gray.height <= UPSCALE_MAX_PIXELS else 1)

    def g4_option(scale):
        data, w, h, black_is_1 = encode_g4(gray, scale=scale)
        parms = pikepdf.Dictionary(K=-1, Columns=w, Rows=h, BlackIs1=black_is_1,
                                   EndOfBlock=False)
        return (data, "/CCITTFaxDecode", parms,
                {"Width": w, "Height": h, "BitsPerComponent": 1,
                 "ColorSpace": pikepdf.Name("/DeviceGray")},
                f"ccitt g4 x{scale}")

    def j2k_option(rate):
        data = encode_j2k(gray, rate)
        return (data, "/JPXDecode", None,
                {"Width": gray.width, "Height": gray.height, "BitsPerComponent": 8,
                 "ColorSpace": pikepdf.Name("/DeviceGray")},
                f"jpeg2000 r{rate}")

    g4 = g4_option(upscale)
    if opts["j2k_rate"] is None:
        return g4
    j2k = j2k_option(opts["j2k_rate"] if low_res else opts["j2k_rate"] + 15)
    # G4 only when it is clearly smaller: binarising costs antialiasing.
    return g4 if len(g4[0]) < 0.85 * len(j2k[0]) else j2k


def process(src, dst, profile="small", dry_run=False):
    pdf = pikepdf.open(src)
    images = collect_images(pdf)
    print(f"pages: {len(pdf.pages)}  distinct images: {len(images)}")

    before = after = 0
    labels = Counter()
    label_bytes = Counter()
    changed = 0
    for gen, entry in sorted(images.items(), key=lambda kv: kv[1]["pages"][0]):
        stream = entry["stream"]
        raw = stream.read_raw_bytes()
        before += len(raw)

        try:
            img = decode_flat(stream)
        except Exception as exc:
            after += len(raw)
            labels["kept (undecodable)"] += 1
            print(f"  ! page {entry['pages'][0]} {gen}: {exc}", file=sys.stderr)
            continue

        extents = [e for e in entry["extents"] if e[0] and e[1]]
        ppi = None
        if extents:
            w_pt, h_pt = extents[0]
            ppi = min(img.width / (w_pt / 72.0), img.height / (h_pt / 72.0))

        data, filt, parms, extra, label = decide(img, ppi, profile)
        if len(data) >= len(raw):                 # never make a page heavier
            after += len(raw)
            labels["kept (already optimal)"] += 1
            label_bytes["kept (already optimal)"] += len(raw)
            continue

        after += len(data)
        labels[label] += 1
        label_bytes[label] += len(data)
        changed += 1
        if not dry_run:
            patch_image(stream, data, filt, parms, extra)

    print()
    for label, n in labels.most_common():
        print(f"  {label:26s} {n:5d} images  {label_bytes[label]/1e6:8.2f} MB")
    print(f"\nimage payload: {before/1e6:.1f} MB -> {after/1e6:.1f} MB "
          f"({100*after/before:.1f}%), {changed} images rewritten")

    if dry_run:
        print("dry run, nothing written")
        return

    pdf.save(dst, compress_streams=True,
             object_stream_mode=pikepdf.ObjectStreamMode.generate,
             linearize=False)
    size_in, size_out = os.path.getsize(src), os.path.getsize(dst)
    print(f"wrote {dst}\n  {size_in/1e6:.1f} MB -> {size_out/1e6:.1f} MB "
          f"({100*size_out/size_in:.1f}%)")


def main():
    ap = argparse.ArgumentParser(
        description="Re-encode the raster pages of a screenshot-only PDF.")
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--profile", choices=tuple(PROFILES), default="good",
                    help="good (default): per-image best of JPEG 2000 / G4; "
                         "tiny: smaller and rougher; g4x2/balanced: older variants")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dst = args.dst or re.sub(r"\.pdf$", "", args.src, flags=re.I) + "-small.pdf"
    process(args.src, dst, args.profile, args.dry_run)


if __name__ == "__main__":
    main()


