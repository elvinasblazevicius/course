"""Pre-flight checks for KDP: page size, embedded fonts, margins (gutter-aware), cover dimensions. Exits non-zero on failure."""
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "build"
W, H = 594, 792
IN, OUT_M = 0.875 * 72, 0.6 * 72
errors = []

r = PdfReader(B / "interior.pdf")
pages = len(r.pages)
for i, p in enumerate(r.pages):
    if (round(float(p.mediabox.width)), round(float(p.mediabox.height))) != (W, H):
        errors.append(f"page {i + 1}: size {p.mediabox}")
for fn in ["interior.pdf", "cover_paperback.pdf", "cover_hardcover.pdf"]:
    rr = PdfReader(B / fn)
    for p in rr.pages:
        for f in (p["/Resources"].get("/Font") or {}).values():
            f = f.get_object()
            fd = f.get("/FontDescriptor")
            if fd is None and "/DescendantFonts" in f:
                fd = f["/DescendantFonts"][0].get_object().get("/FontDescriptor")
            if not (fd and any(k in fd.get_object() for k in ("/FontFile", "/FontFile2", "/FontFile3"))):
                errors.append(f"{fn}: font not embedded {f.get('/BaseFont')}")

for fn in ["interior.pdf", "cover_paperback.pdf", "cover_hardcover.pdf"]:
    for i, p in enumerate(PdfReader(B / fn).pages):
        if p.get("/Annots"):
            errors.append(f"{fn} page {i + 1}: annotations/links (KDP removes them as non-printable markup)")

min_gutter = 999
with pdfplumber.open(B / "interior.pdf") as pdf:
    for i, p in enumerate(pdf.pages):
        odd = (i + 1) % 2 == 1
        left, right = (IN, W - OUT_M) if odd else (OUT_M, W - IN)
        objs = p.chars + p.rects + p.lines + p.curves
        for o in objs:
            if o["x0"] < left - 0.5 or o["x1"] > right + 0.5:
                errors.append(f"page {i + 1}: object outside text block ({o['x0']:.1f}–{o['x1']:.1f})")
                break
        if objs:
            g = min(o["x0"] for o in objs) if odd else W - max(o["x1"] for o in objs)
            min_gutter = min(min_gutter, g)
need = 0.625 * 72 if pages > 300 else 0.5 * 72
if min_gutter < need:
    errors.append(f"gutter {min_gutter / 72:.3f} in below KDP minimum {need / 72:.3f} in")

spine = pages * 0.002252
cw = float(PdfReader(B / "cover_paperback.pdf").pages[0].mediabox.width) / 72
exp = 0.25 + 2 * 8.25 + spine
if abs(cw - exp) > 0.01:
    errors.append(f"paperback cover width {cw:.4f} in, expected {exp:.4f} in")

print(f"pages={pages} min_gutter={min_gutter / 72:.3f}in spine={spine:.4f}in cover_width={cw:.4f}in")
if errors:
    print("FAILED:\n  " + "\n  ".join(errors[:30]))
    sys.exit(1)
print("All pre-flight checks passed.")
