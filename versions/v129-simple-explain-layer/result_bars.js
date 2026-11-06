/* Add source-checked bar-chart companions before the presentation engine counts slides. */
(function () {
  'use strict';
  var stage = document.getElementById('stage');
  var specs = window.ACMOT_RESULT_BARS;
  if (!stage || !Array.isArray(specs)) throw Error('Result bar-chart manifest missing');
  function esc(value) {
    return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  var anchors = {};
  specs.forEach(function (spec) {
    var source = anchors[spec.after] || stage.querySelector('.slide[data-title="' + spec.after + '"]');
    if (!source) throw Error('Missing bar-chart anchor: ' + spec.after);
    var slide = document.createElement('section');
    var sec = source.getAttribute('data-sec');
    slide.className = 'slide result-bar-slide';
    slide.setAttribute('data-sec', sec);
    slide.setAttribute('data-secname', source.getAttribute('data-secname'));
    slide.setAttribute('data-title', spec.title);
    slide.setAttribute('data-parent', spec.after);
    slide.setAttribute('data-chart-id', spec.id);
    slide.innerHTML = '<header class="s-head"><div class="kicker">' +
      (sec === '11' ? 'Paper 1' : sec === '12' ? 'Paper 2' : 'Result') +
      ' · baseline comparison</div><h2>' + esc(spec.title) + '</h2></header>' +
      '<div class="s-body result-bars-body"><p class="result-bar-intro">' + esc(spec.intro) + '</p>' +
      '<div class="result-bar-frame"><img class="result-chart-image zoomable" tabindex="0" role="button" ' +
      'aria-label="Enlarge the bar chart" data-src="' + esc(spec.image) + '" alt="' + esc(spec.alt) + '"></div>' +
      '<p class="result-bar-note"><b>Read it fairly:</b> ' + esc(spec.note) +
      '<small>Percent and point labels use the displayed rounded aggregates; the original result slide keeps reported estimates and intervals.</small></p></div>' +
      '<footer class="s-foot"><span class="prov p-paper">' + esc(spec.source) + '</span></footer>' +
      '<aside class="notes"><p><b>Say:</b> ' + esc(spec.intro) + ' ' + esc(spec.note) +
      '</p><p><b>Percent rule:</b> Percent change is the aggregate difference divided by the same-cell baseline. ' +
      'Score differences are also shown in points. A zero or negative baseline has no valid relative percentage.</p></aside>';
    source.parentNode.insertBefore(slide, source.nextSibling);
    anchors[spec.after] = slide;
  });
  var all = Array.prototype.slice.call(stage.querySelectorAll('.slide'));
  for (var n = 1; n <= 10; n++) {
    var start = all.findIndex(function (s) { return s.id === 'sec-' + n; });
    var end = n === 10 ? all.findIndex(function (s) { return s.id === 'sec-11'; }) :
      all.findIndex(function (s) { return s.id === 'sec-' + (n + 1); });
    var row = stage.querySelector('.ol-row[data-goto="sec-' + n + '"] .rg');
    if (row && start >= 0 && end > start) row.textContent = 'slides ' + (start + 1) + ' - ' + end;
  }
  window.ACMOT_RESULT_BAR_COUNT = specs.length;
})();
