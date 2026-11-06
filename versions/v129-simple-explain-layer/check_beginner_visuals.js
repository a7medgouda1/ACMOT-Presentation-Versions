/* Structural and asset check for the added beginner visual slides. */
'use strict';
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const path = require('path');
const dir = __dirname;
const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
assert(html.includes('<script src="diagrams.js"></script>\n<script src="beginner_visuals.js"></script>\n<script src="assets/results/manifest.js"></script>\n<script src="result_bars.js"></script>\n<script src="script.js"></script>'));
const staticSlides = [...html.matchAll(/<[a-z][^>]*\bclass="([^"]*)"/g)]
  .filter(x => x[1].split(/\s+/).includes('slide')).length;
assert.strictEqual(staticSlides, 188);
const source = [];
const re = /<section\s+class="slide"\s+data-sec="(11|12)"[^>]*data-title="([^"]+)"/g;
let m;
while ((m = re.exec(html))) source.push({sec: m[1], title: m[2]});
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
    const i = before ? all.indexOf(before) : all.length;
    assert(i >= 0);
    all.splice(i, 0, slide);
  }
};
source.forEach(x => all.push(element(x.sec, x.title)));
const window = {};
const document = {getElementById(id) { return id === 'stage' ? stage : null; },
  createElement() { return element('', ''); }};
for (const filename of ['diagrams.js', 'beginner_visuals.js']) {
  vm.runInNewContext(fs.readFileSync(path.join(dir, filename), 'utf8'),
    {window, document, Error});
}
const diagrams = all.filter(x => x.className === 'slide diagram-slide');
const visuals = all.filter(x => x.className === 'slide beginner-slide');
assert.strictEqual(diagrams.length, 26);
assert.strictEqual(visuals.length, 35);
assert.strictEqual(visuals.length, window.ACMOT_BEGINNER_VISUAL_COUNT);
assert.strictEqual(all.length, source.length + 26 + 35);
assert.strictEqual(new Set(visuals.map(x => x.getAttribute('data-title'))).size, visuals.length);
for (const slide of visuals) {
  assert(slide.innerHTML.includes('Simple idea'));
  assert(slide.innerHTML.includes('Easy example'));
  assert(slide.innerHTML.includes('beginner-source'));
  assert(slide.getAttribute('data-origin'));
  assert(!/NaN|undefined/.test(slide.innerHTML));
  assert(['11', '12'].includes(slide.getAttribute('data-sec')));
  const parent = all.find(x => x.getAttribute('data-title') === slide.getAttribute('data-parent'));
  assert(parent, 'Missing teaching parent for ' + slide.getAttribute('data-title'));
  assert(all.indexOf(slide) < all.indexOf(parent), 'Beginner visual must come first');
  for (const between of all.slice(all.indexOf(slide) + 1, all.indexOf(parent))) {
    assert(between.className === 'slide beginner-slide' &&
           between.getAttribute('data-parent') === slide.getAttribute('data-parent'),
           'A different topic interrupts ' + slide.getAttribute('data-title'));
  }
  const assets = [...slide.innerHTML.matchAll(/(?:src|data-src)="(assets\/[^"]+)"/g)];
  assert(assets.length);
  for (const a of assets) assert(fs.existsSync(path.join(dir, a[1])), 'Missing ' + a[1]);
}
const fig1 = visuals.find(x => x.getAttribute('data-title') === 'A simple scale for LOW, MEDIUM, HIGH');
const diagram1 = diagrams.find(x => x.getAttribute('data-title') === 'Paper 1 — target-state decision');
const teach1 = all.find(x => x.getAttribute('data-title') === 'Paper 1 target state');
assert(all.indexOf(fig1) < all.indexOf(teach1));
assert(all.indexOf(teach1) < all.indexOf(diagram1));
const fig2 = visuals.find(x => x.getAttribute('data-title') === 'Three groups from the last 10 frames');
const diagram2 = diagrams.find(x => x.getAttribute('data-title') === 'Paper 2 — thresholds come from earlier frames');
const teach2 = all.find(x => x.getAttribute('data-title') === 'Paper 2 nested Otsu');
assert(all.indexOf(fig2) < all.indexOf(teach2));
assert(all.indexOf(teach2) < all.indexOf(diagram2));
console.log('OK: 188 original + 26 accurate diagrams + 35 beginner visuals = 249 slides.');
console.log('OK: every new visual has its asset, source cue, simple point and example.');
