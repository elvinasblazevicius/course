"""Bestseller-style covers: paperback full wrap, hardcover case laminate and Kindle front (native 1:1.6). All vector.

Design: one rich EU-blue field, huge stacked condensed title (Anton), one graphic idea (the "O" of REASONING is a
gold ring ticked through), gold accent line, tone-on-tone line drawing of a Brussels-style building for recognition.
Paperback: width = 0.125 + 8.25 + spine + 8.25 + 0.125 in, height 11.25 in, spine = pages x 0.002252 in.
Hardcover: wrap 0.591 in, hinge 0.394 in, spine = pages x 0.002252 + 0.187 in; verify against KDP's template and
pass --hc-width/--hc-height/--hc-spine if they differ.
"""
import argparse
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fontsetup  # noqa: F401,E402  (must precede other reportlab imports)
from pypdf import PdfReader  # noqa: E402
from reportlab.lib.colors import Color, HexColor  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.pdfbase.pdfmetrics import stringWidth  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import Frame, Paragraph  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build"

TRIM_W, TRIM_H = 8.25, 11.0
BLUE = HexColor("#1747A6")
BLUE_LIGHT = HexColor("#2D66D2")
BLUE_DEEP = HexColor("#0E2F7A")
LINE = HexColor("#5C8BE6")
GOLD = HexColor("#FFC72C")
WHITE = Color(1, 1, 1)
PALE = HexColor("#D6E2FF")
AUTHOR = "CONCOURS PREP"
ANTON_CAP = 0.859  # cap height / font size for Anton (OS/2 sCapHeight)


def tracked(c, x, y, text, font, size, track, color, anchor="middle"):
    """Draw letter-spaced text; anchor middle/left/right."""
    w = stringWidth(text, font, size) + track * (len(text) - 1)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "right":
        x -= w
    c.saveState()
    t = c.beginText(x, y)
    t.setFont(font, size); t.setCharSpace(track); t.setFillColor(color); t.textOut(text)
    c.drawText(t)
    c.restoreState()
    return w


def fit_size(text, font, width):
    return width / stringWidth(text, font, 100) * 100


def star(c, x, y, r, fill=GOLD, alpha=1.0):
    pts = [(x + (r if i % 2 == 0 else r * 0.42) * math.cos(math.radians(90 + i * 36)),
            y + (r if i % 2 == 0 else r * 0.42) * math.sin(math.radians(90 + i * 36))) for i in range(10)]
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    p.close()
    c.saveState(); c.setFillColor(fill); c.setFillAlpha(alpha); c.drawPath(p, stroke=0, fill=1); c.restoreState()


def background(c, w, h):
    c.saveState(); c.setFillColor(BLUE); c.rect(0, 0, w, h, stroke=0, fill=1); c.restoreState()


def glow(c, cx, cy, r):
    c.saveState()
    p = c.beginPath(); p.circle(cx, cy, r); c.clipPath(p, stroke=0)
    c.radialGradient(cx, cy, r, (BLUE_LIGHT, BLUE), extend=False)
    c.restoreState()


def building_lines(c, cx, base, W, H, x0, panel_w):
    """Tone-on-tone line drawing of a Brussels-style institutional building (curved wings, louvres, central core)."""
    core = W * 0.055
    floors = 11
    c.saveState()
    c.setStrokeColor(HexColor("#7FA6F0"))
    for sign, hmul in ((-1, 1.05), (1, 0.97)):
        x_in, x_out = cx + sign * core, cx + sign * W / 2
        top_in, top_out = base + H * hmul, base + H * 0.78 * hmul
        p = c.beginPath()
        p.moveTo(x_in, base); p.lineTo(x_out, base); p.lineTo(x_out, top_out)
        p.curveTo(x_out - sign * W * 0.12, top_out + H * 0.1 * hmul, x_in + sign * W * 0.12, top_in + H * 0.01, x_in, top_in)
        c.setStrokeAlpha(0.95); c.setLineWidth(1.5)
        c.drawPath(p, stroke=1, fill=0)
        for i in range(1, floors + 1):
            t = i / (floors + 1)
            c.setStrokeAlpha(0.55); c.setLineWidth(0.9)
            c.line(x_in, base + H * hmul * t, x_out, base + H * 0.78 * hmul * t)
    c.setStrokeAlpha(0.95); c.setLineWidth(1.5)
    c.rect(cx - core, base, 2 * core, H * 1.12, stroke=1, fill=0)
    c.line(cx - core * 1.4, base + H * 1.12, cx + core * 1.4, base + H * 1.12)
    half = min(W / 2 + 0.15 * inch, panel_w / 2 - 0.3 * inch)
    c.line(cx - half, base, cx + half, base)
    c.restoreState()


