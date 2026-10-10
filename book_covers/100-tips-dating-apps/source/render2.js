// usage: node render2.js <html> <out.png> <dpi> <wIn> <hIn>
const { chromium } = require('playwright');
(async () => {
  const [html, out, dpi, w, h] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.round(w * 96), height: Math.round(h * 96) }, deviceScaleFactor: Number(dpi) / 96 });
  await p.goto('file://' + html); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: out }); await b.close();
})();
