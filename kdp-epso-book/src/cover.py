"""Full-wrap covers (paperback + hardcover case laminate) and the Kindle front cover (native 1:1.6 layout). All vector.

Paperback: width = 0.125 + 8.25 + spine + 8.25 + 0.125 in, height = 11.25 in, spine = pages x 0.002252 in (white paper).
Hardcover: wrap 0.591 in on every edge, hinge 0.394 in; spine = pages x 0.002252 + 0.187 in. Verify against the KDP
template for the final page count and pass exact values with --hc-width/--hc-height/--hc-spine if they differ.
"""
import argparse
import math
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fontsetup  # noqa: F401,E402  (must precede other reportlab imports)
from pypdf import PdfReader  # noqa: E402
from reportlab.lib.colors import Color, HexColor  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import Frame, Paragraph  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build"

TRIM_W, TRIM_H = 8.25, 11.0
NAVY_TOP = HexColor("#0F3596")
NAVY_BOT = HexColor("#0A1E55")
GOLD = HexColor("#FFCC00")
GOLD_SOFT = HexColor("#F2C230")
WHITE = Color(1, 1, 1)
PALE = HexColor("#C9D8FF")
AUTHOR = "CONCOURS PREP"


def star(c, x, y, r, fill=GOLD, alpha=1.0, rot=0):
    pts = []
    for i in range(10):
        ang = math.radians(90 + rot + i * 36)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.saveState(); c.setFillColor(fill); c.setFillAlpha(alpha); c.drawPath(p, stroke=0, fill=1); c.restoreState()


def background(c, x0, y0, w, h):
    c.saveState()
    p = c.beginPath(); p.rect(x0, y0, w, h); c.clipPath(p, stroke=0)
    c.linearGradient(x0, y0 + h, x0, y0, (NAVY_TOP, NAVY_BOT), extend=True)
    c.restoreState()


def building(c, cx, base, W, H, seed=3):
    """Stylised modern Brussels-style institutional building: curved glass wings and horizontal louvres."""
    core = W * 0.06
    floors = 13
    c.saveState()
    c.setFillColor(HexColor("#2050C0")); c.setFillAlpha(0.22)
    c.ellipse(cx - W * 0.56, base - H * 0.06, cx + W * 0.56, base + H * 0.04, stroke=0, fill=1)
    c.restoreState()

    def wing(sign, hmul):
        x_in = cx + sign * core
        x_out = cx + sign * W / 2
        top_in = base + H * hmul
        top_out = base + H * 0.80 * hmul
        p = c.beginPath()
        p.moveTo(x_in, base)
        p.lineTo(x_out, base + H * 0.02)
        p.lineTo(x_out, top_out)
        p.curveTo(x_out - sign * W * 0.12, top_out + H * 0.1 * hmul, x_in + sign * W * 0.12, top_in + H * 0.01, x_in, top_in)
        p.close()
        c.saveState()
        c.clipPath(p, stroke=0)
        light = HexColor("#3A72E0") if sign < 0 else HexColor("#2B5CC8")
        c.linearGradient(x_in, top_in, x_in, base, (light, HexColor("#0E3590")), extend=True)
        for i in range(1, floors + 1):
            t = i / (floors + 1)
            y_in = base + H * hmul * t
            y_out = base + H * 0.02 + (H * 0.80 * hmul - H * 0.02) * t
            c.setStrokeColor(PALE); c.setStrokeAlpha(0.55); c.setLineWidth(1.8)
            c.line(x_in, y_in, x_out, y_out)
        for j in range(1, 14):
            xx = x_in + (x_out - x_in) * j / 14
            c.setStrokeColor(WHITE); c.setStrokeAlpha(0.12); c.setLineWidth(0.5)
            c.line(xx, base, xx, base + H * 1.2)
        c.setFillColor(WHITE); c.setFillAlpha(0.06)
        c.rect(min(x_in, x_out) + abs(x_out - x_in) * 0.18, base, abs(x_out - x_in) * 0.16, H * 1.2, stroke=0, fill=1)
        c.restoreState()
        c.saveState(); c.setStrokeColor(PALE); c.setStrokeAlpha(0.85); c.setLineWidth(1.1)
        c.drawPath(p, stroke=1, fill=0); c.restoreState()

    wing(-1, 1.06)
    wing(1, 0.96)
    c.saveState()
    c.setFillColor(HexColor("#0B2A78")); c.rect(cx - core, base, 2 * core, H * 1.12, stroke=0, fill=1)
    c.setStrokeColor(PALE); c.setStrokeAlpha(0.85); c.setLineWidth(1.1); c.rect(cx - core, base, 2 * core, H * 1.12, stroke=1, fill=0)
    for i in range(1, floors + 1):
        y = base + H * 1.06 * i / (floors + 1)
        c.setStrokeColor(GOLD_SOFT); c.setStrokeAlpha(0.35); c.setLineWidth(0.8)
        c.line(cx - core * 0.6, y, cx + core * 0.6, y)
    c.setFillColor(PALE); c.setFillAlpha(0.9)
    c.rect(cx - core * 1.35, base + H * 1.12, core * 2.7, H * 0.025, stroke=0, fill=1)
    c.restoreState()
    c.saveState(); c.setStrokeColor(PALE); c.setStrokeAlpha(0.9); c.setLineWidth(1.4)
    c.line(cx - W * 0.5, base, cx + W * 0.5, base)
    c.setFillColor(GOLD_SOFT); c.setFillAlpha(0.85)
    c.rect(cx - core * 2.2, base + H * 0.05, core * 4.4, H * 0.012, stroke=0, fill=1)
    for k in range(1, 5):
        c.setStrokeColor(PALE); c.setStrokeAlpha(0.14 - k * 0.025); c.setLineWidth(0.8)
        c.line(cx - W * (0.46 - k * 0.04), base - k * 5, cx + W * (0.46 - k * 0.04), base - k * 5)
    c.restoreState()