def building_hero(c, cx, base, W, H, panel_w):
    """Solid tone-on-tone illustration of a Brussels-style institutional building (curved glass wings, louvres,
    central core). Kept below #C4D6FA in brightness so white and gold stay reserved for the type."""
    core = W * 0.06
    floors = 12
    outline = HexColor("#C4D6FA")

    def wing(sign, hmul, c_top, c_bot):
        x_in, x_out = cx + sign * core, cx + sign * W / 2
        top_in, top_out = base + H * hmul, base + H * 0.80 * hmul
        p = c.beginPath()
        p.moveTo(x_in, base); p.lineTo(x_out, base); p.lineTo(x_out, top_out)
        p.curveTo(x_out - sign * W * 0.12, top_out + H * 0.1 * hmul, x_in + sign * W * 0.12, top_in + H * 0.01, x_in, top_in)
        p.close()
        c.saveState()
        c.clipPath(p, stroke=0)
        c.linearGradient(x_in, top_in, x_in, base, (c_top, c_bot), extend=True)
        for i in range(1, floors + 1):
            t = i / (floors + 1)
            c.setStrokeColor(HexColor("#9DBBF4")); c.setStrokeAlpha(0.6); c.setLineWidth(1.2)
            c.line(x_in, base + H * hmul * t, x_out, base + H * 0.80 * hmul * t)
        c.restoreState()
        c.saveState(); c.setStrokeColor(outline); c.setLineWidth(1.4); c.drawPath(p, stroke=1, fill=0); c.restoreState()

    wing(-1, 1.05, HexColor("#4A80E6"), HexColor("#2A5BC0"))   # sunlit
    wing(1, 0.97, HexColor("#3569CF"), HexColor("#22509F"))    # shade
    c.saveState()
    c.setFillColor(BLUE_DEEP); c.rect(cx - core, base, 2 * core, H * 1.14, stroke=0, fill=1)
    c.setStrokeColor(outline); c.setLineWidth(1.4); c.rect(cx - core, base, 2 * core, H * 1.14, stroke=1, fill=0)
    c.setFillColor(outline); c.rect(cx - core * 1.4, base + H * 1.14, core * 2.8, H * 0.025, stroke=0, fill=1)
    c.restoreState()
    # fade the bottom 0.4 in into the background (stepped overlay; no hard edge above the imprint)
    steps, fade_h = 24, 0.4 * inch
    half = W / 2 + 2
    c.saveState(); c.setFillColor(BLUE)
    for k in range(steps):
        y = base + fade_h * k / steps
        c.setFillAlpha(min(1.0, (1 - k / steps) * 0.95))
        c.rect(cx - half, y - 2, 2 * half, fade_h / steps + 2.2, stroke=0, fill=1)
    c.restoreState()


