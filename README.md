# Eserciziario Unico per il Semestre Filtro 2 — 196.6 MB → 23.6 MB

The `... .pdf alias` in this folder points at
`~/Downloads/Eserciziario Unico per il Semestre Filtro  2.pdf` (902 pages, 196.6 MB).

## What that PDF actually is

| Finding | Value |
|---|---|
| Pages | 902; page boxes vary (441×587, 595×842, and 1290×18xx phone captures) |
| Producer | macOS Quartz PDFContext |
| Text layer | essentially none — `pdftotext` yields 15 KB for 902 pages |
| Fonts | 28 embedded fonts exist, but the body pages reference **no** `/Font` at all |
| Images | 934 images = **99.3 %** of the file (194.1 MB) |
| Page content | one JPEG per page, drawn with a single `q … cm /ImNN Do Q` |

Each body page is **one screenshot** of a PDF reader (page 866 even shows the
iOS status bar, toolbar and "862/898"), so the text is pixels, not vectors.

**Consequence: "remove all images" is not possible without destroying the
document.** It would leave ~2.5 MB of blank pages. The rest of this note is
about shrinking it while keeping every word.

## Result

`Eserciziario Unico per il Semestre Filtro  2-lite.pdf` — **23.6 MB (12.0 %)**

`Eserciziario Unico per il Semestre Filtro  2-lite-tight.pdf` — the same file
with the last of the white border cut off (see the `tight_pdf.py` section below).

`shrink_pdf.py` decodes each page bitmap and re-encodes it with the codec that
fits it, patching the image XObject *in place* (no object renumbering, no
page/content-stream edits, page count and geometry untouched):

| Decision | Images | Size |
|---|---|---|
| `ccitt g4 x2` — text at <140 ppi, binarised at 2× so viewers downsample smoothly | 284 | 5.93 MB |
| `ccitt g4 x1` — everything else (200–300 ppi text, phone captures) | 644 | 14.86 MB |
| `colour jpeg q88` — cover and genuinely colourful pages | 3 | 0.78 MB |

Verified: 902/902 pages render, 0 poppler warnings, 0 blank pages, 0 page-size
changes, identical `pdftotext` output (902 pages, PDF 1.5), and every G4
codestream is decoded back and compared to its source bitmap before writing.

## What was tried and rejected (measured, not guessed)

| Idea | Outcome |
|---|---|
| Delete the images | leaves 902 blank pages |
| Re-JPEG grayscale q85 | 79 % of the original bytes — pointless |
| Lossless PNG / Flate | **153 %** — worse than the source JPEG |
| JPEG-2000 lossy, 40–50:1 | 8–11 KB/page and small, but visibly **blurry/smeared** at 96 dpi — rejected after rendering it |
| Median filter before binarising | destroys 1 px strokes at 96 dpi; glyphs break apart |
| Crop pixels outside the page box | measured 0 hidden pixels — nothing to gain |
| 2× upscale on multi-megapixel captures | doubles bytes for no visible gain — now capped at ≤1.2 Mpx |

Two real bugs were caught by testing rather than by reading the spec: libtiff
writes one EOFB per strip (corrupting the PDF stream — fixed with
`RowsPerStrip`), and libtiff's output needs `/BlackIs1 true` (established by
rendering a known pattern through both settings).

## Known trade-offs

* Binarisation turns mid-grey decoration black: grey chapter banners and the
  `Edises` footer bars now print black-on-white (text inside stays legible).
* 96 dpi screenshots lose antialiasing and look like clean fax output, while the
  200–300 ppi pages actually get **sharper** than the JPEG source.
* Pages that were 300 dpi *colour* but only ~0.1 % non-neutral (JPEG chroma
  fringing rather than real colour) are now binarised. The cover stays colour.

## Usage