def scattered_stars(c, cx, cy, sw, sh):
    # an irregular scatter of 8 stars of different sizes; deliberately not a ring, arc or flag pattern
    pts = [(-0.46, 0.05, 0.17), (-0.27, 0.92, 0.10), (-0.05, 0.55, 0.22), (0.12, 0.98, 0.08), (0.34, 0.62, 0.14),
           (0.50, -0.15, 0.09), (-0.20, 0.10, 0.07), (0.22, 0.20, 0.06)]
    for i, (dx, dy, r) in enumerate(pts):
        star(c, cx + dx * sw, cy + dy * sh, r * inch, alpha=0.95 if r > 0.1 else 0.72, rot=(i * 7) % 15 - 7)


def pill(c, x, y, text, fs=11, pad=10, h=23):
    w = c.stringWidth(text, "Sans-Semi", fs) + 2 * pad
    c.saveState()
    c.setStrokeColor(GOLD); c.setLineWidth(1.1); c.setFillColor(WHITE); c.setFillAlpha(0.07)
    c.roundRect(x, y, w, h, h / 2, stroke=1, fill=1)
    c.setFillAlpha(1); c.setFillColor(WHITE); c.setFont("Sans-Semi", fs)
    c.drawString(x + pad, y + h / 2 - fs * 0.35, text)
    c.restoreState()
    return w


