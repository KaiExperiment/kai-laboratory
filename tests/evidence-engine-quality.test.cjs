// Run: node --test tests/evidence-engine-quality.test.cjs
// Extract the real validation and assessment functions from the shipped HTML.
// No external packages required. These tests do not replace real browser testing.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync('evidence-engine.html','utf8');
const start=html.indexOf('const validate=x=>');
const end=html.indexOf('function update(){',start);
assert.ok(start>0&&end>start,'Validation functions present');
const source=html.slice(start,end);
const context=vm.createContext({URL,Date,Number,String});
const {validate,assess}=vm.runInContext(source+';({validate,assess})',context);
const base=()=>({seller:'Sample seller',product:'Maple bookmark',url:'https://shop.example.co.uk/item',price:'5.00',date:'2026-10-20',vat:'included',shipping:'£2.50',material:'3 mm maple',evidence:'Manually checked for QA',review:'checked'});
test('complete inputs pass field validation',()=>{const a=assess(base());assert.equal(a.errors.length,0);assert.equal(a.warnings.length,0)});
test('five pounds is a valid price',()=>assert.ok(!validate(base()).includes('Invalid GBP price')));
test('invalid price and future date fail',()=>{const a=validate({...base(),price:'five',date:'2099-01-01'});assert.ok(a.includes('Invalid GBP price'));assert.ok(a.includes('Missing/invalid date'))});
test('missing core fields are invalid',()=>{const a=assess({...base(),seller:'',url:'oops',material:''});assert.equal(a.status,'Invalid')});
test('uncertain commercial details are flagged',()=>{for(const shipping of ['Not stated','unknown','TBC','N/A','not specified']){const a=assess({...base(),shipping,vat:'unknown',review:'unchecked'});assert.equal(a.status,'Uncertain');assert.ok(a.warnings.includes('Shipping charge unknown'))}});
test('example domains are flagged, not similarly named hosts',()=>{assert.ok(assess({...base(),url:'https://sub.example.org/item'}).warnings.some(x=>x.includes('Demonstration')));assert.ok(!assess({...base(),url:'https://notexample.com/item'}).warnings.some(x=>x.includes('Demonstration')))});
