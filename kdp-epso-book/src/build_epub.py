"""Build the Kindle eBook as a reflowable EPUB 3 (KDP converts it). Figures are small palette PNGs."""
import fontsetup  # noqa: F401,E402  (must precede other reportlab imports)
import html
import io
import re
import sys
import uuid
import zipfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import assemble  # noqa: E402
from figures import abstract_row, chart  # noqa: E402
from reportlab.graphics import renderPM  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build"
IMAGES = {}


def png_of(drawing, name, dpi=150, colors=8):
    buf = io.BytesIO()
    renderPM.drawToFile(drawing, buf, fmt="PNG", dpi=dpi, bg=0xFFFFFF)
    im = Image.open(io.BytesIO(buf.getvalue())).convert("L")
    im = im.quantize(colors=colors)
    out = io.BytesIO(); im.save(out, "PNG", optimize=True)
    IMAGES[f"images/{name}.png"] = out.getvalue()
    return f"../images/{name}.png"


def e(t):
    return html.escape(t, quote=False)


def md_inline(t):
    t = e(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", t)
    return t


def xhtml(title, body):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head><meta charset="utf-8"/><title>{e(title)}</title><link rel="stylesheet" type="text/css" href="../style.css"/></head>
<body>
{body}
</body></html>"""


CSS = """
body { font-family: serif; line-height: 1.45; margin: 0 2%; }
h1 { font-family: sans-serif; font-size: 1.6em; margin: 0.6em 0 0.4em; page-break-before: always; }
h2 { font-family: sans-serif; font-size: 1.2em; margin: 1.2em 0 0.4em; }
h3 { font-family: sans-serif; font-size: 1.05em; margin: 1em 0 0.3em; }
p { margin: 0 0 0.6em; text-indent: 0; }
.q { margin: 1.4em 0 0.4em; font-family: sans-serif; font-weight: bold; border-top: 1px solid #999; padding-top: 0.5em; }
.stem { font-family: sans-serif; font-weight: bold; margin: 0.6em 0 0.4em; }
ol.opts { list-style-type: upper-alpha; margin: 0.2em 0 0.8em 1.6em; padding: 0; }
ol.opts li { margin: 0.15em 0; }
table { border-collapse: collapse; margin: 0.4em 0 0.6em; font-family: sans-serif; font-size: 0.85em; }
th, td { border: 1px solid #888; padding: 0.15em 0.4em; }
th { background: #e6e6e6; }
td.n { text-align: right; }
.keynote { font-size: 1em; font-style: normal; color: inherit; margin: 0.3em 0 0.6em; }
.note { font-size: 0.8em; font-style: italic; color: #555; }
.tip { background: #eee; border-left: 4px solid #222; padding: 0.5em 0.7em; margin: 0.8em 0; }
.fig { text-align: center; margin: 0.4em 0; }
.fig img { width: 100%; max-width: 100%; }
.key { font-family: sans-serif; }
.back { font-size: 0.85em; font-family: sans-serif; }
.center { text-align: center; }
.title { font-family: sans-serif; font-size: 2em; text-align: center; margin-top: 2em; }
.subtitle { font-style: italic; text-align: center; }
.small { font-size: 0.85em; }
"""

NUM = re.compile(r"^[€−\-+]?[\d,.]+%?k?$")


def table_html(fig, rownums=False):
    cols = list(fig["columns"]); rows = [list(r) for r in fig["rows"]]
    if rownums:
        cols = ["Row"] + cols; rows = [[str(i + 1)] + r for i, r in enumerate(rows)]
    h = "<table><tr>" + "".join(f"<th>{e(str(c))}</th>" for c in cols) + "</tr>"
    for r in rows:
        h += "<tr>" + "".join(f'<td class="{"n" if NUM.match(str(v).replace(" ", "")) else ""}">{e(str(v))}</td>' for v in r) + "</tr>"
    return h + "</table>"


def opts_html(opts):
    return '<ol class="opts">' + "".join(f"<li>{e(o)}</li>" for o in opts) + "</ol>"


def figure_html(fig, name):
    out = ""
    if fig["type"] == "tables":
        for f in fig["tables"]:
            out += f'<p class="stem">{e(f["title"])}</p>' + table_html(f)
    elif fig["type"] == "table":
        out += f'<p class="stem">{e(fig["title"])}</p>' + table_html(fig)
        if fig.get("note"):
            out += f'<p class="keynote">{e(fig["note"])}</p>'
    else:
        out += f'<p class="stem">{e(fig["title"])}</p>'
        src = png_of(chart(fig, width=430), name, dpi=170, colors=12)
        out += f'<div class="fig"><img src="{src}" alt="{e(fig["title"])}"/></div>'
        if fig["type"] in ("line", "bar"):
            cols = ["Series"] + fig["categories"]
            rows = [[s["name"]] + [(f"{v:.1f}" if fig["type"] == "line" else str(v)) for v in s["values"]] for s in fig["series"]]
            out += table_html({"columns": cols, "rows": rows})
        if fig["type"] == "pie":
            out += table_html({"columns": ["Item", "Share"], "rows": [[l, f"{v}%"] for l, v in zip(fig["labels"], fig["values"])]})
    return out + '<p class="note">All data are fictitious.</p>'


def q_html(it, anchor, sol_href, label):
    t = it["type"]
    h = f'<p class="q" id="{anchor}">{e(label)}</p>'
    if t == "verbal":
        h += "".join(f"<p>{e(p)}</p>" for p in it["passage"].split("\n\n"))
        h += f'<p class="stem">{e(it["question"])}</p>' + opts_html(it["options"])
    elif t == "numerical":
        h += figure_html(it["figure"], anchor) + f'<p class="stem">{e(it["question"])}</p>' + opts_html(it["options"])
    elif t == "abstract":
        s1 = png_of(abstract_row(it["series"], size=60, question_mark=True), anchor + "_s", dpi=230, colors=4)
        s2 = png_of(abstract_row(it["options"], size=60, labels=list("ABCDE")), anchor + "_o", dpi=230, colors=4)
        h += ('<p class="stem">Which figure comes next in the series?</p>'
              f'<div class="fig"><img src="{s1}" alt="Series of five figures"/></div><p class="stem">Answer options</p>'
              f'<div class="fig"><img src="{s2}" alt="Answer options A to E"/></div>')
    elif t == "sjt":
        h += f'<p>{e(it["scenario"])}</p><p class="stem">Which action is the MOST effective, and which is the LEAST effective?</p>' + opts_html(it["options"])
    elif t == "accuracy":
        ref = {"columns": ["Reference", "Beneficiary", "Country", "Amount (€)"],
               "rows": [[r["ref"], r["name"], r["cc"], r["amount"]] for r in it["reference"]]}
        h += '<p class="stem">Reference table</p>' + table_html(ref, rownums=True)
        if it["kind"] == "field":
            r = it["record"]
            h += f'<p class="stem">Copied record (from row {it["row"]})</p>' + table_html(
                {"columns": ref["columns"], "rows": [[r["ref"], r["name"], r["cc"], r["amount"]]]})
            h += f'<p class="stem">{e(it["question"])}</p>' + opts_html(it["options"])
        elif it["kind"] == "match":
            h += f'<p class="stem">{e(it["question"])}</p>' + table_html(
                {"columns": ["Option"] + ref["columns"], "rows": [[L, c["ref"], c["name"], c["cc"], c["amount"]] for L, c in zip("ABCD", it["candidates"])]})
        else:
            h += '<p class="stem">Copied records</p>' + table_html(
                {"columns": ["Copy", "Source row"] + ref["columns"],
                 "rows": [[str(i + 1), str(rw), c["ref"], c["name"], c["cc"], c["amount"]] for i, (rw, c) in enumerate(it["copies"])]})
            h += f'<p class="stem">{e(it["question"])}</p>' + opts_html(it["options"])
    elif t == "prioritising":
        if it["kind"] == "meeting":
            g = it["grid"]
            h += '<p class="stem">Who is busy, by day and start time</p>' + table_html({"columns": g["columns"], "rows": g["rows"]})
            h += f'<p class="keynote">{e(g["note"])} Key: {e(g["legend"])}.</p>'
        elif it["kind"] == "critical":
            h += '<p class="stem">Project tasks</p>' + table_html(it["table"])
        else:
            h += f'<p class="stem">{e(it["question"])}</p><p class="stem">Constraints</p><ul>' + "".join(f"<li>{e(c)}</li>" for c in it["constraints"]) + "</ul>"
            h += opts_html(it["options"]) + f'<p class="small"><a href="{sol_href}">Go to the solution</a></p>'
            return h
        h += f'<p class="stem">{e(it["question"])}</p>' + opts_html(it["options"])
    h += f'<p class="small"><a href="{sol_href}">Go to the solution</a></p>'
    return h


def sol_html(it, anchor, q_href, label):
    t = it["type"]
    if t == "sjt":
        head = f'Most effective: {it["most"]} · Least effective: {it["least"]}'
    else:
        head = f'Answer: {it["answer"]}'
    h = f'<p class="q" id="{anchor}">{e(label)} — {e(head)}</p>'
    if t == "verbal":
        h += "".join(f"<p><b>{L}.</b> {e(it['explanations'][L])}</p>" for L in "ABCD")
    elif t == "numerical":
        h += "<ul>" + "".join(f"<li>{e(s)}</li>" for s in it["steps"]) + "</ul>"
    elif t == "abstract":
        h += f"<p><b>Rules:</b> {e('; '.join(it['rules']))}.</p>"
        h += "<p><b>Why the other options are wrong:</b> " + "; ".join(f"<b>{L}</b> – {e(w)}" for L, w in sorted(it["why_wrong"].items())) + ".</p>"
    elif t == "sjt":
        h += f"<p><i>{e(it['competency'])}</i> · Ranking: {e(it['ranking'])}</p>"
        h += "".join(f"<p><b>{L}.</b> {e(it['explanations'][L])}</p>" for L in "ABCD")
    else:
        h += f"<p>{e(it['explanation'])}</p>"
    return h + f'<p class="small"><a href="{q_href}">Back to the question</a></p>'


ABS_EXAMPLE = {
    "series": [[{"kind": "arrow", "rot": r}, {"kind": "orbit", "shape": "circle", "pos": p, "fill": "black"}]
               for r, p in ((0, 2), (2, 1), (4, 0), (6, 7), (0, 6))],
    "options": [[{"kind": "arrow", "rot": r}, {"kind": "orbit", "shape": "circle", "pos": p, "fill": "black"}]
                for r, p in ((2, 6), (4, 5), (2, 5), (6, 5), (2, 4))],
}


def guide_html(text):
    chapters = []
    cur = None
    in_list = None
    table = []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            table.append([c.strip() for c in line.strip().strip("|").split("|")])
            continue
        if table and cur is not None:
            h = "<table><tr>" + "".join(f"<th>{md_inline(c)}</th>" for c in table[0]) + "</tr>"
            h += "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>" for r in table[1:])
            cur[1] += h + "</table>"; table = []
        if line.strip() == "[[abstract-example]]" and cur is not None:
            s1 = png_of(abstract_row(ABS_EXAMPLE["series"], size=60, question_mark=True), "guide_abs_s", dpi=230, colors=4)
            s2 = png_of(abstract_row(ABS_EXAMPLE["options"], size=60, labels=list("ABCDE")), "guide_abs_o", dpi=230, colors=4)
            cur[1] += (f'<div class="fig"><img src="{s1}" alt="Worked example series"/></div><p class="stem">Answer options</p>'
                       f'<div class="fig"><img src="{s2}" alt="Worked example options A to E"/></div>')
            continue
        if line.startswith("# "):
            cur = [line[2:].strip(), ""]; chapters.append(cur); in_list = None; continue
        if cur is None:
            continue
        s = line.rstrip()
        if not s:
            if in_list:
                cur[1] += f"</{in_list}>"; in_list = None
            continue
        if s.startswith("- ") or re.match(r"^\d+\. ", s):
            tag = "ul" if s.startswith("- ") else "ol"
            if in_list != tag:
                if in_list:
                    cur[1] += f"</{in_list}>"
                cur[1] += f"<{tag}>"; in_list = tag
            cur[1] += "<li>" + md_inline(s[2:] if tag == "ul" else s.split(". ", 1)[1]) + "</li>"
            continue
        if in_list:
            cur[1] += f"</{in_list}>"; in_list = None
        if s.startswith("## "):
            cur[1] += f"<h2>{md_inline(s[3:])}</h2>"
        elif s.startswith("> "):
            cur[1] += f'<div class="tip"><p>{md_inline(s[2:])}</p></div>'
        else:
            cur[1] += f"<p>{md_inline(s)}</p>"
    for c in chapters:
        if in_list:
            pass
    return chapters


def build(path=OUT / "kindle.epub"):
    book = assemble.load()
    meta = book["meta"]
    docs = []  # (filename, title, xhtml, toc_level)

    title_body = (f'<p class="title">{e(meta["title"])}</p><p class="subtitle">{e(meta["subtitle"])}</p>'
                  f'<p class="center"><b>{e(meta["author"])}</b></p>')
    docs.append(("title.xhtml", "Title Page", xhtml("Title", title_body), None))
    cp = (f"<p class='small'><b>{e(meta['title'])}</b></p><p class='small'>Copyright © {meta['year']} {e(meta['author'])}. All rights reserved.</p>"
          "<p class='small'><b>Independent publication.</b> This book is not affiliated with, authorised, sponsored or endorsed by the European "
          "Personnel Selection Office (EPSO), the European Union or any EU institution, body or agency. “EPSO” is used solely to describe "
          "the selection tests that this book helps readers to prepare for.</p>"
          f"<p class='small'><b>Original content.</b> All {book['total']} questions are original and were written for this book. "
          "All names, organisations, data and scenarios in the questions are fictitious or used illustratively.</p>"
          "<p class='small'><b>Disclaimer.</b> Test formats, question numbers, time limits and pass marks vary between procedures and may change. "
          "Always check the Notice of Competition for your procedure.</p>"
          "<p class='small'><b>Using this eBook.</b> Write your answers on paper as you go. Every question links to its solution, and every "
          "solution links back to its question. Figures are best viewed in landscape orientation on smaller screens.</p>")
    docs.append(("copyright.xhtml", "Copyright", xhtml("Copyright", cp), None))

    chapters = guide_html(book["guide"])
    for i, (t, body) in enumerate(chapters):
        docs.append((f"guide{i}.xhtml", t, xhtml(t, f"<h1>{e(t)}</h1>{body}"), 0 if i == 0 else 1))

    def sid(prefix, it):
        return f"{prefix}-{it['n']}"
    for s in book["sets"]:
        fn, sfn = f"set_{s['key']}.xhtml", f"sol_{s['key']}.xhtml"
        body = f"<h1>Practice Set — {e(s['title'])}</h1>"
        last = None
        for it in s["items"]:
            d = it.get("difficulty")
            if s["type"] in ("verbal", "numerical", "abstract") and d != last:
                body += f"<h2>{d.capitalize()}</h2>"; last = d
            body += q_html(it, sid("q" + s["key"], it), f"{sfn}#{sid('s' + s['key'], it)}", f"Question {it['n']}")
        docs.append((fn, f"Practice Set — {s['title']}", xhtml(s["title"], body), 1))
    for mk in book["mocks"]:
        fn, sfn = f"{mk['key']}.xhtml", f"sol_{mk['key']}.xhtml"
        body = (f"<h1>{e(mk['title'])}</h1><p><b>40 questions · suggested time: 65 minutes</b> (verbal 1–20 about 35 minutes; "
                "numerical 21–30 about 20 minutes; abstract 31–40 about 10 minutes). Note your answers on paper and answer every question.</p>"
                "<div class='tip'><p><b>Score guide (out of 40).</b> 34–40 excellent; 28–33 strong; 22–27 developing; below 22: build accuracy "
                "with the practice sets first. Real pass marks differ between procedures.</p></div>")
        for it in mk["items"]:
            body += q_html(it, f"q{mk['key']}-{it['n']}", f"{sfn}#s{mk['key']}-{it['n']}", f"Question {it['n']}")
        docs.append((fn, mk["title"], xhtml(mk["title"], body), 1))
    for s in book["sets"]:
        fn = f"sol_{s['key']}.xhtml"
        body = f"<h1>Solutions — {e(s['title'])}</h1>"
        for it in s["items"]:
            body += sol_html(it, sid("s" + s["key"], it), f"set_{s['key']}.xhtml#{sid('q' + s['key'], it)}", f"Question {it['n']}")
        docs.append((fn, f"Solutions — {s['title']}", xhtml("Solutions", body), 1))
    from build_pdf import verbal_traps, ABS_SKILL
    for mk in book["mocks"]:
        fn = f"sol_{mk['key']}.xhtml"
        body = f"<h1>Solutions — {e(mk['title'])}</h1>"
        rows = []
        for it in mk["items"]:
            if it["type"] == "verbal":
                rows.append([str(it["n"]), "Verbal: " + ", ".join(verbal_traps(it)), "Chapter 2"])
            elif it["type"] == "numerical":
                rows.append([str(it["n"]), "Numerical: " + it["skill"], "Chapter 3"])
            else:
                rows.append([str(it["n"]), "Abstract: " + " · ".join(dict.fromkeys(ABS_SKILL[p] for p in it["template"].split("+"))), "Chapter 4"])
        body += ("<h2>Answer key</h2><p>" + " · ".join(f"{it['n']}: {it['answer']}" for it in mk["items"]) + "</p>"
                 "<h2>Diagnostic: what each question tests</h2>" + table_html({"columns": ["Q", "Skill tested", "Review"], "rows": rows})
                 + "<p>Two or more misses on the same skill? Re-read that chapter and redo the matching practice block.</p>")
        for it in mk["items"]:
            body += sol_html(it, f"s{mk['key']}-{it['n']}", f"{mk['key']}.xhtml#q{mk['key']}-{it['n']}", f"Question {it['n']}")
        docs.append((fn, f"Solutions — {mk['title']}", xhtml("Solutions", body), 1))
    qr = [["Percentage change", "(new − old) ÷ old × 100"], ["Percentage points", "new rate − old rate"],
          ["Reverse percentage", "original = new ÷ (1 + rate)"], ["Successive changes", "multiply the factors"],
          ["Compound growth", "value × (1 + r)^n"], ["Weighted average", "sum of (size × average) ÷ total size"],
          ["Index numbers", "(later − earlier) ÷ earlier × 100"], ["Currency into euros", "local price ÷ units per €1"],
          ["Average speed", "total distance ÷ total time"], ["Critical path", "longest chain of dependent tasks"]]
    docs.append(("quickref.xhtml", "Quick-Reference Card", xhtml("Quick reference", "<h1>Quick-Reference Card</h1>" +
                 table_html({"columns": ["Situation", "Formula or method"], "rows": qr}) +
                 "<h2>Verbal traps</h2><p>Extreme wording · scope shift · cause and effect · outside knowledge · partial truth · "
                 "contradiction · unsupported comparison · unsupported inference · a proposal is not a decision.</p>"), 0))
    track = ("<h1>Score Tracker and Error Log</h1><p>Keep a simple notebook: for each set, record the date, your score and your time. For "
             "every wrong answer, write one line: what you did, what you should have done, and the rule to remember. Re-read it before "
             "each mock exam.</p><h2>A final word</h2><p>Reasoning tests reward method, calm and practice, and all three can be learned. "
             "Good luck with your selection procedure. If this workbook has helped you, a short review helps other candidates to find it.</p>")
    docs.append(("final.xhtml", "Score Tracker and Final Word", xhtml("Final", track), 0))

    # nav + opf
    nav_items = ""
    groups = [("Front matter", [d for d in docs[:2]]), ]
    lis = []
    groups = [("Part I — Understanding the Tests", lambda f: f.startswith("guide") and f != "guide0.xhtml"),
              ("Part II — Practice Sets", lambda f: f.startswith("set_")),
              ("Part III — Mock Exams", lambda f: f.startswith("mock")),
              ("Part IV — Answers and Worked Solutions", lambda f: f.startswith("sol_"))]
    lis.append('<li><a href="text/guide0.xhtml">How to Use This Book</a></li>')
    for gname, pred in groups:
        members = [(fn, title) for fn, title, _, lvl in docs if lvl is not None and pred(fn)]
        sub = "".join(f'<li><a href="text/{fn}">{e(title)}</a></li>' for fn, title in members)
        lis.append(f'<li><a href="text/{members[0][0]}">{e(gname)}</a><ol>{sub}</ol></li>')
    lis.append('<li><a href="text/quickref.xhtml">Quick-Reference Card</a></li>')
    lis.append('<li><a href="text/final.xhtml">Score Tracker and Final Word</a></li>')
    nav = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head><meta charset="utf-8"/><title>Contents</title></head>
<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{''.join(lis)}</ol></nav>
<nav epub:type="landmarks" hidden=""><ol>
<li><a epub:type="bodymatter" href="text/guide0.xhtml">Start</a></li></ol></nav></body></html>"""
    uid = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_DNS, "epso-reasoning-workbook"))
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="cover" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
                '<item id="coverpage" href="text/cover.xhtml" media-type="application/xhtml+xml"/>']
    spine = ['<itemref idref="coverpage" linear="yes"/>']
    for k, (fn, title, _, _) in enumerate(docs):
        manifest.append(f'<item id="d{k}" href="text/{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="d{k}"/>')
    for k, name in enumerate(IMAGES):
        manifest.append(f'<item id="i{k}" href="{name}" media-type="image/png"/>')
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{uid}</dc:identifier>
<dc:title>{e(meta['title'])}</dc:title>
<dc:creator>{e(meta['author'])}</dc:creator>
<dc:publisher>{e(meta['imprint'])}</dc:publisher>
<dc:language>en</dc:language>
<dc:description>{e(meta['subtitle'])}</dc:description>
<meta property="dcterms:modified">2026-10-01T00:00:00Z</meta>
<meta name="cover" content="cover"/>
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine>
{chr(10).join(spine)}
</spine>
</package>"""
    cover_x = xhtml("Cover", '<div class="center"><img src="../images/cover.jpg" alt="Cover" style="max-width:100%;"/></div>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>""",
                   compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/text/cover.xhtml", cover_x, compress_type=zipfile.ZIP_DEFLATED)
        cov = Image.open(OUT / "kindle_cover.jpg"); cov.thumbnail((1000, 1600))
        b = io.BytesIO(); cov.save(b, "JPEG", quality=85); z.writestr("OEBPS/images/cover.jpg", b.getvalue())
        for fn, _, x, _ in docs:
            z.writestr(f"OEBPS/text/{fn}", x, compress_type=zipfile.ZIP_DEFLATED)
        for name, data in IMAGES.items():
            z.writestr(f"OEBPS/{name}", data)
    return path


if __name__ == "__main__":
    p = build()
    print("epub", p, round(p.stat().st_size / 1e6, 2), "MB", len(IMAGES), "images")
