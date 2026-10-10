// Renders the background without text and reports text-vs-background contrast for every text item.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [html, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1210, height: 888 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  const items = await p.evaluate(() => {
    const sel = ['#kicker span', '#hundred', '#tips', '#dating', '#apps', '#sub', '#author', '.sp-title', '.sp-title b', '.sp-author',
      '#hook', '#hook em', '#body', '#inside', '#list li', '#close', '#imprint', '#shelf'];
    const r = [];
    for (const s of sel) document.querySelectorAll(s).forEach((e, i) => {
      for (const rc of e.getClientRects()) r.push({ s: s + (i ? '#' + i : ''), color: getComputedStyle(e).color,
        x: rc.x, y: rc.y, w: rc.width, h: rc.height });
    });
    return r;
  });
  await p.addStyleTag({ content: '#kicker,#hundred,#tips,#dating,#apps,#sub,#author,#spinetext,#backflow,#imprint,#shelf{visibility:hidden}' });
  await p.screenshot({ path: out });
  fs.writeFileSync(out + '.json', JSON.stringify(items));
  await b.close();
})();