def front(c, x0, y0, H_in=TRIM_H):
    """Front panel at trim origin (x0, y0); taller panels (Kindle) stretch the middle."""
    W, H = TRIM_W * inch, H_in * inch
    extra = (H_in - TRIM_H) * inch
    left = x0 + 0.6 * inch
    top = y0 + H
    c.setFillColor(GOLD); c.setFont("Sans-Bold", 10.5)
    c.drawString(left, top - 0.95 * inch, "INDEPENDENT PRACTICE WORKBOOK  ·  VERBAL · NUMERICAL · ABSTRACT & MORE")
    sh = extra * 0.15
    c.setFillColor(WHITE); c.setFont("Sans-Bold", 60)
    c.drawString(left - 2, top - 1.95 * inch - sh, "REASONING TESTS")
    c.drawString(left - 2, top - 2.75 * inch - sh, "WORKBOOK")
    c.setFillColor(GOLD); c.setFont("Serif-BoldIt", 42)
    c.drawString(left, top - 3.45 * inch - sh, "for EPSO Exams")
    yb = top - 3.72 * inch - sh
    c.setStrokeColor(GOLD); c.setLineWidth(2.2); c.line(left, yb, left + 1.4 * inch, yb)
    c.setFillColor(WHITE); c.setFont("Serif", 16.5)
    c.drawString(left, yb - 0.45 * inch, "413 original practice questions with full worked solutions")
    x = left; y = yb - 1.05 * inch
    for t in ["Verbal", "Numerical", "Abstract", "Situational judgement"]:
        x += pill(c, x, y, t) + 8
    bx, by, br = x0 + W - 1.3 * inch, y - 0.37 * inch - extra * 0.04, 0.68 * inch
    c.saveState(); c.setFillColor(GOLD); c.circle(bx, by, br, stroke=0, fill=1)
    c.setStrokeColor(NAVY_BOT); c.setLineWidth(1.2); c.circle(bx, by, br - 5, stroke=1, fill=0)
    c.setFillColor(NAVY_BOT); c.setFont("Sans-Bold", 30); c.drawCentredString(bx, by + 6, "3")
    c.setFont("Sans-Bold", 10); c.drawCentredString(bx, by - 10, "TIMED MOCK")
    c.drawCentredString(bx, by - 22, "TESTS"); c.restoreState()
    cx = x0 + W / 2
    b_h = 2.45 * inch + extra * 0.45
    base = y0 + 1.55 * inch + extra * 0.12
    building(c, cx, base, W * 0.80, b_h)
    scattered_stars(c, cx - 0.2 * inch, base + b_h * 1.12 + 0.42 * inch + extra * 0.05, W * 0.36, 0.5 * inch + extra * 0.06)
    c.setFillColor(WHITE); c.setFont("Sans-Bold", 15)
    c.drawCentredString(cx, y0 + 0.95 * inch, AUTHOR)
    c.setFillColor(PALE); c.setFont("Sans", 10.5)
    c.drawCentredString(cx, y0 + 0.62 * inch, "Independent guide · Not affiliated with or endorsed by EPSO or the European Union")


BACK_BLURB = (
    "Selection tests for careers in the EU institutions are demanding, and the candidates who succeed are usually those who "
    "have practised under realistic conditions. This workbook gives you exactly that: <b>413 original questions</b> in the "
    "formats used in EPSO-style computer-based tests, each with a <b>full worked solution</b> that shows not only the right "
    "answer but why every other option is wrong."
)
BACK_BULLETS = [
    "<b>Verbal reasoning</b> — 125 passages, with common traps named and explained",
    "<b>Numerical reasoning</b> — 105 table and chart questions with step-by-step calculations",
    "<b>Abstract reasoning</b> — 105 figure series with every rule spelled out",
    "<b>Situational judgement</b>, <b>accuracy &amp; precision</b> and <b>prioritising &amp; organising</b> sets for assistant-level procedures",
    "<b>3 timed mock tests</b> (40 reasoning questions each), score guides, answer sheets, a score tracker and an error log",
    "<b>Strategy chapters</b> with clear methods, 4- and 8-week study plans and test-day tactics",
]