def tick_o(c, x, base, size):
    """Gold 'O' (set in Anton for a perfect type match) with a white check mark sweeping through it."""
    c.setFillColor(GOLD); c.setFont("Anton", size); c.drawString(x, base, "O")
    ow = stringWidth("O", "Anton", size)
    cap = size * ANTON_CAP
    cx, cy = x + ow / 2, base + cap / 2
    p = c.beginPath()
    p.moveTo(cx - ow * 0.30, cy - cap * 0.02)
    p.lineTo(cx - ow * 0.04, cy - cap * 0.26)
    p.lineTo(cx + ow * 0.52, cy + cap * 0.45)
    c.saveState()
    c.setLineCap(1); c.setLineJoin(1)
    c.setStrokeColor(BLUE); c.setLineWidth(size * 0.115); c.drawPath(p, stroke=1, fill=0)
    c.setStrokeColor(WHITE); c.setLineWidth(size * 0.075); c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def front(c, x0, y0, H_in=TRIM_H):
    W, H = TRIM_W * inch, H_in * inch
    extra = (H_in - TRIM_H) * inch
    cx = x0 + W / 2
    glow(c, cx, y0 + H * 0.62, W * (0.62 if extra == 0 else 0.72))

    top = y0 + H - 0.78 * inch - extra * 0.18
    title_w = W - 1.2 * inch
    s1 = fit_size("REASONING", "Anton", title_w)
    cap1 = s1 * ANTON_CAP
    b1 = top - 0.48 * inch - cap1
    b2 = b1 - cap1 - 0.20 * inch
    b3 = b2 - 0.55 * inch
    s3 = fit_size("EPSO EXAMS", "Anton", title_w * 0.80)
    b4 = b3 - 0.28 * inch - s3 * ANTON_CAP
    b5 = b4 - 0.55 * inch
    # lower third: building fills the space under the text (core top 0.39-0.45 in below the categories line)
    base = y0 + 1.40 * inch + extra * 0.05
    gap = 0.39 * inch if extra == 0 else 0.45 * inch
    bh = (b5 - gap - base) / 1.12
    building_hero(c, cx, base, W * 0.88, bh, W)

    tracked(c, cx, top, "400+ QUESTIONS · FULL WORKED SOLUTIONS", "Mont-Bold", 12.5, 3.2, GOLD)
    xs = cx - stringWidth("REASONING", "Anton", s1) / 2
    c.setFillColor(WHITE); c.setFont("Anton", s1); c.drawString(xs, b1, "REAS")
    xo = xs + stringWidth("REAS", "Anton", s1)
    tick_o(c, xo, b1, s1)
    c.setFillColor(WHITE); c.setFont("Anton", s1)
    c.drawString(xo + stringWidth("O", "Anton", s1), b1, "NING")
    # TESTS + seal balanced as one unit; seal diameter = cap height
    tests_w = stringWidth("TESTS", "Anton", s1)
    r = cap1 / 2
    sgap = 0.25 * inch
    gx = cx - (tests_w + sgap + 2 * r) / 2
    c.drawString(gx, b2, "TESTS")
    sx, sy = gx + tests_w + sgap + r, b2 + cap1 / 2
    c.saveState()
    c.setFillColor(GOLD); c.circle(sx, sy, r, stroke=0, fill=1)
    c.setStrokeColor(BLUE_DEEP); c.setLineWidth(1.2); c.circle(sx, sy, r - 6, stroke=1, fill=0)
    c.setFillColor(BLUE_DEEP); c.setFont("Anton", 44); c.drawCentredString(sx, sy + 4, "3")
    c.setFont("Mont-XBold", 10); c.drawCentredString(sx, sy - 14, "TIMED MOCK")
    c.drawCentredString(sx, sy - 26, "EXAMS")
    c.restoreState()
    w = tracked(c, cx, b3, "WORKBOOK FOR", "Mont-Bold", 15, 4, WHITE)
    c.setStrokeColor(GOLD); c.setLineWidth(1.6)
    c.line(x0 + 0.6 * inch, b3 + 5, cx - w / 2 - 14, b3 + 5)
    c.line(cx + w / 2 + 14, b3 + 5, x0 + W - 0.6 * inch, b3 + 5)
    c.setFillColor(GOLD); c.setFont("Anton", s3); c.drawCentredString(cx, b4, "EPSO EXAMS")
    tracked(c, cx, b5, "VERBAL · NUMERICAL · ABSTRACT · SITUATIONAL JUDGEMENT", "Mont-Semi", 12, 1.6, PALE)
    tracked(c, cx, y0 + 0.92 * inch, AUTHOR, "Mont-XBold", 17, 4.5, WHITE)
    tracked(c, cx, y0 + 0.58 * inch, "INDEPENDENT GUIDE · NOT AFFILIATED WITH OR ENDORSED BY EPSO OR THE EU",
            "Mont-Med", 8.6, 0.8, PALE)


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
    "<b>3 timed mock exams</b> (40 reasoning questions each), score guides, answer sheets, a score tracker and an error log",
    "<b>Strategy chapters</b> with clear methods, 4- and 8-week study plans and test-day tactics",
]


