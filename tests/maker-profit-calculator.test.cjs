// Run with Node 18+: node --test tests/maker-profit-calculator.test.cjs
// No packages required. Execute the model from the HTML, not a duplicate formula.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(require('node:path').join(__dirname,'../maker-profit-calculator.html'),'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const context = vm.createContext({Intl});
vm.runInContext(script.slice(0,script.indexOf('for (const id of numericIds) {\n  const field')) + '\nthis.model = {compute,validateValue,roundPriceUp,defaults};',context);
const {compute,validateValue,roundPriceUp,defaults} = context.model;
const run = (values={}) => compute({...defaults,...values});
const close = (actual,expected) => assert.ok(Math.abs(actual-expected)<1e-8,`${actual} != ${expected}`);
const zero = Object.fromEntries(Object.keys(defaults).filter(k=>k!=='product').map(k=>[k,0]));
test('example, independently calculated',()=>{
 const r=run(); close(r.costs,7.2); close(r.labour,125/24); close(r.fees,2.57405);
 close(r.total,14.9823833333333); close(r.profit,10.0076166666667);
 close(r.prelabour,15.21595); close(r.margin,40.04648526077098);
 assert.equal(r.breakeven,13.94); assert.equal(r.target,17.89);
});
test('direct sale, fractional minutes and labour',()=>{
 const r=run({...zero,price:30,materials:2,packaging:1,other:3,overheads:4,minutes:1.5,hourly:20});
 assert.equal(r.labour,.5); assert.equal(r.total,10.5); assert.equal(r.profit,19.5);
 assert.equal(r.margin,65); assert.equal(r.breakeven,10.5); assert.equal(r.target,13.13);
});
test('fees are additive on selling price plus fixed fee',()=>{
 const r=run({...zero,price:100,platform:10,processing:5,fixed:2});
 assert.equal(r.fees,17); assert.equal(r.profit,83); assert.equal(r.breakeven,2.36);
});
test('zero selling price and loss',()=>{
 const r=run({price:0}); assert.equal(r.margin,null); close(r.profit,-(7.2+125/24+.2));
 assert.ok(run({price:1}).profit<0);
});
test('percentage fee boundaries with positive costs',()=>{
 for (const rate of [79.9,80,80.1,99.9,100,150,200]) {
  const r=run({...zero,materials:1,platform:Math.min(rate,100),processing:Math.max(0,rate-100)});
  assert.equal(r.target===null,rate>=80); assert.equal(r.breakeven===null,rate>=100);
 }
});
test('zero costs, zero revenue and exact 80% / 100% boundaries',()=>{
 for (const platform of [0,79.9,80,80.1,100]) {
  const r=run({...zero,platform}); assert.equal(r.breakeven,0);
  assert.equal(r.target,platform<=80?.01:null);
 }
 assert.equal(run({...zero,platform:100,processing:100}).breakeven,0);
});
test('price recommendations round upward; exact pennies stay exact',()=>{
 assert.equal(roundPriceUp(1.001),1.01); assert.equal(roundPriceUp(.1+.2),.3);
 const r=run({...zero,materials:1,platform:10});
 assert.equal(r.breakeven,1.12); assert.equal(r.target,1.43);
 assert.ok(run({...zero,materials:1,platform:10,price:r.breakeven}).profit>=0);
});
test('validation rejects blank, negative, nonfinite and excessive values',()=>{
 for(const id of Object.keys(zero)) {
  for(const raw of ['', ' ', '-1','NaN','Infinity','1e309','abc',undefined,'1e-300']) assert.ok(validateValue(id,raw),`${id}: ${raw}`);
  assert.equal(validateValue(id,'0'),''); assert.equal(validateValue(id,'.25'),'');
  const max=['platform','processing'].includes(id)?100:1000000;
  assert.equal(validateValue(id,String(max)),''); assert.ok(validateValue(id,String(max+1)));
  assert.throws(()=>run({[id]:-1})); assert.throws(()=>run({[id]:Infinity}));
 }
});
test('large valid values remain finite',()=>{
 const r=run(Object.fromEntries(Object.keys(zero).map(k=>[k,['platform','processing'].includes(k)?99:1000000])));
 for(const [key,value] of Object.entries(r)) assert.ok(value===null||Number.isFinite(value),key);
});
test('deterministic sweep: recommended penny prices meet goals and previous penny fails',()=>{
 for(let i=1;i<=500;i++) {
  const n={...zero,materials:(i*17%499)/100,minutes:i%47,hourly:12.5,platform:(i*7%790)/10,processing:0,fixed:.2};
  const r=run(n);
  const at=run({...n,price:r.breakeven}); assert.ok(at.profit>=-1e-10);
  assert.ok(run({...n,price:r.breakeven-.01}).profit<1e-10);
  const target=run({...n,price:r.target}); assert.ok(target.margin>=20-1e-9);
  const previous=run({...n,price:r.target-.01}); assert.ok(previous.margin<20+1e-9);
 }
});
