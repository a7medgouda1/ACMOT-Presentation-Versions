/* Small teaching simulations. Inputs are illustrative; rules are copied from the cited papers. */
(function (root) {
  'use strict';
  var rules = {
    paper1Target: function (sci, tinyShare) {
      if (sci > 0.511 || tinyShare > 0.50) return 'HIGH';
      if (sci > 0.297) return 'MEDIUM';
      return 'LOW';
    },
    scoreGate: function (score, birthGate) { return score >= birthGate; },
    paper2Mode: function (validSplit, medianShare) {
      return !validSplit ? 'COLD' : medianShare >= 0.50 ? 'CLEAN' : 'NOISY';
    },
    scoreRemap: function (group, rank) {
      if (group === 'uncertain') return 0.10 + 0.40 * rank;
      if (group === 'confident') return 0.50 + 0.50 * rank;
      throw Error('Unknown foreground group');
    }
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = rules;
  if (!root || !root.document) return;
  root.ACMOT_INTERACTION_RULES = rules;
  var document = root.document, stage = document.getElementById('stage');
  if (!stage) return;
  var lab = document.createElement('div');
  lab.className = 'overlay interactive-lab';
  lab.innerHTML = '<div class="lab-panel" role="dialog" aria-modal="true" aria-labelledby="lab-title"></div>';
  document.body.appendChild(lab);
  var panel = lab.querySelector('.lab-panel'), opener = null, active = '';

  var views = {
    'paper1-target': {
      title: 'Try choosing a scene setting',
      intro: 'Move the sliders. See which ready-made setting the paper would ask for.',
      fields: '<label class="lab-field" for="lab-sci"><span class="lab-field-head">Scene score <output data-out="sci">0.330</output></span><input id="lab-sci" type="range" min="0" max="1" step="0.001" value="0.330" data-field="sci"></label>' +
        '<label class="lab-field" for="lab-tiny"><span class="lab-field-head">Tiny-box share <output data-out="tiny">0.300</output></span><input id="lab-tiny" type="range" min="0" max="1" step="0.001" value="0.300" data-field="tiny"></label>',
      scale: 'lab-scale',
      labels: ['LOW · up to 0.297', 'MEDIUM', 'HIGH · above 0.511'],
      source: 'Teaching simplification of Paper 1 Eq. 17. The scene-label guard, recovery, hysteresis and 30-frame dwell are explained separately; this is the proposed target only.'
    },
    'score-gate': {
      title: 'Try a fixed score limit',
      intro: 'Move the box score. In this made-up example, a new track needs at least 0.70.',
      fields: '<label class="lab-field" for="lab-score"><span class="lab-field-head">Box score <output data-out="score">0.45</output></span><input id="lab-score" type="range" min="0" max="1" step="0.01" value="0.45" data-field="score"></label>',
      scale: 'lab-scale gate-scale',
      labels: ['0.00 · below birth gate', '0.70 · birth gate', '1.00'],
      source: 'Made-up score and gate to illustrate the fixed-score mismatch in Paper 2 Introduction. This only checks whether a new track can start; an existing track can use a different host gate.'
    },
    'paper2-mode': {
      title: 'Try choosing the score path',
      intro: 'First check whether past scores split into groups. Then use the middle share to choose a path.',
      fields: '<label class="lab-check"><input type="checkbox" checked data-field="valid">Valid split from past frames</label>' +
        '<label class="lab-field" for="lab-rho"><span class="lab-field-head">Past median confident share <output data-out="rho">0.63</output></span><input id="lab-rho" type="range" min="0" max="1" step="0.01" value="0.63" data-field="rho"></label>',
      scale: 'lab-scale mode-scale',
      labels: ['NOISY · below 0.50', '0.50', 'CLEAN · 0.50 or above'],
      source: 'Paper 2 Algorithm 1, lines 2–8. No valid split means COLD even if the median slider is high. The slider is an illustrative input, not a new measured result.'
    },
    'score-remap': {
      title: 'Try giving a box a new score',
      intro: 'In the noisy path, choose a box group and where it stands within that group.',
      fields: '<label class="lab-field" for="lab-band"><span>Foreground group</span><select id="lab-band" data-field="band"><option value="uncertain">Uncertain</option><option value="confident">Confident</option></select></label>' +
        '<label class="lab-field" for="lab-rank"><span class="lab-field-head">Rank in group <output data-out="rank">0.30</output></span><input id="lab-rank" type="range" min="0.01" max="0.99" step="0.01" value="0.30" data-field="rank"></label>',
      scale: 'lab-scale remap-scale',
      labels: ['0.10 · uncertain band', '0.50', '1.00 · confident band'],
      source: 'Paper 2 Eq. 8. This applies in NOISY mode only. Background-like boxes are dropped first; these are made-up ranks passed through the paper formula.'
    }
  };
  function field(name) { return panel.querySelector('[data-field="' + name + '"]'); }
  function out(name, value) { var el = panel.querySelector('[data-out="' + name + '"]'); if (el) el.textContent = value; }
  function update() {
    var marker = panel.querySelector('.lab-scale'), result = panel.querySelector('.lab-result'), detail = panel.querySelector('.lab-detail');
    if (!marker || !result || !detail) return;
    var position = 0, heading = '', more = '', warn = false;
    if (active === 'paper1-target') {
      var sci = +field('sci').value, tiny = +field('tiny').value, state = rules.paper1Target(sci, tiny);
      out('sci', sci.toFixed(3)); out('tiny', tiny.toFixed(3));
      position = sci * 100;
      heading = 'Proposed target: ' + state;
      more = tiny > 0.50 ? 'Tiny share asks for HIGH.' : sci > 0.511 ? 'Scene score asks for HIGH.' : sci > 0.297 ? 'Scene score asks for MEDIUM.' : 'Neither HIGH nor MEDIUM condition is met.';
      warn = state === 'HIGH';
    } else if (active === 'score-gate') {
      var score = +field('score').value, accepted = rules.scoreGate(score, 0.70);
      out('score', score.toFixed(2)); position = score * 100;
      heading = accepted ? 'This box can start a new track' : 'This box cannot start a new track';
      more = 'Box score ' + score.toFixed(2) + (accepted ? ' reaches ' : ' is below ') + 'the illustrative birth gate 0.70.';
      warn = !accepted;
    } else if (active === 'paper2-mode') {
      var valid = field('valid').checked, rho = +field('rho').value, mode = rules.paper2Mode(valid, rho);
      field('rho').disabled = !valid;
      marker.classList.toggle('cold', !valid);
      out('rho', rho.toFixed(2)); position = rho * 100;
      heading = 'Chosen mode: ' + mode;
      more = !valid ? 'No valid past split, so use COLD.' : mode === 'CLEAN' ? 'The past median is at least 0.50.' : 'The past median is below 0.50.';
      warn = mode === 'NOISY';
    } else if (active === 'score-remap') {
      var band = field('band').value, rank = +field('rank').value, mapped = rules.scoreRemap(band, rank);
      out('rank', rank.toFixed(2)); position = mapped * 100;
      heading = 'New score: ' + mapped.toFixed(2);
      more = band === 'uncertain' ? 'Uncertain boxes stay in the 0.10–0.50 band.' : 'Confident boxes stay in the 0.50–1.00 band.';
      warn = band === 'uncertain';
    }
    marker.style.setProperty('--marker', position.toFixed(1) + '%');
    result.classList.toggle('warn', warn);
    result.querySelector('strong').textContent = heading;
    detail.textContent = more;
  }
  function close() {
    lab.classList.remove('open');
    panel.innerHTML = '';
    if (opener) opener.focus();
    opener = null; active = '';
  }
  function open(kind, button) {
    var view = views[kind]; if (!view) return;
    if (root.ACMOT_SETTLE_AUTO) root.ACMOT_SETTLE_AUTO();
    document.querySelectorAll('.overlay.open').forEach(function (o) { o.classList.remove('open'); });
    opener = button; active = kind;
    panel.innerHTML = '<button type="button" class="lab-close" aria-label="Close interactive example">×</button>' +
      '<div class="lab-kicker">Interactive teaching example</div><h2 id="lab-title">' + view.title + '</h2>' +
      '<p class="lab-intro">' + view.intro + '</p><div class="lab-fields">' + view.fields + '</div>' +
      '<div class="' + view.scale + '"><i class="lab-marker"></i></div>' +
      '<div class="lab-scale-labels"><span>' + view.labels[0] + '</span><span>' + view.labels[1] + '</span><span>' + view.labels[2] + '</span></div>' +
      '<div class="lab-result" aria-live="polite"><strong></strong><div class="lab-detail"></div></div>' +
      '<div class="lab-source">' + view.source + '</div>';
    lab.classList.add('open'); update();
    var first = panel.querySelector('input,select'); if (first) first.focus();
  }
  stage.addEventListener('click', function (e) {
    if (root.ACMOT_VIEW_MODE === 'static') return;
    var b = e.target.closest('.lab-open');
    if (b) { e.preventDefault(); open(b.getAttribute('data-lab'), b); }
  });
  panel.addEventListener('input', update);
  panel.addEventListener('change', update);
  panel.addEventListener('click', function (e) { if (e.target.closest('.lab-close')) close(); });
  lab.addEventListener('click', function (e) { if (e.target === lab) close(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lab.classList.contains('open')) { e.preventDefault(); e.stopPropagation(); close(); }
  }, true);
})(typeof window !== 'undefined' ? window : null);
