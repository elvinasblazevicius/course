# Generates cover.html: KDP paperback wrap, 6x9 in, 140 pp cream (spine 0.35 in), 0.125 in bleed.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))

def ring(px, col):
    return ','.join(f'{px*math.cos(a*math.pi/8):.2f}px {px*math.sin(a*math.pi/8):.2f}px 0 {col}' for a in range(16))

def cup(x, y, handle_deg, latte, k=1.2):
    """Top-down cup on saucer at (x,y), viewBox units = 300/in, scaled by k. Light from upper left."""
    def arc(r, a0, a1, w, op):
        p0 = (r*math.cos(math.radians(a0)), r*math.sin(math.radians(a0)))
        p1 = (r*math.cos(math.radians(a1)), r*math.sin(math.radians(a1)))
        return f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" stroke="#FFFFFF" stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
    # handle: solid, tapering away from the cup, with a shade along its lower edge
    handle = 'M150 -46 C190 -44 226 -36 252 -32 C284 -28 284 28 252 32 C226 36 190 44 150 46 Z'
    hshade = 'M160 30 C196 34 226 30 252 28 C270 26 278 16 280 6 C276 22 262 34 246 38 C220 42 190 46 160 44 Z'
    return f'''
<g transform="translate({x} {y}) scale({k})">
  <circle cx="12" cy="18" r="238" fill="#2E0F2A" opacity=".18" filter="url(#contact)"/>
  <circle r="235" fill="url(#porc)"/>
  <circle r="235" fill="none" stroke="#E2D3C1" stroke-width="3"/>
  {arc(222, 196, 246, 7, .8)}
  <g transform="rotate({handle_deg})">
    <g transform="rotate({-handle_deg}) translate(10 14) rotate({handle_deg})"><path d="{handle}" fill="#6B3A10" opacity=".22" filter="url(#soft)"/></g>
    <path d="{handle}" fill="url(#porc)" stroke="#E0D1BF" stroke-width="3"/>
    <path d="{hshade}" fill="#E6D8C6"/>
  </g>
  <circle cx="14" cy="20" r="160" fill="#6B3A10" opacity=".24" filter="url(#cast)"/>
  <circle r="160" fill="url(#porc)"/>
  <circle r="160" fill="none" stroke="#E0D1BF" stroke-width="3"/>
  <circle r="134" fill="url(#well)"/>
  {arc(148, 200, 250, 6, .9)}
  {latte}
</g>'''

ROSETTA = '''<circle r="118" fill="url(#crema)"/>
  <g transform="rotate(-20)" filter="url(#feather)" fill="#F3E3CC">
    <path d="M0 -84 Q0 -60 0 -40" stroke="#F3E3CC" stroke-width="5" fill="none" stroke-linecap="round"/>
    <use href="#hrt" transform="translate(0 52) scale(2.05 1.7)"/>
    <use href="#hrt" transform="translate(0 2) scale(1.62 1.34)" stroke="#C48650" stroke-width="2.4"/>
    <use href="#hrt" transform="translate(0 -40) scale(1.18 .98)" stroke="#C48650" stroke-width="2.6"/>
    <path d="M0 -50 Q2 20 0 98" stroke="#C48650" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  </g>'''
HEART = '''<circle r="118" fill="url(#crema)"/>
  <g transform="rotate(-24) scale(1.12)" filter="url(#feather)">
    <path fill="#F3E3CC" d="M0 64 C-14 44 -64 20 -64 -16 C-64 -46 -43 -62 -22 -62 C-10 -62 -2 -54 0 -46 C2 -54 10 -62 22 -62 C43 -62 64 -46 64 -16 C64 20 14 44 0 64Z"/>
  </g>'''
SPOON = '''<g transform="translate(640 1800) rotate(-48) translate(0 246)">
  <ellipse rx="26" ry="36" fill="#8A4A0E" opacity=".25" filter="url(#soft)" transform="translate(8 6)"/>
  <ellipse rx="25" ry="35" fill="url(#steel)"/>
  <rect x="-7" y="30" width="14" height="150" rx="7" fill="url(#steel)"/>
</g>'''

