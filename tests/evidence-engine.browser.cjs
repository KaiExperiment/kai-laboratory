// AI-authored experimental browser regression checks for Evidence Engine 0.4.
// Run on a complete repository checkout: CHROMIUM_PATH=/usr/bin/chromium node tests/evidence-engine.browser.cjs
// Requires Playwright. Tests synthetic examples only; does not validate real seller listings.
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const appPath = process.env.EVIDENCE_HTML || path.join(__dirname, '..', 'evidence-engine.html');
const html = fs.readFileSync(appPath, 'utf8');
const cssPath = path.join(path.dirname(appPath), 'assets', 'laboratory.css');
assert.ok(fs.existsSync(cssPath), 'Full laboratory stylesheet must exist');
const scenarios = [
  ['UK summer midnight', '2026-10-22T23:30:00Z', 'Europe/London', '2026-10-23', '2026-10-24'],
  ['Los Angeles before midnight', '2026-10-23T06:30:00Z', 'America/Los_Angeles', '2026-10-22', '2026-10-23'],
  ['Kathmandu fractional offset', '2026-10-22T19:00:00Z', 'Asia/Kathmandu', '2026-10-23', '2026-10-24'],
  ['Kiritimati UTC+14', '2026-10-22T12:30:00Z', 'Pacific/Kiritimati', '2026-10-23', '2026-10-24'],
  ['Honolulu UTC-10', '2026-10-23T05:30:00Z', 'Pacific/Honolulu', '2026-10-22', '2026-10-23'],
  ['UK DST before fall-back', '2026-10-25T00:30:00Z', 'Europe/London', '2026-10-25', '2026-10-26'],
  ['UK DST after fall-back', '2026-10-25T01:30:00Z', 'Europe/London', '2026-10-25', '2026-10-26'],
  ['UTC midday control', '2026-10-23T12:00:00Z', 'UTC', '2026-10-23', '2026-10-24'],
  ['Auckland leap-day boundary', '2028-02-28T11:30:00Z', 'Pacific/Auckland', '2028-02-29', '2028-03-01'],
];
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || undefined,headless:true,args:['--no-sandbox']});
 let passes=0;
 try {
  for(const [name,instant,timeZone,today,tomorrow] of scenarios){
   const context=await browser.newContext({timezoneId:timeZone,viewport:{width:390,height:844},acceptDownloads:true});
   const page=await context.newPage();const errors=[];
   page.on('pageerror',e=>errors.push(e.message));page.on('dialog',dialog=>dialog.accept());
   await page.clock.install({time:new Date(instant)});
   await page.setContent(html);
   // setContent uses about:blank, so relative stylesheets are not fetched.
   // Inject the checked-out site's real CSS to include it in viewport checks.
   await page.addStyleTag({path:cssPath});
   assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--acid').trim()),'#cefa69','laboratory stylesheet applied');
   assert.equal(await page.locator('#field-0-date').count(),1,name+' initial input');
   await page.locator('#demo').click();
   const date=page.locator('#field-0-date');
   assert.equal(await date.inputValue(),today,name+' demo date');
   await date.fill(today);
   assert.doesNotMatch(await page.locator('#results tr').first().innerText(),/ERROR: Missing\/invalid date/,name+' today valid');
   await date.fill(tomorrow);
   assert.match(await page.locator('#results tr').first().innerText(),/ERROR: Missing\/invalid date/,name+' tomorrow invalid');
   assert.deepEqual(errors,[],name+' page errors');
   passes++;console.log('PASS date scenario:',name);
   await context.close();
  }
  for(const width of [320,390,768,1280]){
   const context=await browser.newContext({viewport:{width,height:850},acceptDownloads:true});
   const page=await context.newPage();const errors=[];
   page.on('pageerror',e=>errors.push(e.message));page.on('dialog',dialog=>dialog.accept());
   await page.setContent(html);
   // setContent uses about:blank, so relative stylesheets are not fetched.
   // Inject the checked-out site's real CSS to include it in viewport checks.
   await page.addStyleTag({path:cssPath});
   assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--acid').trim()),'#cefa69','laboratory stylesheet applied');
   assert.equal(await page.locator('#entries section').count(),1);
   await page.locator('#add').click();
   assert.equal(await page.locator('#entries section').count(),2);
   await page.getByRole('button',{name:'Remove comparable'}).last().click();
   assert.equal(await page.locator('#entries section').count(),1);
   await page.locator('#demo').click();
   assert.match(await page.locator('#summary').innerText(),/1 comparables/);
   await page.locator('#field-0-product').fill('<img src=x onerror=alert(1)>');
   assert.equal(await page.locator('img').count(),0,'user text not interpreted as HTML');
   const downloadPromise=page.waitForEvent('download');
   await page.locator('#export').click();
   const download=await downloadPromise;
   assert.equal(download.suggestedFilename(),'evidence-engine-comparables.csv');
   const file=await download.path();
   const csv=fs.readFileSync(file,'utf8');
   assert(csv.includes('quality_issues'));
   assert(csv.includes('<img src=x onerror=alert(1)>'));
   await page.locator('#clear').click();
   assert.equal(await page.locator('#entries section').count(),0);
   assert.deepEqual(errors,[],'page errors');
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
   assert.equal(overflow,false,'overflow at '+width);
   passes++;console.log('PASS interaction scenario:',width);
   await context.close();
  }
  console.log('PASS '+passes+'/'+(scenarios.length+4)+' browser scenarios');
 } finally {await browser.close();}
})().catch(e=>{console.error('FAIL',e.stack||e);process.exitCode=1;});
