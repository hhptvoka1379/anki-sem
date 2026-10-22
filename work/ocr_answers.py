import pymupdf, numpy as np, sys
from rapidocr_onnxruntime import RapidOCR
d = pymupdf.open('/home/user/anki-sem/Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf')
ocr = RapidOCR()
start, end, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
with open(out, 'w') as f:
    for i in range(start, end):
        pix = d[i].get_pixmap(dpi=200)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        res, _ = ocr(img)
        f.write(f'\n===PDF {i}=== (printed ~{i-3})\n')
        if res:
            for box, text, score in res:
                f.write(f'[{round(box[0][1])},{round(box[0][0])}] {text}\n')
        f.flush()
print('done', start, end)
