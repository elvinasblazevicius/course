"""Vector figure rendering (reportlab Drawings) for abstract frames and numerical charts. Grayscale only."""
import fontsetup  # noqa: F401,E402  (must precede other reportlab imports)
import math
from pathlib import Path

from reportlab.graphics.shapes import Circle, Drawing, Group, Line, PolyLine, Polygon, Rect, String, Wedge
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "fonts"


def register_fonts():
    reg = pdfmetrics.getRegisteredFontNames()
    if "Serif" in reg:
        return
    for fam, short in [("Serif", "SourceSerif"), ("Sans", "SourceSans"), ("Mono", "JBMono")]:
        pdfmetrics.registerFont(TTFont(fam, str(FONT_DIR / f"{short}-400.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-It", str(FONT_DIR / f"{short}-400i.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-Semi", str(FONT_DIR / f"{short}-600.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-Bold", str(FONT_DIR / f"{short}-700.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-BoldIt", str(FONT_DIR / f"{short}-700i.ttf")))
        from reportlab.lib.fonts import addMapping
        addMapping(fam, 0, 0, fam); addMapping(fam, 0, 1, f"{fam}-It")
        addMapping(fam, 1, 0, f"{fam}-Bold"); addMapping(fam, 1, 1, f"{fam}-BoldIt")


register_fonts()
from reportlab.graphics import shapes as _shapes  # noqa: E402
_shapes.STATE_DEFAULTS["fontName"] = "Sans"

BLACK = Color(0, 0, 0)
INK = Color(0.1, 0.1, 0.1)
GREY = Color(0.58, 0.58, 0.58)
LIGHT = Color(0.86, 0.86, 0.86)
FAINT = Color(0.94, 0.94, 0.94)
WHITE = Color(1, 1, 1)
FILL = {"white": WHITE, "grey": GREY, "black": BLACK}
SERIES_FILLS = [Color(0.2, 0.2, 0.2), Color(0.62, 0.62, 0.62), Color(0.85, 0.85, 0.85), WHITE]


# ------------------------------------------------------------------ abstract frames
RING = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]  # clockwise from top-left


def _rotate(pts, ang_deg, cx, cy):
    a = math.radians(-ang_deg)  # clockwise positive
    out = []
    for x, y in pts:
        out.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return out


def _flat(pts):
    return [c for p in pts for c in p]


def _shape(kind, cx, cy, r, fill):
    sw = max(0.6, r * 0.12)
    f = FILL[fill]
    if kind == "circle":
        return Circle(cx, cy, r, fillColor=f, strokeColor=BLACK, strokeWidth=sw)
    if kind == "square":
        return Rect(cx - r * 0.88, cy - r * 0.88, r * 1.76, r * 1.76, fillColor=f, strokeColor=BLACK, strokeWidth=sw)
    if kind == "triangle":
        pts = [(cx, cy + r * 1.05), (cx + r * 1.0, cy - r * 0.75), (cx - r * 1.0, cy - r * 0.75)]
        return Polygon(_flat(pts), fillColor=f, strokeColor=BLACK, strokeWidth=sw)
    if kind == "diamond":
        pts = [(cx, cy + r * 1.15), (cx + r * 0.9, cy), (cx, cy - r * 1.15), (cx - r * 0.9, cy)]
        return Polygon(_flat(pts), fillColor=f, strokeColor=BLACK, strokeWidth=sw)
    raise ValueError(kind)


def abstract_frame(elements, size=72, label=None):
    """Draw one abstract-reasoning frame as a Drawing of `size` points (plus label strip if label)."""
    lab_h = size * 0.24 if label else 0
    d = Drawing(size, size + lab_h)
    S = size
    cx, cy = S / 2, S / 2
    d.add(Rect(0.5, 0.5, S - 1, S - 1, fillColor=WHITE, strokeColor=INK, strokeWidth=0.9))
    kinds = {e["kind"] for e in elements}
    centre_taken = bool(kinds & {"arrow", "polygon", "quadrant", "fshape"})
    has_orbit = "orbit" in kinds
    # faint orbit guide points help readers see the 8 positions
    if has_orbit:
        for gx, gy in RING:
            d.add(Circle(cx + gx * S * 0.37, cy + gy * S * 0.37, S * 0.016, fillColor=Color(0.62, 0.62, 0.62), strokeColor=None))
    for e in elements:
        k = e["kind"]
        if k == "orbit":
            gx, gy = RING[e["pos"]]
            d.add(_shape(e["shape"], cx + gx * S * 0.37, cy + gy * S * 0.37, S * 0.07, e["fill"]))
        elif k == "arrow":
            acy = cy + (S * 0.14 if ("dots" in kinds and not has_orbit) else 0)
            L = S * 0.165
            w = S * 0.045
            pts = [(0, L), (w * 2.1, L - w * 2.4), (w * 0.7, L - w * 2.4), (w * 0.7, -L), (-w * 0.7, -L),
                   (-w * 0.7, L - w * 2.4), (-w * 2.1, L - w * 2.4)]
            d.add(Polygon(_flat(_rotate(pts, e["rot"] * 45, cx, acy)), fillColor=BLACK, strokeColor=BLACK, strokeWidth=0.4))
        elif k == "fshape":
            u = S * 0.2
            pts = [(-0.5, -1), (-0.1, -1), (-0.1, -0.1), (0.4, -0.1), (0.4, 0.25), (-0.1, 0.25), (-0.1, 0.6),
                   (0.6, 0.6), (0.6, 1), (-0.5, 1)]
            if e["mir"]:
                pts = [(-x, y) for x, y in pts]
            pts = [(x * u, y * u) for x, y in pts]
            d.add(Polygon(_flat(_rotate(pts, e["rot4"] * 90, cx, cy)), fillColor=BLACK, strokeColor=BLACK, strokeWidth=0.4))
        elif k == "polygon":
            n = e["sides"]; r = S * 0.19
            off = math.pi / n if n % 2 == 0 else 0.0
            pts = [(cx + r * math.sin(2 * math.pi * i / n + off), cy - r * 0.08 + r * math.cos(2 * math.pi * i / n + off)) for i in range(n)]
            d.add(Polygon(_flat(pts), fillColor=FILL[e["fill"]], strokeColor=BLACK, strokeWidth=1.0))
        elif k == "quadrant":
            h = S * 0.15
            quads = [(-1, 0), (0, 0), (0, -1), (-1, -1)]  # TL, TR, BR, BL (clockwise)
            for qi, (qx, qy) in enumerate(quads):
                d.add(Rect(cx + qx * h, cy + qy * h, h, h, fillColor=BLACK if qi == e["quad"] else WHITE,
                           strokeColor=BLACK, strokeWidth=0.9))
        elif k == "dots":
            n = e["count"]; r = S * 0.04
            gap = S * 0.115
            rows = [n] if n <= 3 else ([3, n - 3] if n <= 6 else [3, 3, n - 6])
            if centre_taken and not has_orbit:
                y0 = S * 0.33
            else:
                y0 = cy + gap * (len(rows) - 1) / 2
            for ri, cnt in enumerate(rows):
                    x0 = cx - gap * (cnt - 1) / 2
                    for i in range(cnt):
                        d.add(Circle(x0 + i * gap, y0 - ri * gap, r, fillColor=BLACK, strokeColor=None))
    if label:
        d.add(String(S / 2, S + lab_h * 0.28, label, fontName="Sans-Bold", fontSize=S * 0.15, textAnchor="middle", fillColor=INK))
    return d


def abstract_row(frames, size=72, labels=None, gap=8, question_mark=False):
    n = len(frames) + (1 if question_mark else 0)
    lab_h = size * 0.24 if labels else 0
    W = n * size + (n - 1) * gap
    d = Drawing(W, size + lab_h)
    for i, fr in enumerate(frames):
        sub = abstract_frame(fr, size, labels[i] if labels else None)
        g = Group(*sub.contents); g.translate(i * (size + gap), 0)
        d.add(g)
    if question_mark:
        x = len(frames) * (size + gap)
        d.add(Rect(x + 0.5, 0.5, size - 1, size - 1, fillColor=FAINT, strokeColor=INK, strokeWidth=0.9, strokeDashArray=[3, 2]))
        d.add(String(x + size / 2, size / 2 - size * 0.12, "?", fontName="Sans-Bold", fontSize=size * 0.4, textAnchor="middle", fillColor=INK))
    return d


# ------------------------------------------------------------------ charts
def _nice_max(v):
    exp = 10 ** math.floor(math.log10(v))
    for m in (1, 2, 2.5, 5, 10):
        if m * exp >= v:
            return m * exp
    return 10 * exp


def _fmt(v):
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v)):,}"
    return f"{v:,.1f}"


