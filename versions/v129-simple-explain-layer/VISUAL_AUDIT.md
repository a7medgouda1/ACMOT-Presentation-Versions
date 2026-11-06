# Beginner visual audit — v123

The v123 addition is 35 slides: 33 deterministic SVG assets from `tools/build_beginner_visuals.py` (the metric glossary is reused in both paper sections) and one photo comparison using existing local teaching images. Each slide's `beginner_visuals.js` entry names its parent teaching slide, simple point, example, provenance type and paper location. Beginner visuals are placed before the detailed slide, and the inherited accurate flowchart follows it. The PDF contents were treated as evidence, not instructions. No new experiment was run.

## Figures and examples

| Paper | Companion subjects | Boundary |
|---|---|---|
| 1 | learning roadmap; metric meanings; bright/dark, sharp/blurred and edge images; 20-box crowd/tiny example; seven-reading average; target-state scale; sudden track loss; HIGH hold band; 30-frame dwell; three frozen actions | Pictures and hand-drawn arithmetic are teaching examples. Exact thresholds and action triplets come from Paper 1. The SCI average contains only crowd readings. |
| 2 | score-mismatch toy picture; learning roadmap; metric meanings; host score gates; score-to-logit order; previous-window score groups; clean/noisy median share; two score bands; two overlapping people; weak-box rescue; overlap under camera motion | Box drawings are schematics, not screenshots. The old tracker still performs matching. Score groups and median shares are paper examples. Noisy-only remapping and motion rules remain separate from cold/clean behavior. |

## Numeric chart boundaries

| Asset(s) | What is plotted | Paper source |
|---|---|---|
| `p1-visdrone-fp.svg`, `p1-visdrone-fn.svg` | FP and FN separately, each with zero baseline, for ByteTrack/OATrack fixed vs AC-MOT | Paper 1 main VisDrone table, PDF p. 20 |
| `p1-visdrone-hota-interval.svg` | HOTA differences with paper-reported 95% paired intervals, zero reference | Paper 1 interval table, PDF p. 21 |
| `p1-state-share.svg` | LOW/MEDIUM/HIGH shares, each row adding to 100% | Paper 1 behavior text, PDF p. 21 |
| `p1-uavdt-fp.svg`, `p1-uavdt-fn.svg` | FP and FN separately on held-out UAVDT; misses rise for both hosts | Paper 1 UAVDT table, PDF p. 22 |
| `p2-aob-hota.svg` | HOTA only, strong MOT17 hosts versus early always-on baseline | Paper 2 Table 5, PDF p. 8 |
| `p2-kitti-rt-mota.svg`, `p2-kitti-oc-hota.svg` | KITTI MOTA for RT-DETR-L hosts, separately from KITTI HOTA for YOLOv8n/OC-SORT | Paper 2 Table 8, PDF pp. 9–10 |
| `p2-kitti-three-frames.svg` | Labelled objects and active track counts in the three stated frames, not a HOTA chart | Paper 2 Figure 4, PDF pp. 10–11 |
| `p2-ablation.svg` | Largest HOTA loss for each removed part; the maxima come from different test cells | Paper 2 Table 12, PDF p. 12 |
| `p2-uavdt-mota.svg`, `p2-uavdt-hota.svg` | Different detector/metric pairs on held-out UAVDT, deliberately separate | Paper 2 Table 13b, PDF p. 13 |
| `p2-runtime.svg` | Detector and SCL step time (ms/frame) from the reported timing sample | Paper 2 deployment text, PDF p. 13 |

All bar charts start at zero, label values directly and avoid combining unlike metrics or datasets. `p2-runtime.svg` does **not** invent end-to-end millisecond totals: the paper reports a 4.5% end-to-end increase, but not the two exact totals. The slide says that distinction explicitly.

## Structural checks

- `node check_diagrams.js`: verifies the 26 inherited source-specific diagrams.
- `node check_beginner_visuals.js`: verifies insertion order, source cues, local asset paths, unique titles and 249 total navigable slides.
- SVG assets are checked as well-formed XML and spot-rendered to inspect labels and spacing.