def back(c, x0, y0):
    W, H = TRIM_W * inch, TRIM_H * inch
    left = x0 + 0.65 * inch
    c.setFillColor(GOLD); c.setFont("Sans-Bold", 26)
    c.drawString(left, y0 + H - 1.2 * inch, "Practise like it’s the real test.")
    st = ParagraphStyle("b", fontName="Serif", fontSize=12.5, leading=18, textColor=WHITE)
    bl = ParagraphStyle("bl", parent=st, fontSize=12, leading=16.5, leftIndent=18, bulletIndent=0, spaceAfter=7,
                        bulletFontName="DejaVu", bulletColor=GOLD)
    who = ParagraphStyle("w", parent=st, fontSize=11.5, leading=16.5)
    f = Frame(left, y0 + 4.75 * inch, W - 1.3 * inch, H - 6.15 * inch, showBoundary=0, leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
    gap = ParagraphStyle("sp", parent=st, fontSize=5, leading=7)
    story = [Paragraph(BACK_BLURB, st), Paragraph("&nbsp;", gap)]
    story += [Paragraph(b, bl, bulletText="★") for b in BACK_BULLETS]
    story += [Paragraph("&nbsp;", gap), Paragraph(
        "<b>Who is it for?</b> Candidates for administrator (AD), assistant (AST), AST-SC, contract-agent (CAST) and specialist "
        "selection procedures, and anyone preparing for European-style reasoning tests. The core reasoning skills stay the same "
        "even when test formats change, so always check your Notice of Competition.", who)]
    f.addFromList(story, c)
    sy = y0 + 3.95 * inch
    c.saveState(); c.setFillColor(WHITE); c.setFillAlpha(0.08)
    c.roundRect(left, sy, W - 1.3 * inch, 0.62 * inch, 8, stroke=0, fill=1); c.restoreState()
    items = [("413", "questions"), ("3", "timed mock tests"), ("6", "test types"), ("4 & 8", "week study plans")]
    colw = (W - 1.3 * inch) / 4
    for i, (n, lab) in enumerate(items):
        cxx = left + colw * (i + 0.5)
        c.setFillColor(GOLD); c.setFont("Sans-Bold", 17); c.drawCentredString(cxx, sy + 0.33 * inch, n)
        c.setFillColor(WHITE); c.setFont("Sans", 9.5); c.drawCentredString(cxx, sy + 0.12 * inch, lab)
    c.setFillColor(WHITE); c.setFont("Sans-Bold", 12); c.drawString(left, y0 + 3.55 * inch, AUTHOR)
    c.setFillColor(PALE); c.setFont("Serif-It", 10.5)
    c.drawString(left, y0 + 3.32 * inch, "Every question checked for a single, defensible correct answer,")
    c.drawString(left, y0 + 3.14 * inch, "with explanations written to teach the method, not just the result.")
    c.setFont("Sans", 8.6)
    c.drawString(left, y0 + 0.78 * inch, "Independent publication. Not affiliated with, authorised or endorsed by the European")
    c.drawString(left, y0 + 0.63 * inch, "Personnel Selection Office (EPSO), the European Union or any EU institution.")
    c.drawString(left, y0 + 0.48 * inch, "All questions are original.")
    return (x0 + W - 0.25 * inch - 2.0 * inch, y0 + 0.25 * inch, 2.0 * inch, 1.2 * inch)


def spine(c, x, sheet_h, w, y_trim, trim_h):
    c.saveState(); c.setFillColor(HexColor("#0A2668")); c.rect(x, 0, w, sheet_h, stroke=0, fill=1); c.restoreState()
    if w < 0.35 * inch:
        return
    cx = x + w / 2
    top, bot = y_trim + trim_h, y_trim
    half = (top - bot) / 2
    c.saveState()
    c.translate(cx, (top + bot) / 2); c.rotate(-90)
    fs = min(15, w / inch * 19)
    c.setFillColor(WHITE); c.setFont("Sans-Bold", fs)
    t = "REASONING TESTS WORKBOOK"
    start = -half + 0.95 * inch
    c.drawString(start, -fs * 0.35, t)
    tw = c.stringWidth(t, "Sans-Bold", fs)
    c.setFillColor(GOLD); c.setFont("Serif-BoldIt", fs)
    c.drawString(start + tw + 10, -fs * 0.35, "for EPSO Exams")
    c.setFillColor(PALE); c.setFont("Sans-Semi", fs * 0.72)
    c.drawRightString(half - 0.5 * inch, -fs * 0.27, AUTHOR)
    c.restoreState()
    star(c, cx, top - 0.5 * inch, min(0.13 * inch, w * 0.26))


def make_wrap(path, pages, kind="paperback", hc_width=None, hc_height=None, hc_spine=None):
    if kind == "paperback":
        sp = pages * 0.002252
        bleed = 0.125
        Wt, Ht = bleed * 2 + TRIM_W * 2 + sp, TRIM_H + bleed * 2
        back_x, front_x, spine_x, y_trim = bleed, bleed + TRIM_W + sp, bleed + TRIM_W, bleed
    else:
        wrap = 0.591
        sp = hc_spine or (pages * 0.002252 + 0.187)
        Wt = hc_width or (2 * (TRIM_W + 0.197) + sp + 2 * wrap)
        Ht = hc_height or (TRIM_H + 0.236 + 2 * wrap)
        panel = (Wt - sp) / 2 - wrap
        back_x = wrap + (panel - TRIM_W) / 2
        front_x = wrap + panel + sp + (panel - TRIM_W) / 2
        spine_x = wrap + panel
        y_trim = (Ht - TRIM_H) / 2
    c = canvas.Canvas(str(path), pagesize=(Wt * inch, Ht * inch), initialFontName="Sans")
    c.setTitle("Cover — Reasoning Tests Workbook for EPSO Exams")
    background(c, 0, 0, Wt * inch, Ht * inch)
    front(c, front_x * inch, y_trim * inch)
    bc = back(c, back_x * inch, y_trim * inch)
    spine(c, spine_x * inch, Ht * inch, sp * inch, y_trim * inch, TRIM_H * inch)
    c.showPage(); c.save()
    return {"width_in": round(Wt, 4), "height_in": round(Ht, 4), "spine_in": round(sp, 4), "barcode_box_pt": [round(v, 1) for v in bc]}


def make_front_only(path, h_in=TRIM_H):
    c = canvas.Canvas(str(path), pagesize=(TRIM_W * inch, h_in * inch), initialFontName="Sans")
    background(c, 0, 0, TRIM_W * inch, h_in * inch)
    front(c, 0, 0, h_in)
    c.showPage(); c.save()


def kindle_jpg(out_jpg):
    from PIL import Image
    pdf = OUT / "kindle_front.pdf"
    make_front_only(pdf, TRIM_W * 1.6)
    tmp = OUT / "kindle_tmp"
    subprocess.run(["pdftoppm", "-r", str(round(1600 / TRIM_W)), "-png", "-singlefile", str(pdf), str(tmp)], check=True)
    im = Image.open(str(tmp) + ".png").convert("RGB").resize((1600, 2560), Image.LANCZOS)
    im.save(out_jpg, "JPEG", quality=92, optimize=True, progressive=True)
    Path(str(tmp) + ".png").unlink(); pdf.unlink()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interior", default=str(OUT / "interior.pdf"))
    ap.add_argument("--hc-width", type=float); ap.add_argument("--hc-height", type=float); ap.add_argument("--hc-spine", type=float)
    a = ap.parse_args()
    pages = len(PdfReader(a.interior).pages)
    info_pb = make_wrap(OUT / "cover_paperback.pdf", pages, "paperback")
    info_hc = make_wrap(OUT / "cover_hardcover.pdf", pages, "hardcover", a.hc_width, a.hc_height, a.hc_spine)
    make_front_only(OUT / "cover_front.pdf")
    kindle_jpg(OUT / "kindle_cover.jpg")
    print("pages", pages)
    print("paperback", info_pb)
    print("hardcover", info_hc)


if __name__ == "__main__":
    main()
