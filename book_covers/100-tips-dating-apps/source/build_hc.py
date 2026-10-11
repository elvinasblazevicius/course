# Hardcover (case laminate) wrap from the same design as build.py.
# 6x9, 140 pp cream. Spine = 140*0.0025 + 0.1885 = 0.5385 in.
# Width  = 0.591 wrap + 6 board + 0.197 hinge + spine + 0.197 hinge + 6 board + 0.591 wrap = 14.115 in
# Height = 0.591 wrap + 9.236 board (9 in + 0.236 overhang) + 0.591 wrap = 10.417 in
import os, re, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(HERE, 'build.py'))           # writes cover.html (paperback)
s = open(os.path.join(HERE, 'cover.html')).read()

WRAP, HINGE, SPINE = 0.591, 0.197, 0.5385
W = 2*WRAP + 2*6 + 2*HINGE + SPINE                       # 14.1145
H = 10.417
BACK_X = WRAP                                            # back board left edge
SPINE_X = WRAP + 6 + HINGE                               # 6.788
FRONT_X = SPINE_X + SPINE + HINGE                        # 7.5235
TOP = WRAP + 0.118                                       # 6x9 design centred on the 9.236 in board

def r(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

r('html,body{width:12.6in;height:9.25in;', f'html,body{{width:{W:.4f}in;height:{H}in;')
r('#wrap{position:relative;width:12.6in;height:9.25in;', f'#wrap{{position:relative;width:{W:.4f}in;height:{H}in;')
r('#grain{left:0;top:0;width:12.6in;height:9.25in;', f'#grain{{left:0;top:0;width:{W:.4f}in;height:{H}in;')
# front: same 6x9 design placed on the front board
r('#front{left:6.475in;top:.125in;', f'#front{{left:{FRONT_X:.4f}in;top:{TOP:.3f}in;')
# table art: bleeds into the right and bottom wraps, stops 0.03 in short of the spine edge
clip_x = SPINE_X + SPINE + 0.03
r('#artclip{left:6.505in;top:0;width:6.095in;height:9.25in;overflow:hidden}',
  f'#artclip{{left:{clip_x:.4f}in;top:0;width:{W-clip_x:.4f}in;height:{H}in;overflow:hidden}}')
r('<div style="position:absolute;left:-.03in;top:.125in;width:6in;height:9in">',
  f'<div style="position:absolute;left:{FRONT_X-clip_x:.4f}in;top:{TOP:.3f}in;width:6in;height:9in">')
# spine
r('#spinetext{left:6.125in;top:0;width:.35in;height:9.25in}', f'#spinetext{{left:{SPINE_X:.4f}in;top:0;width:{SPINE}in;height:{H}in}}')
r('width:8.5in;height:.35in;transform', f'width:8.4in;height:{SPINE}in;transform')
r('.sp-title{font:900 11.5pt/1 Fraunces;', '.sp-title{font:900 15pt/1 Fraunces;')
r('.sp-author{font:800 9.5pt/1 Brico;', '.sp-author{font:800 11pt/1 Brico;')
# back: its inner layout assumes the trim starts at 0.125 in, so shift the panel
r('<div id="back" class="abs" style="left:0;top:0;width:6.125in;height:9.25in">',
  f'<div id="back" class="abs" style="left:{BACK_X-0.125:.3f}in;top:{TOP-0.125:.3f}in;width:6.125in;height:9.25in">')
pass
open(os.path.join(HERE, 'cover_hc.html'), 'w').write(s)
print(f'wrote cover_hc.html  {W:.4f} x {H} in; spine {SPINE_X:.4f}-{SPINE_X+SPINE:.4f}; front board {FRONT_X:.4f}-{FRONT_X+6:.4f}')
