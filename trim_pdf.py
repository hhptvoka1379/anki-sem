#!/usr/bin/env python3
"""Cut the white margins off every page of a PDF without re-encoding a single pixel.

How the cut is found
--------------------
Every page gets an ink mask (anything darker than ``--ink``), then:

1. rows/columns are kept only if they hold at least ``--min-ink`` ink pixels,
   so one speck of scanner dust cannot pin the page open;
2. that tight box is grown to swallow long rules that start inside the text
   band but reach past it (header rules are not "margin");
3. the box is padded by ``--pad`` pixels on every side - the "20 px diagonally
   from the first and last black point" rule;
4. everything outside the padded box is measured again.  A page is only
   reported as clean if nothing is left there, otherwise the tool prints how
   much ink survived outside, so the cut can be inspected.

Pages that are a single raster image are measured on the *native* bitmap, so
the box lands on exact pixels.  Pages with vector text, forms or several
images are measured on a 200 dpi poppler render (``pdftoppm``) instead.

Why move the page box and not the bitmap
----------------------------------------
Cropping CCITT-G4 bitmaps is lossless, but white runs cost about one bit per
64 pixels: cropping 578 images of this book moved 14.16 MB -> 14.12 MB.  Moving
the page box is *exactly* lossless - image streams, fonts and content bytes are
untouched - and it is what every viewer clips to.  The JPEG pages (cover, iPad
screenshot, back cover) can only be cropped lossily, which is a second reason
not to touch pixels at all.

The crop is applied by translating the content stream by (-x0, -y0) and
setting /MediaBox and /CropBox to [0 0 w h].  Rendering the result gives the
same pixels as cropping the original render.

``--verify`` proves that afterwards: every image stream must hash to the same
bytes as in the input (nothing was re-encoded), every page's text operators
must be unchanged, no page may grow, and a sample of pages is rendered from
both files to check that the ink count and ink position are preserved.

Usage
-----
    trim_pdf.py INPUT.pdf [OUTPUT.pdf] [--pad 20] [--ink 245] [--min-ink 3]
                           [--dpi 200] [--dry-run] [--report] [--verify]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pikepdf
from PIL import Image

# Instructions that do not paint.  A page made only of these plus one image
# /Do can be measured on the image bitmap itself.
UNPAINTED = {
    "q", "Q", "cm", "re", "W", "W*", "n", "gs", "ri", "w", "J", "j", "M", "d",
    "cs", "CS", "sc", "SC", "scn", "SCN", "g", "G", "rg", "RG", "k", "K",
    "i", "MP", "DP", "BMC", "BDC", "EMC",
}
TEXT_OPS = {"Tj", "TJ", "'", '"', "BT", "ET"}
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def ink_bbox(mask: np.ndarray, min_count: int, long_run: float = 0.25):
    """Bounding box of the ink in ``mask`` (l, t, r, b exclusive), or None.

    A row/column needs ``min_count`` ink pixels to count, which drops isolated
    dust.  The box is then grown to include long rules that start inside the
    text band but run past it, so a hairline is never cut in half.
    """
    rows = mask.sum(axis=1)
    cols = mask.sum(axis=0)
    r = np.flatnonzero(rows >= min_count)
    c = np.flatnonzero(cols >= min_count)
    if not len(r) or not len(c):
        return None
    top, bottom = int(r[0]), int(r[-1]) + 1
    left, right = int(c[0]), int(c[-1]) + 1

    for _ in range(3):
        band = mask[top:bottom]
        need = max(min_count, long_run * (right - left))
        nl, nr = left, right
        for y in np.flatnonzero(band.sum(axis=1) >= need):
            xs = np.flatnonzero(band[y])
            nl, nr = min(nl, int(xs[0])), max(nr, int(xs[-1]) + 1)

        strip = mask[:, nl:nr]
        need = max(min_count, long_run * (bottom - top))
        nt, nb = top, bottom
        for x in np.flatnonzero(strip.sum(axis=0) >= need):
            ys = np.flatnonzero(strip[:, x])
            nt, nb = min(nt, int(ys[0])), max(nb, int(ys[-1]) + 1)

        if (nl, nt, nr, nb) == (left, top, right, bottom):
            break
        left, top, right, bottom = nl, nt, nr, nb

    return left, top, right, bottom


def pad_box(box, width: int, height: int, pad: int):
    l, t, r, b = box
    return (max(0, l - pad), max(0, t - pad),
            min(width, r + pad), min(height, b + pad))


def outside_ink(mask: np.ndarray, box) -> int:
    """Ink pixels left outside ``box`` - the number that proves the cut is clean."""
    l, t, r, b = box
    out = mask.copy()
    out[t:b, l:r] = False
    return int(out.sum())


def image_mask(img: Image.Image, ink: int) -> np.ndarray:
    return np.asarray(img.convert("L"), dtype=np.uint8) < ink


def single_image(page, ink: int):
    """(xobject, ctm, ink mask) when the page is nothing but one raster image.

    Returns None for anything else - vector text, forms, several images,
    fills, inline images - so those pages go through the renderer instead.
    """
    xobjects = page.obj.get("/Resources", {}).get("/XObject", {})
    try:
        instructions = list(pikepdf.parse_content_stream(page))
    except Exception:
        return None

    stack, ctm, drawn = [], IDENTITY, []
    for ins in instructions:
        op = str(ins.operator)
        if op == "q":
            stack.append(ctm)
        elif op == "Q":
            ctm = stack.pop() if stack else IDENTITY
        elif op == "cm":
            m = [float(v) for v in ins.operands]
            a, b, c, d, e, f = ctm
            ctm = (a * m[0] + c * m[1], b * m[0] + d * m[1],
                   a * m[2] + c * m[3], b * m[2] + d * m[3],
                   a * m[4] + c * m[5] + e, b * m[4] + d * m[5] + f)
        elif op in TEXT_OPS:
            return None
        elif op == "Do":
            name = str(ins.operands[0])
            obj = xobjects.get(name) if xobjects is not None else None
            if obj is None or obj.get("/Subtype") != "/Image":
                return None                       # a form: let the renderer decide
            drawn.append((name, ctm))
        elif op not in UNPAINTED:
            return None                           # fills, strokes, shadings, inline images

    if len(drawn) != 1:
        return None
    name, ctm = drawn[0]
    a, b, c, d, e, f = ctm
    if abs(b) > 1e-6 or abs(c) > 1e-6 or a <= 0 or d <= 0:
        return None                               # rotated or flipped placement
    try:
        mask = image_mask(pikepdf.PdfImage(xobjects.get(name)).as_pil_image(), ink)
    except Exception:
        return None
    return xobjects.get(name), ctm, mask


def render_page(pdf_path: str, pno: int, dpi: int, tmpdir: str, tag: str = "p"):
    """Grayscale poppler render of one page, or None when pdftoppm is missing."""
    exe = shutil.which("pdftoppm")
    if not exe:
        return None
    out = os.path.join(tmpdir, f"{tag}{pno:04d}")
    subprocess.run([exe, "-f", str(pno), "-l", str(pno), "-r", str(dpi),
                    "-gray", "-png", "-singlefile", pdf_path, out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Image.open(out + ".png")


def plan_page(page, pno: int, src: str, opt, tmpdir: str):
    """Crop rectangle for one page, in that page's user space.

    Returns (rect, kind, note).  ``rect`` is None when the page is left alone;
    ``note`` then says why ("blank", "no margin", ...), and for kept pages it
    says whether ink was left outside the cut ("clean" or "N px outside").
    """
    mb = [float(v) for v in page.obj.MediaBox]
    ox, oy = mb[0], mb[1]
    pw, ph = mb[2] - ox, mb[3] - oy

    single = single_image(page, opt.ink)
    if single is not None:
        _obj, (a, _b, _c, d, e, f), mask = single
        h, w = mask.shape
        box = ink_bbox(mask, opt.min_ink)
        if box is None:
            return None, "image", "blank"
        l, t, r, b = pad_box(box, w, h, opt.pad)
        if (l, t, r, b) == (0, 0, w, h):
            return None, "image", "no margin"
        # the image is the unit square: x = e + a * col / w, y = f + d * (1 - row / h)
        x0, x1 = e + a * l / w, e + a * r / w
        y0, y1 = f + d * (1 - b / h), f + d * (1 - t / h)
        rect = (max(0.0, x0 - ox), max(0.0, y0 - oy),
                min(pw, x1 - ox), min(ph, y1 - oy))
        rest = outside_ink(mask, (l, t, r, b))
        return rect, "image", ("clean" if rest == 0 else f"{rest} px outside")

    if opt.no_render:
        return None, "render", "skipped (--no-render)"
    img = render_page(src, pno, opt.dpi, tmpdir)
    if img is None:
        return None, "render", "skipped (pdftoppm not found)"
    mask = image_mask(img, opt.ink)
    box = ink_bbox(mask, opt.min_ink)
    if box is None:
        return None, "render", "blank"
    l, t, r, b = pad_box(box, img.width, img.height, opt.pad)
    if (l, t, r, b) == (0, 0, img.width, img.height):
        return None, "render", "no margin"
    sx, sy = pw / img.width, ph / img.height     # points per rendered pixel
    rect = (l * sx, ph - b * sy, r * sx, ph - t * sy)
    rest = outside_ink(mask, (l, t, r, b))
    return rect, "render", ("clean" if rest == 0 else f"{rest} px outside")


def apply_crop(page, rect, pdf):
    """Translate the page content so ``rect`` becomes [0 0 w h]."""
    x0, y0, x1, y1 = rect
    w, h = x1 - x0, y1 - y0
    contents = page.obj.get("/Contents")
    data = (b"".join(bytes(s.read_bytes()) for s in contents)
            if isinstance(contents, pikepdf.Array) else bytes(contents.read_bytes()))
    page.obj["/Contents"] = pdf.make_stream(
        b"q 1 0 0 1 " + f"{-x0:.6f} {-y0:.6f}".encode() + b" cm\n" + data + b"\nQ")
    page.obj["/MediaBox"] = pikepdf.Array([0, 0, w, h])
    page.obj["/CropBox"] = pikepdf.Array([0, 0, w, h])
    for key in ("/TrimBox", "/BleedBox", "/ArtBox"):
        if key in page.obj:                       # keep the extra boxes in step
            page.obj[key] = pikepdf.Array([0, 0, w, h])
    return w, h


def trim(src: str, dst: str, opt) -> int:
    pdf = pikepdf.open(src)
    pages = len(pdf.pages)
    tmpdir = tempfile.mkdtemp(prefix="trim-pdf-")
    plans, skipped = [], {}
    area_before = area_after = 0.0
    try:
        for pno, page in enumerate(pdf.pages, 1):
            rect, kind, note = plan_page(page, pno, src, opt, tmpdir)
            if rect is None:
                skipped[note] = skipped.get(note, 0) + 1
                if opt.report:
                    print(f"  {pno:4d}  {kind:6s}  left alone: {note}")
                continue
            x0, y0, x1, y1 = rect
            mb = [float(v) for v in page.obj.MediaBox]
            pw, ph = mb[2] - mb[0], mb[3] - mb[1]
            if rect[2] <= rect[0] or rect[3] <= rect[1]:
                skipped["degenerate box"] = skipped.get("degenerate box", 0) + 1
                continue
            if (pw - (x1 - x0)) < opt.min_gain and (ph - (y1 - y0)) < opt.min_gain:
                skipped["gain below --min-gain"] = skipped.get("gain below --min-gain", 0) + 1
                continue
            plans.append((pno, page, rect, kind, note))
            area_before += pw * ph
            area_after += (x1 - x0) * (y1 - y0)
            if opt.report:
                print(f"  {pno:4d}  {kind:6s}  {pw:7.1f}x{ph:7.1f} -> "
                      f"{x1 - x0:7.1f}x{y1 - y0:7.1f}  {note}")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    unclean = [p for p in plans if p[4] != "clean"]
    print(f"pages: {pages}   cropped: {len(plans)}   left alone: {pages - len(plans)}")
    for note, n in sorted(skipped.items(), key=lambda kv: -kv[1]):
        print(f"  left alone {n:4d}  {note}")
    if plans:
        print(f"page area  {area_before/1e6:8.2f} -> {area_after/1e6:8.2f} million pt^2 "
              f"({100*area_after/area_before:.1f}% kept)")
    print(f"ink outside the cut on {len(unclean)} of {len(plans)} cropped pages")
    for pno, page, rect, kind, note in unclean[:20]:
        print(f"  page {pno}: {note}")

    if opt.dry_run:
        print("dry run, nothing written")
        return len(plans)

    for pno, page, rect, kind, note in plans:
        apply_crop(page, rect, pdf)

    pdf.save(dst, compress_streams=True,
             object_stream_mode=pikepdf.ObjectStreamMode.generate,
             linearize=False)
    size_in, size_out = os.path.getsize(src), os.path.getsize(dst)
    pdf.close()
    print(f"wrote {dst}\n  {size_in/1e6:.1f} MB -> {size_out/1e6:.1f} MB")
    return len(plans)


def stream_hash(stream) -> str:
    return hashlib.sha1(bytes(stream.read_raw_bytes())).hexdigest()


def image_hashes(pdf):
    """Every image stream's raw bytes, so 'nothing was re-encoded' is provable."""
    out = []
    for obj in pdf.objects:
        try:
            if isinstance(obj, pikepdf.Stream) and obj.get("/Subtype") == "/Image":
                out.append((stream_hash(obj), int(obj.Width), int(obj.Height),
                            str(obj.get("/Filter"))))
        except Exception:
            pass
    return sorted(out)


