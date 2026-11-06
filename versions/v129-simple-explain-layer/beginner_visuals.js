/* Beginner-first visual companions. Loaded after accurate diagrams and before script.js. */
(function () {
  'use strict';
  var stage = document.getElementById('stage');
  if (!stage) return;
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function visual(after, heading, asset, point, example, source, origin) {
    return { after: after, heading: heading, asset: asset, point: point,
             example: example, source: source, origin: origin };
  }

  var items = [
    visual('Paper 1 overview', 'Paper 1: the easy path through the story', 'p1-roadmap.svg',
      'A detector finds objects in each picture. A tracker follows the same objects across pictures.',
      'First see the problem, then how the paper changes a ready-made detector setting, then how it tests the result.',
      'Paper 1 · Introduction and method overview', 'Teaching roadmap'),
    visual('Paper 1 VisDrone results', 'Paper 1 numbers in everyday words', 'metrics-plain.svg',
      'One score cannot tell the whole story. Check wrong boxes, missed objects and changed ID numbers too.',
      'A false alarm is a box around nothing real. A miss is a real object with no box. An ID switch gives the same object a new number.',
      'Paper 1 · evaluation measures, Sect. II', 'Plain-language definitions'),
    visual('Paper 1 image cues', 'See dark, blur and busy edges', 'photos',
      'The picture gives three simple clues: how bright, how sharp and how busy it looks.',
      'Dark can be labelled NIGHT. Blur can be labelled BLUR. These checks do not enter the final crowd average.',
      'Paper 1 · Sect. III-B, pp. 8–10 · illustrative images reused from the original deck', 'Illustrative pictures'),
    visual('Paper 1 box cues', 'Count old boxes, then count tiny boxes', 'p1-box-clues.svg',
      'Old tracks tell the controller how crowded the scene is and how many boxes are tiny.',
      'In this made-up picture: 20 tracks give crowd 0.67; 12 tiny tracks give tiny share 0.60.',
      'Paper 1 · Eqs. 10–12, pp. 8–9', 'Made-up picture; paper rules'),
    visual('Paper 1 SCI', 'Seven crowd readings become one number', 'p1-seven-crowds.svg',
      'The final scene score averages how crowded the last seven checks were.',
      'Made-up readings 0.2, 0.3, 0.3, 0.4, 0.4, 0.5 and 0.7 average to 0.40.',
      'Paper 1 · Eqs. 13–15, pp. 9–10', 'Made-up numbers; paper rule'),
    visual('Paper 1 target state', 'A simple scale for LOW, MEDIUM, HIGH', 'p1-target-scale.svg',
      'The paper asks whether the scene needs the HIGH, MEDIUM or LOW ready-made setting, in that order.',
      'A scene score of 0.33 asks for MEDIUM. More than half tiny objects can ask for HIGH even with a lower scene score.',
      'Paper 1 · Eq. 17, p. 11', 'Illustrative scale; paper limits'),
    visual('Paper 1 recovery probe', 'When many tracks disappear', 'p1-track-drop.svg',
      'If many followed objects vanish at once, the system checks whether it lost them.',
      'If it recently followed 20 objects but now sees only 6, it asks briefly for HIGH. A waiting rule still controls when settings can change.',
      'Paper 1 · Eqs. 18–19, p. 11', 'Made-up numbers; paper rule'),
    visual('Paper 1 hysteresis', 'Why HIGH does not switch off at once', 'p1-hold-band.svg',
      'The system needs a little more evidence to enter HIGH than to stay there. This avoids flickering between settings.',
      'At scene score 0.505, a current HIGH setting can stay HIGH, but a MEDIUM setting does not move up from that score alone.',
      'Paper 1 · Eq. 20, p. 12', 'Made-up SCI example; paper limits'),
    visual('Paper 1 dwell rule', 'The state waits at least 30 frames', 'p1-dwell-timeline.svg',
      'After changing settings, the system waits at least 30 video frames before another change.',
      'A new request at frame 11 may wait until frame 31. Finding and following objects still happen on every frame.',
      'Paper 1 · Eq. 21, p. 12', 'Made-up timeline; paper rule'),
    visual('Paper 1 action map', 'See the three frozen actions', 'p1-action-cards.svg',
      'Each setting chooses picture size, how overlapping boxes are handled and the lowest box score to keep.',
      'In this paper, HIGH means a hard scene. It actually uses the smallest input picture, not the largest.',
      'Paper 1 · Table 2, p. 13', 'Paper values'),
    visual('Paper 1 full VisDrone results', 'VisDrone: fewer false alarms', 'p1-visdrone-fp.svg',
      'Both hosts produce fewer wrong boxes with AC-MOT.',
      'ByteTrack falls from 39,274 to 24,892 false alarms. Lower is better.',
      'Paper 1 · main VisDrone results table, p. 20', 'Measured paper numbers'),
    visual('Paper 1 full VisDrone results', 'VisDrone: check the missed objects too', 'p1-visdrone-fn.svg',
      'The gain is not free for ByteTrack: it misses more real objects.',
      'ByteTrack misses 24,121 before and 25,902 after. The OATrack count falls slightly.',
      'Paper 1 · main VisDrone results table, p. 20', 'Measured paper numbers'),
    visual('Paper 1 VisDrone intervals', 'VisDrone: how steady is the HOTA gain?', 'p1-visdrone-hota-interval.svg',
      'Both paired ranges are above zero on the seven final videos.',
      'ByteTrack gains 2.937 HOTA points; OATrack gains 1.325. The whiskers show the paper\'s 95% intervals.',
      'Paper 1 · paired VisDrone intervals, p. 21', 'Measured paper numbers'),
    visual('Paper 1 controller behavior and runtime', 'Which state did it use most?', 'p1-state-share.svg',
      'The selective HIGH action was used on most frames for both hosts.',
      'ByteTrack used HIGH on 62.5% of frames; OATrack used it on 59.3%.',
      'Paper 1 · controller-behaviour results, p. 21', 'Measured paper numbers'),
    visual('Paper 1 full UAVDT results', 'New drone data: false alarms fall', 'p1-uavdt-fp.svg',
      'The frozen controller also filters many wrong boxes on the unseen drone dataset.',
      'ByteTrack false alarms fall from 279,616 to 212,077. This is transfer without retuning.',
      'Paper 1 · UAVDT results table, p. 22', 'Measured paper numbers'),
    visual('Paper 1 full UAVDT results', 'New drone data: misses rise', 'p1-uavdt-fn.svg',
      'On UAVDT, both hosts miss more objects even while false alarms fall.',
      'ByteTrack misses rise from 66,050 to 73,702. This trade-off must stay visible.',
      'Paper 1 · UAVDT results table, p. 22', 'Measured paper numbers'),

    visual('Paper 2 problem', 'A useful box can fail a fixed score gate', 'p2-score-mismatch.svg',
      'Each found object has a score. A tracker may reject a useful box when that score falls below its fixed limit.',
      'In this made-up example, a score falls from 0.90 to 0.45, while a new track still needs at least 0.70.',
      'Paper 2 · Introduction, pp. 1–2', 'Made-up numbers; paper problem'),
    visual('Paper 2 five steps', 'Paper 2: the easy path through the method', 'p2-roadmap.svg',
      'The small layer checks recent scores, decides whether help is needed, and passes boxes to the same tracker.',
      'Next we explain how it makes that choice, changes scores when needed and keeps the original tracker.',
      'Paper 2 · Figure 1 and Algorithm 1, pp. 4–8', 'Teaching roadmap'),
    visual('Paper 2 main evidence', 'Paper 2 numbers in everyday words', 'metrics-plain.svg',
      'Tracking scores ask different questions: were objects found, followed and kept under the same ID?',
      'A better overall score can still come with more misses. A range across videos shows how steady a result is.',
      'Paper 2 · evaluation measures, Sect. 2', 'Plain-language definitions'),
    visual('Paper 2 host contract', 'Every host has its own score gates', 'p2-host-score-lines.svg',
      'Before changing a box score, the new layer reads the limits the tracker already uses.',
      'One tracker can use boxes scored as low as 0.10; this other setup starts at 0.60. The same box may work for one but not the other.',
      'Paper 2 · Table 3, pp. 3–4', 'Paper host settings'),
    visual('Paper 2 logits', 'The score order stays the same', 'p2-logit-points.svg',
      'A mathematical change spreads scores out. It never changes which box has the higher score.',
      'Scores 0.1, 0.5 and 0.9 become about −2.2, 0 and +2.2, still in the same order.',
      'Paper 2 · Sect. 3.2, p. 4', 'Rounded arithmetic from paper equation'),
    visual('Paper 2 nested Otsu', 'Three groups from the last 10 frames', 'p2-otsu-groups.svg',
      'The system looks at scores from the ten previous pictures and sorts them into three groups.',
      'In one paper example, the past window has 653 weak, 88 uncertain and 175 strong boxes. It does not look ahead.',
      'Paper 2 · Fig. 2a and Sect. 3.2, pp. 4–5', 'Measured paper example'),
    visual('Paper 2 mode rule', 'Clean or noisy? Look at the middle share', 'p2-mode-gauge.svg',
      'If past scores form useful groups, the system checks how many boxes were in the strong group.',
      'A middle share of 0.63 gives the clean path; 0.42 gives the noisy path. If groups cannot be made, use the tracker as it is.',
      'Paper 2 · Fig. 2 and Sect. 3.3, pp. 5–6', 'Reported example values'),
    visual('Paper 2 noisy mode remapping', 'Give weak and strong boxes separate bands', 'p2-rank-bands.svg',
      'Only the noisy path removes likely background boxes and gives the remaining boxes scores the tracker can use.',
      'Order within each group matters: a made-up position 0.3 becomes score 0.22; position 0.8 in the strong group becomes 0.90.',
      'Paper 2 · Eq. 8, pp. 5–6', 'Made-up ranks; paper formulas'),
    visual('Paper 2 duplicate handling', 'Do not erase a second real person', 'p2-two-people.svg',
      'Two boxes may overlap because two people are close, not because one box is a duplicate.',
      'If different old tracks support both boxes, noisy mode keeps both.',
      'Paper 2 · Sect. 3.4, p. 6', 'Illustrative drawing; paper rule'),
    visual('Paper 2 weak detection recovery', 'Give one weak box a careful second chance', 'p2-weak-rescue.svg',
      'A weak box is rescued only if it is foreground-like, fits an old track and would otherwise be lost.',
      'The score is raised just above the host\'s usable floor. The frozen host still decides the match.',
      'Paper 2 · Sect. 3.5 and Algorithm 1, pp. 6–8', 'Illustrative drawing; paper rule'),
    visual('Paper 2 motion tolerance', 'Loosen matching only in noisy mode', 'p2-motion-rings.svg',
      'Camera movement may justify a more forgiving match, but only in the noisy branch.',
      'With host value 0.80 and motion ratio 2, the paper formula gives 0.90. Cold and clean keep 0.80.',
      'Paper 2 · Eq. 9, pp. 6–7', 'Made-up arithmetic; paper formula'),
    visual('Paper 2 AOB failure', 'Why always changing scores was a bad idea', 'p2-aob-hota.svg',
      'The early always-on design hurt already good trackers.',
      'SparseTrack HOTA falls from 68.88 to 64.72. BoostTrack also falls. This led to the clean/noisy check.',
      'Paper 2 · Table 5 and Sect. 4.3, p. 8', 'Measured development numbers'),
    visual('Paper 2 KITTI RT-DETR results', 'New detector: MOTA rises with the same hosts', 'p2-kitti-rt-mota.svg',
      'SCL helps two trackers use a replacement detector without retraining either one.',
      'ByteTrack rises from 47.27 to 53.24 MOTA; BoT-SORT rises from 48.25 to 56.11.',
      'Paper 2 · Table 8, pp. 9–10', 'Measured paper numbers'),
    visual('Paper 2 KITTI OC-SORT results', 'One score gate: more useful boxes get through', 'p2-kitti-oc-hota.svg',
      'The single-stage host gains most when weak, useful boxes become visible.',
      'OC-SORT HOTA rises from 36.27 to 44.18 on KITTI with YOLOv8n.',
      'Paper 2 · Table 8, pp. 9–10', 'Measured paper numbers'),
    visual('Paper 2 qualitative KITTI example', 'Three real frames, more objects followed', 'p2-kitti-three-frames.svg',
      'The selected median-gain sequence shows more active tracks with SCL.',
      'At frame 102: ten labelled objects, six host tracks, nine tracks with SCL. Counts are not a HOTA score.',
      'Paper 2 · Fig. 4, pp. 10–11', 'Reported frame counts'),
    visual('Paper 2 component ablation', 'What breaks when a part is removed?', 'p2-ablation.svg',
      'The parts have different jobs. The largest observed loss comes from removing weak-box recovery.',
      'These are each part\'s largest HOTA loss across different test cells, not one shared run.',
      'Paper 2 · Table 12, p. 12', 'Measured losses; different cells'),
    visual('Paper 2 UAVDT results', 'Unseen drone video: MOTA improves', 'p2-uavdt-mota.svg',
      'The frozen system transfers to a new dataset with a replacement detector.',
      'RT-DETR-L + ByteTrack MOTA rises from 3.29 to 27.99. This is not the HOTA result.',
      'Paper 2 · Table 13b, p. 13', 'Measured paper numbers'),
    visual('Paper 2 UAVDT results', 'Unseen drone video: HOTA also improves', 'p2-uavdt-hota.svg',
      'A second detector pair has a smaller but positive HOTA change.',
      'YOLOv8n + ByteTrack HOTA rises from 29.05 to 30.83. This is not the MOTA result.',
      'Paper 2 · Table 13b, p. 13', 'Measured paper numbers'),
    visual('Paper 2 runtime', 'The added step is small beside detection', 'p2-runtime.svg',
      'SCL adds work, but the complete detector-and-tracker pipeline grows only a little in this timing test.',
      'The detector takes 42 ms and SCL averages 2.95 ms per frame. The paper reports a 4.5% increase for the whole pipeline.',
      'Paper 2 · runtime study, p. 13', 'Measured timing sample')
  ];

  var photos = [
    ['gray_day.jpg', 'Bright image'], ['gray_night.jpg', 'Dark image'],
    ['blur_sharp.jpg', 'Sharp image'], ['blur_blurred.jpg', 'Blurred image'],
    ['edges_easy.png', 'Few edges'], ['edges_hard.png', 'Many edges']
  ];
  function photoMarkup() {
    return '<div class="beginner-photos">' + photos.map(function (pair) {
      return '<figure class="zoomable" tabindex="0" role="button" aria-label="Enlarge ' + esc(pair[1]) + '"><img src="assets/figures/generated/' + pair[0] + '" alt="' + esc(pair[1]) + '"><figcaption>' + esc(pair[1]) + '</figcaption></figure>';
    }).join('') + '</div>';
  }
  var labs = {
    'p1-target-scale.svg': 'paper1-target',
    'p2-score-mismatch.svg': 'score-gate',
    'p2-mode-gauge.svg': 'paper2-mode',
    'p2-rank-bands.svg': 'score-remap'
  };
  function stageLabel(sec, after) {
    if (sec === '11') {
      if (['Paper 1 overview', 'Paper 1 VisDrone results'].indexOf(after) >= 0) return 'Start · The big idea';
      if (['Paper 1 image cues', 'Paper 1 box cues', 'Paper 1 SCI'].indexOf(after) >= 0) return 'Step 1 · Read the scene';
      if (['Paper 1 target state', 'Paper 1 recovery probe', 'Paper 1 hysteresis', 'Paper 1 dwell rule', 'Paper 1 action map'].indexOf(after) >= 0) return 'Step 2 · Choose settings';
      return 'Step 3 · Read the results';
    }
    if (['Paper 2 problem', 'Paper 2 five steps', 'Paper 2 main evidence'].indexOf(after) >= 0) return 'Start · The big idea';
    if (['Paper 2 host contract', 'Paper 2 logits', 'Paper 2 nested Otsu', 'Paper 2 mode rule'].indexOf(after) >= 0) return 'Step 1 · Check score fit';
    if (['Paper 2 noisy mode remapping', 'Paper 2 duplicate handling', 'Paper 2 weak detection recovery', 'Paper 2 motion tolerance'].indexOf(after) >= 0) return 'Step 2 · Repair if needed';
    return 'Step 3 · Read the results';
  }
  var count = 0;
  items.forEach(function (spec) {
    var source = stage.querySelector('.slide[data-title="' + spec.after + '"]');
    if (!source) throw Error('Missing visual anchor: ' + spec.after);
    var slide = document.createElement('section');
    var sec = source.getAttribute('data-sec');
    slide.className = 'slide beginner-slide';
    slide.setAttribute('data-sec', sec);
    slide.setAttribute('data-secname', source.getAttribute('data-secname'));
    slide.setAttribute('data-title', spec.heading);
    slide.setAttribute('data-parent', spec.after);
    slide.setAttribute('data-origin', spec.origin);
    var visualBody = spec.asset === 'photos' ? photoMarkup() :
      '<img class="beginner-svg zoomable" tabindex="0" role="button" aria-label="Enlarge this figure" title="Click to enlarge" src="assets/beginner/' + esc(spec.asset) + '" alt="' + esc(spec.heading) + '">';
    var lab = labs[spec.asset] ? '<button type="button" class="lab-open" data-lab="' + labs[spec.asset] + '">Try a small example</button>' : '';
    slide.innerHTML = '<header class="s-head"><div class="kicker">Paper ' + (sec === '11' ? '1' : '2') + ' · ' + stageLabel(sec, spec.after) + '</div><h2>' + esc(spec.heading) + '</h2></header>' +
      '<div class="s-body"><div class="beginner-frame">' + visualBody + lab + '</div>' +
      '<div class="beginner-notes"><div class="frag"><strong>Simple idea</strong>' + esc(spec.point) + '</div>' +
      '<div class="frag"><strong>Easy example</strong>' + esc(spec.example) + '</div></div></div>' +
      '<div class="beginner-source">' + esc(spec.origin) + ' · ' + esc(spec.source) + '</div>' +
      '<aside class="notes"><p><b>Say:</b> ' + esc(spec.point) + ' ' + esc(spec.example) + '</p></aside>';
    source.parentNode.insertBefore(slide, source);
    count++;
  });
  window.ACMOT_BEGINNER_VISUAL_COUNT = count;
})();