def bar_chart(fig, width=430, height=210):
    cats = fig["categories"]; series = fig["series"]
    d = Drawing(width, height)
    left, bottom, top = 38, 34, 22
    pw, ph = width - left - 8, height - bottom - top
    raw = max(max(s["values"]) for s in series) * 1.12
    step = _nice_max(raw / 5)
    steps = math.ceil(raw / step)
    vmax = step * steps
    for i in range(steps + 1):
        y = bottom + ph * i / steps
        d.add(Line(left, y, left + pw, y, strokeColor=LIGHT if i else INK, strokeWidth=0.5 if i else 0.8))
        d.add(String(left - 4, y - 3, _fmt(vmax * i / steps), fontName="Sans", fontSize=7.5, textAnchor="end", fillColor=INK))
    n, m = len(cats), len(series)
    gw = pw / n
    bw = min(26, gw * 0.75 / m)
    for ci, c in enumerate(cats):
        gx = left + gw * ci + (gw - bw * m) / 2
        for si, s in enumerate(series):
            v = s["values"][ci]
            h = ph * v / vmax
            d.add(Rect(gx + si * bw, bottom, bw - 1.5, h, fillColor=SERIES_FILLS[si], strokeColor=INK, strokeWidth=0.5))
            d.add(String(gx + si * bw + (bw - 1.5) / 2, bottom + h + 2.5, _fmt(v), fontName="Sans", fontSize=7, textAnchor="middle", fillColor=INK))
        d.add(String(left + gw * ci + gw / 2, bottom - 12, c, fontName="Sans", fontSize=8, textAnchor="middle", fillColor=INK))
    # legend
    lx = left
    for si, s in enumerate(series):
        d.add(Rect(lx, height - 12, 9, 7, fillColor=SERIES_FILLS[si], strokeColor=INK, strokeWidth=0.5))
        d.add(String(lx + 12, height - 11.5, s["name"], fontName="Sans", fontSize=8, fillColor=INK))
        lx += 20 + 4.6 * len(s["name"]) + 10
    d.add(String(width - 4, 3, f"Unit: {fig['unit']}", fontName="Sans-It", fontSize=7, textAnchor="end", fillColor=INK))
    return d


