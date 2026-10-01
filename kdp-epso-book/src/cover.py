"""Bestseller-style covers: paperback full wrap, hardcover case laminate and Kindle front (native 1:1.6). All vector.

Design: one rich EU-blue field, huge stacked condensed title (League Gothic; small type in Libre Franklin), one graphic idea (the "O" of REASONING is a
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
ANTON_CAP = 0.735  # cap height / font size for League Gothic (OS/2 sCapHeight)


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


def glow(c, cx, cy, r, panel=None):
    c.saveState()
    if panel:
        q = c.beginPath(); q.rect(*panel); c.clipPath(q, stroke=0)
    p = c.beginPath(); p.circle(cx, cy, r); c.clipPath(p, stroke=0)
    c.radialGradient(cx, cy, r, (BLUE_LIGHT, BLUE, BLUE), positions=(0, 0.62, 1), extend=False)
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
    """Solid tone-on-tone Brussels-style institutional building: raised on pilotis, curved glass wings with
    horizontal louvres, a slightly taller central block with vertical fins. Nothing brighter than #C4D6FA."""
    outline = HexColor("#C4D6FA")
    pod = H * 0.16
    core = W * 0.075
    floors = 11
    top_base = base + pod
    hh = H - pod

    # podium on pilotis
    c.saveState()
    c.setFillColor(HexColor("#0E2F7A")); c.rect(cx - W / 2 + W * 0.03, base, W - W * 0.06, pod, stroke=0, fill=1)
    c.setFillColor(HexColor("#3A6BCF"))
    n = 16
    span = W * 0.90
    colw = span / n * 0.32
    for k in range(n + 1):
        x = cx - span / 2 + span * k / n
        c.rect(x - colw / 2, base, colw, pod, stroke=0, fill=1)
    c.restoreState()

    def wing(sign, hmul, c_top, c_bot):
        x_in, x_out = cx + sign * core, cx + sign * W / 2
        top_in, top_out = top_base + hh * hmul, top_base + hh * 0.74 * hmul
        p = c.beginPath()
        p.moveTo(x_in, top_base); p.lineTo(x_out, top_base); p.lineTo(x_out, top_out)
        p.curveTo(x_out - sign * W * 0.16, top_out + hh * 0.17 * hmul, x_in + sign * W * 0.10, top_in, x_in, top_in)
        p.close()
        c.saveState()
        c.clipPath(p, stroke=0)
        c.linearGradient(x_in, top_in, x_in, top_base, (c_top, c_bot), extend=True)
        for i in range(1, floors + 1):
            t = i / (floors + 1)
            c.setStrokeColor(HexColor("#9DBBF4")); c.setStrokeAlpha(0.6); c.setLineWidth(1.3)
            c.line(x_in, top_base + hh * hmul * t, x_out, top_base + hh * 0.74 * hmul * t)
        c.restoreState()
        c.saveState(); c.setStrokeColor(outline); c.setLineWidth(1.4); c.drawPath(p, stroke=1, fill=0); c.restoreState()
        # darker end face for volume
        ew = W * 0.05
        q = c.beginPath()
        xe = x_out if sign > 0 else x_out
        q.moveTo(xe, top_base); q.lineTo(xe + sign * ew, top_base + hh * 0.03)
        q.lineTo(xe + sign * ew, top_out - hh * 0.04); q.lineTo(xe, top_out); q.close()
        c.saveState(); c.setFillColor(HexColor("#22509F")); c.setStrokeColor(outline); c.setLineWidth(1.0)
        c.drawPath(q, stroke=1, fill=1); c.restoreState()

    wing(-1, 1.0, HexColor("#4A80E6"), HexColor("#2A5BC0"))
    wing(1, 0.95, HexColor("#3569CF"), HexColor("#22509F"))
    # central block: same family of blues, taller, vertical fins (reads as architecture, not a doorway)
    ch = hh * 1.12
    c.saveState()
    c.setFillColor(HexColor("#3466CC")); c.rect(cx - core, top_base, 2 * core, ch, stroke=0, fill=1)
    c.setStrokeColor(HexColor("#9DBBF4")); c.setStrokeAlpha(0.7); c.setLineWidth(1.0)
    for k in (-0.5, 0, 0.5):
        c.line(cx + core * k, top_base, cx + core * k, top_base + ch)
    c.setStrokeAlpha(1); c.setStrokeColor(outline); c.setLineWidth(1.4)
    c.rect(cx - core, top_base, 2 * core, ch, stroke=1, fill=0)
    c.setFillColor(outline); c.rect(cx - core * 1.12, top_base + ch, core * 2.24, H * 0.04, stroke=0, fill=1)
    c.restoreState()
    # soft fade at the very bottom
    steps, fade_h = 14, 0.12 * inch
    c.saveState(); c.setFillColor(BLUE)
    for k in range(steps):
        y = base - fade_h + fade_h * k / steps
        c.setFillAlpha(min(1.0, (1 - k / steps) * 0.9))
        c.rect(cx - W / 2 - 2, y - 2, W + 4, fade_h / steps + 2.2, stroke=0, fill=1)
    c.restoreState()


