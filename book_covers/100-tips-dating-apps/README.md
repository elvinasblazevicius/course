# 100 Tips for Successful Dating on Dating Apps: paperback cover

**Status: the cover file is print-ready and ready to upload to KDP (paperback). It is NOT signed off on design: the last independent audit scored 8.0 against the agreed 9.0 pass mark. Final files were generated on request before a fresh re-audit of the last fixes.**

## Files

| File | Use |
|---|---|
| `paperback_cover.pdf` | **Upload this to KDP.** Paperback, then Cover, then "Upload a cover you already have" |
| `front_cover_6x9.jpg` | Front only, at trim size: 1800 × 2700 px at 300 DPI. For previews, ads and A+ |
| `preview_full_wrap.png` | Low-resolution preview of the full wrap |
| `source/build.py` | Generates `source/cover.html`. Render it with `render.js` (Playwright + Chromium) |
| `source/concepts/` | The three concept mockups (A type-led, B match flame, C café table) |
| `work/` | Audit packs for rounds 1–3 and the concept pack |

## Specification (unchanged from the original file)

- Trim 6 × 9 in, cream paper, 140 pages, black ink.
- Spine: 140 × 0.0025 in = 0.35 in.
- Full wrap with 0.125 in bleed: 12.6 × 9.25 in (907.2 × 666 pt), one page.
- 300 DPI raster (3778 × 2775 px), JPEG quality 95, RGB.
- Title, subtitle, author, imprint and all back-cover wording are unchanged.

## Design

- **Concept:** a top-down café table with two half-drunk coffees (a tulip and a heart in the latte art) and the phone face down at the table's edge. The after-state the book promises is a real date, with the phone put away.
- **Palette:** tomato red #CB2A37 ground, cream #FFF3E3 type, butter-yellow table, aubergine #2E0F2A author line.
- **Type:** Fraunces Black and Black Italic for "100" and "Dating", Bricolage Grotesque ExtraBold for the caps lines. Both are OFL fonts. No outlines and no 3D effects.
- The art is code-drawn vector (no AI images, no photos) with 7% paper grain.

## Audit history (fresh independent reviewers each round)

| Round | Concept | Design scores | 160 px | Main changes before the next round |
|---|---|---|---|---|
| 1 | Pink, glossy heart and chat bubble | 7.5 / 7.5 | 8.5 / 8.5 | Flat type effects, spine colour made continuous, kicker removed |
| 2 | Pink, two-bubble heart | 8.0 / 7.5 | 8.0 / 8.0 | Restarted from scratch with three concepts |
| Concepts | A yellow type-led, B match flame, C café table, D pink bubble | Both reviewers picked **C** (potential 8.5; buyer 7.5 to buy, against 4.5 for D) | | C built properly |
| 3 | C, café table | 8.0 / 8.0 | 8.5 / 8.5 | Listed below |

**Fixes made after round 3:**
- The left latte art is now a tulip, replacing the "fishbone" rosetta.
- The cups were rebuilt: fewer rings, rim highlights, tapered solid handles and contact shadows.
- The cups and phone are 1.2× larger and staggered diagonally, which removes the side-by-side "two eyes" read.
- The phone has a lighter rim, a sheen and clearer lenses.
- The table is a softer butter yellow.
- "ON DATING APPS" is 15% larger.
- The spine title is smaller, so it sits further from the folds.
- The yellow table ends 0.03 in short of the front fold, so fold drift shows red on red.

**These fixes have not been re-audited.**

## Open items (from the round-3 reviewers, not yet done)

- The phone is still the darkest object, so it can pull focus from the cups. Option: shrink it to 0.85×, crop about 25% of it off the left trim, and lighten it.
- Show "half-drunk" more clearly: lower the coffee levels and add foam tide rings.
- Type and image are stacked rather than interlocked. Option: let the heart cup's saucer cross the table rim into the red.
- Taste items: raspberry #C21F4A instead of tomato (less "ketchup and mustard"), an aluminium bistro rim on the table, and matching sizes for the two caps lines.

## Checks (final file)

- **Contrast:** every text item ≥ 4.92:1 (cream on red); the author on the table is 11.6:1.
- **Front safe zone:** display type ink is ≥ 0.32 in inside the trim on all sides.
- **Spine:** title em box ≥ 0.074 in from each fold (KDP minimum 0.0625).
- **Back:** text is clear of the KDP barcode box (x 3.875–5.875 in, y 7.675–8.875 in); the closing paragraph ends at 7.24 in.
- **Before release:** order a printed proof. RGB is converted to CMYK by KDP, so check the red and yellow on paper.

## Rebuild

```bash
cd source
python3 build.py                                                     # writes cover.html
NODE_PATH=$(npm root -g) node render.js "$PWD/cover.html" final300.png 300
# wrap final300.png into a 907.2 x 666 pt single-page PDF (ReportLab drawImage at full page)
NODE_PATH=$(npm root -g) node checks.js "$PWD/cover.html" bg.png && python3 contrast.py bg.png
```