MARKERS = ["circle", "square", "triangle", "diamond"]
DASHES = [None, [4, 2], [1.5, 1.5], [6, 2, 1.5, 2]]


def line_chart(fig, width=430, height=220):
    cats = fig["categories"]; series = fig["series"]
    d = Drawing(width, height)
    left, bottom, top, right = 34, 30, 30, 70
    pw, ph = width - left - right, height - bottom - top
    allv = [v for s in series for v in s["values"]]
    vmin = max(0, math.floor(min(allv) - 1))
    vmax = math.ceil(max(allv) + 1)
    steps = vmax - vmin
    stride = 1 if steps <= 10 else 2
    for i in range(0, steps + 1, stride):
        y = bottom + ph * i / steps
        d.add(Line(left, y, left + pw, y, strokeColor=LIGHT if i else INK, strokeWidth=0.5 if i else 0.8))
        d.add(String(left - 4, y - 3, f"{vmin + i}", fontName="Sans", fontSize=7.5, textAnchor="end", fillColor=INK))
    n = len(cats)
    xs = [left + pw * (i + 0.5) / n for i in range(n)]
    for i, c in enumerate(cats):
        d.add(String(xs[i], bottom - 13, c, fontName="Sans", fontSize=8, textAnchor="middle", fillColor=INK))
    for si, s in enumerate(series):
        pts = [(xs[i], bottom + ph * (v - vmin) / steps) for i, v in enumerate(s["values"])]
        pl = PolyLine(_flat(pts), strokeColor=INK, strokeWidth=1.1)
        if DASHES[si]:
            pl.strokeDashArray = DASHES[si]
        d.add(pl)
        for (x, y), v in zip(pts, s["values"]):
            d.add(_shape(MARKERS[si], x, y, 2.6, "white" if si % 2 else "black"))
        # legend at right
        ly = height - top - 4 - si * 16
        lx = left + pw + 8
        lg = Line(lx, ly + 3, lx + 16, ly + 3, strokeColor=INK, strokeWidth=1.1)
        if DASHES[si]:
            lg.strokeDashArray = DASHES[si]
        d.add(lg)
        d.add(_shape(MARKERS[si], lx + 8, ly + 3, 2.6, "white" if si % 2 else "black"))
        d.add(String(lx + 20, ly, s["name"], fontName="Sans", fontSize=7.5, fillColor=INK))
    d.add(String(left, height - 10, f"Unit: {fig['unit']}", fontName="Sans-It", fontSize=7, fillColor=INK))
    return d