def tick_o(c, x, base, size):
    """Gold 'O' (set in the display face for a perfect type match) with a white check mark sweeping through it."""
    c.setFillColor(GOLD); c.setFont("Display", size); c.drawString(x, base, "O")
    ow = stringWidth("O", "Display", size)
    cap = size * ANTON_CAP
    cx, cy = x + ow / 2, base + cap / 2
    p = c.beginPath()
    p.moveTo(cx - ow * 0.32, cy - cap * 0.02)
    p.lineTo(cx - ow * 0.06, cy - cap * 0.18)
    p.lineTo(cx + ow * 0.40, cy + cap * 0.34)
    c.saveState()
    c.setLineCap(1); c.setLineJoin(1)
    c.setStrokeColor(BLUE); c.setLineWidth(size * 0.10); c.drawPath(p, stroke=1, fill=0)
    c.setStrokeColor(WHITE); c.setLineWidth(size * 0.065); c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def front(c, x0, y0, H_in=TRIM_H):
    W, H = TRIM_W * inch, H_in * inch
    extra = (H_in - TRIM_H) * inch
    k = 1 + extra * 0.7 / (4 * inch)
    cx = x0 + W / 2
    glow(c, cx, y0 + H * 0.62, W * 0.66, panel=(x0, y0, W, H))

    top = y0 + H - 0.78 * inch - extra * 0.12
    title_w = W - 0.9 * inch
    s1 = fit_size("REASONING", "Display", title_w)
    cap1 = s1 * ANTON_CAP
    b1 = top - 0.48 * inch * k - cap1
    b2 = b1 - cap1 - 0.18 * inch * k
    b3 = b2 - 0.62 * inch * k
    s3 = fit_size("EPSO EXAMS", "Display", title_w * 0.92)
    b4 = b3 - 0.30 * inch * k - s3 * ANTON_CAP
    b5 = b4 - 0.62 * inch * k
    base = y0 + 1.24 * inch
    gap = 0.42 * inch if extra == 0 else 0.50 * inch
    bh = min((b5 - gap - base) / 1.04, 2.0 * inch if extra == 0 else 2.6 * inch)
    building_hero(c, cx, base, W * 0.72, bh, W)

    tracked(c, cx, top, "400+ QUESTIONS · FULL WORKED SOLUTIONS", "Frank-Bold", 12.5, 3.2, GOLD)
    xs = cx - stringWidth("REASONING", "Display", s1) / 2
    c.setFillColor(WHITE); c.setFont("Display", s1); c.drawString(xs, b1, "REAS")
    xo = xs + stringWidth("REAS", "Display", s1)
    tick_o(c, xo, b1, s1)
    c.setFillColor(WHITE); c.setFont("Display", s1)
    c.drawString(xo + stringWidth("O", "Display", s1), b1, "NING")
    tests_w = stringWidth("TESTS", "Display", s1)
    r = cap1 * 0.45
    sgap = 0.28 * inch
    gx = cx - (tests_w + sgap + 2 * r) / 2
    c.drawString(gx, b2, "TESTS")
    sx, sy = gx + tests_w + sgap + r, b2 + cap1 / 2
    c.saveState()
    c.translate(sx, sy)
    c.setFillColor(BLUE_DEEP); c.circle(0, 0, r, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(2.4); c.circle(0, 0, r - 6, stroke=1, fill=0)
    c.setLineWidth(0.9); c.circle(0, 0, r - 10.5, stroke=1, fill=0)
    c.setFillColor(WHITE); c.setFont("Display", r * 1.10)
    c.drawCentredString(0, -r * 0.06, "3")
    c.setStrokeColor(GOLD); c.setLineWidth(1.4); c.line(-r * 0.34, -r * 0.17, r * 0.34, -r * 0.17)
    lab = r * 0.135
    c.restoreState()
    c.saveState(); c.translate(sx, sy)
    tracked(c, 0, -r * 0.36, "TIMED MOCK", "Frank-Black", lab, 1.0, GOLD)
    tracked(c, 0, -r * 0.36 - lab * 1.25, "EXAMS", "Frank-Black", lab, 1.0, GOLD)
    c.restoreState()
    w = tracked(c, cx, b3, "WORKBOOK FOR", "Frank-Bold", 15, 4, WHITE)
    c.setStrokeColor(GOLD); c.setLineWidth(1.6)
    c.line(x0 + 0.6 * inch, b3 + 5, cx - w / 2 - 14, b3 + 5)
    c.line(cx + w / 2 + 14, b3 + 5, x0 + W - 0.6 * inch, b3 + 5)
    c.setFillColor(GOLD); c.setFont("Display", s3); c.drawCentredString(cx, b4, "EPSO EXAMS")
    tracked(c, cx, b5, "VERBAL · NUMERICAL · ABSTRACT · SITUATIONAL JUDGEMENT", "Frank-Semi", 12, 1.6, PALE)
    tracked(c, cx, y0 + 0.80 * inch, AUTHOR, "Frank-XBold", 17, 4.5, WHITE)
    tracked(c, cx, y0 + 0.48 * inch, "INDEPENDENT GUIDE · NOT AFFILIATED WITH OR ENDORSED BY EPSO OR THE EU",
            "Frank-Med", 8.6, 0.8, PALE)


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
    c.setFillColor(WHITE); c.setFont("Display", 50)
    c.drawString(left, y0 + H - 1.2 * inch, "PRACTISE LIKE IT’S")
    c.setFillColor(GOLD); c.drawString(left, y0 + H - 1.2 * inch - 52, "THE REAL TEST.")
    st = ParagraphStyle("b", fontName="Serif", fontSize=12.2, leading=17.2, textColor=WHITE)
    bl = ParagraphStyle("bl", parent=st, fontSize=11.2, leading=15.2, leftIndent=18, bulletIndent=0, spaceAfter=5,
                        bulletFontName="DejaVu", bulletColor=GOLD)
    who = ParagraphStyle("w", parent=st, fontSize=10.8, leading=15)
    f = Frame(left, y0 + 3.15 * inch, W - 1.3 * inch, H - 1.2 * inch - 52 - 26 - 3.15 * inch, showBoundary=0, leftPadding=0, rightPadding=0,
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
    sy = y0 + 2.35 * inch
    c.saveState(); c.setFillColor(BLUE_DEEP); c.setFillAlpha(0.55)
    c.roundRect(left, sy, W - 1.3 * inch, 0.66 * inch, 8, stroke=0, fill=1); c.restoreState()
    items = [("413", "QUESTIONS"), ("3", "TIMED MOCK EXAMS"), ("6", "TEST TYPES"), ("4 & 8", "WEEK STUDY PLANS")]
    colw = (W - 1.3 * inch) / 4
    for i, (n, lab) in enumerate(items):
        cxx = left + colw * (i + 0.5)
        c.setFillColor(GOLD); c.setFont("Display", 20); c.drawCentredString(cxx, sy + 0.30 * inch, n)
        tracked(c, cxx, sy + 0.11 * inch, lab, "Frank-Semi", 7.5, 0.8, WHITE)
    tracked(c, left, y0 + 1.95 * inch, AUTHOR, "Frank-XBold", 12.5, 3, WHITE, anchor="left")
    c.setFillColor(PALE); c.setFont("Serif-It", 10.5)
    c.drawString(left, y0 + 1.72 * inch, "Every question checked for a single, defensible correct answer,")
    c.drawString(left, y0 + 1.54 * inch, "with explanations written to teach the method, not just the result.")
    c.setFont("Frank-Med", 8.2)
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
    fs = min(34, w / inch * 44)
    capoff = fs * ANTON_CAP / 2
    x = -half + 0.85 * inch
    c.setFillColor(WHITE); c.setFont("Display", fs); c.drawString(x, -capoff, "REASONING TESTS")
    x += stringWidth("REASONING TESTS", "Display", fs) + 12
    x += tracked(c, x, -fs * 0.14, "WORKBOOK FOR", "Frank-Bold", fs * 0.4, 2, PALE, anchor="left") + 12
    c.setFillColor(GOLD); c.setFont("Display", fs); c.drawString(x, -capoff, "EPSO EXAMS")
    tracked(c, half - 0.5 * inch, -fs * 0.14, AUTHOR, "Frank-XBold", fs * 0.36, 1.5, PALE, anchor="right")
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