```bash
python3 -m venv .venv && .venv/bin/pip install pikepdf Pillow numpy
# trim_pdf.py also shells out to poppler's pdftoppm (already used below)

# see the decisions and projected size without writing anything
.venv/bin/python shrink_pdf.py "~/Downloads/Eserciziario Unico per il Semestre Filtro  2.pdf" --dry-run

# default "good" profile (this is what produced the 23.6 MB file)
.venv/bin/python shrink_pdf.py INPUT.pdf OUTPUT.pdf

# other profiles
.venv/bin/python shrink_pdf.py INPUT.pdf O.pdf --profile g4x2     # 32.7 MB, 2x kept on big captures
.venv/bin/python shrink_pdf.py INPUT.pdf O.pdf --profile j2k      # smaller, but soft text
.venv/bin/python shrink_pdf.py INPUT.pdf O.pdf --profile balanced # keeps <140 ppi pages as grey JPEG
```

If a page's re-encode is not smaller than the original, the original stream is
kept, so the script never inflates a file.

## Trimming the white margins

`trim_pdf.py` writes `Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf`:
902 pages, **70.3 % of the page area kept** (791.01 → 556.41 million pt²), every
page cropped to its ink plus 20 px, and not one pixel re-encoded.

| Check | Result |
|---|---|
| pages cropped | 884 / 902 |
| left alone | 15 full-bleed pages (covers, section banners) + 3 blank |
| ink outside the cut | **0 px** on all 884 cropped pages |
| image streams | **960 / 960 byte-identical** (SHA-1 of the raw stream) |
| text operators | identical on every page |
| sample renders (`--verify`) | ink count within 1.5 %, ink position within 1 px |
| file size | 23,644,374 → 23,623,270 bytes (−21 KB) |

The median page keeps 77 % of its area, 276 of the 884 drop below half, and the
most extreme (page 35, a page with four leftover lines) goes from 595 × 842 to
352 × 173 pt.

The size does not move because the margins were already nearly free: cropping
578 CCITT-G4 bitmaps by hand measured 14.16 MB → 14.12 MB, and the three JPEG
pages (cover, iPad screenshot, back cover) can only be cropped lossily. So the
tool leaves the pixels alone and moves the page box, which is what viewers clip
to and is exactly lossless.

### How the cut is found

For every page an ink mask is built (pixel < `--ink`, default 245), then:

1. a row/column counts only if it holds `--min-ink` (3) ink pixels — one speck
   of dust cannot pin the page open;
2. the tight box is grown to swallow long rules that start inside the text band
   but run past it (the iPad screenshot's toolbar rules span the full width;
   without this, they would be cut in half);
3. the box is padded by `--pad` (20) pixels on each side;
4. the ink left outside the padded box is counted again — that is the "is the
   rest of the page really white?" test. All 884 pages report 0.

Pages that are one raster image are measured on the **native bitmap**, so the
box lands on exact pixels. Pages with vector text, forms, several images or a
vector frame over the scan (pages 313–672) are measured on a 200 dpi poppler
render, because their ink is not only in the bitmap.

The crop is applied by prefixing the content stream with
`q 1 0 0 1 -x0 -y0 cm` and setting `/MediaBox` and `/CropBox` to `[0 0 w h]`;
image XObjects, fonts and every other object are untouched.

### Verification

`--verify` reopens both files and checks page count, that no page grew, the
SHA-1 of every image stream (all 960 identical), the text-showing operators of
all 902 pages, and renders a sample of pages from both files to compare ink
count and ink position.

`pdftotext` output is also unchanged except for six decorative glyphs (`一` ×4,
`口`, `土`) that Quartz emitted as 1 pt wide, **zero-height** words pinned to
the top edge of their page (`yMin = yMax`). They never rendered, and their
anchor now falls outside the CropBox. Nothing visible is lost, and the page
numbers are untouched.

### Usage

```bash
.venv/bin/python trim_pdf.py INPUT.pdf OUT.pdf --verify
.venv/bin/python trim_pdf.py INPUT.pdf --dry-run --report   # one line per page
.venv/bin/python trim_pdf.py INPUT.pdf --pad 30             # more air
```

Tuning knobs, in the order to reach for them: `--pad` (20 px is ≈1.2–1.5 % of
the page width), `--ink` (lower = stricter about what counts as ink), and
`--min-ink` (raise it if a page has a dust speck near the edge). `--no-render`
skips the 408 pages that need poppler and leaves them untouched.

