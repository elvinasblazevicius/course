# 100 Tips for Successful Dating on Dating Apps: paperback cover (redesign)

**Status: cover READY TO UPLOAD to KDP (paperback). The book as a whole is NOT READY TO PUBLISH until the independent 3-pass audit and a printed proof are done.**

## Files

| File | Use |
|---|---|
| `paperback_cover.pdf` | Upload this to KDP: Paperback Content, Cover, "Upload a cover you already have" |
| `front_cover_6x9.jpg` | Front only, trim size, 1800 × 2700 px. For previews, ads and A+ |
| `preview_full_wrap.png` | Low-resolution preview of the full wrap |
| `source/` | Editable HTML/SVG source, OFL fonts, render and check scripts |

## Specification (same as the original file)

- Trim 6 × 9 in, cream paper, 140 pages, black ink
- Spine 140 × 0.0025 in = 0.35 in
- Full wrap with 0.125 in bleed: 12.6 × 9.25 in (907.2 × 666 pt), single page
- 300 DPI raster (3778 × 2775 px), JPEG quality 95, RGB
- Unchanged fields: title, subtitle, author, imprint and all back-cover copy. The only copy edit is a hyphen changed to an en dash.

## Design brief, following the cover rules in the `kdp-book-production` skill

- **Emotion:** hope and delight, the feeling of a match that turns into something real.
- **After-state, not the problem:** a glossy heart (the connection) with an incoming "typing…" bubble (the app conversation that is going well).
- **Bright ground:** saturated raspberry-to-hot-pink, with a warm coral glow behind the heart and 1–2% grain against banding.
- **Title as image:** Fraunces Black (with the SOFT and WONK axes) in a dimensional extruded style with a wine outline; "TIPS FOR SUCCESSFUL" and "ON DATING APPS" in Bricolage Grotesque ExtraBold, in sun yellow. The title fills about 55% of the front.
- **Layered:** the heart sits behind "Dating" and between the title lines, crossing them.
- **Hierarchy:** 100 / Dating > heart > the two support lines > subtitle > author.
- **Avoided:** stock photo, identifiable people, the old "Canva stack" plain caps, spinner or chip shapes.

## Checks run

- Page size 907.2 × 666 pt, 1 page, image at 300 ppi (`pdfinfo`, `pdfimages`).
- **Contrast** (`source/contrast.py`, WCAG ratio against the actual pixels behind each item):
  - All front, spine and back body text: ≥ 4.5:1 (lowest is the kicker at 4.78:1).
  - The four display lines (100, TIPS FOR SUCCESSFUL, Dating, ON DATING APPS) are each ringed by a solid wine outline: cream 12.8:1 and yellow 9.9:1 against it. The box sampler shows them as low only because it averages the heart under the whole text box.
- **Safe zones:**
  - Front text is at least 0.28 in from the trim, and the sparkles are kept inside 0.2 in.
  - Spine text is at least 0.08 in from each fold (KDP minimum 0.0625) and at least 0.2 in from the head and foot trims.
  - The barcode area (lower right of the back, about 2 × 1.2 in) is clear.
- **Thumbnail:** at 160 px, "100", "Dating" and the heart all read; the old cover's title was illegible at that size.

## Open items

- Run an independent cover audit (fresh reviewer, at least 9.5) per the skill before release.
- Order a printed proof. RGB is converted by KDP, and the hot pink shifts slightly in CMYK, so check it on the proof.
- Hardcover wrap and ebook cover (1600 × 2560) have not been made yet. Both can be built from the same source.

## Rebuild

```bash
cd source
NODE_PATH=$(npm root -g) node render.js "$PWD/cover.html" final300.png 300   # Playwright + Chromium
# then wrap final300.png into a 907.2 x 666 pt PDF (ReportLab drawImage at full page)
NODE_PATH=$(npm root -g) node checks.js "$PWD/cover.html" bgonly.png && python3 contrast.py bgonly.png
```