ART = f'''<svg id="art" class="abs" viewBox="0 0 1800 2700" style="overflow:visible">
<defs>
  <radialGradient id="table" cx=".35" cy=".25" r=".8"><stop offset="0" stop-color="#FFE6A0"/><stop offset=".55" stop-color="#FFD877"/><stop offset="1" stop-color="#F6C75E"/></radialGradient>
  <radialGradient id="porc" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#FFFDF8"/><stop offset="1" stop-color="#EADFD2"/></radialGradient>
  <radialGradient id="well" cx=".62" cy=".66" r=".7"><stop offset="0" stop-color="#FFFDF8"/><stop offset=".8" stop-color="#F1E8DD"/><stop offset="1" stop-color="#E2D4C4"/></radialGradient>
  <radialGradient id="crema" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#D49A64"/><stop offset=".72" stop-color="#C98A55"/><stop offset=".93" stop-color="#9C6237"/><stop offset="1" stop-color="#8A5530"/></radialGradient>
  <linearGradient id="phone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4E2148"/><stop offset=".45" stop-color="#3B1736"/><stop offset="1" stop-color="#2C0F28"/></linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F2F0"/><stop offset=".5" stop-color="#BDB7B2"/><stop offset="1" stop-color="#8E8781"/></linearGradient>
  <filter id="cast" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="contact" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="24"/></filter>
  <filter id="feather" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.4"/></filter>
  <path id="hrt" d="M0 30 C-6 18 -30 4 -30 -14 C-30 -28 -20 -36 -9 -36 C-3 -36 0 -31 0 -27 C0 -31 3 -36 9 -36 C20 -36 30 -28 30 -14 C30 4 6 18 0 30Z"/>
</defs>
<!-- the table, cropped by the bottom trim: the viewer is sitting at it -->
<circle cx="930" cy="2560" r="1062" fill="#5E0F14" opacity=".30" filter="url(#cast)"/>
<circle cx="900" cy="2520" r="1050" fill="#E9B54A"/>
<circle cx="900" cy="2520" r="1036" fill="url(#table)"/>
<!-- phone face down, set aside at the table edge -->
<g transform="translate(232 2190) rotate(14) scale(1.1)">
  <rect x="-105" y="-215" width="210" height="430" rx="40" fill="#2E0F2A" opacity=".22" filter="url(#contact)" transform="translate(12 18)"/>
  <rect x="-105" y="-215" width="210" height="430" rx="40" fill="#6E3E66"/>
  <rect x="-100" y="-210" width="200" height="420" rx="36" fill="url(#phone)"/>
  <path d="M-100 40 L100 -120 L100 -60 L-100 100 Z" fill="#FFFFFF" opacity=".06"/>
  <rect x="-80" y="-190" width="88" height="124" rx="26" fill="#3A1534" stroke="#7A4A72" stroke-width="4"/>
  <circle cx="-36" cy="-158" r="22" fill="#1A0818" stroke="#9A7A95" stroke-width="6"/>
  <circle cx="-36" cy="-98" r="22" fill="#1A0818" stroke="#9A7A95" stroke-width="6"/>
</g>
{cup(640, 1800, 215, ROSETTA)}
{SPOON}
{cup(1210, 2075, 30, HEART)}
</svg>'''

CREAM = '#FFF3E3'; RED = '#CB2A37'; INK = '#2E0F2A'

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:600;font-style:normal;src:url(fonts/fraunces-latin-600-normal.woff2)}}
@font-face{{font-family:Fraunces;font-weight:600;font-style:italic;src:url(fonts/fraunces-latin-600-italic.woff2)}}
@font-face{{font-family:Fraunces;font-weight:900;font-style:normal;src:url(fonts/fraunces-latin-900-normal.woff2)}}
@font-face{{font-family:Fraunces;font-weight:900;font-style:italic;src:url(fonts/fraunces-latin-900-italic.woff2)}}
@font-face{{font-family:Brico;font-weight:400;src:url(fonts/bricolage-grotesque-latin-400-normal.woff2)}}
@font-face{{font-family:Brico;font-weight:600;src:url(fonts/bricolage-grotesque-latin-600-normal.woff2)}}
@font-face{{font-family:Brico;font-weight:800;src:url(fonts/bricolage-grotesque-latin-800-normal.woff2)}}
:root{{--cream:{CREAM};--red:{RED};--ink:{INK}}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:12.6in;height:9.25in;overflow:hidden;background:var(--red)}}
.abs{{position:absolute}}
#wrap{{position:relative;width:12.6in;height:9.25in;overflow:hidden;background:var(--red)}}
#grain{{left:0;top:0;width:12.6in;height:9.25in;opacity:.07;mix-blend-mode:multiply;pointer-events:none}}

/* front: trim box 6x9 in at (6.475, 0.125) */
#front{{left:6.475in;top:.125in;width:6in;height:9in}}
#artclip{{left:6.505in;top:0;width:6.095in;height:9.25in;overflow:hidden}}
#art{{left:0;top:0;width:6in;height:9in}}
.col{{position:absolute;left:0;width:6in;text-align:center}}
#lock{{position:absolute;top:.30in;left:0;width:6in;display:flex;justify-content:center;align-items:center;gap:.16in}}
#hundred{{font:900 108pt/.86 Fraunces;color:var(--cream);letter-spacing:-.03em;font-variation-settings:"SOFT" 30,"opsz" 144}}
#tips{{font:800 20.5pt/1.1 Brico;color:var(--cream);letter-spacing:.09em;text-align:left;padding-top:.06in}}
#dating{{top:1.53in;left:-.04in;font:italic 900 113pt/1 Fraunces;color:var(--cream);letter-spacing:-.02em;font-variation-settings:"SOFT" 50,"WONK" 1,"opsz" 144}}
#apps{{top:3.34in;font:800 24pt/1 Brico;color:var(--cream);letter-spacing:.16em}}
#sub{{top:3.90in;font:italic 600 14.5pt/1.36 Fraunces;color:var(--cream)}}
#author{{top:8.24in;font:800 15pt/1 Brico;color:var(--ink);letter-spacing:.2em}}