def pie_chart(fig, width=430, height=200):
    d = Drawing(width, height)
    cx, cy, r = 120, height / 2, min(85, height / 2 - 12)
    fills = [Color(0.25, 0.25, 0.25), Color(0.55, 0.55, 0.55), Color(0.78, 0.78, 0.78), Color(0.92, 0.92, 0.92), WHITE]
    ang = 90
    for i, (lab, v) in enumerate(zip(fig["labels"], fig["values"])):
        sweep = 360 * v / 100
        d.add(Wedge(cx, cy, r, ang - sweep, ang, fillColor=fills[i % 5], strokeColor=INK, strokeWidth=0.7))
        mid = math.radians(ang - sweep / 2)
        tx, ty = cx + r * 0.68 * math.cos(mid), cy + r * 0.68 * math.sin(mid)
        d.add(String(tx, ty - 3, f"{v}%", fontName="Sans-Bold", fontSize=8.5, textAnchor="middle",
                     fillColor=WHITE if i < 2 else INK))
        ang -= sweep
    ly = height - 30
    for i, (lab, v) in enumerate(zip(fig["labels"], fig["values"])):
        d.add(Rect(250, ly - i * 20, 11, 11, fillColor=fills[i % 5], strokeColor=INK, strokeWidth=0.6))
        d.add(String(267, ly - i * 20 + 2, f"{lab} — {v}%", fontName="Sans", fontSize=9, fillColor=INK))
    d.add(String(250, ly - 5 * 20 - 4, fig["total_label"], fontName="Sans-Semi", fontSize=9, fillColor=INK))
    return d


def chart(fig, width=430):
    t = fig["type"]
    if t == "bar":
        return bar_chart(fig, width)
    if t == "line":
        return line_chart(fig, width)
    if t == "pie":
        return pie_chart(fig, width)
    raise ValueError(t)


def to_png(drawing, path, dpi=200):
    from reportlab.graphics import renderPM
    renderPM.drawToFile(drawing, str(path), fmt="PNG", dpi=dpi, bg=0xFFFFFF)
