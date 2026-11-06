/* Structural and rule-boundary checks for the v127 two-mode presentation. */
'use strict';
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const path = require('path');
const dir = __dirname;
const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
assert(html.includes('<link rel="stylesheet" href="interactions.css">'));
assert(html.includes('<link rel="stylesheet" href="polish.css">'));
assert(html.includes('<link rel="stylesheet" href="modes.css">'));
assert(html.includes('<link rel="stylesheet" href="result_bars.css">'));
assert(html.includes('data-mode="static"'));
assert(html.includes('data-mode="interactive"'));
assert(html.includes('<script src="script.js"></script>\n<script src="interactive_lab.js"></script>'));
assert(html.includes('<script src="assets/results/manifest.js"></script>\n<script src="result_bars.js"></script>\n<script src="script.js"></script>'));
const source = [];
const re = /<section\s+class="slide"\s+data-sec="(11|12)"[^>]*data-title="([^"]+)"/g;
let hit;
while ((hit = re.exec(html))) source.push({sec: hit[1], title: hit[2]});
const all = [];
function element(sec, title) {
  const attrs = {'data-sec': sec, 'data-title': title,
    'data-secname': sec === '11' ? 'XI · Paper 1: AC-MOT' : 'XII · Paper 2: SCL'};
  return {attrs, className: '', innerHTML: '', parentNode: stage,
    getAttribute(k) { return attrs[k]; }, setAttribute(k, v) { attrs[k] = v; },
    get nextSibling() { return all[all.indexOf(this) + 1] || null; }};
}
const stage = {
  querySelector(selector) {
    const title = selector.match(/data-title="([^"]+)"/);
    return title ? all.find(x => x.getAttribute('data-title') === title[1]) : null;
  },
  insertBefore(slide, before) {
    const at = before ? all.indexOf(before) : all.length;
    assert(at >= 0);
    all.splice(at, 0, slide);
  }
};
source.forEach(x => all.push(element(x.sec, x.title)));
const window = {};
const document = {getElementById(id) { return id === 'stage' ? stage : null; },
  createElement() { return element('', ''); }};
for (const name of ['diagrams.js', 'beginner_visuals.js']) {
  vm.runInNewContext(fs.readFileSync(path.join(dir, name), 'utf8'), {window, document, Error, Set, Array});
}
const beginners = all.filter(x => x.className === 'slide beginner-slide');
const diagrams = all.filter(x => x.className === 'slide diagram-slide');
assert.strictEqual(beginners.length, 35);
assert.strictEqual(diagrams.length, 26);
for (const slide of beginners) {
  assert(!slide.innerHTML.includes('stepbar'));
  assert(!slide.innerHTML.includes('step-play'));
  assert.strictEqual((slide.innerHTML.match(/class="frag"/g) || []).length, 2);
}
assert.strictEqual(beginners.filter(x => x.innerHTML.includes('class="lab-open"')).length, 4);
const flows = diagrams.filter(x => x.innerHTML.includes('diagram-build'));
const charts = diagrams.filter(x => x.innerHTML.includes('diagram-chart'));
assert(flows.length >= 18);
assert.strictEqual(charts.length, 5);
for (const slide of flows) {
  assert(!slide.innerHTML.includes('stepbar'));
  const steps = [...slide.innerHTML.matchAll(/data-build="(\d+)"/g)].map(x => +x[1]);
  assert(steps.includes(0), 'Flow must begin visibly');
  const max = Math.max(...steps);
  assert(max >= 2, 'Flow must reveal in at least three stages');
  for (let n = 0; n <= max; n++) assert(steps.includes(n), 'Missing build stage ' + n);
  assert(slide.innerHTML.includes('diagram-node'));
}
const engine = fs.readFileSync(path.join(dir, 'script.js'), 'utf8');
assert(engine.includes('function startAuto(s)'));
assert(engine.includes("presentationMode === 'static'"));
assert(engine.includes('function setMode(mode)'));
assert(engine.includes('k === 1 ? 80 : 340'));
assert(engine.includes('setTimeout(function ()'));
assert(engine.includes('function stopAuto()'));
assert(!engine.includes('togglePlay('));
assert(!engine.includes('step-play'));
assert(!engine.includes('Next step / next slide'));
const rules = require('./interactive_lab.js');
assert.strictEqual(rules.paper1Target(.297, .5), 'LOW');
assert.strictEqual(rules.paper1Target(.298, .5), 'MEDIUM');
assert.strictEqual(rules.paper1Target(.511, .5), 'MEDIUM');
assert.strictEqual(rules.paper1Target(.512, .5), 'HIGH');
assert.strictEqual(rules.paper1Target(.1, .501), 'HIGH');
assert.strictEqual(rules.scoreGate(.69, .70), false);
assert.strictEqual(rules.scoreGate(.70, .70), true);
assert.strictEqual(rules.paper2Mode(false, .9), 'COLD');
assert.strictEqual(rules.paper2Mode(true, .49), 'NOISY');
assert.strictEqual(rules.paper2Mode(true, .50), 'CLEAN');
assert(Math.abs(rules.scoreRemap('uncertain', .3) - .22) < 1e-12);
assert(Math.abs(rules.scoreRemap('confident', .8) - .9) < 1e-12);
console.log('OK: title-slide still and fast interactive modes; 35 figures, ' + flows.length + ' flowcharts, 5 charts, 4 optional teaching labs.');
console.log('OK: no on-slide play controls; slide navigation remains manual.');
console.log('OK: exact threshold boundaries and remap examples match the cited rules.');
