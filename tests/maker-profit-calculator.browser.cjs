// Optional browser checks: requires a developer-installed Playwright and Chromium.
// CHROMIUM_PATH=/usr/bin/chromium node tests/maker-profit-calculator.browser.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || undefined,headless:true,args:['--no-sandbox']});
 let checks=0;
 try {
  for (const width of [320,375,390,430,768,1280]) {
   const context=await browser.newContext({viewport:{width,height:844},isMobile:width<500,hasTouch:width<500,deviceScaleFactor:width<500?3:1});
   const page=await context.newPage(); const errors=[]; const external=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('request',r=>{if(/^https?:/.test(r.url())) external.push(r.url());});
   await page.setContent(fs.readFileSync(path.join(__dirname,'../maker-profit-calculator.html'),'utf8'));
   assert.equal(await page.locator('#profit').textContent(),'£10.01');
   assert.equal(await page.locator('#fees').textContent(),'£2.57');
   assert.equal(await page.locator('#breakeven').textContent(),'£13.94');
   assert.equal(await page.locator('#target').textContent(),'£17.89');
   const layout=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,fields:[...document.querySelectorAll('input')].map(e=>({font:parseFloat(getComputedStyle(e).fontSize),height:e.getBoundingClientRect().height}))}));
   assert.equal(layout.overflow,false,`overflow at ${width}`);
   assert.ok(layout.fields.every(f=>f.font>=16&&f.height>=44));
   await page.locator('#materials').fill('');
   assert.equal(await page.locator('#materials').getAttribute('aria-invalid'),'true');
   assert.match(await page.locator('#materials-error').textContent(),/Enter a number/);
   assert.equal(await page.locator('#profit').textContent(),'—');
   await page.locator('#materials').fill('-1');
   assert.match(await page.locator('#materials-error').textContent(),/0 to 1,000,000/);
   await page.locator('#materials').fill('1000001');
   assert.equal(await page.locator('#materials').getAttribute('aria-invalid'),'true');
   await page.locator('#reset').click();
   assert.equal(await page.locator('#materials').inputValue(),'4.5');
   assert.equal(await page.locator('#materials').getAttribute('aria-invalid'),'false');
   assert.equal(await page.locator('#materials-error').textContent(),'');
   await page.locator('#platform').fill('100');
   assert.equal(await page.locator('#breakeven').textContent(),'Not possible');
   assert.match(await page.locator('#warning').textContent(),/100%/);
   await page.locator('#platform').fill('101');
   assert.equal(await page.locator('#platform').getAttribute('aria-invalid'),'true');
   await page.locator('#reset').click();
   await page.locator('#price').fill('0');
   assert.equal(await page.locator('#margin').textContent(),'N/A (price is £0)');
   assert.match(await page.locator('#warning').textContent(),/does not cover/);
   await page.locator('#reset').focus(); await page.keyboard.press('Enter');
   assert.equal(await page.locator('#price').inputValue(),'24.99');
   await page.locator('#minutes').fill('1.5');
   assert.equal(await page.locator('#minutes').evaluate(e=>e.validity.valid),true);
   await page.locator('#product').fill('<img src=x onerror=alert(1)>');
   assert.equal(await page.locator('img').count(),0);
   await page.locator('#reset').click();
   assert.deepEqual(errors,[]); assert.deepEqual(external,[]);
   if(width===390 && process.env.SCREENSHOT_PATH) await page.screenshot({path:process.env.SCREENSHOT_PATH,fullPage:true});
   checks++; console.log(`PASS: ${width}px layout, inputs, results, reset, keyboard and no network requests`);
   await context.close();
  }
  const context=await browser.newContext({javaScriptEnabled:false});const page=await context.newPage();
  await page.setContent(fs.readFileSync(path.join(__dirname,'../maker-profit-calculator.html'),'utf8'));
  assert.equal(await page.locator('noscript').isVisible(),true);await context.close();
  console.log(`PASS: JavaScript-disabled explanation; ${checks} viewport scenarios passed`);
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
