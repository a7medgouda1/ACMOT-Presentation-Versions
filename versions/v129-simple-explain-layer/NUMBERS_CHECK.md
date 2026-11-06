# Numerical evidence check — v123

This file records the manuscript numbers used in Sections XI and XII. Values are copied from the two supplied PDFs; no metric was recomputed and no new experiment was run. New v123 charts use only values listed here or directly transcribed from the same tables; see `VISUAL_AUDIT.md`. The runtime visual does not present invented end-to-end millisecond totals.

## Paper 1 — AC-MOT

### Controller and protocol

- Analysis stride: 10 frames; image cues use quarter width and quarter height.
- Image checks: Canny 50/120, night below brightness 80, blur below Laplacian variance 180.
- Box checks: crowd count divided by 30 and capped at 1; tiny box below 32 × 32; tiny ratio guard above 0.50.
- SCI: mean of the last 7 crowd values; medium entry 0.297; high entry 0.511.
- Recovery: previous peak at least 5; current count below 40% of peak; peak decay 0.8; at most 3 analysis steps.
- Hysteresis: hold high above SCI 0.50 or tiny ratio 0.40; hold medium above SCI 0.25.
- Dwell: 30 frames.
- Actions: LOW `(1536, 0.70, 0.10)`; MEDIUM `(1280, 0.45, 0.40)`; HIGH `(1088, 0.60, 0.40)` for resolution, NMS IoU and score threshold.
- Search: 60 TPE trials, seed 43, four folds; fold HOTA changes `+0.592`, `+4.164`, `+2.029`, `+3.004`, mean `+2.447`.

### Frozen VisDrone results

| Metric | ByteTrack fixed | ByteTrack AC-MOT | OATrack fixed | OATrack AC-MOT |
|---|---:|---:|---:|---:|
| HOTA | 41.586 | 44.523 | 46.770 | 48.095 |
| MOTA | 9.876 | 27.871 | 28.165 | 34.483 |
| IDF1 | 48.569 | 53.929 | 57.107 | 59.364 |
| IDS | 1,341 | 1,016 | 773 | 604 |
| FP | 39,274 | 24,892 | 25,394 | 21,400 |
| FN | 24,121 | 25,902 | 25,432 | 25,057 |
| Precision | 54.849 | 64.852 | 64.628 | 68.609 |
| Recall | 66.419 | 63.940 | 64.594 | 65.116 |

Paired headline changes:

- ByteTrack: HOTA `+2.937 [2.356, 3.375]`; MOTA `+17.995 [13.541, 23.282]`; IDF1 `+5.360 [4.490, 6.178]`; IDS `−325 [−498, −164]`; FP `−14,382 [−19,176, −9,620]`; FN `+1,781`; recall `−2.479`.
- OATrack: HOTA `+1.325 [0.200, 2.264]`; MOTA `+6.318 [4.741, 7.879]`; IDF1 `+2.258 [0.548, 3.474]`; IDS `−169 [−292, −42]`; FP `−3,994 [−6,190, −2,494.9]`; FN `−375` with an interval crossing zero.
- Controller time: `4.26 ms/frame` with ByteTrack and `4.20 ms/frame` with OATrack.

### Frozen UAVDT results

| Metric | ByteTrack fixed | ByteTrack AC-MOT | OATrack fixed | OATrack AC-MOT |
|---|---:|---:|---:|---:|
| HOTA | 45.923 | 47.004 | 47.728 | 47.640 |
| MOTA | −1.573 | 16.028 | 19.607 | 22.873 |
| IDF1 | 58.400 | 61.767 | 62.101 | 62.931 |
| IDS | 601 | 486 | 517 | 486 |
| FP | 279,616 | 212,077 | 197,937 | 183,669 |
| FN | 66,050 | 73,702 | 75,612 | 78,774 |
| Precision | 49.571 | 55.751 | 57.270 | 58.800 |
| Recall | 80.625 | 78.381 | 77.820 | 76.893 |

## Paper 2 — SCL

### Fixed method values

- Otsu history: 10 frames; clean if whole-stream median confident share is at least 0.50.
- Noisy ranges: confident `[0.5, 1)` and uncertain `[0.1, 0.5)`; noisy matching and birth thresholds 0.50.
- Rank memory: 20 sampled frames, first frame and every tenth frame.
- Duplicate and recovery IoU: 0.50; rescued score: host's lowest usable score plus 0.001.
- Motion: quarter-resolution phase correlation; 100-frame history; 5-frame warm-up; tolerance cap 0.95.
- Evaluation: TrackEval commit `12c8791`; 10,000 whole-sequence paired bootstrap resamples; seed 42.

### MOT17