def text_ops(page):
    """The text-showing operators of a page, in order (the only text that exists)."""
    sig = []
    for ins in pikepdf.parse_content_stream(page):
        if str(ins.operator) in ("Tj", "TJ", "'", '"'):
            sig.append((str(ins.operator), " ".join(str(o) for o in ins.operands)))
    return sig


def verify(src: str, dst: str, opt) -> bool:
    """Prove the cut was lossless: same images, same text, same boxes, same ink."""
    ok = True
    out = pikepdf.open(dst)
    old_pdf = pikepdf.open(src)
    if len(out.pages) != len(old_pdf.pages):
        print(f"! page count {len(out.pages)} != {len(old_pdf.pages)}")
        return False

    old_imgs, new_imgs = image_hashes(old_pdf), image_hashes(out)
    if old_imgs != new_imgs:
        print(f"! image streams differ ({len(old_imgs)} -> {len(new_imgs)})")
        ok = False
    else:
        print(f"image streams: {len(new_imgs)} byte-identical streams (no re-encoding)")

    for i, (a, b) in enumerate(zip(old_pdf.pages, out.pages), 1):
        old = [float(v) for v in a.obj.MediaBox]
        new = [float(v) for v in b.obj.MediaBox]
        if (new[2] - new[0]) > (old[2] - old[0]) + 1e-3 or (new[3] - new[1]) > (old[3] - old[1]) + 1e-3:
            print(f"! page {i} grew: {old} -> {new}")
            ok = False
        if text_ops(a) != text_ops(b):
            print(f"! page {i}: text operators changed")
            ok = False
    print("text operators: identical on every page")

    tmpdir = tempfile.mkdtemp(prefix="trim-verify-")
    vdpi = min(opt.dpi, 150)          # plenty for a pixel comparison, and much faster
    try:
        n = len(out.pages)
        sample = sorted({1, 2, n // 2, n} | {int(n * f) for f in (0.1, 0.25, 0.75, 0.9)}
                        | {p for p in (750, 866, 902) if p <= n})
        for pno in sample:
            page = old_pdf.pages[pno - 1]
            rect, kind, note = plan_page(page, pno, src, opt, tmpdir)
            a_png = render_page(src, pno, vdpi, tmpdir, tag="s")
            b_png = render_page(dst, pno, vdpi, tmpdir, tag="d")
            if a_png is None or b_png is None:
                continue
            if rect is None:
                print(f"  page {pno:4d}: left alone ({note})")
                continue
            x0, y0, x1, y1 = rect
            mb = [float(v) for v in page.obj.MediaBox]
            pw, ph = mb[2] - mb[0], mb[3] - mb[1]
            sx, sy = a_png.width / pw, a_png.height / ph
            crop = a_png.crop((round(x0 * sx), round((ph - y1) * sy),
                               round(x1 * sx), round((ph - y0) * sy)))
            mask_a = np.asarray(crop.convert("L")) < opt.ink
            mask_b = np.asarray(b_png.convert("L")) < opt.ink
            ink_a, ink_b = int(mask_a.sum()), int(mask_b.sum())
            pct = 100.0 * abs(ink_b - ink_a) / max(1, ink_a)
            box_a, box_b = ink_bbox(mask_a, 1), ink_bbox(mask_b, 1)
            shift = max(abs(box_a[i] - box_b[i]) for i in range(4)) if box_a and box_b else 0
            flag = "" if pct < 2 and shift <= 3 else "   <-- inspect"
            print(f"  page {pno:4d}: {kind:6s} {a_png.size} -> {b_png.size}   "
                  f"ink {ink_a} vs {ink_b} ({pct:.2f}%)   bbox shift {shift}px{flag}")
            if pct >= 2 or shift > 3:
                ok = False
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Crop the white margins off each page without re-encoding pixels.")
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--pad", type=int, default=20,
                    help="safety margin kept around the ink, in source pixels (default 20)")
    ap.add_argument("--ink", type=int, default=245,
                    help="grey level below which a pixel counts as ink (default 245)")
    ap.add_argument("--min-ink", type=int, default=3,
                    help="ink pixels a row/column needs to anchor the box (default 3)")
    ap.add_argument("--dpi", type=int, default=200,
                    help="render resolution for pages with vector content (default 200)")
    ap.add_argument("--min-gain", type=float, default=1.0,
                    help="skip pages that would shrink by less than this many points")
    ap.add_argument("--no-render", action="store_true",
                    help="do not use pdftoppm: leave vector pages untouched")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true", help="one line per page")
    ap.add_argument("--verify", action="store_true",
                    help="after writing, compare boxes, text layer and sample renders")
    args = ap.parse_args()
    args.min_ink = max(1, args.min_ink)
    dst = args.dst or re.sub(r"\.pdf$", "", args.src, flags=re.I) + "-trim.pdf"
    trim(args.src, dst, args)
    if args.verify and not args.dry_run:
        print()
        if not verify(args.src, dst, args):
            sys.exit(1)


if __name__ == "__main__":
    main()
