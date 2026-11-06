# Interaction audit — v129

Parent: `../v127-results-bar-charts/`. This version preserves both title-slide viewing modes and adds a read-only Plain words guide for all 276 slides and 59 optional detail pages. Measured values, full paper tables, bar charts, and diagram nodes and arrows remain inherited.

## Still view

- Figures, flowcharts, charts, and text fragments are fully visible on entry. CSS animations and transitions are disabled. The three inherited GIF placements use their still PNG equivalents, and videos do not autoplay.
- Optional teaching labs, zooms, detailed-explanation panels, definition popups, and video tabs are disabled or hidden. The read-only Plain words guide remains available by toolbar button or E. Normal slide navigation and outline links still work. The title's mode buttons remain available for switching.

## Interactive view

- All 35 beginner visuals show the figure immediately, the simple idea at about 0.08 seconds, and the easy example at about 0.34 seconds.
- All 21 node-and-arrow flowcharts start with the leftmost input or earlier-data column visible. Other columns and incoming arrows build in ordered groups, typically completing within about one second. Branches in one column appear together; that does not imply both branches execute in one run.
- Five comparison charts animate their connectors and marks quickly when entered. Their axes and reported values are unchanged.
- Inherited slides with fragment builds also reveal automatically. A right arrow or Space moves to the next slide; it does not have to advance each fragment manually. The presentation never auto-advances to a different slide.
- There are no Play/Pause or step-control buttons. Changing slides cancels pending timers; revisiting restarts the build. Opening an overlay or zoom settles the current build. With reduced motion, all parts appear at once. Print shows all parts.
- Plain words opens on any slide without advancing it. The 17 detailed-explanation panels have the same reading aid on all 59 pages. Esc closes the reading aid first and returns to that detail page, then Esc again returns to the main slide.

## Teaching examples

| Example | Rule shown | Boundary and caveat |
|---|---|---|
| Paper 1 target | Eq. 17: HIGH if SCI > 0.511 or tiny share > 0.50; else MEDIUM if SCI > 0.297; else LOW | The toy omits the separately explained scene-label, recovery, hold and dwell rules. It shows the proposed target only. |
| Paper 2 score gate | Box score ≥ an illustrative 0.70 gate can start a new track | The gate and example score are made up; existing-track matching may use another gate. |
| Paper 2 mode | No valid past split → COLD; otherwise median confident share ≥ 0.50 → CLEAN, else NOISY | The median is illustrative and does not use a future frame. |
| Paper 2 remap | Eq. 8: uncertain → 0.10 + 0.40u; confident → 0.50 + 0.50u | NOISY mode only; background-like boxes are removed first. Example ranks are illustrative. |

`check_interactivity.js` checks the UI structure and exact rule boundaries. `check_diagrams.js` and `check_beginner_visuals.js` check diagram/asset ordering and provenance. `build_result_bars.py --check` verifies source-slide numbers and 27 generated images. `check_modes_browser.js` clicks both title buttons, checks still/interactive behavior, all guide entries and detail-page return navigation, and verifies representative result charts load and fit. A guide screenshot was inspected at 1600×900.