/* spine: 6.125 to 6.475 in */
#spinetext{{left:6.125in;top:0;width:.35in;height:9.25in}}
#spinetext .rot{{position:absolute;left:50%;top:50%;width:8.5in;height:.35in;transform:translate(-50%,-50%) rotate(90deg);
  display:flex;align-items:center;justify-content:space-between}}
.sp-title{{font:900 11.5pt/1 Fraunces;color:var(--cream);white-space:nowrap}}
.sp-title i{{font-style:italic}}
.sp-author{{font:800 9.5pt/1 Brico;color:var(--cream);letter-spacing:.16em;white-space:nowrap}}

/* back: trim box (0.125..6.125) */
#backflow{{position:absolute;left:.72in;top:.74in;width:4.95in;color:var(--cream)}}
#hook{{font:italic 600 17pt/1.26 Fraunces}}
#rule{{margin:.26in 0 .2in;width:.6in;height:2pt;background:#FFD15C}}
#body{{font:400 11.2pt/1.45 Brico}}
#inside{{margin-top:.24in;font:800 11pt/1 Brico;letter-spacing:.08em}}
#list{{margin-top:.13in;font:400 11pt/1.32 Brico;list-style:none}}
#list li{{position:relative;padding-left:.2in;margin-bottom:.05in}}
#list li:before{{content:"";position:absolute;left:.02in;top:.06in;width:.075in;height:.075in;border-radius:50%;background:#FFD15C}}
#close{{margin-top:.16in;font:italic 600 12pt/1.38 Fraunces}}
#imprint{{position:absolute;left:.72in;top:7.98in;font:800 10.5pt/1 Brico;color:var(--cream);letter-spacing:.12em}}
#shelf{{position:absolute;left:.72in;top:8.21in;font:400 9pt/1 Brico;color:var(--cream);letter-spacing:.08em}}
</style></head><body><div id="wrap">

<div id="artclip" class="abs"><div style="position:absolute;left:-.03in;top:.125in;width:6in;height:9in">{ART}</div></div>
<div id="front" class="abs">
<div id="lock"><div id="hundred">100</div><div id="tips">TIPS FOR<br>SUCCESSFUL</div></div>
<div id="dating" class="col">Dating</div>
<div id="apps" class="col">ON DATING APPS</div>
<div id="sub" class="col">To Better Profiles, Clearer Conversations,<br>and More Meaningful Connections</div>
<div id="author" class="col">ELENA MARLOWE VALE</div>
</div>

<div id="spinetext" class="abs"><div class="rot">
  <span class="sp-title">100 Tips for Successful <i>Dating on Dating Apps</i></span>
  <span class="sp-author">ELENA MARLOWE VALE</span>
</div></div>

<div id="back" class="abs" style="left:0;top:0;width:6.125in;height:9.25in">
  <div id="backflow">
    <div id="hook">Every dating app book tells you to “just be yourself” and “stay positive.” Neither one tells you what to actually write in a bio, how to tell a real match from a time-waster in the first three messages, or when to stop swiping and go outside instead.</div>
    <div id="rule"></div>
    <div id="body">This book is the practical half. One hundred concrete moves for the profile, the opening message, the in-app conversation, and the leap to a real first date – built for the apps as they actually work, not as the marketing copy describes them.</div>
    <div id="inside">INSIDE, AMONG THE HUNDRED</div>
    <ul id="list">
      <li>A profile and photo set that actually gets matches, not just views</li>
      <li>Opening lines that get replies, and the ones that kill a conversation</li>
      <li>Reading red flags in a bio and in the first few messages</li>
      <li>Getting from chatting to a real date without it fizzling out</li>
      <li>Staying safe: verification, video calls, and the first meetup</li>
      <li>Handling ghosting, rejection, and matches that go nowhere</li>
      <li>Avoiding burnout and swipe fatigue over a long search</li>
      <li>Knowing when an app conversation is worth your time at all</li>
    </ul>
    <div id="close">One hundred concrete actions for dating apps, each ending with one thing to do today. No generic positivity, and no pretending every match deserves your time.</div>
  </div>
  <div id="imprint">MARLOWE VALE PRESS</div>
  <div id="shelf">SELF-HELP / DATING &amp; RELATIONSHIPS</div>
</div>

<svg id="grain" class="abs" viewBox="0 0 1260 925" preserveAspectRatio="none">
  <filter id="n"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
  <rect width="100%" height="100%" filter="url(#n)"/>
</svg>
</div></body></html>'''

open(os.path.join(HERE, 'cover.html'), 'w').write(HTML)
print('wrote cover.html')
