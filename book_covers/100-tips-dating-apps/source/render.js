// usage: node render.js <html> <out.png> <dpi>
const { chromium } = require('playwright');
(async () => {
  const [html, out, dpi] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.round(12.6 * 96), height: Math.round(9.25 * 96) },
                              deviceScaleFactor: Number(dpi || 300) / 96 });
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: 12.6 * 96, height: 9.25 * 96 } });
  await b.close();
})();
