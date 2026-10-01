"""Register the embedded OFL fonts and make them reportlab's defaults. Import before any other reportlab module."""
from pathlib import Path

from reportlab import rl_config
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"

if "Sans" not in pdfmetrics.getRegisteredFontNames():
    for fam, short in [("Serif", "SourceSerif"), ("Sans", "SourceSans"), ("Mono", "JBMono")]:
        pdfmetrics.registerFont(TTFont(fam, str(FONT_DIR / f"{short}-400.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-It", str(FONT_DIR / f"{short}-400i.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-Semi", str(FONT_DIR / f"{short}-600.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-Bold", str(FONT_DIR / f"{short}-700.ttf")))
        pdfmetrics.registerFont(TTFont(f"{fam}-BoldIt", str(FONT_DIR / f"{short}-700i.ttf")))
        addMapping(fam, 0, 0, fam); addMapping(fam, 0, 1, f"{fam}-It")
        addMapping(fam, 1, 0, f"{fam}-Bold"); addMapping(fam, 1, 1, f"{fam}-BoldIt")
    pdfmetrics.registerFont(TTFont("Display", str(FONT_DIR / "LeagueGothic-400.ttf")))
    for w, nm in (("500", "Frank-Med"), ("600", "Frank-Semi"), ("700", "Frank-Bold"), ("800", "Frank-XBold"), ("900", "Frank-Black")):
        pdfmetrics.registerFont(TTFont(nm, str(FONT_DIR / f"LibreFranklin-{w}.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
    addMapping("DejaVu", 0, 0, "DejaVu"); addMapping("DejaVu", 1, 0, "DejaVu")
    addMapping("DejaVu", 0, 1, "DejaVu"); addMapping("DejaVu", 1, 1, "DejaVu")

rl_config.canvas_basefontname = "Sans"
