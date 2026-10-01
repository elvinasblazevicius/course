"""Build the print-ready interior PDF (paperback and hardcover share it): 8.25 x 11 in, B&W, no bleed."""
import fontsetup  # noqa: F401,E402  (must precede other reportlab imports)
import re
import sys
from pathlib import Path

from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

sys.path.insert(0, str(Path(__file__).parent))
import assemble  # noqa: E402
from figures import abstract_row, chart, register_fonts  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build"
register_fonts()
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

PAGE_W, PAGE_H = 8.25 * inch, 11 * inch
M_IN, M_OUT, M_TOP, M_BOT = 0.875 * inch, 0.6 * inch, 0.8 * inch, 0.75 * inch
FW = PAGE_W - M_IN - M_OUT
FH = PAGE_H - M_TOP - M_BOT
INK = colors.Color(0.1, 0.1, 0.1)
MID = colors.Color(0.45, 0.45, 0.45)
RULE = colors.Color(0.7, 0.7, 0.7)
SHADE = colors.Color(0.92, 0.92, 0.92)
SHADE2 = colors.Color(0.86, 0.86, 0.86)

# ------------------------------------------------------------------ styles
ST = {
    "body": ParagraphStyle("body", fontName="Serif", fontSize=10.5, leading=15, textColor=INK, spaceAfter=6),
    "small": ParagraphStyle("small", fontName="Serif", fontSize=9.5, leading=13, textColor=INK, spaceAfter=4),
    "passage": ParagraphStyle("passage", fontName="Serif", fontSize=10.3, leading=14.6, textColor=INK, spaceAfter=6),
    "stem": ParagraphStyle("stem", fontName="Sans-Semi", fontSize=10.5, leading=14, textColor=INK, spaceBefore=2, spaceAfter=5),
    "opt": ParagraphStyle("opt", fontName="Serif", fontSize=10.2, leading=13.6, textColor=INK),
    "optl": ParagraphStyle("optl", fontName="Sans-Bold", fontSize=10.2, leading=13.6, textColor=INK),
    "qhead": ParagraphStyle("qhead", fontName="Sans-Bold", fontSize=10.5, leading=13, textColor=INK, spaceAfter=4),
    "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=22, leading=27, textColor=INK, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=13.5, leading=17, textColor=INK, spaceBefore=12, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="Sans-Bold", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4),
    "bullet": ParagraphStyle("bullet", fontName="Serif", fontSize=10.5, leading=15, textColor=INK, leftIndent=16,
                             bulletIndent=4, spaceAfter=3, bulletFontName="Serif"),
    "tip": ParagraphStyle("tip", fontName="Serif", fontSize=10.2, leading=14.5, textColor=INK),
    "figtitle": ParagraphStyle("figtitle", fontName="Sans-Semi", fontSize=9.5, leading=12, textColor=INK, spaceAfter=4),
    "figinfo": ParagraphStyle("figinfo", fontName="Sans", fontSize=8.8, leading=11.5, textColor=INK, spaceBefore=3, spaceAfter=6),
    "fignote": ParagraphStyle("fignote", fontName="Sans-It", fontSize=8, leading=10, textColor=MID, spaceBefore=2, spaceAfter=6),
    "cell": ParagraphStyle("cell", fontName="Sans", fontSize=8.8, leading=11, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Sans-Bold", fontSize=8.8, leading=11, textColor=INK),
    "cellm": ParagraphStyle("cellm", fontName="Mono", fontSize=8.3, leading=11, textColor=INK),
    "sol": ParagraphStyle("sol", fontName="Serif", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=2),
    "solh": ParagraphStyle("solh", fontName="Sans-Bold", fontSize=9.8, leading=13, textColor=INK, spaceBefore=7, spaceAfter=2),
    "solb": ParagraphStyle("solb", fontName="Serif", fontSize=9.6, leading=13.2, textColor=INK, leftIndent=14, bulletIndent=2, spaceAfter=1.5,
                           bulletFontName="Serif"),
    "center": ParagraphStyle("center", fontName="Serif", fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=INK),
    "toc0": ParagraphStyle("toc0", fontName="Sans-Bold", fontSize=11, leading=16, spaceBefore=8),
    "toc1": ParagraphStyle("toc1", fontName="Serif", fontSize=10.2, leading=14, leftIndent=16),
}

SPECIAL = {"→": "→", "≈": "≈"}


def esc(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for ch in SPECIAL:
        t = t.replace(ch, f'<font name="DejaVu">{ch}</font>')
    return t


def md(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", t)
    return t


def P(t, st="body", raw=False):
    return Paragraph(t if raw else esc(t), ST[st])


# ------------------------------------------------------------------ special flowables
class Marker(Flowable):
    """Zero-size marker: sets running header, no-header pages, TOC entries."""

    def __init__(self, section=None, noheader=False, toc=None, toc_level=0, key=None, nofooter=False):
        super().__init__()
        self.section, self.noheader, self.toc, self.toc_level, self.key, self.nofooter = section, noheader, toc, toc_level, key, nofooter
        self.width = self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        doc = self.canv._doctemplate
        if self.section is not None:
            doc.section = self.section
        if self.noheader:
            doc.noheader.add(doc.page)
        if self.nofooter:
            doc.nofooter.add(doc.page)
        if self.key:
            self.canv.bookmarkPage(self.key)


class RectoBreak(Flowable):
    """Start on the next right-hand (odd) page, leaving a truly blank verso if needed."""

    def wrap(self, aw, ah):
        doc = self.canv._doctemplate
        if doc.page % 2 == 0 and ah >= FH - 1:
            doc.blank.add(doc.page)
            return aw, ah  # consume the whole (empty) verso page
        return 0, 0

    def draw(self):
        pass


def recto():
    return [PageBreak(), RectoBreak()]


class Doc(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(str(path), pagesize=(PAGE_W, PAGE_H), leftMargin=M_IN, rightMargin=M_OUT,
                         topMargin=M_TOP, bottomMargin=M_BOT, title=assemble.META["title"],
                         author=assemble.META["author"], subject="EPSO reasoning tests practice workbook", **kw)
        self.section = ""
        self.noheader, self.nofooter, self.blank = set(), set(), set()
        odd = Frame(M_IN, M_BOT, FW, FH, id="odd", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        even = Frame(M_OUT, M_BOT, FW, FH, id="even", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate("odd", [odd], onPageEnd=self.decorate),
                               PageTemplate("even", [even], onPageEnd=self.decorate)])

    def handle_pageBegin(self):
        # recto (odd) pages carry the gutter on the left, verso (even) pages on the right
        self.pageTemplate = self.pageTemplates[0 if (self.page + 1) % 2 == 1 else 1]
        super().handle_pageBegin()

    def beforeDocument(self):
        self.section = ""
        self.noheader, self.nofooter, self.blank = set(), set(), set()

    def decorate(self, canv, doc):
        pg = doc.page
        if pg in doc.blank:
            return
        odd = pg % 2 == 1
        canv.saveState()
        if pg not in doc.noheader:
            canv.setFont("Sans", 7.8)
            canv.setFillColor(MID)
            y = PAGE_H - M_TOP + 22
            if odd:
                canv.drawRightString(PAGE_W - M_OUT, y, (doc.section or "").upper())
            else:
                canv.drawString(M_OUT, y, assemble.META["short_title"].upper())
            canv.setStrokeColor(RULE); canv.setLineWidth(0.4)
            x0 = M_IN if odd else M_OUT
            canv.line(x0, y - 5, x0 + FW, y - 5)
        if pg not in doc.nofooter:
            canv.setFont("Sans-Semi", 9); canv.setFillColor(INK)
            y = M_BOT - 30
            if odd:
                canv.drawRightString(PAGE_W - M_OUT, y, str(pg))
            else:
                canv.drawString(M_OUT, y, str(pg))
        canv.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Marker) and f.toc:
            self.notify("TOCEntry", (f.toc_level, f.toc, self.page, f.key))


# ------------------------------------------------------------------ helpers
def heading_chapter(title, section=None, toc_level=1, key=None, first=False, any_page=False):
    out = [] if first else ([PageBreak()] if any_page else recto())
    shown = esc(title)
    if len(title) > 44 and " and " in title:
        shown = esc(title).replace(" and ", "<br/>and ", 1)
    out += [Marker(section=section or title, toc=title, toc_level=toc_level, key=key, noheader=True), Spacer(1, 30),
            Paragraph(shown, ST["h1"]), HRule(FW, 1.2), Spacer(1, 12)]
    return out


class HRule(Flowable):
    def __init__(self, w, t=0.6, col=INK):
        super().__init__(); self.w, self.t, self.col = w, t, col

    def wrap(self, aw, ah):
        return self.w, self.t + 2

    def draw(self):
        self.canv.setStrokeColor(self.col); self.canv.setLineWidth(self.t); self.canv.line(0, 1, self.w, 1)


def part_divider(num, title, blurb, key):
    return recto() + [Marker(section=title, noheader=True, nofooter=True, toc=f"Part {num} — {title}", toc_level=0, key=key),
                      Spacer(1, 2.6 * inch), P(f"PART {num}", "center"), Spacer(1, 6),
                      Paragraph(esc(title), ParagraphStyle("pt", fontName="Sans-Bold", fontSize=30, leading=36, alignment=TA_CENTER)),
                      Spacer(1, 14), HRuleCentered(1.4 * inch), Spacer(1, 16),
                      Paragraph(esc(blurb), ParagraphStyle("pb", parent=ST["center"], fontName="Serif-It", fontSize=11.5, leading=17,
                                                           leftIndent=0.6 * inch, rightIndent=0.6 * inch))]


class HRuleCentered(Flowable):
    def __init__(self, w):
        super().__init__(); self.w = w

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 4

    def draw(self):
        self.canv.setLineWidth(1.2); self.canv.line((self.aw - self.w) / 2, 2, (self.aw + self.w) / 2, 2)


def tip_box(text):
    t = Table([[Paragraph(md(text), ST["tip"])]], colWidths=[FW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SHADE), ("LINEBEFORE", (0, 0), (0, -1), 3, INK),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return [Spacer(1, 4), t, Spacer(1, 8)]


NUMERIC = re.compile(r"^[€−\-+]?[\d,.]+%?k?$")


def data_table(fig, mono_cols=(), width=None, rownums=False, zebra=True):
    cols = list(fig["columns"])
    rows = [list(r) for r in fig["rows"]]
    if rownums:
        cols = ["Row"] + cols
        rows = [[str(i + 1)] + r for i, r in enumerate(rows)]
    data = [[Paragraph(esc(c), ST["cellb"]) for c in cols]]
    for r in rows:
        line = []
        for j, v in enumerate(r):
            st = ST["cellm"] if j in mono_cols else ST["cell"]
            line.append(Paragraph(esc(str(v)), st))
        data.append(line)
    widths = []
    for j in range(len(cols)):
        w = pdfmetrics.stringWidth(str(cols[j]), "Sans-Bold", 8.8)
        for r in rows:
            fn, fs = ("Mono", 8.3) if j in mono_cols else ("Sans", 8.8)
            w = max(w, pdfmetrics.stringWidth(str(r[j]), fn, fs))
        widths.append(w + 14)
    avail = width or FW
    if sum(widths) > avail:
        widths = [w * avail / sum(widths) for w in widths]
    elif sum(widths) < avail * 0.55:
        widths = [w * (avail * 0.55) / sum(widths) for w in widths]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("BACKGROUND", (0, 0), (-1, 0), SHADE2),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if zebra:
        for i in range(2, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), colors.Color(0.965, 0.965, 0.965)))
    # right-align numeric columns
    for j in range(len(cols)):
        if all(NUMERIC.match(str(r[j]).replace(" ", "")) for r in rows if str(r[j]) not in ("—", "")):
            for i in range(1, len(data)):
                data[i][j].style = ParagraphStyle("r", parent=data[i][j].style, alignment=2)
    t.setStyle(TableStyle(style))
    return t


def options_block(opts, letters="ABCDE"):
    data = [[Paragraph(letters[i], ST["optl"]), Paragraph(esc(o), ST["opt"])] for i, o in enumerate(opts)]
    t = Table(data, colWidths=[20, FW - 20], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    return t


def qhead(label):
    return [P(label, "qhead")]


def item_block(parts):
    return KeepTogether(parts + [Spacer(1, 14)])


# ------------------------------------------------------------------ item renderers
def r_verbal(it, label):
    parts = qhead(label)
    for para in it["passage"].split("\n\n"):
        parts.append(P(para, "passage"))
    parts += [P(it["question"], "stem"), options_block(it["options"])]
    return item_block(parts)


def figure_block(fig):
    out = []
    if fig["type"] == "tables":
        for f in fig["tables"]:
            out += [P(f["title"], "figtitle"), data_table(f), Spacer(1, 8)]
        out.append(P("All data are fictitious.", "fignote"))
        return out
    out.append(P(fig["title"], "figtitle"))
    if fig["type"] == "table":
        out.append(data_table(fig))
        if fig.get("note"):
            out.append(P(fig["note"], "figinfo"))
    else:
        out.append(chart(fig, width=min(FW, 440)))
        if fig["type"] == "line":
            cols = ["Series"] + fig["categories"]
            rows = [[s["name"]] + [f"{v:.1f}" for v in s["values"]] for s in fig["series"]]
            out += [Spacer(1, 4), data_table({"columns": cols, "rows": rows})]
    out.append(P("All data are fictitious.", "fignote"))
    return out


def r_numerical(it, label):
    parts = qhead(label) + figure_block(it["figure"]) + [P(it["question"], "stem"), options_block(it["options"])]
    return item_block(parts)


FR = 66


def r_abstract(it, label):
    parts = qhead(label) + [P("Which figure comes next in the series?", "stem"),
                            abstract_row(it["series"], size=FR, question_mark=True, gap=10), Spacer(1, 10),
                            P("Answer options", "figtitle"),
                            abstract_row(it["options"], size=FR, labels=list("ABCDE"), gap=10)]
    return item_block(parts)


def r_sjt(it, label):
    parts = qhead(label) + [P(it["scenario"], "passage"), P("Which action is the MOST effective, and which is the LEAST effective?", "stem"),
                            options_block(it["options"]), Spacer(1, 4),
                            P("Most effective: ______        Least effective: ______", "small")]
    return item_block(parts)


def ref_table(rows):
    fig = {"columns": ["Reference", "Beneficiary", "Country", "Amount (€)"],
           "rows": [[r["ref"], r["name"], r["cc"], r["amount"]] for r in rows]}
    return data_table(fig, mono_cols=(1, 4), rownums=True)


def r_accuracy(it, label):
    parts = qhead(label) + [P("Reference table", "figtitle"), ref_table(it["reference"]), Spacer(1, 8)]
    if it["kind"] == "field":
        rec = it["record"]
        parts += [P(f"Copied record (from row {it['row']})", "figtitle"),
                  data_table({"columns": ["Reference", "Beneficiary", "Country", "Amount (€)"],
                              "rows": [[rec["ref"], rec["name"], rec["cc"], rec["amount"]]]}, mono_cols=(0, 3), zebra=False),
                  Spacer(1, 6), P(it["question"], "stem"), options_block(it["options"])]
    elif it["kind"] == "match":
        parts += [P(it["question"], "stem"),
                  data_table({"columns": ["Option", "Reference", "Beneficiary", "Country", "Amount (€)"],
                              "rows": [[L, c["ref"], c["name"], c["cc"], c["amount"]] for L, c in zip("ABCD", it["candidates"])]},
                             mono_cols=(1, 4), zebra=False)]
    else:
        parts += [P("Copied records", "figtitle"),
                  data_table({"columns": ["Copy", "Source row", "Reference", "Beneficiary", "Country", "Amount (€)"],
                              "rows": [[str(i + 1), str(rw), c["ref"], c["name"], c["cc"], c["amount"]] for i, (rw, c) in enumerate(it["copies"])]},
                             mono_cols=(2, 5), zebra=False),
                  Spacer(1, 6), P(it["question"], "stem"), options_block(it["options"])]
    return item_block(parts)


def r_prioritising(it, label):
    parts = qhead(label)
    if it["kind"] == "meeting":
        g = it["grid"]
        rows = g["rows"][:3] + [["12:00–14:00", "lunch break", "", "", "", ""]] + g["rows"][3:]
        t = data_table({"columns": g["columns"], "rows": rows}, zebra=False)
        t.setStyle(TableStyle([("SPAN", (1, 4), (-1, 4)), ("BACKGROUND", (0, 4), (-1, 4), SHADE)]))
        parts += [P("Who is busy, by day and start time", "figtitle"), t, P(g["note"] + " Key: " + g["legend"] + ".", "figinfo")]
    elif it["kind"] == "critical":
        parts += [P("Project tasks", "figtitle"), data_table(it["table"]), Spacer(1, 6)]
    else:
        parts += [P(it["question"], "stem"), P("Constraints", "figtitle")]
        parts += [Paragraph(esc(c), ST["bullet"], bulletText="•") for c in it["constraints"]]
        parts += [Spacer(1, 4), options_block(it["options"])]
        return item_block(parts)
    parts += [P(it["question"], "stem"), options_block(it["options"])]
    return item_block(parts)


RENDER = {"verbal": r_verbal, "numerical": r_numerical, "abstract": r_abstract, "sjt": r_sjt,
          "accuracy": r_accuracy, "prioritising": r_prioritising}


# ------------------------------------------------------------------ solutions
def sol_head(it):
    if "most" in it:
        return f"Question {it['n']} — Most effective: {it['most']} · Least effective: {it['least']}"
    return f"Question {it['n']} — Answer: {it['answer']}"


def sol_verbal(it):
    out = []
    for L in "ABCD":
        out.append(Paragraph(f"<b>{L}.</b> " + esc(it["explanations"][L]), ST["solb"]))
    return out


def sol_numerical(it):
    i = "ABCD".index(it["answer"])
    out = [Paragraph(esc(s), ST["solb"], bulletText="›") for s in it["steps"]]
    out.append(Paragraph(f"<b>Correct option: {it['answer']}</b> ({esc(it['options'][i])})", ST["sol"]))
    return out


def sol_abstract(it):
    out = [Paragraph("<b>Rule" + ("s" if len(it["rules"]) > 1 else "") + ":</b> " + esc("; ".join(it["rules"])) + ".", ST["sol"])]
    wrong = "; ".join(f"<b>{L}</b> — {esc(w)}" for L, w in sorted(it["why_wrong"].items()))
    out.append(Paragraph("<b>Why the other options are wrong:</b> " + wrong + ".", ST["sol"]))
    return out


def sol_sjt(it):
    out = [Paragraph(f"<b>Ranking: {esc(it['ranking'])}</b> <i>({esc(it['competency'])})</i>", ST["sol"])]
    for L in "ABCD":
        out.append(Paragraph(f"<b>{L}.</b> " + esc(it["explanations"][L]), ST["solb"]))
    return out


def sol_text(it):
    return [Paragraph(esc(it["explanation"]), ST["sol"])]


SOL = {"verbal": sol_verbal, "numerical": sol_numerical, "abstract": sol_abstract, "sjt": sol_sjt,
       "accuracy": sol_text, "prioritising": sol_text}


def answer_key_table(items, key="answer", label_fn=None):
    cells = []
    for it in items:
        if "most" in it:
            cells.append(f"<b>{it['n']}</b>  {it['most']} / {it['least']}")
        else:
            cells.append(f"<b>{label_fn(it) if label_fn else it['n']}</b>  {it[key]}")
    ncol = 6 if any("most" in it for it in items) else 8
    rows = [cells[i:i + ncol] for i in range(0, len(cells), ncol)]
    rows[-1] += [""] * (ncol - len(rows[-1]))
    data = [[Paragraph(c, ST["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=[FW / ncol] * ncol, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
    return t


# ------------------------------------------------------------------ front & back matter
def title_page(meta):
    big = ParagraphStyle("tt", fontName="Sans-Bold", fontSize=30, leading=36, alignment=TA_CENTER, textColor=INK)
    sub = ParagraphStyle("ts", fontName="Serif-It", fontSize=13, leading=19, alignment=TA_CENTER, textColor=INK)
    t = esc(meta["title"]).replace(" for EPSO", "<br/>for EPSO")
    return [Marker(noheader=True, nofooter=True), Spacer(1, 1.9 * inch), Paragraph(t, big), Spacer(1, 18),
            HRuleCentered(1.6 * inch), Spacer(1, 18), Paragraph(esc(meta["subtitle"]), sub), Spacer(1, 2.6 * inch),
            Paragraph(esc(meta["author"]).upper(), ParagraphStyle("ta", fontName="Sans-Semi", fontSize=11, leading=14, alignment=TA_CENTER))]


def copyright_page(meta, total):
    s = ParagraphStyle("cp", fontName="Serif", fontSize=8.8, leading=12.5, textColor=INK, spaceAfter=7)
    lines = [
        f"<b>{esc(meta['title'])}</b><br/>{esc(meta['subtitle'])}",
        f"Copyright © {meta['year']} {esc(meta['author'])}. All rights reserved. No part of this publication may be reproduced, "
        "stored or transmitted in any form or by any means without the prior written permission of the publisher, except for "
        "brief quotations in reviews.",
        "<b>Independent publication.</b> This book is not affiliated with, authorised, sponsored or endorsed by the European "
        "Personnel Selection Office (EPSO), the European Union or any EU institution, body or agency. “EPSO” is used solely to "
        "describe the selection tests that this book helps readers to prepare for.",
        f"<b>Original content.</b> All {total} questions in this book are original and were written for it. None is reproduced from "
        "EPSO or from any other publisher. All names, organisations, data and scenarios in the questions are fictitious or "
        "used illustratively; any resemblance to real persons or data is coincidental.",
        "<b>Disclaimer.</b> Test formats, question numbers, time limits and pass marks vary between selection procedures and may "
        "change. Always check the Notice of Competition and the official candidate information for your procedure. The author "
        "and publisher accept no liability for decisions taken on the basis of this book, and no particular result is guaranteed.",
    ]
    if meta.get("isbn_paperback"):
        lines.append(f"ISBN (paperback): {meta['isbn_paperback']}")
    if meta.get("isbn_hardcover"):
        lines.append(f"ISBN (hardcover): {meta['isbn_hardcover']}")
    lines.append(f"Published by {esc(meta['imprint'])}. Typeset in Source Serif 4 and Source Sans 3.")
    return [Marker(noheader=True, nofooter=True), Spacer(1, 4.2 * inch)] + [Paragraph(x, s) for x in lines]


def guide_story(text, first_section_is_front=True):
    """Convert guide markdown to flowables; returns list of (title, flowables)."""
    sections = []
    cur = None
    for line in text.splitlines():
        if line.startswith("# "):
            cur = [line[2:].strip(), []]; sections.append(cur); continue
        if cur is None:
            continue
        fl = cur[1]
        s = line.rstrip()
        if not s:
            continue
        if s.startswith("## "):
            fl.append(CondPageBreak(1.3 * inch)); fl.append(P(s[3:], "h2"))
        elif s.startswith("> "):
            fl += tip_box(s[2:])
        elif s.startswith("- "):
            fl.append(Paragraph(md(s[2:]), ST["bullet"], bulletText="•"))
        elif re.match(r"^\d+\. ", s):
            num, rest = s.split(". ", 1)
            fl.append(Paragraph(md(rest), ST["bullet"], bulletText=f"{num}."))
        else:
            fl.append(Paragraph(md(s), ST["body"]))
    return sections


SET_INTRO = {
    "verbal": ("Read each passage and choose the ONE statement that is supported by the passage alone. Do not use outside knowledge. "
               "Suggested pace: about 1 minute 45 seconds per question once you move on to timed practice."),
    "numerical": ("Use the data provided to answer each question. A basic calculator is allowed. All data are fictitious. "
                  "Suggested pace: about 2 minutes per question."),
    "abstract": ("Each series of five figures follows one or more rules. Choose the figure (A–E) that comes next. "
                 "Suggested pace: about 1 minute per question."),
    "sjt": ("For each scenario, choose the MOST effective and the LEAST effective action. Answer as an effective EU staff member would. "
            "Suggested pace: about 2 minutes per scenario."),
    "accuracy": ("Compare the records with the reference table carefully. Every character counts, including accents and punctuation. "
                 "Suggested pace: about 1 minute 30 seconds per question."),
    "prioritising": ("Use the information given to plan, schedule or allocate work. Read every condition before choosing. "
                     "Suggested pace: about 2 minutes 30 seconds per question."),
}
DIFF_HEAD = {"foundation": "Foundation", "intermediate": "Intermediate", "advanced": "Advanced"}


def answer_sheet(mock_title):
    d = Drawing(FW, 520)
    d.add(String(0, 505, f"{mock_title} — answer sheet", fontName="Sans-Bold", fontSize=13))
    d.add(String(0, 488, "Name: ______________________   Date: ____________   Time taken: ________   Score: ____ / 40",
                 fontName="Sans", fontSize=9))
    for q in range(40):
        col, row = divmod(q, 20)
        x = col * (FW / 2) + 10
        y = 455 - row * 22
        d.add(String(x, y - 3, f"{q + 1:>2}", fontName="Sans-Bold", fontSize=9))
        letters = "ABCDE" if q >= 30 else "ABCD"
        for k, L in enumerate(letters):
            cx = x + 34 + k * 24
            d.add(Circle(cx, y, 7.5, strokeColor=INK, strokeWidth=0.7, fillColor=None))
            d.add(String(cx, y - 3, L, fontName="Sans", fontSize=7.5, textAnchor="middle", fillColor=MID))
    d.add(String(0, 0, "Questions 1–20: verbal · 21–30: numerical · 31–40: abstract", fontName="Sans-It", fontSize=8.5, fillColor=MID))
    return d


def lined_table(cols, widths, nrows, h=26):
    data = [[Paragraph(esc(c), ST["cellb"]) for c in cols]] + [[""] * len(cols) for _ in range(nrows)]
    t = Table(data, colWidths=widths, rowHeights=[18] + [h] * nrows, hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("BACKGROUND", (0, 0), (-1, 0), SHADE2)]))
    return t


# ------------------------------------------------------------------ main story
def build(path=OUT / "interior.pdf"):
    book = assemble.load()
    meta = book["meta"]
    guide = guide_story(book["guide"])
    story = []
    story += title_page(meta)
    story += [PageBreak()] + copyright_page(meta, book["total"])
    toc = TableOfContents(levelStyles=[ST["toc0"], ST["toc1"]], dotsMinLevel=0)
    story += recto() + [Marker(section="Contents", noheader=True), P("Contents", "h1"), HRule(FW, 1.2), Spacer(1, 10), toc]
    # How to use (front matter)
    howto = guide[0]
    story += heading_chapter(howto[0], key="howto", toc_level=0) + howto[1]

    # Part I
    story += part_divider("I", "Understanding the Tests",
                          "What each test measures, how the questions are built, and proven methods for answering them quickly and accurately.", "part1")
    for i, (title, fl) in enumerate(guide[1:]):
        story += heading_chapter(title, section=title, any_page=i > 0) + fl

    # Part II
    story += part_divider("II", "Practice Sets",
                          f"{sum(len(s['items']) for s in book['sets'])} questions across six test types, graded from foundation to advanced. "
                          "Mark each block straight away and study every solution in Part IV.", "part2")
    for s in book["sets"]:
        story += heading_chapter(f"Practice Set — {s['title']}", section=s["title"], key=f"set_{s['key']}")
        story += [P(SET_INTRO[s["type"]], "body"),
                  P(f"{len(s['items'])} questions · answers and worked solutions in Part IV.", "fignote"), Spacer(1, 6)]
        last = None
        for it in s["items"]:
            d = it.get("difficulty")
            if s["type"] in ("verbal", "numerical", "abstract") and d != last:
                story += [CondPageBreak(2.5 * inch), P(DIFF_HEAD[d], "h2"), HRule(FW, 0.5, RULE), Spacer(1, 8)]
                last = d
            story.append(RENDER[s["type"]](it, f"Question {it['n']}"))

    # Part III
    story += part_divider("III", "Mock Exams",
                          "Three timed mock exams combining verbal, numerical and abstract reasoning. Sit each one in a single session.", "part3")
    for mk in book["mocks"]:
        story += heading_chapter(mk["title"], section=mk["title"], key=mk["key"])
        story += [P("<b>40 questions · suggested time: 65 minutes</b>", "body", raw=True),
                  Paragraph("• Questions 1–20: verbal reasoning (about 35 minutes)<br/>• Questions 21–30: numerical reasoning (about 20 minutes)"
                            "<br/>• Questions 31–40: abstract reasoning (about 10 minutes)", ST["body"]),
                  P("These timings reflect typical past EPSO formats; check the Notice of Competition for your procedure. Use the answer "
                    "sheet at the back of the book, work without interruptions, and answer every question: in typical formats there is no "
                    "penalty for a wrong answer.", "body")]
        story += tip_box("**Score guide (out of 40).** 34–40: excellent, test-ready. 28–33: strong; polish weaker areas. 22–27: developing; "
                         "revisit the method chapters and redo your errors. Below 22: build accuracy first with the practice sets. "
                         "Real pass marks differ between procedures, so treat these bands as a guide only.")
        story.append(PageBreak())
        cur = None
        for it in mk["items"]:
            if it["type"] != cur:
                cur = it["type"]
                name = {"verbal": "Verbal reasoning (questions 1–20)", "numerical": "Numerical reasoning (questions 21–30)",
                        "abstract": "Abstract reasoning (questions 31–40)"}[cur]
                if cur != "verbal":
                    story.append(PageBreak())
                story += [P(name, "h2"), HRule(FW, 0.5, RULE), Spacer(1, 8)]
            story.append(RENDER[it["type"]](it, f"Question {it['n']}"))

    # Part IV
    story += part_divider("IV", "Answers and Worked Solutions",
                          "A quick answer key for every set, followed by a full explanation of every question.", "part4")
    for s in book["sets"]:
        story += heading_chapter(f"Solutions — {s['title']}", section=f"Solutions — {s['title']}", key=f"sol_{s['key']}")
        story += [P("Answer key", "h3"), answer_key_table(s["items"]), Spacer(1, 10), P("Worked solutions", "h3")]
        for it in s["items"]:
            body = [P(sol_head(it), "solh")] + SOL[s["type"]](it)
            story.append(KeepTogether(body))
    for mk in book["mocks"]:
        story += heading_chapter(f"Solutions — {mk['title']}", section=f"Solutions — {mk['title']}", key=f"sol_{mk['key']}")
        story += [P("Answer key", "h3"), answer_key_table(mk["items"]), Spacer(1, 10), P("Worked solutions", "h3")]
        for it in mk["items"]:
            body = [P(sol_head(it), "solh")] + SOL[it["type"]](it)
            story.append(KeepTogether(body))

    # Back matter
    story += heading_chapter("Score Tracker", toc_level=0, key="tracker")
    rows = [[s["title"], str(len(s["items"]))] for s in book["sets"]] + [[m["title"], "40"] for m in book["mocks"]]
    data = [[Paragraph(esc(c), ST["cellb"]) for c in ["Set", "Questions", "Attempt 1 score", "Date", "Attempt 2 score", "Date"]]]
    data += [[Paragraph(esc(r[0]), ST["cell"]), Paragraph(r[1], ST["cell"]), "", "", "", ""] for r in rows]
    t = Table(data, colWidths=[FW * 0.3, FW * 0.12, FW * 0.17, FW * 0.12, FW * 0.17, FW * 0.12], rowHeights=[20] + [30] * len(rows))
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("BACKGROUND", (0, 0), (-1, 0), SHADE2), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story += [P("Record every attempt. Seeing your scores rise is one of the best motivators there is.", "body"), Spacer(1, 6), t]

    story += heading_chapter("Error Log", toc_level=0, key="errorlog")
    story += [P("For every question you get wrong, write one line. Re-read this log before each mock exam and on the day before your test.", "body"),
              Spacer(1, 6), lined_table(["Set / Q", "What I did", "What I should have done", "Rule to remember"],
                                        [FW * 0.13, FW * 0.29, FW * 0.29, FW * 0.29], 19)]
    story += [PageBreak(), lined_table(["Set / Q", "What I did", "What I should have done", "Rule to remember"],
                                       [FW * 0.13, FW * 0.29, FW * 0.29, FW * 0.29], 25)]

    story += heading_chapter("Answer Sheets", toc_level=0, key="sheets")
    story += [P("Photocopy or tear out these sheets for the mock exams.", "body")]
    for i, mk in enumerate(book["mocks"]):
        if i:
            story += recto()
        story += [Spacer(1, 8), answer_sheet(mk["title"])]

    story += heading_chapter("A Final Word", toc_level=0, key="final")
    story += [P("Reasoning tests reward method, calm and practice, and all three can be learned. If you have worked through this book, "
                "reviewed your errors and sat the mock exams under timed conditions, you have done exactly what high scorers do.", "body"),
              P("Good luck with your selection procedure, and with the career in European public service that it can open up.", "body"),
              Spacer(1, 10),
              P("If this workbook has helped you, a short review on the store where you bought it helps other candidates to find it. Thank you.", "body")]

    from reportlab.pdfgen.canvas import Canvas

    def mk(*a, **k):
        k.setdefault("initialFontName", "Sans")
        return Canvas(*a, **k)
    doc = Doc(path)
    doc.multiBuild(story, maxPasses=6, canvasmaker=mk)
    return path, doc.page


if __name__ == "__main__":
    p, n = build()
    print("built", p, "pages:", n)