def back(c, x0, y0):
    W, H = TRIM_W * inch, TRIM_H * inch
    left = x0 + 0.65 * inch
    c.setFillColor(WHITE); c.setFont("Anton", 34)
    c.drawString(left, y0 + H - 1.25 * inch, "PRACTISE LIKE IT’S")
    c.setFillColor(GOLD); c.drawString(left, y0 + H - 1.25 * inch - 40, "THE REAL TEST.")
    st = ParagraphStyle("b", fontName="Serif", fontSize=11.8, leading=16.6, textColor=WHITE)
    bl = ParagraphStyle("bl", parent=st, fontSize=11.2, leading=15.2, leftIndent=18, bulletIndent=0, spaceAfter=5,
                        bulletFontName="DejaVu", bulletColor=GOLD)
    who = ParagraphStyle("w", parent=st, fontSize=10.8, leading=15)
    f = Frame(left, y0 + 3.98 * inch, W - 1.3 * inch, H - 1.25 * inch - 64 - 3.98 * inch, showBoundary=0, leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
    gap = ParagraphStyle("sp", parent=st, fontSize=5, leading=7)
    story = [Paragraph(BACK_BLURB, st), Paragraph("&nbsp;", gap)]
    story += [Paragraph(b, bl, bulletText="✓") for b in BACK_BULLETS]
    story += [Paragraph("&nbsp;", gap), Paragraph(
        "<b>Who is it for?</b> Candidates for administrator (AD), assistant (AST), AST-SC, contract-agent (CAST) and specialist "
        "selection procedures, and anyone preparing for European-style reasoning tests. The core reasoning skills stay the same "
        "even when test formats change, so always check your Notice of Competition.", who)]
    f.addFromList(story, c)
    assert not story, "back-cover copy does not fit its frame"
    sy = y0 + 3.15 * inch
    c.saveState(); c.setFillColor(BLUE_DEEP); c.setFillAlpha(0.55)
    c.roundRect(left, sy, W - 1.3 * inch, 0.66 * inch, 8, stroke=0, fill=1); c.restoreState()
    items = [("413", "QUESTIONS"), ("3", "TIMED MOCK EXAMS"), ("6", "TEST TYPES"), ("4 & 8", "WEEK STUDY PLANS")]
    colw = (W - 1.3 * inch) / 4
    for i, (n, lab) in enumerate(items):
        cxx = left + colw * (i + 0.5)
        c.setFillColor(GOLD); c.setFont("Anton", 20); c.drawCentredString(cxx, sy + 0.30 * inch, n)
        tracked(c, cxx, sy + 0.11 * inch, lab, "Mont-Semi", 7.5, 0.8, WHITE)
    tracked(c, left, y0 + 2.72 * inch, AUTHOR, "Mont-XBold", 12.5, 3, WHITE, anchor="left")
    c.setFillColor(PALE); c.setFont("Serif-It", 10.5)
    c.drawString(left, y0 + 2.49 * inch, "Every question checked for a single, defensible correct answer,")
    c.drawString(left, y0 + 2.31 * inch, "with explanations written to teach the method, not just the result.")
    c.setFont("Mont-Med", 8.2)
    c.drawString(left, y0 + 0.78 * inch, "Independent publication. Not affiliated with, authorised or endorsed by the European")
    c.drawString(left, y0 + 0.63 * inch, "Personnel Selection Office (EPSO), the European Union or any EU institution.")
    c.drawString(left, y0 + 0.48 * inch, "All questions are original.")
    return (x0 + W - 0.25 * inch - 2.0 * inch, y0 + 0.25 * inch, 2.0 * inch, 1.2 * inch)


def spine(c, x, w, y_trim, trim_h):
    if w < 0.35 * inch:
        return
    cx = x + w / 2
    top, bot = y_trim + trim_h, y_trim
    half = (top - bot) / 2
    c.saveState()
    c.translate(cx, (top + bot) / 2); c.rotate(-90)
    fs = min(22, w / inch * 27)
    capoff = fs * ANTON_CAP / 2
    start = -half + 0.9 * inch
    c.setFillColor(WHITE); c.setFont("Anton", fs); c.drawString(start, -capoff, "REASONING TESTS WORKBOOK")
    tw = stringWidth("REASONING TESTS WORKBOOK", "Anton", fs)
    c.setFillColor(GOLD); c.drawString(start + tw + 12, -capoff, "FOR EPSO EXAMS")
    tracked(c, half - 0.5 * inch, -fs * 0.22, AUTHOR, "Mont-XBold", fs * 0.5, 1.5, PALE, anchor="right")
    c.restoreState()


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
    background(c, Wt * inch, Ht * inch)
    front(c, front_x * inch, y_trim * inch)
    bc = back(c, back_x * inch, y_trim * inch)
    spine(c, spine_x * inch, sp * inch, y_trim * inch, TRIM_H * inch)
    c.showPage(); c.save()
    return {"width_in": round(Wt, 4), "height_in": round(Ht, 4), "spine_in": round(sp, 4), "barcode_box_pt": [round(v, 1) for v in bc]}


def make_front_only(path, h_in=TRIM_H):
    c = canvas.Canvas(str(path), pagesize=(TRIM_W * inch, h_in * inch), initialFontName="Sans")
    background(c, TRIM_W * inch, h_in * inch)
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
