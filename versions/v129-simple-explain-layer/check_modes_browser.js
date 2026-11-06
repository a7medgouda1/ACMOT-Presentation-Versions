/* End-to-end checks for the two title-slide viewing modes. Requires local Chrome. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawn} = require('node:child_process');

const chromePath = process.env.ACMOT_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'acmot-v129-browser-'));
const base = new URL('file://' + path.join(__dirname, 'index.html'));
const chrome = spawn(chromePath, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-background-networking',
  '--window-size=1600,900',
  '--no-first-run', '--remote-debugging-port=0', '--user-data-dir=' + profile,
  base.href + '#1'
], {stdio: 'ignore'});
let ws;
let serial = 0;
const pending = new Map();
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));

async function until(fn, label, timeout = 12000) {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const result = await fn();
    if (result) return result;
    await pause(60);
  }
  throw new Error('Timed out waiting for ' + label);
}
function send(method, params = {}) {
  const id = ++serial;
  return new Promise((resolve, reject) => {
    pending.set(id, {resolve, reject});
    ws.send(JSON.stringify({id, method, params}));
  });
}
async function evaluate(expression) {
  const response = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
  if (response.exceptionDetails) throw new Error(response.exceptionDetails.text);
  return response.result.value;
}
async function navigate(mode, slide) {
  const url = new URL(base.href);
  if (mode) url.searchParams.set('view', mode);
  url.hash = '#' + slide;
  await send('Page.navigate', {url: url.href});
  await until(async () => {
    try { return await evaluate(`location.href === ${JSON.stringify(url.href)}`); }
    catch { return false; }
  }, 'destination URL');
  await send('Page.reload', {ignoreCache: true});
  try {
    await until(async () => {
      try {
        return await evaluate(`document.readyState === 'complete' && location.hash === '#${slide}' &&
          document.querySelector('#stage .slide.active') === document.querySelectorAll('#stage .slide')[${slide - 1}]`);
      } catch { return false; }
    }, 'slide ' + slide);
  } catch (error) {
    const state = await evaluate(`({href:location.href,ready:document.readyState,
      active:[...document.querySelectorAll('#stage .slide')].findIndex(s=>s.classList.contains('active'))+1,
      count:document.querySelectorAll('#stage .slide').length,mode:window.ACMOT_VIEW_MODE})`);
    throw new Error(error.message + ': ' + JSON.stringify(state));
  }
}
async function run() {
  const portFile = path.join(profile, 'DevToolsActivePort');
  await until(() => fs.existsSync(portFile), 'Chrome debugging port');
  const port = fs.readFileSync(portFile, 'utf8').split('\n')[0];
  const pages = await (await fetch('http://127.0.0.1:' + port + '/json/list')).json();
  const page = pages.find(p => p.type === 'page');
  assert(page, 'Chrome did not open a page');
  ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve, {once: true});
    ws.addEventListener('error', reject, {once: true});
  });
  ws.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    if (!message.id || !pending.has(message.id)) return;
    const call = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) call.reject(new Error(message.error.message));
    else call.resolve(message.result);
  });
  await send('Runtime.enable');
  await send('Page.enable');
  await until(async () => await evaluate("document.readyState === 'complete' && !!document.querySelector('.mode-choice')"), 'title choice');
  const slideIds = await evaluate(`(() => {
    const slides = [...document.querySelectorAll('#stage .slide')];
    return {
      beginner: slides.findIndex(s => s.classList.contains('beginner-slide')) + 1,
      lab: slides.findIndex(s => s.querySelector('.lab-open')) + 1,
      diagram: slides.findIndex(s => s.classList.contains('diagram-slide') && s.querySelector('.diagram-build')) + 1,
      chart: slides.findIndex(s => s.querySelector('[data-chart]')) + 1,
      video: slides.findIndex(s => s.querySelector('video[data-autoplay]')) + 1,
      paper1Bars: slides.findIndex(s => s.getAttribute('data-chart-id') === 'p1-vis-bt-quality') + 1,
      negativeBars: slides.findIndex(s => s.getAttribute('data-chart-id') === 'p1-uav-bt-quality') + 1,
      paper2Bars: slides.findIndex(s => s.getAttribute('data-chart-id') === 'p2-kitti-bt') + 1,
      zeroBars: slides.findIndex(s => s.getAttribute('data-chart-id') === 'p2-score-shift') + 1
    };
  })()`);
  assert(Object.values(slideIds).every(x => x > 0), JSON.stringify(slideIds));
  assert.equal(await evaluate('window.ACMOT_RESULT_BAR_COUNT'), 27);
  assert.equal(await evaluate("document.querySelectorAll('#stage .slide').length"), 276);
  assert.equal(await evaluate('window.ACMOT_SIMPLE_GUIDE_COUNT'), 276);
  assert(await evaluate('window.ACMOT_DETAIL_GUIDE_COUNT > 40'), 'All optional detail pages need a reading aid');
  const guideGaps = await evaluate(`window.ACMOT_SIMPLE_GUIDE.map((g,i) => ({i:i+1, empty:!g.simple||!g.story}))
    .filter(x => x.empty)`);
  assert.deepEqual(guideGaps, [], 'Every slide needs a plain-English line and a place in the story');
  const guideFallbacks = await evaluate(`window.ACMOT_SIMPLE_GUIDE.map((g,i) => ({i:i+1, fallback:g.simple.startsWith('This slide is part of the story')}))
    .filter(x => x.fallback)`);
  assert.deepEqual(guideFallbacks, [], 'Every guide must use authored slide or speaker-note text');
  const detailGaps = await evaluate(`window.ACMOT_DETAIL_GUIDES.map((g,i) => ({i:i+1,
    empty:!g.simple||!g.story, fallback:g.simple.startsWith('This slide is part of the story')}))
    .filter(x => x.empty || x.fallback)`);
  assert.deepEqual(detailGaps, [], 'Every optional detail page must reuse its authored explanation');
  if (process.env.ACMOT_QA_GUIDES) {
    const longest = await evaluate(`window.ACMOT_SIMPLE_GUIDE.map((g,i) => ({slide:i+1,words:g.simple.trim().split(' ').length,text:g.simple}))
      .sort((a,b) => b.words-a.words).slice(0,12)`);
    console.log('Longest guide openings:', JSON.stringify(longest));
  }
  if (process.env.ACMOT_QA_TITLE_SCREENSHOT) {
    const shot = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync(process.env.ACMOT_QA_TITLE_SCREENSHOT, Buffer.from(shot.data, 'base64'));
  }
  const imageCheck = await evaluate(`Promise.all(window.ACMOT_RESULT_BARS.map(spec => new Promise(resolve => {
    const image = new Image();
    image.onload = () => resolve({id: spec.id, ok: image.naturalWidth > 0});
    image.onerror = () => resolve({id: spec.id, ok: false});
    image.src = spec.image;
  })))`);
  assert.equal(imageCheck.length, 27);
  assert.deepEqual(imageCheck.filter(x => !x.ok), [], 'Every result chart asset must load');

  await evaluate("document.querySelector('[data-mode=static]').click()");
  await until(async () => await evaluate("window.ACMOT_VIEW_MODE === 'static' && location.search.includes('view=static') && location.hash === '#2'"), 'still-view button');
  await navigate('static', slideIds.beginner);
  assert(await evaluate(`(() => {const s=document.querySelector('#stage .slide.active');return s.querySelectorAll('.frag').length>0 &&
    [...s.querySelectorAll('.frag')].every(f=>f.classList.contains('on') && f.getAttribute('aria-hidden')==='false') &&
    getComputedStyle(s.querySelector('.frag')).transitionDuration==='0s'})()`), 'Still view must show every figure part instantly');
  await navigate('static', slideIds.lab);
  await evaluate("document.querySelector('#stage .slide.active .lab-open').click()");
  assert.equal(await evaluate("!!document.querySelector('.interactive-lab.open')"), false, 'Still view must not open teaching labs');
  await navigate('static', slideIds.diagram);
  assert(await evaluate(`(() => {const s=document.querySelector('#stage .slide.active');return [...s.querySelectorAll('.frag')].every(f=>f.classList.contains('on'))})()`), 'Still view must show the full flowchart');
  await navigate('static', slideIds.chart);
  assert(await evaluate("!!document.querySelector('#stage .slide.active [data-chart].play')"), 'Still view must show full charts');
  assert.equal(await evaluate("document.querySelectorAll('#stage .slide.active .chart-missing').length"), 0, 'Chart must render without errors');
  await navigate('static', slideIds.video);
  assert(await evaluate("[...document.querySelectorAll('#stage .slide.active video')].every(v=>v.paused)"), 'Still view must not autoplay video');
  for (const id of [slideIds.paper1Bars, slideIds.negativeBars, slideIds.paper2Bars, slideIds.zeroBars]) {
    await navigate('static', id);
    await until(async () => await evaluate("!!document.querySelector('#stage .slide.active .result-chart-image')?.naturalWidth"), 'result chart image');
    assert(await evaluate(`(() => {const s=document.querySelector('#stage .slide.active');const b=s.querySelector('.s-body').getBoundingClientRect();
      const r=s.querySelector('.result-chart-image').getBoundingClientRect();return r.left>=b.left-2 && r.right<=b.right+2 && r.top>=b.top-2 && r.bottom<=b.bottom+2})()`), 'Result chart must fit the slide body');
  }
  await evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'e',bubbles:true}))");
  assert(await evaluate("document.querySelector('.explain.open .ex-simple')?.textContent.includes('Changing score values')"),
    'The still view should offer a plain-English reading aid without running an activity');
  await evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))");
  assert.equal(await evaluate("!!document.querySelector('.explain.open')"), false);
  await navigate('static', 1);
  assert(await evaluate("document.querySelector('.tr-inset img').getAttribute('src').endsWith('.png')"), 'Still view must use a still image');

  await evaluate("document.querySelector('[data-mode=interactive]').click()");
  await until(async () => await evaluate("window.ACMOT_VIEW_MODE === 'interactive' && location.search.includes('view=interactive') && location.hash === '#2'"), 'interactive-view button');
  assert(await evaluate("document.querySelector('.tr-inset img').getAttribute('src').endsWith('.gif')"), 'Interactive view must restore the animated image');
  await navigate('interactive', slideIds.beginner);
  await evaluate("document.querySelector('.ui [data-act=explain]').click()");
  assert(await evaluate("!!document.querySelector('.explain.open .ex-example')"),
    'Beginner visual should expose its authored easy example');
  if (process.env.ACMOT_QA_SCREENSHOT) {
    const shot = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync(process.env.ACMOT_QA_SCREENSHOT, Buffer.from(shot.data, 'base64'));
  }
  await evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))");
  await pause(650);
  assert(await evaluate(`(() => {const s=document.querySelector('#stage .slide.active');return [...s.querySelectorAll('.frag')].every(f=>f.classList.contains('on'))})()`), 'Interactive figure must finish quickly');
  await evaluate("window.ACMOT_X.open('x-challenges', 1)");
  assert(await evaluate("!!document.querySelector('#xview.open .xpage.active')"), 'Detailed explanation must open');
  await evaluate("document.querySelector('#xview .xpage.active .xguide').click()");
  assert(await evaluate("document.querySelector('.explain.open .ex-simple')?.textContent.includes('hides the object')"),
    'Detailed explanation should expose its authored simple idea');
  if (process.env.ACMOT_QA_DETAIL_SCREENSHOT) {
    const shot = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync(process.env.ACMOT_QA_DETAIL_SCREENSHOT, Buffer.from(shot.data, 'base64'));
  }
  await evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))");
  assert(await evaluate("!!document.querySelector('#xview.open') && !document.querySelector('.explain.open')"),
    'Closing the reading aid should return to its detail page');
  await evaluate("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))");
  assert.equal(await evaluate("!!document.querySelector('#xview.open')"), false);
  await navigate('interactive', slideIds.diagram);
  await pause(900);
  assert(await evaluate(`(() => {const s=document.querySelector('#stage .slide.active');return [...s.querySelectorAll('.frag')].every(f=>f.classList.contains('on'))})()`), 'Interactive flowchart must finish quickly');
  console.log('OK: both title buttons start the chosen view; still view is fully revealed and has no optional activity or autoplay.');
  console.log('OK: 27 source-checked bar-chart slides load and fit; fast interactive figure and flowchart complete automatically.');
  console.log('OK: 276 slide guides and ' + await evaluate('window.ACMOT_DETAIL_GUIDE_COUNT') +
    ' optional-detail guides reuse authored examples and preserve navigation.');
  console.log('Sample slides:', JSON.stringify(slideIds));
}
run().catch(error => {console.error(error); process.exitCode = 1;}).finally(async () => {
  if (ws) ws.close();
  chrome.kill();
  await pause(1000);
  try {fs.rmSync(profile, {recursive: true, force: true, maxRetries: 5, retryDelay: 200});}
  catch (error) {console.error('Temporary Chrome profile remains:', profile, error.message);}
});
