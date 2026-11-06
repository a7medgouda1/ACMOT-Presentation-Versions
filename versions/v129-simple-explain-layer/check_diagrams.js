/* Non-browser structural test for all inserted paper diagrams. */
'use strict';
const fs=require('fs');
const vm=require('vm');
const assert=require('assert');
const html=fs.readFileSync(__dirname+'/index.html','utf8');
const staticSlides=[...html.matchAll(/<[a-z][^>]*\bclass="([^"]*)"/g)].filter(x=>x[1].split(/\s+/).includes('slide')).length;
assert.strictEqual(staticSlides,188);
const source=[];
const re=/<section\s+class="slide"\s+data-sec="(11|12)"[^>]*data-title="([^"]+)"/g;
let match;
while((match=re.exec(html))) source.push({sec:match[1],title:match[2]});
const all=[];
function element(sec,title){
  const attrs={'data-sec':sec,'data-title':title,'data-secname':sec==='11'?'XI · Paper 1: AC-MOT':'XII · Paper 2: SCL'};
  return {attrs,className:'',innerHTML:'',parentNode:stage,getAttribute(k){return attrs[k];},setAttribute(k,v){attrs[k]=v;},get nextSibling(){return all[all.indexOf(this)+1]||null;}};
}
const stage={
  querySelector(selector){const title=selector.match(/data-title="([^"]+)"/);return title?all.find(x=>x.getAttribute('data-title')===title[1]):null;},
  insertBefore(slide,before){const i=before?all.indexOf(before):all.length;assert(i>=0);all.splice(i,0,slide);}
};
source.forEach(x=>all.push(element(x.sec,x.title)));
const window={};
const document={getElementById(id){return id==='stage'?stage:null;},createElement(){return element('', '');}};
const code=fs.readFileSync(__dirname+'/diagrams.js','utf8');
vm.runInNewContext(code,{window,document,Error});
const inserted=all.filter(x=>x.className==='slide diagram-slide');
assert.strictEqual(inserted.length,window.ACMOT_DIAGRAM_COUNT);
assert.strictEqual(inserted.length,26);
for(const slide of inserted){
  assert(slide.innerHTML.includes('role="img"'));
  assert(!/NaN|undefined|<text[^>]*>false<\/text>/.test(slide.innerHTML));
  assert(slide.innerHTML.includes('Main point'));
  assert(slide.innerHTML.includes('Simple example'));
  assert(slide.getAttribute('data-sec')==='11'||slide.getAttribute('data-sec')==='12');
}
const complete=inserted.filter(x=>x.getAttribute('data-title').startsWith('Paper 2 — causal')||x.getAttribute('data-title').startsWith('Paper 2 — update memories'));
assert.strictEqual(complete.length,2);
assert(all.indexOf(complete[1])===all.indexOf(complete[0])+1);
assert(!code.includes('visualPlan('));
if(process.argv.includes('--export-svg')||process.argv.includes('--export-all-svg')){
  const dir=fs.mkdtempSync('/private/tmp/acmot-diagram-');
  const css=fs.readFileSync(__dirname+'/diagrams.css','utf8');
  const titles=['Paper 1 — scene-label priority','Paper 1 — short recovery probe','Paper 2 — thresholds come from earlier frames','Paper 2 — causal branch and merge','Paper 2 — motion tolerance is mode-gated'];
  const samples=process.argv.includes('--export-all-svg')?inserted:titles.map(title=>inserted.find(x=>x.getAttribute('data-title')===title));
  samples.forEach((slide,i)=>{
    assert(slide,'Missing visual sample '+titles[i]);
    const svg=slide.innerHTML.match(/<svg[\s\S]*?<\/svg>/);
    assert(svg,'Missing SVG '+slide.getAttribute('data-title'));
    fs.writeFileSync(dir+'/'+(i+1)+'.svg',svg[0].replace(/(<svg[^>]*>)/,'$1<style>'+css+'</style>'));
  });
  console.log('SVG samples: '+dir);
}
console.log('OK: '+inserted.length+' source-specific diagrams; all sources, paths, labels and ordering resolve.');
console.log('OK: '+staticSlides+' original slides + '+inserted.length+' diagrams (beginner visuals checked separately).');
