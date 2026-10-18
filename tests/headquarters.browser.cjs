// Optional development checks: install Playwright and Chromium outside the site.
// Start a root static server, then run:
// CHROMIUM_PATH=/usr/bin/chromium node tests/headquarters.browser.cjs
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
(async () => {
  const base = process.env.BASE_URL || 'http://127.0.0.1:8000/';
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox']});
  try {
    for (const width of [320, 375, 390, 430, 768, 1024, 1440]) {
      const context = await browser.newContext({viewport: {width, height: 900}, isMobile: width < 500, hasTouch: width < 500});
      const page = await context.newPage();
      const errors = [], requests = [], failures = [];
      page.on('pageerror', e => errors.push(e.message));
      page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
      page.on('request', r => requests.push(r.url()));
      page.on('response', r => { if (r.status() >= 400) failures.push(r.url()); });
      assert.equal((await page.goto(base)).status(), 200);
      assert.equal(await page.locator('h1').count(), 1);
      assert.equal(await page.locator('script').count(), 0);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow at ${width}`);
      for (const a of await page.locator('a[href^="#"]').all()) {
        assert.equal(await page.locator(await a.getAttribute('href')).count(), 1);
      }
      await page.locator('nav a[href="#mission-log"]').click();
      assert.equal(new URL(page.url()).hash, '#mission-log');
      await page.goto(base);
      await page.keyboard.press('Tab');
      assert.equal(await page.locator(':focus').textContent(), 'Skip to content');
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash, '#main');
      const detail = page.locator('details').first();
      await detail.locator('summary').click();
      assert.equal(await detail.getAttribute('open'), null);
      await detail.locator('summary').focus();
      await page.keyboard.press('Enter');
      assert.notEqual(await detail.getAttribute('open'), null);
      await page.emulateMedia({reducedMotion: 'reduce'});
      assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior), 'auto');
      for (const path of ['experiment-001.md', 'maker-profit-calculator.html']) {
        assert.equal((await page.request.get(new URL(path, base).href)).status(), 200);
      }
      assert.deepEqual(errors, []);
      assert.deepEqual(failures, []);
      assert(requests.every(u => new URL(u).origin === new URL(base).origin || u.startsWith('data:')));
      await page.locator('a.button[href="maker-profit-calculator.html"]').click();
      await page.waitForURL('**/maker-profit-calculator.html');
      assert.equal(await page.locator('#profit').textContent(), '£10.01');
      await context.close();
      console.log(`PASS ${width}px: layout, anchors, keyboard, details, reduced motion, links, calculator and homepage errors/network`);
    }
    const context = await browser.newContext({javaScriptEnabled: false, viewport: {width: 390, height: 844}});
    const page = await context.newPage();
    await page.goto(base);
    await page.locator('nav a[href="#inventions"]').click();
    assert.equal(new URL(page.url()).hash, '#inventions');
    await context.close();
    console.log('PASS navigation with JavaScript disabled');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
