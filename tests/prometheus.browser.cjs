// Optional development-only checks against a locally served checkout.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
(async () => {
  const base = process.env.BASE_URL || 'http://127.0.0.1:8000/';
  const summary = JSON.parse(fs.readFileSync(path.join(__dirname, '../prometheus/results/ignition-001/summary.json')));
  const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined, args:['--no-sandbox']});
  try {
    for (const width of [320,375,390,430,768,1024,1440]) {
      const context = await browser.newContext({viewport:{width,height:900},isMobile:width<500,hasTouch:width<500,javaScriptEnabled:false,reducedMotion:'reduce'});
      const page = await context.newPage();
      const errors=[], external=[];
      page.on('pageerror',e=>errors.push(e.message));
      page.on('request',r=>{if(!r.url().startsWith(base)&&!r.url().startsWith('data:')) external.push(r.url());});
      assert.equal((await page.goto(new URL('prometheus/',base).href)).status(),200);
      assert.equal(await page.locator('h1').count(),1);
      assert.equal(await page.locator('script').count(),0);
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`horizontal overflow ${width}`);
      assert.equal(await page.locator('html').getAttribute('lang'),'en-GB');
      assert((await page.locator('.metric').first().textContent()).includes(summary.validation.mean_percent_reduction.toFixed(2)+'%'));
      await page.keyboard.press('Tab');
      assert.equal(await page.locator(':focus').textContent(),'Skip to content');
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash,'#main');
      for(const a of await page.locator('a[href^="#"]').all()) assert.equal(await page.locator(await a.getAttribute('href')).count(),1);
      for(const a of await page.locator('a').all()) {
        const url=new URL(await a.getAttribute('href'),page.url());
        if(url.origin===new URL(base).origin && !url.hash) assert.equal((await page.request.get(url.href)).status(),200,url.href);
      }
      assert.equal(await page.locator('table caption').count(),1);
      for(const th of await page.locator('th').all()) assert(['row','col'].includes(await th.getAttribute('scope')));
      assert.equal(await page.locator('svg[role="img"][aria-label]').count(),2);
      await page.emulateMedia({reducedMotion:'reduce'});
      assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
      if(width===390||width===1440) await page.screenshot({path:`work/prometheus-${width}.png`,fullPage:true});
      if(width<761)await page.locator('.navigation summary').click();
      await page.locator((width<761?'.navigation nav':'.desktop-nav')+' a[href="../index.html"]').click();
      if(width<761)await page.locator('.navigation summary').click();
      await page.locator((width<761?'.navigation nav':'.desktop-nav')+' a[href="prometheus/index.html"]').click();
      assert(new URL(page.url()).pathname.endsWith('/prometheus/index.html'));
      assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
      await context.close();
      console.log(`PASS ${width}px: overflow, evidence links, measured copy, keyboard, table semantics, labelled plots, reduced motion and HQ round trip; JS disabled`);
    }
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
