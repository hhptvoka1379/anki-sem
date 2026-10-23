#!/usr/bin/env python3
"""Crop every page of a PDF to its ink, in points, without re-encoding a pixel.

Why this exists next to ``trim_pdf.py``
---------------------------------------
``trim_pdf.py`` crops with a pad measured in *source pixels*.  On a 300 ppi scan
20 px is 4.8 pt of air, but on the 1290 px wide screenshots in this book it is
17.6 pt - a visible white frame.  It also decides "no margin" by comparing the
ink box with the *image*, so a page whose image sits inside a bigger sheet
(eleven A4 worksheets in this book draw a 391x519 pt image at x=56.8, y=252.1)
is reported as having no margin at all and is left untouched.

This tool fixes both:

1. the pad is in **points**, so every page is left with the same physical air
   (``--pad``, default 1 pt ~ 0.35 mm);
2. "no margin" is decided against the **page box**, so an inset image is cropped
   down to exactly the ink, even though the bitmap itself keeps its white edge;
3. the ink box is measured on the native bitmap for single-image pages (exact
   pixels) and on a poppler render for anything with vector text or several
   images.

The crop only moves the page boxes: ``/MediaBox`` and ``/CropBox`` become the
ink rectangle, in place.  The content stream is not even rewritten (``grep`` it
before and after: bytes identical), so text matrices, image placements and the
glyph coordinates behind the text layer are untouched - a renderer simply maps
the smaller box onto the screen.  ``--shift-origin`` is available for tools that
insist on a ``[0 0 w h]`` MediaBox; it translates the content and can re-order
extracted text, which is why it is not the default.

``--verify`` proves it: image streams must hash to the same bytes, content
streams must be byte-identical, text operators must be unchanged, no page may
grow, and sample pages are rendered from both files to check that ink count and
ink position are preserved.

Usage
-----
    tight_pdf.py INPUT.pdf [OUTPUT.pdf] [--pad 1.0] [--ink 245] [--min-ink 3]
                            [--dpi 200] [--dry-run] [--report] [--verify]
                            [--shift-origin] [--no-render]
"""
from __future__ import annotations

import argparse
import math
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pikepdf

from trim_pdf import (apply_crop, image_hashes, image_mask, ink_bbox,
                      outside_ink, render_page, single_image, text_ops)

EPS = 0.02          # points; a crop smaller than this is not a crop


def clamp_box(box, w: int, h: int, padx: int, pady: int):
    """Grow ``box`` by (padx, pady) but never outside the bitmap."""
    l, t, r, b = box
    return (max(0, l - padx), max(0, t - pady),
            min(w, r + padx), min(h, b + pady))


def swallow_dust(mask: np.ndarray, box, radius: int = 8, max_px: int = 64):
    """Grow ``box`` over stray ink that hugs it instead of cutting that ink off.

    ``ink_bbox`` needs ``--min-ink`` pixels in a row/column, so a lone pixel —
    JPEG ringing three rows under a barcode, say — is ignored and would end up
    outside the cut.  If the leftovers are few and close, they are swallowed;
    a genuine speck far out in the margin is left alone (and reported).
    """
    l, t, r, b = box
    out = mask.copy()
    out[t:b, l:r] = False
    ys, xs = np.nonzero(out)
    if not len(ys) or len(ys) > max_px:
        return box
    if (ys.min() >= t - radius and ys.max() < b + radius
            and xs.min() >= l - radius and xs.max() < r + radius):
        return (min(l, int(xs.min())), min(t, int(ys.min())),
                max(r, int(xs.max()) + 1), max(b, int(ys.max()) + 1))
    return box


def covers_page(local, pw: float, ph: float, eps: float = EPS) -> bool:
    """True when a page-local ``rect`` is the whole page (nothing to gain)."""
    x0, y0, x1, y1 = local
    return (x0 <= eps and y0 <= eps
            and x1 >= pw - eps and y1 >= ph - eps)


