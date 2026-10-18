const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
 const base=process.env.BASE_URL||'http://127.0.0.1:8000/';
 const paths=['index.html','experiments.html','inventions.html','mission.html','prometheus/index.html','maker-profit-calculator.html'];
 try{
 for(const width of [320,390,768,1440]){
 const context=await browser.newContext({viewport:{width,height:900},isMobile:width<500,hasTouch:width<500,reducedMotion:'reduce'});
 const page=await context.newPage();let errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const path of paths){
 assert.equal((await page.goto(base+path)).status(),200);
 assert.equal(await page.locator('h1').count(),1);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${path} ${width}`);
 assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
 await page.keyboard.press('Tab');assert.equal((await page.locator(':focus').textContent()).trim(),'Skip to content');
 await page.keyboard.press('Enter');assert.equal(new URL(page.url()).hash,'#main');
 if(width<761){const summary=page.locator('.navigation summary');await summary.focus();await page.keyboard.press('Enter');assert(await page.locator('.navigation nav').isVisible());for(const a of await page.locator('.navigation nav a').all()){const box=await a.boundingBox();assert(box.height>=44)}await page.keyboard.press('Enter');assert(!(await page.locator('.navigation nav').isVisible()));}
 for(const a of await page.locator('a[href]').all()){
 const url=new URL(await a.getAttribute('href'),page.url());if(url.origin!==new URL(base).origin)continue;
 const res=await page.request.get(url.href);assert.equal(res.status(),200,url.href);
 if(url.pathname===new URL(page.url()).pathname&&url.hash)assert(await page.locator(url.hash).count(),url.hash);
 }
 const top=page.locator('a[href="#top"]').last();await top.click();assert.equal(new URL(page.url()).hash,'#top');assert(await page.evaluate(()=>scrollY<5));
 if((width===390||width===1440)&&path!=='maker-profit-calculator.html')await page.screenshot({path:`work/mission004-${path.replace('/index','').replace('.html','')}-${width}.png`,fullPage:true});
 }
 // Follow every major destination using the actual visible navigation.
 for(const path of paths.slice(0,5)){
 if(width<761)await page.locator('.navigation summary').click();
 await page.locator((width<761?'.navigation nav':'.desktop-nav')+` a[href="${path}"]`).click();
 assert(new URL(page.url()).pathname.endsWith('/'+path));
 }
 assert.deepEqual(errors,[]);await context.close();console.log(`PASS ${width}px: six pages, links, no overflow, menu keyboard/touch targets, skip links, top controls, reduced motion and page navigation`);
 }
 const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});const page=await context.newPage();
 await page.goto(base);await page.locator('.navigation summary').click();await page.locator('.navigation nav a[href="experiments.html"]').click();assert(new URL(page.url()).pathname.endsWith('/experiments.html'));await context.close();console.log('PASS navigation without JavaScript');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
