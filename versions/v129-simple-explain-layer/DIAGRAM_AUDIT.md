# Diagram audit — v123 (26 diagrams inherited from v122)

Each listed visual is inserted immediately after the teaching slide named below. Shapes and arrows are explanatory redrawings of the manuscript logic, not screenshots or new experimental results. `diagrams.js` contains the hand-authored nodes and paths. `diagrams.css` contains only layout and styling.

| Teaching slide | Visual focus | Manuscript evidence |
|---|---|---|
| Paper 1 complete map | Current frame and previous tracks feed the controller; settings affect the frozen detector and tracker | Figure 1, PDF p. 9 |
| Paper 1 analysis schedule | Analysis-frame yes/no branch; action still used every frame | Algorithm 1, PDF p. 13 |
| Paper 1 SCI | Crowd-only seven-step SCI; tiny and image checks separate | Eqs. 13–16, PDF pp. 9–10 |
| Paper 1 scene labels | Night → blur → tiny → crowded → clear priority | Eq. 16, PDF p. 10 |
| Paper 1 target state | HIGH test before MEDIUM test, else LOW | Eq. 17, PDF p. 11 |
| Paper 1 recovery probe | Collapse check, three-step limit and non-collapse reset | Eqs. 18–19, PDF p. 11 |
| Paper 1 hysteresis | Holds only downward moves near their thresholds | Eq. 20, PDF p. 12 |
| Paper 1 dwell rule | State-change gate at 30 frames | Eq. 21, PDF p. 12 |
| Paper 1 action map | Exact LOW/MEDIUM/HIGH triplets, all selected together | Table 2, PDF p. 13 |
| Paper 1 final protocol | Development selection before frozen VisDrone and UAVDT evaluation | Sect. IV, PDF pp. 14–20 |
| Paper 1 full VisDrone results | HOTA only, fixed versus AC-MOT, ByteTrack and OATrack | Main results table, PDF p. 20 |
| Paper 1 full UAVDT results | HOTA only, including OATrack's slight negative change | Transfer results table, PDF p. 22 |
| Paper 2 complete map | Frozen detector → SCL → frozen host; past-state and host-contract inputs | Figure 1, PDF p. 4 |
| Paper 2 nested Otsu | Prior 10-frame window; current box application; history update after host | Sect. 3.2, Algorithm 1, PDF pp. 4–8 |
| Paper 2 mode rule | Cold when no valid split, else clean/noisy by median ρ | Sect. 3.3, Algorithm 1, PDF pp. 5–8 |
| Paper 2 clean mode thresholds | Cross-class deduplication, raw scores, threshold caps only when clean | Eq. 7, Algorithm 1, PDF pp. 5–8 |
| Paper 2 noisy mode remapping | Track-aware deduplication, background removal, separate rank bands | Eq. 8, Algorithm 1, PDF pp. 5–8 |
| Paper 2 duplicate handling | Keep overlapping people when distinct previous tracks support them | Sect. 3.4, PDF p. 6 |
| Paper 2 weak detection recovery | Eligibility decision and minimal score lift | Sect. 3.5, PDF p. 6 |
| Paper 2 motion tolerance | Noisy-only branch; otherwise mₜ = m₀ | Eq. 9, Algorithm 1, PDF pp. 6–8 |
| Paper 2 full algorithm | Two visuals: branch/merge, then host update before memory writes | Algorithm 1, PDF p. 8 |
| Paper 2 freezing and tests | Development, repair, tests, frozen external assessment | Sects. 4.3 and 5.6–5.7, PDF pp. 8–13 |
| Paper 2 MOT17 results | OC-SORT HOTA only at two score floors | Table 7, PDF pp. 9–10 |
| Paper 2 score shift robustness | HOTA only for controlled halved-score tests | Table 9, PDF pp. 10–11 |
| Paper 2 unseen trackers | HOTA only for PD-SORT and identical Hybrid-SORT output | Table 13a, PDF p. 12 |

The numeric charts label their nonzero axis minimum and print both measured values. They should be read within the stated metric and dataset only. The v121 generic charts, including those that mixed HOTA with MOTA or compared unlike timings, are not shown in this version.
