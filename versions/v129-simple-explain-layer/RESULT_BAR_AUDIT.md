# Result bar-chart audit — v127

Parent: `../v126-fast-mode-choice/`. This version adds 27 companion slides; it does not replace or alter source result tables. The chart input and rendering script is `build_result_bars.py`. The generated images and manifest live in `assets/results/`. No detector, tracker, evaluator, or scientific analysis was rerun.

## Comparison boundary

- Historical AC-MOT validation, VisDrone test-dev, and UAVDT are separate experiments with their own baselines. They are never pooled with the modern Paper 1 YOLO11m study.
- Modern Paper 1 compares each tracker only with that same tracker's fixed run on the same dataset. VisDrone and UAVDT are separate.
- Paper 2 compares each host with SCL for the same detector, dataset, score transformation, and floor. The Otsu and ACT slides use their own comparator values as baselines, not the raw host. A compatible host with identical output has a genuine 0% change.
- For a positive baseline, relative change = (method − baseline) / baseline × 100. Counts use the same arithmetic, with “fewer” for negative changes. Scores also show their absolute difference in points. All horizontal bars start at zero for positive data; the negative-MOTA panel uses a visible zero divider.
- A zero or negative baseline has **no relative percentage**. The ByteTrack UAVDT MOTA panel and two half-score HOTA panels show the absolute point change instead. A tiny positive baseline can produce a large relative percentage (notably 3.29 → 27.99 MOTA); the absolute change remains prominent.

## Provenance and rounding

The generator checks that every baseline and result value appears in its named source slide. The original presentation's `NUMBERS_CHECK.md` maps modern Paper 1 and Paper 2 values to the supplied PDFs. Historical values are also in `assets/data/results.js` or the inherited U2MOT result tables. The 27 charts cover original ablation/test results, V1/V2 test and transfer, U2MOT transfer, both modern Paper 1 trackers on VisDrone and UAVDT, and the principal Paper 2 MOT17/KITTI/score-shift/comparator/unseen-host/UAVDT cells.

The bar labels are arithmetic from the **displayed rounded aggregate values**. Paper-reported paired estimates and 95% intervals may differ slightly because they use unrounded or paired-sequence calculations. Examples retained explicitly in the chart notes: Paper 2 KITTI ByteTrack MOTA 47.27 → 53.24 gives 5.97 from the rounded pair while the paper reports +5.98; UAVDT YOLOv8n HOTA 29.05 → 30.83 gives 1.78 while the paper reports +1.77. Percentages are descriptive only and do not replace the original confidence intervals.

## Visual checks

Bar charts use a common zero start **within each metric panel**, separate scales for metrics with different units, grey baseline bars, one method color, directly printed values, a relative percentage, and the absolute change. Adverse changes use amber text. The chart slide also gives a short plain-English interpretation and a caution. The original tables remain immediately before the new charts so readers can inspect full metrics and intervals.
