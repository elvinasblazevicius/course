// Contrast + safe-zone data: renders the page with text hidden and records each text item's glyph box.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.round(+process.argv[4]*96), height: Math.round(+process.argv[5]*96) }, deviceScaleFactor: 1 });
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  const items = await p.evaluate(() => {
    const sel = ['#hundred', '#tips', '#dating', '#apps', '#sub', '#author', '.sp-title', '.sp-author',
      '#hook', '#body', '#inside', '#list li', '#close', '#imprint', '#shelf'];
    const r = [];
    for (const s of sel) document.querySelectorAll(s).forEach((e, i) => {
      const rg = document.createRange(); rg.selectNodeContents(e);
      for (const rc of rg.getClientRects()) if (rc.width > 2) r.push({ s: s + (i ? '#' + i : ''), color: getComputedStyle(e).color,
        x: rc.x, y: rc.y, w: rc.width, h: rc.height });
    });
    return r;
  });
  await p.addStyleTag({ content: '#lock,#dating,#apps,#sub,#author,#spinetext,#backflow,#imprint,#shelf{visibility:hidden}' });
  await p.screenshot({ path: out });
  fs.writeFileSync(out + '.json', JSON.stringify(items));
  await b.close();
})();
