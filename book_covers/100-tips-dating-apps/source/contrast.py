import json, re, sys
import numpy as np
from PIL import Image

bg = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float) / 255
items = json.load(open(sys.argv[1] + '.json'))

def lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def lum(rgb):
    l = lin(rgb)
    return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]

L = lum(bg)
worst = 99
for it in items:
    c = np.array([int(v) for v in re.findall(r'\d+', it['color'])[:3]]) / 255
    lt = float(lum(c))
    x0, y0 = max(0, int(it['x'])), max(0, int(it['y']))
    x1, y1 = min(bg.shape[1], int(it['x'] + it['w'])), min(bg.shape[0], int(it['y'] + it['h']))
    if x1 <= x0 or y1 <= y0:
        continue
    region = L[y0:y1, x0:x1].ravel()
    ratios = (np.maximum(lt, region) + .05) / (np.minimum(lt, region) + .05)
    r = float(np.percentile(ratios, 2))  # near-worst pixel behind the text
    worst = min(worst, r)
    print(f"{it['s']:16s} {r:5.2f}:1 {'OK' if r >= 4.5 else 'LOW'}")
print(f'worst {worst:.2f}:1')
