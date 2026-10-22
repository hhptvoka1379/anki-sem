import pymupdf, numpy as np, re, sys, json, time
from rapidocr_onnxruntime import RapidOCR
d = pymupdf.open('Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf')
ocr = RapidOCR()
def header(i):
    p = d[i]
    r = p.rect
    clip = pymupdf.Rect(r.x0, r.y0, r.x1, r.y0 + r.height*0.06)
    pix = p.get_pixmap(dpi=200, clip=clip)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    res, _ = ocr(img)
    return ' | '.join(t for _,t,_ in res) if res else ''
targets = [int(x) for x in sys.argv[1:]]
out = {}
t0=time.time()
for t in targets:
    base = t + 3
    found = None
    for off in range(-12, 16):
        i = base + off
        if i < 0 or i >= len(d): continue
        h = header(i)
        nums = re.findall(r'(\d+)\s*$', h)
        if nums and int(nums[-1]) == t:
            found = (i, h); break
    out[t] = found
    print(t, found, flush=True)
print('elapsed', round(time.time()-t0,1), file=sys.stderr)
