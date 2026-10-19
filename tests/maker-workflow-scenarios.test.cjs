// Run: node --test tests/maker-workflow-scenarios.test.cjs
// Execute the real shipped calculator's compute function; scenarios are synthetic.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(require('node:path').join(__dirname,'../maker-profit-calculator.html'),'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({Intl});
vm.runInContext(script.slice(0,script.indexOf('for (const id of numericIds) {\n  const field')) + '\nthis.model={compute,defaults};',context);
const {compute,defaults} = context.model;
const run = (n) => compute({...defaults,product:'Synthetic test',price:0,materials:0,packaging:0,other:0,overheads:0,minutes:0,hourly:0,platform:0,processing:0,fixed:0,...n});
const close = (actual,expected) => assert.ok(Math.abs(actual-expected)<1e-8,actual+' != '+expected);

test('W01 bookmark: postage revenue and cost explicitly included',()=>{
  const r=run({price:10.5,materials:1.2,packaging:.35,other:1.8,minutes:12,hourly:12});
  close(r.labour,2.4);close(r.costs,3.35);close(r.profit,4.75);close(r.margin,4.75/10.5*100);
});

test('W02 batch: manually allocate setup, wastage and inputs over 18 saleable units',()=>{
  const unitMaterial=(12+6)/18;
  const unitMinutes=(90+20*5)/18;
  const r=run({price:10,materials:unitMaterial,minutes:unitMinutes,hourly:12});
  close(r.costs,1);close(r.labour,190/18/60*12);close(r.profit,10-1-190/18/60*12);
  // Current UI does not allocate batch quantities or wastage automatically.
});

test('W03 marketplace: model computes editable fees but not multiple fee bases',()=>{
  const r=run({price:21,materials:4.25,other:2.6,minutes:20,hourly:12,platform:6.5,processing:3,fixed:.2});
  close(r.fees,21*.095+.2);close(r.labour,4);
  close(r.profit,21-4.25-2.6-4-(21*.095+.2));
  // These percentages are synthetic inputs, NOT verified Etsy rates.
});

test('W04 wholesale and direct: distinct manually configured channels',()=>{
  const common={materials:3,packaging:.5,minutes:25,hourly:12};
  const wholesale=run({...common,price:12});
  const direct=run({...common,price:21});
  close(wholesale.profit,3.5);close(direct.profit,12.5);
  // There is no side-by-side comparison UI.
});

test('W05 VAT uncertainty: no tax computation or VAT status question',()=>{
  const r=run({price:25});
  close(r.profit,25);
  // This output is intentionally pre-tax and must not be presented as post-tax.
});

test('W06 material cost sensitivity: £1.20 increase reduces per-item profit by £1.20',()=>{
  const original=run({price:10,materials:2.4});
  const increased=run({price:10,materials:3.6});
  close(original.profit-increased.profit,1.2);
  // User must manually change input; no built-in history/comparison.
});