def plan_page(page, pno: int, src: str, opt, tmpdir: str):
    """Crop rectangle for one page in that page's user space.

    Returns ``(rect, kind, note)``; ``rect`` is None when the page is left
    alone and ``note`` says why ("blank", "no margin", "gain below ...").
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
        box = swallow_dust(mask, box)
        # 1 pt of air = w/a bitmap columns (and h/d rows)
        padx = math.ceil(opt.pad * w / a) if opt.pad > 0 else 0
        pady = math.ceil(opt.pad * h / d) if opt.pad > 0 else 0
        l, t, r, b = clamp_box(box, w, h, padx, pady)
        # the image is the unit square: x = e + a * col / w, y = f + d * (1 - row / h)
        rect = (max(ox, e + a * l / w), max(oy, f + d * (1 - b / h)),
                min(ox + pw, e + a * r / w), min(oy + ph, f + d * (1 - t / h)))
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
    box = swallow_dust(mask, box)
    pad_px = math.ceil(opt.pad * opt.dpi / 72) if opt.pad > 0 else 0
    l, t, r, b = clamp_box(box, img.width, img.height, pad_px, pad_px)
    sx, sy = pw / img.width, ph / img.height     # points per rendered pixel
    rect = (ox + l * sx, oy + ph - b * sy, ox + r * sx, oy + ph - t * sy)
    rest = outside_ink(mask, (l, t, r, b))
    return rect, "render", ("clean" if rest == 0 else f"{rest} px outside")


def set_page_box(page, rect):
    """Shrink the page boxes to ``rect`` and leave the content stream alone.

    The rectangle keeps its place in user space, so every coordinate inside the
    page - text matrices, image placements, vectors - stays exactly as it was:
    the glyphs do not move on the page, they are just framed more tightly.  A
    renderer maps the MediaBox onto the device, so the visible result is the crop.
    """
    x0, y0, x1, y1 = rect
    page.obj["/MediaBox"] = pikepdf.Array([x0, y0, x1, y1])
    page.obj["/CropBox"] = pikepdf.Array([x0, y0, x1, y1])
    for key in ("/TrimBox", "/BleedBox", "/ArtBox"):
        if key in page.obj:                   # keep the extra boxes in step
            page.obj[key] = pikepdf.Array([x0, y0, x1, y1])
    return x1 - x0, y1 - y0


def trim(src: str, dst: str, opt) -> list:
    """Crop every page that has white to spare and write ``dst``.

    Returns the list of ``(pno, rect, kind, note, margin_before)`` plans that
    were applied, so ``verify`` can reuse exactly the same rectangles.
    """
    pdf = pikepdf.open(src)
    pages = len(pdf.pages)
    tmpdir = tempfile.mkdtemp(prefix="tight-pdf-")
    plans, skipped = [], {}
    area_before = area_after = 0.0
    margins_before = []
    try:
        for pno, page in enumerate(pdf.pages, 1):
            rect, kind, note = plan_page(page, pno, src, opt, tmpdir)
            if rect is None:
                skipped[note] = skipped.get(note, 0) + 1
                if opt.report:
                    print(f"  {pno:4d}  {kind:6s}  left alone: {note}")
                continue
            mb = [float(v) for v in page.obj.MediaBox]
            ox, oy = mb[0], mb[1]
            pw, ph = mb[2] - ox, mb[3] - oy
            x0, y0, x1, y1 = rect
            local = (x0 - ox, y0 - oy, x1 - ox, y1 - oy)
            if x1 - x0 <= EPS or y1 - y0 <= EPS:
                skipped["degenerate box"] = skipped.get("degenerate box", 0) + 1
                continue
            if covers_page(local, pw, ph):
                skipped["no margin"] = skipped.get("no margin", 0) + 1
                if opt.report:
                    print(f"  {pno:4d}  {kind:6s}  left alone: no margin")
                continue
            if (pw - (x1 - x0) < opt.min_gain) and (ph - (y1 - y0) < opt.min_gain):
                skipped["gain below --min-gain"] = skipped.get("gain below --min-gain", 0) + 1
                continue
            plans.append((pno, rect, kind, note,
                          (local[0], local[1], pw - local[2], ph - local[3])))
            area_before += pw * ph
            area_after += (x1 - x0) * (y1 - y0)
            margins_before += [local[0], local[1], pw - local[2], ph - local[3]]
            if opt.report:
                print(f"  {pno:4d}  {kind:6s}  {pw:7.1f}x{ph:7.1f} -> "
                      f"{x1 - x0:7.1f}x{y1 - y0:7.1f}  "
                      f"L{local[0]:.1f} B{local[1]:.1f} R{pw - local[2]:.1f} "
                      f"T{ph - local[3]:.1f}  {note}")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    unclean = [p for p in plans if p[3] != "clean"]
    print(f"pages: {pages}   cropped: {len(plans)}   left alone: {pages - len(plans)}")
    for note, n in sorted(skipped.items(), key=lambda kv: -kv[1]):
        print(f"  left alone {n:4d}  {note}")
    if plans:
        print(f"page area  {area_before/1e6:8.2f} -> {area_after/1e6:8.2f} million pt^2 "
              f"({100*area_after/area_before:.1f}% kept)")
        if margins_before:
            q = np.percentile(margins_before, [50, 90, 99])
            print(f"margin before crop  median {q[0]:.1f} pt   p90 {q[1]:.1f}   p99 {q[2]:.1f}"
                  f"   max {max(margins_before):.1f}")
    print(f"ink outside the cut on {len(unclean)} of {len(plans)} cropped pages")
    for pno, rect, kind, note, _m in unclean[:20]:
        print(f"  page {pno}: {note}")

    if opt.dry_run:
        print("dry run, nothing written")
        return plans

    for pno, rect, kind, note, _m in plans:
        page = pdf.pages[pno - 1]
        if opt.shift_origin:
            apply_crop(page, rect, pdf)      # conventional [0 0 w h] boxes
        else:
            set_page_box(page, rect)         # content bytes stay untouched

    pdf.save(dst, compress_streams=True,
             object_stream_mode=pikepdf.ObjectStreamMode.generate,
             linearize=False)
    size_in, size_out = os.path.getsize(src), os.path.getsize(dst)
    pdf.close()
    print(f"wrote {dst}\n  {size_in/1e6:.1f} MB -> {size_out/1e6:.1f} MB")
    return plans


def content_bytes(page) -> bytes:
    """The page's content stream(s) as raw bytes, to prove they were not touched."""
    contents = page.obj.get("/Contents")
    if contents is None:
        return b""
    if isinstance(contents, pikepdf.Array):
        return b"".join(bytes(s.read_bytes()) for s in contents)
    return bytes(contents.read_bytes())