## Cutting the last white edge — `tight_pdf.py`

`trim_pdf.py` left two kinds of white on the page. `tight_pdf.py` removes both:
**896 / 902 pages cropped, 94 % of the page area kept** (563.8 → 530.6 million
pt²), and still not one pixel re-encoded.

| What was left | Why | Fixed by |
|---|---|---|
| ~7 pt on the 200–300 ppi pages, **17–19 pt** on the 1290 px screenshots | the pad was 20 *source pixels*, which is 4.8 pt at 300 ppi but 17.6 pt at 80 ppi | `--pad` is now in **points** (default 1 pt ≈ 0.35 mm) |
| 56 / 72 / 147 / 255 pt on eleven A4 worksheets (pp. 96, 98, 103, 135, 138, 154, 167, 169, 193, 228, 236) | the page is a 391×519 pt image drawn at x = 56.8, y = 252.1 inside a 595×842 sheet, but "no margin" was tested against the **image**, not the **page**, so it never cropped | the test is now `rect ≈ page box`, and the crop is clamped to the page |

| Check | Result |
|---|---|
| pages cropped | 896 / 902 |
| left alone | 3 pages whose ink already reaches every edge (front cover, promo page, a section opener) + 3 blank |
| ink outside the cut | **0 px** on all 896 cropped pages |
| image streams | **960 / 960 byte-identical** |
| content streams | **902 / 902 byte-identical** — the crop is only `/MediaBox` + `/CropBox` |
| text operators | identical on all 902 pages |
| `pdftotext` | 897 pages byte-identical; 5 pages (311, 669–672) differ only in the *order* of tiny math fragments — same 10 387 non-space characters, character multiset identical |
| renders | all 902 pages, 0 poppler warnings; sampled pages within 1.4 % ink, bbox shift ≤ 1 px |

The median page drops from 6.1 pt of border to 1 pt; the eleven worksheets go
from 595 × 842 to ≈ 392 × 516 pt, i.e. **60 % less page** for the same ink.  Page
numbers are kept: on these pages they sit inside the header line ("Capitolo 3 …
41"), so dropping them would mean cutting text.

### How the cut is found

The ink mask is the same idea as `trim_pdf.py` (pixel < `--ink`, a row/column
must hold `--min-ink` pixels, long rules are followed out, `--pad` points of
air), plus one step: if a handful of stray pixels (≤ 64, within 8 px of the box)
were excluded by the `--min-ink` rule, the box grows to swallow them rather than
cut them — a JPEG speck under the barcode on the back cover, for instance.

Image pages are measured on the **native bitmap** (`pad` is converted to bitmap
pixels through the placement matrix, so 1 pt is 1 pt at any resolution); pages
with vector text, forms or several images are measured on a 200 dpi poppler
render.

### Why the box is not translated to 0,0

`trim_pdf.py` prefixes `q 1 0 0 1 -x0 -y0 cm` and sets `[0 0 w h]`. That works,
but moving the user space makes poppler's reading-order heuristic regroup a few
superscripts. `tight_pdf.py` instead sets `/MediaBox` and `/CropBox` to the ink
rectangle **in place**: the content stream is not rewritten at all (byte-identical,
checked by `--verify`), so text matrices, image placements and the text layer are
untouched. `--shift-origin` restores the old behaviour for tools that insist on a
`[0 0 w h]` box.

### Usage

```bash
.venv/bin/python tight_pdf.py "…-lite-trim.pdf" "…-lite-tight.pdf" --verify
.venv/bin/python tight_pdf.py INPUT.pdf --dry-run --report   # one line per page
.venv/bin/python tight_pdf.py INPUT.pdf --pad 0              # not even 1 pt of air
.venv/bin/python tight_pdf.py INPUT.pdf --shift-origin        # [0 0 w h] boxes
```

## If you want real text instead of screenshots

That is a different job: OCR the 902 page images (tesseract `ita`) and rebuild a
text PDF. That would land at a few MB and give searchable text, but layout,
maths and superscripts would have to be re-checked. Ask if you want that route.
