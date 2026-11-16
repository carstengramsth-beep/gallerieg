// Laver trykklare PDF'er i fuld størrelse med 3 mm udfald og skæremærker.
// Brug: node tryk.js <udmappe>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const MM = 96 / 25.4;              // CSS-px pr. mm
const BLEED = 3;                   // udfald i mm
const SLUG = 15;                   // plads uden for udfald til mærker (mm)
const MARK_GAP = 3;                // mærker starter 3 mm fra beskæringen
const MARK_LEN = 8;                // mærkernes længde i mm

// side: [html, bredde px, højde px, bredde mm, højde mm]
const SIDER = {
  's-02': [1181, 2362, 300, 600],
  's-03': [1181, 1181, 300, 300],
};
for (let i = 4; i <= 15; i++) SIDER['s-' + String(i).padStart(2, '0')] = [1181, 2362, 300, 600];

const NAVNE = { 's-02': 'Omslag', 's-03': 'Tekstside' };
const MDR = ['Januar','Februar','Marts','April','Maj','Juni','Juli','August','September','Oktober','November','December'];
for (let i = 4; i <= 15; i++) NAVNE['s-' + String(i).padStart(2, '0')] = MDR[i - 4];

async function lavSide(browser, navn, ud) {
  const [wpx, hpx, wmm, hmm] = SIDER[navn];
  const skala = (wmm * MM) / wpx;              // indhold-px -> CSS-px
  const b = BLEED / (skala / MM);              // udfald i indhold-px
  const total = [wmm + 2 * (BLEED + SLUG), hmm + 2 * (BLEED + SLUG)];
  const page = await browser.newPage({ viewport: { width: wpx, height: hpx } });
  await page.goto('file://' + path.join(__dirname, 'pages', navn + '.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(({ wpx, hpx, b, skala, wmm, hmm, total, BLEED, SLUG, MARK_GAP, MARK_LEN, MM, etiket }) => {
    // Udvid billeder, der går til kanten, ind i udfaldet
    const ud = (el, sider) => {
      if (!el) return;
      const r = el.getBoundingClientRect();
      const s = el.style;
      s.position = 'absolute';
      let l = r.left, t = r.top, w = r.width, h = r.height;
      if (sider.includes('l') && l <= 0.5) { l -= b; w += b; }
      if (sider.includes('t') && t <= 0.5) { t -= b; h += b; }
      if (sider.includes('r') && l + w >= wpx - 0.5) { w += b; }
      if (sider.includes('b') && t + h >= hpx - 0.5) { h += b; }
      s.left = l + 'px'; s.top = t + 'px'; s.width = w + 'px'; s.height = h + 'px';
      s.right = 'auto'; s.bottom = 'auto'; s.inset = 'auto';
      s.left = l + 'px'; s.top = t + 'px';
    };
    document.querySelectorAll('.billede').forEach(el => ud(el, 'ltr'));
    document.querySelectorAll('.b').forEach(el => ud(el, 'ltrb'));

    // Pak siden ind og skaler den til mm
    const wrap = document.createElement('div');
    while (document.body.firstChild) wrap.appendChild(document.body.firstChild);
    const off = (BLEED + SLUG) * MM;
    wrap.style.cssText = `position:absolute;left:${off}px;top:${off}px;width:${wpx}px;height:${hpx}px;transform-origin:0 0;transform:scale(${skala});overflow:visible`;
    // Klip alt, der går ud over udfaldet
    const klip = document.createElement('div');
    klip.style.cssText = `position:absolute;left:${SLUG * MM}px;top:${SLUG * MM}px;width:${(wmm + 2 * BLEED) * MM}px;height:${(hmm + 2 * BLEED) * MM}px;overflow:hidden`;
    wrap.style.left = BLEED * MM + 'px'; wrap.style.top = BLEED * MM + 'px';
    klip.appendChild(wrap);
    document.documentElement.style.cssText = document.body.style.cssText = `width:${total[0] * MM}px;height:${total[1] * MM}px;overflow:hidden;margin:0;background:#fff`;
    document.body.appendChild(klip);

    // Skæremærker
    const linje = (x, y, w, h) => {
      const d = document.createElement('div');
      d.style.cssText = `position:absolute;left:${x * MM}px;top:${y * MM}px;width:${w * MM}px;height:${h * MM}px;background:#000`;
      document.body.appendChild(d);
    };
    const t = 0.1; // stregtykkelse mm
    const x0 = BLEED + SLUG, y0 = BLEED + SLUG, x1 = x0 + wmm, y1 = y0 + hmm;
    const g = MARK_GAP, L = MARK_LEN;
    for (const [x, sx] of [[x0, -1], [x1, 1]]) for (const [y, sy] of [[y0, -1], [y1, 1]]) {
      // vandret
      linje(sx < 0 ? x - g - L : x + g, y - t / 2, L, t);
      // lodret
      linje(x - t / 2, sy < 0 ? y - g - L : y + g, t, L);
    }
    const tx = document.createElement('div');
    tx.textContent = etiket;
    tx.style.cssText = `position:absolute;left:${x0 * MM}px;top:${(y1 + BLEED + 4) * MM}px;font:8pt Arial,sans-serif;color:#000;white-space:nowrap`;
    document.body.appendChild(tx);
  }, { wpx, hpx, b, skala, wmm, hmm, total, BLEED, SLUG, MARK_GAP, MARK_LEN, MM,
       etiket: `GalleriEG kunstkalender 2027 · ${NAVNE[navn]} · ${wmm} × ${hmm} mm · 3 mm udfald` });
  await page.waitForTimeout(300);
  const fil = path.join(ud, navn + '.pdf');
  await page.pdf({ path: fil, width: total[0] + 'mm', height: total[1] + 'mm', printBackground: true, pageRanges: '1' });
  await page.close();
  return fil;
}

(async () => {
  const ud = process.argv[2];
  fs.mkdirSync(ud, { recursive: true });
  const browser = await chromium.launch();
  for (const navn of Object.keys(SIDER)) await lavSide(browser, navn, ud);
  await browser.close();
  console.log('ok');
})();
