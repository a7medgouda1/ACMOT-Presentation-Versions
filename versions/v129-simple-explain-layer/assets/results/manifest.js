window.ACMOT_RESULT_BARS = [
  {
    "id": "old-ablation",
    "after": "Ablation result",
    "title": "Original AC-MOT: validation bars",
    "intro": "The full original controller improves tracking quality but costs some speed.",
    "source": "Original AC-MOT ablation · VisDrone validation · source result table",
    "note": "This is the original component study, not the later frozen test set.",
    "image": "assets/results/old-ablation.png",
    "alt": "MOTA: 17.633 to 18.165, 3.0% higher vs baseline; HOTA: 29.837 to 33.064, 10.8% higher vs baseline; IDF1: 30.892 to 36.296, 17.5% higher vs baseline; IDS: 283 to 271, 4.2% fewer vs baseline"
  },
  {
    "id": "old-test",
    "after": "Old AC-MOT on the test set",
    "title": "Original AC-MOT: held-out bars",
    "intro": "The original controller beats the fixed baseline on the 17 test videos.",
    "source": "Historical VisDrone test-dev · assets/data/results.js · testdev.rows",
    "note": "Different from the paper's later YOLO11m experiment. Speed is in the preceding table.",
    "image": "assets/results/old-test.png",
    "alt": "MOTA: 19.729 to 23.236, 17.8% higher vs baseline; HOTA: 28.43 to 32.698, 15.0% higher vs baseline; IDF1: 32.724 to 39.516, 20.8% higher vs baseline; IDS: 1,235 to 1,061, 14.1% fewer vs baseline"
  },
  {
    "id": "v1-test",
    "after": "V1 on the test set",
    "title": "V1: quality gains vs fixed baseline",
    "intro": "Frozen Trial 24 gives the largest quality gain on VisDrone test-dev.",
    "source": "Historical VisDrone test-dev · assets/data/results.js · testdev.rows",
    "note": "The ID-switch difference is not statistically secure; see the paired interval slide.",
    "image": "assets/results/v1-test.png",
    "alt": "MOTA: 19.729 to 26.948, 36.6% higher vs baseline; HOTA: 28.43 to 33.835, 19.0% higher vs baseline; IDF1: 32.724 to 41.546, 27.0% higher vs baseline; IDS: 1,235 to 1,184, 4.1% fewer vs baseline"
  },
  {
    "id": "v2-test",
    "after": "V2 on the test set",
    "title": "V2: identity gains vs fixed baseline",
    "intro": "Frozen Trial 22 improves over baseline; V1 remains better on quality.",
    "source": "Historical VisDrone test-dev · assets/data/results.js · testdev.rows",
    "note": "Compare V1 and V2 separately: V2 trades some quality for fewer switches and more speed.",
    "image": "assets/results/v2-test.png",
    "alt": "MOTA: 19.729 to 23.792, 20.6% higher vs baseline; HOTA: 28.43 to 31.218, 9.8% higher vs baseline; IDF1: 32.724 to 37.87, 15.7% higher vs baseline; IDS: 1,235 to 919, 25.6% fewer vs baseline"
  },
  {
    "id": "uav-v1",
    "after": "UAVDT with zero tuning",
    "title": "UAVDT: V1 vs its own baseline",
    "intro": "The frozen quality profile also works on unseen drone videos.",
    "source": "Historical UAVDT external test · assets/data/results.js · uavdt.rows",
    "note": "Quality and IDs improve, but V1 is slower than the UAVDT baseline.",
    "image": "assets/results/uav-v1.png",
    "alt": "MOTA: 13.841 to 17.399, 25.7% higher vs baseline; HOTA: 24.085 to 28.39, 17.9% higher vs baseline; IDF1: 27.887 to 34.453, 23.5% higher vs baseline; IDS: 558 to 321, 42.5% fewer vs baseline"
  },
  {
    "id": "uav-v2",
    "after": "UAVDT with zero tuning",
    "title": "UAVDT: V2 vs its own baseline",
    "intro": "The frozen identity profile also works on unseen drone videos.",
    "source": "Historical UAVDT external test · assets/data/results.js · uavdt.rows",
    "note": "Both frozen profiles improve over baseline; V1 has higher quality, V2 fewer switches.",
    "image": "assets/results/uav-v2.png",
    "alt": "MOTA: 13.841 to 16.118, 16.5% higher vs baseline; HOTA: 24.085 to 26.93, 11.8% higher vs baseline; IDF1: 27.887 to 32.014, 14.8% higher vs baseline; IDS: 558 to 308, 44.8% fewer vs baseline"
  },
  {
    "id": "u2-val",
    "after": "U2MOT validation comparison",
    "title": "U2MOT validation: a mixed result",
    "intro": "Quality and false alarms improve, while missed objects increase.",
    "source": "U2MOT transfer · VisDrone validation · source result table",
    "note": "The missed-object count rises from 7,091 to 7,726; this trade-off remains visible.",
    "image": "assets/results/u2-val.png",
    "alt": "MOTA: 75.1273 to 75.4738, 0.46% higher vs baseline; IDF1: 75.5578 to 76.5775, 1.3% higher vs baseline; IDS: 1,947 to 1,908, 2.0% fewer vs baseline; FP: 8,837 to 7,992, 9.6% fewer vs baseline"
  },
  {
    "id": "u2-test",
    "after": "U2MOT final test",
    "title": "U2MOT final test: fewer IDs and FP",
    "intro": "MOTA slips slightly; identity switches and false alarms fall.",
    "source": "U2MOT transfer · frozen VisDrone test-dev · source result table",
    "note": "Missed objects rise from 63,241 to 64,801. Do not describe this as an overall win.",
    "image": "assets/results/u2-test.png",
    "alt": "MOTA: 53.9 to 53.7668, 0.25% lower vs baseline; IDF1: 69.8 to 69.8494, 0.07% higher vs baseline; IDS: 1,239 to 1,152, 7.0% fewer vs baseline; FP: 41,385 to 40,155, 3.0% fewer vs baseline"
  },
  {
    "id": "p1-vis-bt-quality",
    "after": "Paper 1 full VisDrone results",
    "title": "Paper 1: ByteTrack quality on VisDrone",
    "intro": "The frozen controller improves three quality scores and reduces ID switches.",
    "source": "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
    "note": "MOTA's relative percentage is large because the fixed MOTA starts at 9.876.",
    "image": "assets/results/p1-vis-bt-quality.png",
    "alt": "HOTA: 41.586 to 44.523, 7.1% higher vs baseline; MOTA: 9.876 to 27.871, 182.2% higher vs baseline; IDF1: 48.569 to 53.929, 11.0% higher vs baseline; IDS: 1,341 to 1,016, 24.2% fewer vs baseline"
  },
  {
    "id": "p1-vis-bt-errors",
    "after": "Paper 1 full VisDrone results",
    "title": "Paper 1: ByteTrack errors and recall",
    "intro": "Fewer false alarms come with more missed objects and lower recall.",
    "source": "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
    "note": "A lower FP count is good; a higher FN count is a real cost.",
    "image": "assets/results/p1-vis-bt-errors.png",
    "alt": "FP: 39,274 to 24,892, 36.6% fewer vs baseline; FN: 24,121 to 25,902, 7.4% more vs baseline; Precision: 54.849 to 64.852, 18.2% higher vs baseline; Recall: 66.419 to 63.94, 3.7% lower vs baseline"
  },
  {
    "id": "p1-vis-oa-quality",
    "after": "Paper 1 full VisDrone results",
    "title": "Paper 1: OATrack quality on VisDrone",
    "intro": "The same frozen controller improves a second tracker too.",
    "source": "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
    "note": "OATrack starts stronger than ByteTrack; compare each host only with its own fixed run.",
    "image": "assets/results/p1-vis-oa-quality.png",
    "alt": "HOTA: 46.77 to 48.095, 2.8% higher vs baseline; MOTA: 28.165 to 34.483, 22.4% higher vs baseline; IDF1: 57.107 to 59.364, 4.0% higher vs baseline; IDS: 773 to 604, 21.9% fewer vs baseline"
  },
  {
    "id": "p1-vis-oa-errors",
    "after": "Paper 1 full VisDrone results",
    "title": "Paper 1: OATrack errors and recall",
    "intro": "False alarms, misses and ID switches all fall for OATrack.",
    "source": "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
    "note": "The OATrack FN interval crosses zero, so avoid a strong claim about that decrease.",
    "image": "assets/results/p1-vis-oa-errors.png",
    "alt": "FP: 25,394 to 21,400, 15.7% fewer vs baseline; FN: 25,432 to 25,057, 1.5% fewer vs baseline; Precision: 64.628 to 68.609, 6.2% higher vs baseline; Recall: 64.594 to 65.116, 0.81% higher vs baseline"
  },
  {
    "id": "p1-uav-bt-quality",
    "after": "Paper 1 full UAVDT results",
    "title": "Paper 1: ByteTrack quality on UAVDT",
    "intro": "The frozen controller raises MOTA from a negative starting score.",
    "source": "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
    "note": "MOTA relative % is undefined because its fixed baseline is negative; +17.601 points is valid.",
    "image": "assets/results/p1-uav-bt-quality.png",
    "alt": "HOTA: 45.923 to 47.004, 2.4% higher vs baseline; MOTA: -1.573 to 16.028, Relative % undefined: baseline is zero or negative; IDF1: 58.4 to 61.767, 5.8% higher vs baseline; IDS: 601 to 486, 19.1% fewer vs baseline"
  },
  {
    "id": "p1-uav-bt-errors",
    "after": "Paper 1 full UAVDT results",
    "title": "Paper 1: ByteTrack UAVDT trade-off",
    "intro": "False alarms fall, but missed objects rise and recall falls.",
    "source": "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
    "note": "This is an external test with no retuning; selectivity costs must remain visible.",
    "image": "assets/results/p1-uav-bt-errors.png",
    "alt": "FP: 279,616 to 212,077, 24.2% fewer vs baseline; FN: 66,050 to 73,702, 11.6% more vs baseline; Precision: 49.571 to 55.751, 12.5% higher vs baseline; Recall: 80.625 to 78.381, 2.8% lower vs baseline"
  },
  {
    "id": "p1-uav-oa-quality",
    "after": "Paper 1 full UAVDT results",
    "title": "Paper 1: OATrack quality on UAVDT",
    "intro": "MOTA and IDF1 rise, while HOTA is almost unchanged.",
    "source": "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
    "note": "HOTA falls slightly; do not call it an improvement.",
    "image": "assets/results/p1-uav-oa-quality.png",
    "alt": "HOTA: 47.728 to 47.64, 0.18% lower vs baseline; MOTA: 19.607 to 22.873, 16.7% higher vs baseline; IDF1: 62.101 to 62.931, 1.3% higher vs baseline; IDS: 517 to 486, 6.0% fewer vs baseline"
  },
  {
    "id": "p1-uav-oa-errors",
    "after": "Paper 1 full UAVDT results",
    "title": "Paper 1: OATrack UAVDT trade-off",
    "intro": "False alarms fall, but missed objects rise and recall falls.",
    "source": "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
    "note": "Both paper hosts have the same missed-object direction on UAVDT.",
    "image": "assets/results/p1-uav-oa-errors.png",
    "alt": "FP: 197,937 to 183,669, 7.2% fewer vs baseline; FN: 75,612 to 78,774, 4.2% more vs baseline; Precision: 57.27 to 58.8, 2.7% higher vs baseline; Recall: 77.82 to 76.893, 1.2% lower vs baseline"
  },
  {
    "id": "p2-mot17",
    "after": "Paper 2 MOT17 results",
    "title": "Paper 2: MOT17 host comparison",
    "intro": "SCL helps OC-SORT while compatible two-stage hosts stay unchanged.",
    "source": "Paper2_V71.pdf · MOT17 result table · NUMBERS_CHECK.md",
    "note": "The first three panels use floor 0.01; the last uses floor 0.10. Rounded HOTA bars differ by 0.47, while the paper reports 0.46.",
    "image": "assets/results/p2-mot17.png",
    "alt": "HOTA · floor .01: 66.43 to 67.04, 0.92% higher vs baseline; MOTA · floor .01: 74.67 to 75.94, 1.7% higher vs baseline; IDS · floor .01: 211 to 203, 3.8% fewer vs baseline; HOTA · floor .10: 66.44 to 66.91, 0.71% higher vs baseline"
  },
  {
    "id": "p2-kitti-bt",
    "after": "Paper 2 KITTI RT-DETR results",
    "title": "Paper 2: KITTI RT-DETR + ByteTrack",
    "intro": "SCL helps the tracker use a replacement detector's scores.",
    "source": "Paper2_V71.pdf · KITTI RT-DETR-L table · NUMBERS_CHECK.md",
    "note": "Only the score interface changes. Small point-difference rounding may differ from the paper's paired estimates.",
    "image": "assets/results/p2-kitti-bt.png",
    "alt": "HOTA: 50.73 to 51.64, 1.8% higher vs baseline; MOTA: 47.27 to 53.24, 12.6% higher vs baseline; IDF1: 64.98 to 68.86, 6.0% higher vs baseline; IDS: 686 to 389, 43.3% fewer vs baseline"
  },
  {
    "id": "p2-kitti-bot",
    "after": "Paper 2 KITTI RT-DETR results",
    "title": "Paper 2: KITTI RT-DETR + BoT-SORT",
    "intro": "SCL improves quality and reduces ID switches for this host too.",
    "source": "Paper2_V71.pdf · KITTI RT-DETR-L table · NUMBERS_CHECK.md",
    "note": "Sequence 0020 is excluded from both runs because the host stops with a numerical error.",
    "image": "assets/results/p2-kitti-bot.png",
    "alt": "MOTA: 48.25 to 56.11, 16.3% higher vs baseline; IDF1: 67.74 to 70.85, 4.6% higher vs baseline; IDS: 476 to 250, 47.5% fewer vs baseline"
  },
  {
    "id": "p2-kitti-oc",
    "after": "Paper 2 KITTI OC-SORT results",
    "title": "Paper 2: KITTI YOLOv8n + OC-SORT",
    "intro": "SCL recovers useful weak boxes for a single-stage tracker.",
    "source": "Paper2_V71.pdf · KITTI OC-SORT table · NUMBERS_CHECK.md",
    "note": "False negatives fall by 5,310. The paper reports IDF1 +9.60; rounded bar values differ by 9.59.",
    "image": "assets/results/p2-kitti-oc.png",
    "alt": "HOTA: 36.27 to 44.18, 21.8% higher vs baseline; MOTA: 33.99 to 43.39, 27.7% higher vs baseline; IDF1: 50.46 to 60.05, 19.0% higher vs baseline"
  },
  {
    "id": "p2-score-shift",
    "after": "Paper 2 score shift robustness",
    "title": "Paper 2: repair a shifted score scale",
    "intro": "Changing score values without changing their order can break a host.",
    "source": "Paper2_V71.pdf · score-transform table · NUMBERS_CHECK.md",
    "note": "For 0.5s, the host HOTA is zero; relative percentages are undefined, not infinite.",
    "image": "assets/results/p2-score-shift.png",
    "alt": "ByteTrack · s³ HOTA: 60.92 to 65.81, 8.0% higher vs baseline; OC-SORT · s³ HOTA: 58.34 to 66.6, 14.2% higher vs baseline; ByteTrack · 0.5s HOTA: 0 to 66.17, Relative % undefined: baseline is zero or negative; OC-SORT · 0.5s HOTA: 0 to 66.72, Relative % undefined: baseline is zero or negative"
  },
  {
    "id": "p2-otsu",
    "after": "Paper 2 Otsu baselines",
    "title": "Paper 2: SCL vs a simple threshold",
    "intro": "SCL beats the stronger simple threshold in all three KITTI cells.",
    "source": "Paper2_V71.pdf · Otsu comparator table · NUMBERS_CHECK.md",
    "note": "Each panel compares SCL with that same cell's t2 baseline; cells are not pooled.",
    "image": "assets/results/p2-otsu.png",
    "alt": "OC-SORT · YOLOv8n HOTA: 41.09 to 44.18, 7.5% higher vs baseline; ByteTrack · half RT-DETR HOTA: 49.5 to 51.79, 4.6% higher vs baseline; OC-SORT · half YOLOv8n HOTA: 43.56 to 46.3, 6.3% higher vs baseline"
  },
  {
    "id": "p2-act",
    "after": "Paper 2 ACT comparison",
    "title": "Paper 2: SCL vs the ACT comparator",
    "intro": "SCL is higher in all three reported HOTA comparisons.",
    "source": "Paper2_V71.pdf · ACT comparison table · NUMBERS_CHECK.md",
    "note": "Each cell uses its own ACT result. The first rounded bars differ by 2.02, while the paper reports +2.01.",
    "image": "assets/results/p2-act.png",
    "alt": "KITTI · ByteTrack HOTA: 49.77 to 51.79, 4.1% higher vs baseline; KITTI · OC-SORT HOTA: 36.24 to 46.3, 27.8% higher vs baseline; UAVDT · ByteTrack HOTA: 29.01 to 30.83, 6.3% higher vs baseline; UAVDT RT-DETR · MOTA: 5.34 to 27.99, 424.2% higher vs baseline"
  },
  {
    "id": "p2-pd",
    "after": "Paper 2 unseen trackers",
    "title": "Paper 2: PD-SORT on MOT17",
    "intro": "A predeclared unseen single-stage host improves with SCL.",
    "source": "Paper2_V71.pdf · frozen PD-SORT test · NUMBERS_CHECK.md",
    "note": "All seven sequences improve in HOTA. Rounded MOTA bars differ by 1.12; the paper reports +1.13.",
    "image": "assets/results/p2-pd.png",
    "alt": "HOTA: 68.01 to 68.62, 0.90% higher vs baseline; MOTA: 75.19 to 76.31, 1.5% higher vs baseline; IDF1: 81.03 to 81.85, 1.0% higher vs baseline"
  },
  {
    "id": "p2-hybrid",
    "after": "Paper 2 unseen trackers",
    "title": "Paper 2: Hybrid-SORT stays unchanged",
    "intro": "A compatible two-stage host produces identical output with SCL.",
    "source": "Paper2_V71.pdf · frozen Hybrid-SORT test · NUMBERS_CHECK.md",
    "note": "No measured gain is the intended compatibility result for this host.",
    "image": "assets/results/p2-hybrid.png",
    "alt": "HOTA: 66.7 to 66.7, 0% change vs baseline; MOTA: 75.52 to 75.52, 0% change vs baseline; IDF1: 77.56 to 77.56, 0% change vs baseline; IDS: 259 to 259, 0% change vs baseline"
  },
  {
    "id": "p2-uav-rtdetr",
    "after": "Paper 2 UAVDT results",
    "title": "Paper 2: UAVDT RT-DETR + ByteTrack",
    "intro": "Frozen SCL transfers to unseen drone videos with a replacement detector.",
    "source": "Paper2_V71.pdf · UAVDT RT-DETR-L test · NUMBERS_CHECK.md",
    "note": "The MOTA baseline is only 3.29; the large relative percentage needs its +24.70-point context.",
    "image": "assets/results/p2-uav-rtdetr.png",
    "alt": "MOTA: 3.29 to 27.99, 750.8% higher vs baseline; IDF1: 48.59 to 54.33, 11.8% higher vs baseline; IDS: 1,041 to 455, 56.3% fewer vs baseline"
  },
  {
    "id": "p2-uav-yolo",
    "after": "Paper 2 UAVDT results",
    "title": "Paper 2: UAVDT YOLOv8n + ByteTrack",
    "intro": "The same frozen layer also helps a second detector–host pair.",
    "source": "Paper2_V71.pdf · UAVDT YOLOv8n test · NUMBERS_CHECK.md",
    "note": "Rounded HOTA bars differ by 1.78; the paper reports +1.77. Its paired interval remains on the preceding slide.",
    "image": "assets/results/p2-uav-yolo.png",
    "alt": "HOTA: 29.05 to 30.83, 6.1% higher vs baseline; IDF1: 34.52 to 38.49, 11.5% higher vs baseline; IDS: 719 to 393, 45.3% fewer vs baseline"
  }
];
