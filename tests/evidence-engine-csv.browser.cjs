// AI-authored experimental browser regression for Evidence Engine CSV/JSON export.
// Tests the exported bytes and CSV structure, NOT execution in spreadsheet software.
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const appPath = path.join(__dirname, '..', 'evidence-engine.html');
const html = fs.readFileSync(appPath, 'utf8');
const css = fs.readFileSync(path.join(__dirname, '..', 'assets', 'laboratory.css'), 'utf8');
const tests = [
 ['equals','=1+1',true,'product'],['plus','+1+1',true,'product'],
 ['minus','-1+1',true,'product'],['at','@SUM(1,1)',true,'product'],
 ['leading space','  =1+1',true,'product'],['leading newline','\n=1+1',true,'evidence'],
 ['leading tab','\t=1+1',true,'evidence'],['fullwidth equals','＝１＋１',true,'product'],
 ['zero width','\u200b=1+1',true,'product'],['embedded comma and quote','=1,"quoted"',true,'product'],
 ['normal text','Nice wooden box',false,'product'],
 ['normal multiline','A,B "quoted"\nSecond line',false,'evidence'],
 ['negative-looking text','-12.50',true,'product'],
 ['normal URL','https://example.com/product',false,'product']
];
function parseCsv(input){
 const rows=[];let row=[],cell='',inQuotes=false;
 for(let i=0;i<input.length;i++){
  const ch=input[i];
  if(inQuotes){
   if(ch==='"'&&input[i+1]==='"'){cell+='"';i++;}
   else if(ch==='"')inQuotes=false;
   else cell+=ch;
  }else if(ch==='"'){inQuotes=true;}
  else if(ch===','){row.push(cell);cell='';}
  else if(ch==='\n'){row.push(cell.replace(/\r$/,''));rows.push(row);row=[];cell='';}
  else cell+=ch;
 }
 assert.equal(inQuotes,false,'CSV quoted field must close');
 row.push(cell.replace(/\r$/,''));rows.push(row);
 return rows;
}
(async()=>{
 const server=http.createServer((req,res)=>{
  const pathname=new URL(req.url,'http://127.0.0.1').pathname;
  if(pathname==='/evidence-engine.html'){res.writeHead(200,{'Content-Type':'text/html; charset=utf-8'});res.end(html);}
  else if(pathname==='/assets/laboratory.css'){res.writeHead(200,{'Content-Type':'text/css; charset=utf-8'});res.end(css);}
  else{res.writeHead(404);res.end('Not found');}
 });
 await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
 let browser;let passed=0;
 try{
  browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,headless:true,args:['--no-sandbox']});
  const context=await browser.newContext({acceptDownloads:true});
  const page=await context.newPage();const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const response=await page.goto('http://127.0.0.1:'+server.address().port+'/evidence-engine.html',{waitUntil:'load'});
  assert.equal(response.status(),200);
  assert.equal(await page.locator('#export-json').count(),1,'lossless JSON export exists');
  for(const [name,value,guard,field] of tests){
   await page.locator('#field-0-'+field).fill(value);
   const csvPromise=page.waitForEvent('download');await page.locator('#export').click();
   const csvDownload=await csvPromise;
   assert.equal(csvDownload.suggestedFilename(),'evidence-engine-comparables.csv');
   const csv=fs.readFileSync(await csvDownload.path(),'utf8').replace(/^\uFEFF/,'');
   const rows=parseCsv(csv);
   assert.equal(rows.length,2,name+' two rows');
   assert.equal(rows[0].length,11,name+' headers');
   assert.equal(rows[1].length,11,name+' data columns');
   const actual=rows[1][rows[0].indexOf(field)];
   assert.equal(actual,(guard?'\t':'')+value,name+' CSV guard');
   const jsonPromise=page.waitForEvent('download');await page.locator('#export-json').click();
   const jsonDownload=await jsonPromise;
   assert.equal(jsonDownload.suggestedFilename(),'evidence-engine-comparables.json');
   const data=JSON.parse(fs.readFileSync(await jsonDownload.path(),'utf8'));
   assert.equal(data.comparables[0][field],value,name+' JSON lossless');
   passed++;console.log('PASS export scenario:',name);
  }
  assert.deepEqual(errors,[],'No page JavaScript errors');
  await context.close();
  console.log('PASS '+passed+'/'+tests.length+' export scenarios (Chromium; no spreadsheet execution tested)');
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error('FAIL',e.stack||e);process.exitCode=1;});
