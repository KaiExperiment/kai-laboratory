// AI-authored synthetic browser-DOM regression test for experimental Evidence Engine.
// Run from repository root: node --test tests/evidence-engine-local-date.test.cjs
'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'evidence-engine.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'Evidence Engine embedded script must exist');

function runScenario({ instant, timeZone }) {
  const nodes = new Map();
  class Element {
    constructor(tag) {
      this.tagName = tag; this.children = []; this.events = {};
      this.dataset = {}; this.textContent = ''; this.value = '';
    }
    set id(id) { this._id = id; nodes.set(id, this); }
    get id() { return this._id; }
    append(...children) { this.children.push(...children); }
    appendChild(child) { this.children.push(child); }
    replaceChildren(...children) { this.children = children; }
    addEventListener(event, callback) { this.events[event] = callback; }
    click() { this.events.click?.(); }
    trigger(event) { this.events[event]?.(); }
  }
  const document = {
    createElement: tag => new Element(tag),
    getElementById: id => nodes.get(id)
  };
  for (const id of ['entries', 'results', 'summary', 'add', 'demo', 'export', 'export-json', 'clear']) {
    const node = new Element('root'); node.id = id;
  }
  const localParts = timestamp => Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', {
      timeZone, year: 'numeric', month: '2-digit', day: '2-digit'
    }).formatToParts(new Date(timestamp))
      .filter(part => ['year', 'month', 'day'].includes(part.type))
      .map(part => [part.type, Number(part.value)])
  );
  class Clock extends Date {
    constructor(...args) { super(...(args.length ? args : [instant])); }
    getFullYear() { return localParts(this.getTime()).year; }
    getMonth() { return localParts(this.getTime()).month - 1; }
    getDate() { return localParts(this.getTime()).day; }
  }
  vm.runInNewContext(script, {
    document, Date: Clock, URL, confirm: () => true,
    Blob: class {}, setTimeout: () => {}
  }, { timeout: 1000 });
  nodes.get('demo').click();
  const demoDate = nodes.get('field-0-date').value;
  const isDateInvalid = date => {
    const input = nodes.get('field-0-date');
    input.value = date;
    input.trigger('input');
    const row = nodes.get('results').children[0];
    return row.children[3].textContent.includes('ERROR: Missing/invalid date');
  };
  return { demoDate, isDateInvalid };
}

const cases = [
  ['UK summer midnight', '2026-10-22T23:30:00Z', 'Europe/London', '2026-10-23', '2026-10-24'],
  ['Los Angeles before midnight', '2026-10-23T06:30:00Z', 'America/Los_Angeles', '2026-10-22', '2026-10-23'],
  ['Kathmandu fractional offset', '2026-10-22T19:00:00Z', 'Asia/Kathmandu', '2026-10-23', '2026-10-24'],
  ['Kiritimati UTC+14', '2026-10-22T12:30:00Z', 'Pacific/Kiritimati', '2026-10-23', '2026-10-24'],
  ['Honolulu UTC-10', '2026-10-23T05:30:00Z', 'Pacific/Honolulu', '2026-10-22', '2026-10-23'],
  ['UK DST before fall-back', '2026-10-25T00:30:00Z', 'Europe/London', '2026-10-25', '2026-10-26'],
  ['UK DST after fall-back', '2026-10-25T01:30:00Z', 'Europe/London', '2026-10-25', '2026-10-26'],
  ['UTC midday control', '2026-10-23T12:00:00Z', 'UTC', '2026-10-23', '2026-10-24'],
  ['Auckland leap-day boundary', '2028-02-28T11:30:00Z', 'Pacific/Auckland', '2028-02-29', '2028-03-01']
];

for (const [name, instant, timeZone, today, tomorrow] of cases) {
  test(name + ': demo and validation respect local calendar date', () => {
    const result = runScenario({ instant, timeZone });
    assert.equal(result.demoDate, today, 'Demo must use local date');
    assert.equal(result.isDateInvalid(today), false, 'Current local date must be valid');
    assert.equal(result.isDateInvalid(tomorrow), true, 'Future local date must be invalid');
  });
}
