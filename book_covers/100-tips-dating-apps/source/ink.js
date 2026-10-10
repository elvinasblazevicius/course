const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1210, height: 888 } });
  await p.goto('file://' + process.argv[2]); await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => ['#hundred','#tips','#dating','#apps','#sub','#author'].map(s => {
    const rg = document.createRange(); rg.selectNodeContents(document.querySelector(s)); const q = rg.getBoundingClientRect();
    return [s, q.x/96, (q.x+q.width)/96, q.y/96, (q.y+q.height)/96]; }));
  for (const [s,x0,x1,y0,y1] of r) console.log(s.padEnd(10), 'left', (x0-6.475).toFixed(2), 'right', (12.475-x1).toFixed(2), 'top', (y0-.125).toFixed(2), 'bottom', (9.125-y1).toFixed(2));
  await b.close(); })();
