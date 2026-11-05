// Gengiver HTML-siderne til JPG-billeder.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = __dirname;
  const out = path.join(dir, 'site', 'sider');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const sizes = { 's-01': [1181, 1575], 's-03': [1181, 1181] };
  for (const f of fs.readdirSync(path.join(dir, 'pages')).sort()) {
    const name = f.replace('.html', '');
    const [w, h] = sizes[name] || [1181, 2362];
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
    await page.goto('file://' + path.join(dir, 'pages', f));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(out, name + '.jpg'), type: 'jpeg', quality: 84 });
    await page.close();
  }
  await browser.close();
  console.log('rendered');
})();
