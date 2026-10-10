# Generates cover.html: KDP paperback wrap, 6x9 in, 140 pp cream (spine 0.35 in), 0.125 in bleed.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))

def ring(px, col):
    return ','.join(f'{px*math.cos(a*math.pi/8):.2f}px {px*math.sin(a*math.pi/8):.2f}px 0 {col}' for a in range(16))

def cup(x, y, handle_deg, latte):
    """Top-down cup on saucer at (x,y), viewBox units = 300/in. Light from upper left."""
    hx = f'rotate({handle_deg})'
    return f'''
<g transform="translate({x} {y})">
  <circle cx="26" cy="30" r="236" fill="#8A4A0E" opacity=".30" filter="url(#cast)"/>
  <circle r="235" fill="url(#porc)"/>
  <circle r="232" fill="none" stroke="#E3D6C6" stroke-width="4"/>
  <circle r="168" fill="#EFE5D8"/>
  <g transform="{hx}">
    <g transform="rotate({-handle_deg}) translate(14 18) rotate({handle_deg})"><path d="M140 -42 H250 a42 42 0 0 1 0 84 H140 Z" fill="#8A4A0E" opacity=".22" filter="url(#soft)"/></g>
    <path d="M140 -42 H250 a42 42 0 0 1 0 84 H140 Z" fill="#FFFDF8" stroke="#E0D2C1" stroke-width="4"/>
    <path d="M172 -15 H238 a15 15 0 0 1 0 30 H172 Z" fill="#E9DED0"/>
  </g>
  <circle cx="18" cy="22" r="160" fill="#8A4A0E" opacity=".26" filter="url(#cast)"/>
  <circle r="160" fill="url(#porc)"/>
  <circle r="160" fill="none" stroke="#E2D4C3" stroke-width="5"/>
  <circle r="138" fill="url(#well)"/>
  <circle r="124" fill="none" stroke="#E9D6BE" stroke-width="10" opacity=".9"/>
  {latte}
</g>'''

ROSETTA = '''<circle r="110" fill="url(#crema)"/>
  <g fill="#F6E7D3" transform="rotate(-18)">
    <path d="M0 -84 C30 -84 44 -66 44 -52 C30 -60 14 -62 0 -60 C-14 -62 -30 -60 -44 -52 C-44 -66 -30 -84 0 -84Z"/>
    <path d="M0 -50 C38 -50 58 -30 60 -12 C40 -24 20 -26 0 -24 C-20 -26 -40 -24 -60 -12 C-58 -30 -38 -50 0 -50Z"/>
    <path d="M0 -14 C42 -14 66 6 68 26 C46 12 22 10 0 12 C-22 10 -46 12 -68 26 C-66 6 -42 -14 0 -14Z"/>
    <path d="M0 22 C40 22 62 40 62 60 C42 48 20 46 0 48 C-20 46 -42 48 -62 60 C-62 40 -40 22 0 22Z"/>
    <path d="M-3 -96 L3 -96 L4 92 L-4 92Z"/>
  </g>'''
HEART = '''<circle r="104" fill="url(#crema)"/>
  <g transform="rotate(-24)">
    <path fill="#F6E7D3" d="M0 64 C-14 44 -64 20 -64 -16 C-64 -46 -43 -62 -22 -62 C-10 -62 -2 -54 0 -46 C2 -54 10 -62 22 -62 C43 -62 64 -46 64 -16 C64 20 14 44 0 64Z"/>
  </g>'''
SPOON = '''<g transform="translate(650 1790) rotate(-40) translate(0 200)">
  <ellipse rx="26" ry="36" fill="#8A4A0E" opacity=".25" filter="url(#soft)" transform="translate(8 6)"/>
  <ellipse rx="25" ry="35" fill="url(#steel)"/>
  <rect x="-7" y="30" width="14" height="150" rx="7" fill="url(#steel)"/>
</g>'''