- Identical output: BoostTrack online HOTA 68.49; BoostTrack + GBI HOTA 71.73; ByteTrack floor 0.10 HOTA 67.70.
- OC-SORT floor 0.01: HOTA `66.43 → 67.04`, change `+0.61 [0.36, 1.24]`; MOTA `74.67 → 75.94`, `+1.27 [0.17, 3.01]`; IDS `211 → 203`, `−8 [−15, −2]`.
- OC-SORT floor 0.10: HOTA `66.44 → 66.91`, `+0.46 [0.27, 1.09]`; MOTA `74.67 → 75.93`, `+1.26 [0.37, 3.34]`; IDF1 `78.05 → 78.33`, `+0.287 [0.003, 0.838]`.

### KITTI cross-detector results

- ByteTrack + RT-DETR-L: HOTA `50.73 → 51.64`, `+0.91 [0.22, 1.55]`; MOTA `47.27 → 53.24`, `+5.98 [1.16, 9.94]`; IDF1 `64.98 → 68.86`, `+3.87 [1.67, 5.06]`; IDS `686 → 389`, `−297 [−530, −122]`.
- BoT-SORT + RT-DETR-L: MOTA `48.25 → 56.11`, `+7.86 [2.21, 13.44]`; IDF1 `67.74 → 70.85`, `+3.10 [1.00, 4.57]`; IDS `476 → 250`, `−226 [−369, −120]`. Sequence 0020 is omitted from both runs because the host code stops with a numerical error.
- OC-SORT + YOLOv8n: HOTA `36.27 → 44.18`, `+7.91 [5.47, 9.98]`; MOTA `33.99 → 43.39`, `+9.40 [1.10, 12.30]`; IDF1 `50.46 → 60.05`, `+9.60 [5.61, 12.16]`; FN decrease 5,310.

### Score transformations

| Host | Transform | Host HOTA | SCL HOTA | Change [95% interval] |
|---|---|---:|---:|---|
| ByteTrack | cube | 60.92 | 65.81 | +4.89 [2.60, 13.69] |
| ByteTrack | half | 0.00 | 66.17 | +66.17 [49.32, 75.40] |
| ByteTrack | T = 2 | 65.84 | 66.95 | +1.11 [0.35, 3.87] |
| OC-SORT | cube | 58.34 | 66.60 | +8.26 [5.86, 16.81] |
| OC-SORT | half | 0.00 | 66.72 | +66.72 [50.32, 75.56] |
| OC-SORT | T = 2 | 65.99 | 67.22 | +1.24 [0.52, 3.42] |
| BoostTrack | cube | 61.33 | 64.84 | +3.51 [0.85, 13.28] |
| BoostTrack | T = 2 | 67.59 | 67.59 | identical |

### Baselines, ablation and sensitivity

- SCL minus the stronger `t₂` baseline: OC-SORT/YOLOv8n `+3.09 [2.00, 4.03]`; halved RT-DETR-L/ByteTrack `+2.29 [0.28, 4.96]`; halved YOLOv8n/OC-SORT `+2.74 [1.32, 3.34]`.
- SCL minus ACT HOTA: KITTI halved RT-DETR-L/ByteTrack `+2.01 [0.01, 4.76]`; KITTI halved YOLOv8n/OC-SORT `+10.06 [6.88, 12.01]`; UAVDT YOLOv8n/ByteTrack `+1.82 [0.65, 3.00]`.
- UAVDT RT-DETR-L: SCL versus ACT MOTA `+22.65 [9.03, 47.21]`; IDS `−418 [−718, −123]`.
- Largest ablation losses: recovery 3.35 HOTA; noisy mode 2.44; remapping 1.67; motion tolerance 0.14.
- Largest sensitivity changes: Otsu window 0.56; mode-history choice 0.36; duplicate/recovery IoU 0.62; motion history 0.09.

### Frozen external tests

- PD-SORT: HOTA `68.01 → 68.62`, `+0.61 [0.27, 1.65]`; MOTA `75.19 → 76.31`, `+1.13 [0.27, 3.03]`; IDF1 `81.03 → 81.85`, `+0.82 [0.43, 1.94]`.
- Hybrid-SORT: HOTA 66.70, MOTA 75.52, IDF1 77.56 and IDS 259 are identical with SCL.
- UAVDT RT-DETR-L + ByteTrack: MOTA `3.29 → 27.99`, `+24.70 [10.06, 51.08]`; IDF1 `48.59 → 54.33`, `+5.74 [0.13, 13.11]`; IDS `1,041 → 455`, `−586 [−951, −248]`.
- UAVDT YOLOv8n + ByteTrack: HOTA `29.05 → 30.83`, `+1.77 [0.70, 2.94]`; IDF1 `34.52 → 38.49`, `+3.97 [1.88, 6.17]`; IDS `719 → 393`, `−326 [−691, −73]`.

### Runtime

- SCL: 2.95 ms/frame; detector: 42 ms/frame; tracker alone: 2.04 ms/frame; tracker after SCL filtering: 1.43 ms/frame; end-to-end increase: 4.5%.
- Timing hardware and sample: 4-vCPU Intel Xeon at 2.10 GHz, YOLOv8n + ByteTrack, three KITTI sequences, 2,279 timed frames.