def verify(src: str, dst: str, opt, plans) -> bool:
    """Prove the cut was lossless: same images, same text, no page grown, same ink."""
    ok = True
    old_pdf = pikepdf.open(src)
    new_pdf = pikepdf.open(dst)
    if len(old_pdf.pages) != len(new_pdf.pages):
        print(f"! page count {len(new_pdf.pages)} != {len(old_pdf.pages)}")
        return False

    print("verify: image streams")
    h_old, h_new = image_hashes(old_pdf), image_hashes(new_pdf)
    if h_old != h_new:
        print("! an image stream changed - the crop is not lossless")
        ok = False
    else:
        print(f"  {len(h_old)} image streams byte-identical")

    print("verify: page geometry and text")
    grown, text_diff, content_diff = [], [], []
    for pno, (old, new) in enumerate(zip(old_pdf.pages, new_pdf.pages), 1):
        ob = [float(v) for v in old.obj.MediaBox]
        nb = [float(v) for v in new.obj.MediaBox]
        if (nb[2] - nb[0] > ob[2] - ob[0] + EPS
                or nb[3] - nb[1] > ob[3] - ob[1] + EPS):
            grown.append(pno)
        if text_ops(old) != text_ops(new):
            text_diff.append(pno)
        if not opt.shift_origin and content_bytes(old) != content_bytes(new):
            content_diff.append(pno)
    if grown:
        print(f"! {len(grown)} pages grew: {grown[:10]}")
        ok = False
    else:
        print("  no page grew")
    if text_diff:
        print(f"! text operators differ on {len(text_diff)} pages: {text_diff[:10]}")
        ok = False
    else:
        print(f"  text-showing operators identical on all {len(new_pdf.pages)} pages")
    if content_diff:
        print(f"! content streams differ on {len(content_diff)} pages: {content_diff[:10]}")
        ok = False
    elif not opt.shift_origin:
        print(f"  content streams byte-identical on all {len(new_pdf.pages)} pages")

    print("verify: renders")
    tmpdir = tempfile.mkdtemp(prefix="tight-verify-")
    by_page = {pno: rect for pno, rect, _k, _n, _m in plans}
    vdpi = min(opt.dpi, 150)          # plenty for a pixel comparison, and much faster
    try:
        n = len(new_pdf.pages)
        sample = sorted({1, 2, n // 2, n} | {int(n * f) for f in (0.1, 0.25, 0.75, 0.9)}
                        | {p for p in (35, 45, 96, 228, 750, 866, 902) if p <= n})
        for pno in sample:
            a_png = render_page(src, pno, vdpi, tmpdir, tag="s")
            b_png = render_page(dst, pno, vdpi, tmpdir, tag="d")
            if a_png is None or b_png is None:
                continue
            rect = by_page.get(pno)
            if rect is None:
                print(f"  page {pno:4d}: left alone")
                continue
            mb = [float(v) for v in old_pdf.pages[pno - 1].obj.MediaBox]
            ox, oy = mb[0], mb[1]
            pw, ph = mb[2] - ox, mb[3] - oy
            sx, sy = a_png.width / pw, a_png.height / ph
            x0, y0, x1, y1 = (rect[0] - ox, rect[1] - oy, rect[2] - ox, rect[3] - oy)
            crop = a_png.crop((round(x0 * sx), round((ph - y1) * sy),
                               round(x1 * sx), round((ph - y0) * sy)))
            mask_a = np.asarray(crop.convert("L")) < opt.ink
            mask_b = np.asarray(b_png.convert("L")) < opt.ink
            ink_a, ink_b = int(mask_a.sum()), int(mask_b.sum())
            pct = 100.0 * abs(ink_b - ink_a) / max(1, ink_a)
            box_a, box_b = ink_bbox(mask_a, 1), ink_bbox(mask_b, 1)
            shift = max(abs(box_a[i] - box_b[i]) for i in range(4)) if box_a and box_b else 0
            flag = "" if pct < 2 and shift <= 3 else "   <-- inspect"
            print(f"  page {pno:4d}: {a_png.size} -> {b_png.size}   "
                  f"ink {ink_a} vs {ink_b} ({pct:.2f}%)   bbox shift {shift}px{flag}")
            if pct >= 2 or shift > 3:
                ok = False
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    old_pdf.close()
    new_pdf.close()
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Crop each page box to its ink, in points, without re-encoding pixels.")
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--pad", type=float, default=1.0,
                    help="white air kept around the ink, in points (default 1.0)")
    ap.add_argument("--ink", type=int, default=245,
                    help="grey level below which a pixel counts as ink (default 245)")
    ap.add_argument("--min-ink", type=int, default=3,
                    help="ink pixels a row/column needs to anchor the box (default 3)")
    ap.add_argument("--dpi", type=int, default=200,
                    help="render resolution for pages with vector content (default 200)")
    ap.add_argument("--min-gain", type=float, default=0.5,
                    help="skip pages that would shrink by less than this many points")
    ap.add_argument("--shift-origin", action="store_true",
                    help="also translate the content so every box reads [0 0 w h]; "
                         "content streams change and pdftotext order can shift")
    ap.add_argument("--no-render", action="store_true",
                    help="do not use pdftoppm: leave vector pages untouched")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true", help="one line per page")
    ap.add_argument("--verify", action="store_true",
                    help="after writing, compare images, text, boxes and sample renders")
    args = ap.parse_args()
    args.min_ink = max(1, args.min_ink)
    dst = args.dst or re.sub(r"\.pdf$", "", args.src, flags=re.I) + "-tight.pdf"
    plans = trim(args.src, dst, args)
    if args.verify and not args.dry_run:
        print()
        if not verify(args.src, dst, args, plans):
            sys.exit(1)


if __name__ == "__main__":
    main()