ART = f'''<svg id="art" class="abs" viewBox="0 0 1800 2700" style="overflow:visible">
<defs>
  <radialGradient id="table" cx=".35" cy=".25" r=".8"><stop offset="0" stop-color="#FFE08A"/><stop offset=".55" stop-color="#FFD15C"/><stop offset="1" stop-color="#F7C346"/></radialGradient>
  <radialGradient id="porc" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#FFFDF8"/><stop offset="1" stop-color="#EADFD2"/></radialGradient>
  <radialGradient id="well" cx=".62" cy=".66" r=".7"><stop offset="0" stop-color="#FFFDF8"/><stop offset=".8" stop-color="#F1E8DD"/><stop offset="1" stop-color="#E2D4C4"/></radialGradient>
  <radialGradient id="crema" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#D49A64"/><stop offset=".72" stop-color="#C98A55"/><stop offset=".93" stop-color="#9C6237"/><stop offset="1" stop-color="#8A5530"/></radialGradient>
  <linearGradient id="phone" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4E2148"/><stop offset=".45" stop-color="#3B1736"/><stop offset="1" stop-color="#2C0F28"/></linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F2F0"/><stop offset=".5" stop-color="#BDB7B2"/><stop offset="1" stop-color="#8E8781"/></linearGradient>
  <filter id="cast" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<!-- the table, cropped by the bottom trim: the viewer is sitting at it -->
<circle cx="930" cy="2560" r="1062" fill="#5E0F14" opacity=".30" filter="url(#cast)"/>
<circle cx="900" cy="2520" r="1050" fill="#EBB23A"/>
<circle cx="900" cy="2520" r="1036" fill="url(#table)"/>
<!-- phone face down, pushed to the table edge -->
<g transform="translate(250 2080) rotate(16)">
  <rect x="-105" y="-215" width="210" height="430" rx="40" fill="#8A4A0E" opacity=".32" filter="url(#cast)" transform="translate(18 22)"/>
  <rect x="-105" y="-215" width="210" height="430" rx="40" fill="url(#phone)"/>
  <rect x="-105" y="-215" width="210" height="430" rx="40" fill="none" stroke="#5E2D57" stroke-width="3"/>
  <rect x="-78" y="-188" width="84" height="120" rx="24" fill="#33122F" stroke="#5A2853" stroke-width="3"/>
  <circle cx="-36" cy="-158" r="22" fill="#1E0A1C" stroke="#4E2148" stroke-width="5"/>
  <circle cx="-36" cy="-100" r="22" fill="#1E0A1C" stroke="#4E2148" stroke-width="5"/>
</g>
{cup(650, 1790, 140, ROSETTA)}
{SPOON}
{cup(1180, 1900, -40, HEART)}
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
#artclip{{left:6.475in;top:0;width:6.125in;height:9.25in;overflow:hidden}}
#art{{left:0;top:0;width:6in;height:9in}}
.col{{position:absolute;left:0;width:6in;text-align:center}}
#lock{{position:absolute;top:.30in;left:0;width:6in;display:flex;justify-content:center;align-items:center;gap:.16in}}
#hundred{{font:900 100pt/.86 Fraunces;color:var(--cream);letter-spacing:-.03em;font-variation-settings:"SOFT" 30,"opsz" 144}}
#tips{{font:800 19pt/1.1 Brico;color:var(--cream);letter-spacing:.09em;text-align:left;padding-top:.06in}}
#dating{{top:1.53in;left:-.04in;font:italic 900 113pt/1 Fraunces;color:var(--cream);letter-spacing:-.02em;font-variation-settings:"SOFT" 50,"WONK" 1,"opsz" 144}}
#apps{{top:3.36in;font:800 21pt/1 Brico;color:var(--cream);letter-spacing:.16em}}
#sub{{top:3.84in;font:italic 600 14.5pt/1.36 Fraunces;color:var(--cream)}}
#author{{top:8.24in;font:800 15pt/1 Brico;color:var(--ink);letter-spacing:.2em}}

/* spine: 6.125 to 6.475 in */
#spinetext{{left:6.125in;top:0;width:.35in;height:9.25in}}
#spinetext .rot{{position:absolute;left:50%;top:50%;width:8.5in;height:.35in;transform:translate(-50%,-50%) rotate(90deg);
  display:flex;align-items:center;justify-content:space-between}}
.sp-title{{font:900 13pt/1 Fraunces;color:var(--cream);white-space:nowrap}}
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

<div id="artclip" class="abs"><div style="position:absolute;left:0;top:.125in;width:6in;height:9in">{ART}</div></div>
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
