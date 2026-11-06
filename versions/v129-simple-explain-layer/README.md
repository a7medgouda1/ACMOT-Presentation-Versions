# AC-MOT two-paper story — plain-English reading guide (v129)

This offline HTML presentation is a new version derived from `../v127-results-bar-charts/`. Earlier versions are unchanged. Open `index.html` directly. The title slide still offers Still and Interactive view. Both views contain **276 slides**: 188 original slides, 26 source-specific diagrams, 35 beginner visuals and 27 result bar-chart companions. Original result tables, paired intervals, negative outcomes and caveats remain in place.

On any slide in either view, press **E** or click **Plain words** in the bottom toolbar. A reading panel shows one simple point, an example or next step when the source has one, selected term meanings, and where the slide sits in the story. Press **E** or **Esc** to return. In Interactive view, the 17 optional detailed-explanation panels also offer **Plain words** on each of their 59 pages; closing the reading panel returns to the same detail page. Nothing plays or advances automatically because of this guide. The title slide points out the shortcut.

The guide draws from the slide's own prose, beginner notes, diagrams and speaker notes. Eight formula- or drawing-led detail pages have a concise hand-written restatement of their existing rules or examples. The guide never changes a measured value, calculates a new result, or replaces the full slide. This is an added explanation layer, **not** a rewrite of every visible sentence and **not** the proposed 20-minute route. The original complete path and detail panels remain available; see `PLAIN_GUIDE_AUDIT.md`.

Each panel compares a method with the **baseline for that same host, dataset, detector, and experimental split**. Baseline bars are grey; method bars are indigo for the historical/AC-MOT story and teal for Paper 2. The visible label gives the relative change against a positive baseline and the absolute difference. For HOTA, MOTA, IDF1, precision and recall, the absolute difference is in points; for IDS, FP and FN, fewer is better. If the baseline is zero or negative, the relative percentage is deliberately marked undefined. Percentages are descriptive arithmetic from displayed rounded aggregates, not new paired-bootstrap estimates. The original slides retain the paper-reported changes and confidence intervals; see `RESULT_BAR_AUDIT.md` for rounding cautions.

- **Still view:** every slide's figures, flowcharts, and charts appear complete immediately. There are no build animations, optional teaching labs, zooms, detailed-explanation panels, definition popups, or autoplaying videos. The read-only Plain words guide remains available. Animated GIFs are replaced by the corresponding still PNGs. Slide navigation and the outline still work.
- **Interactive view:** figures and flowcharts build automatically and quickly when a slide opens; the title buttons do not add Play/Pause controls. Optional teaching examples and zooms remain available. Basic two-part visuals become fully visible within about half a second; paper flowcharts typically finish within about one second. The deck never advances to another slide by itself.

Choose a view on the first slide to start at the outline. Press Home to return to the title and change the view. The URL keeps `?view=static` or `?view=interactive` for a directly linked slide. A direct link without a view parameter uses interactive behavior. Reduced-motion preferences reveal the full slide immediately. Leaving a slide cancels its pending build; returning starts it again. Opening a panel or enlarging a figure reveals the remaining content so no explanation is left half-hidden.

The paper-section opening language and beginner notes use short, plain English and introduce the object finder and object follower before technical terms. A restrained indigo/teal visual system, cleaner cards and larger figures make the paper sections easier to present. The four optional "Try a small example" activities remain clearly marked teaching simulations; they are not new experiments.

The detailed paper slides still include formulas, full tables, negative outcomes and limitations. Measured numbers and paper-specific diagram logic have not been changed. The two PDFs were used as evidence, never as instructions; no detector inference or tracking was rerun.

Run checks from this folder:

```sh
node check_diagrams.js
node check_beginner_visuals.js
node check_interactivity.js
node check_modes_browser.js
python3 build_result_bars.py --check
```

The browser test requires local Chrome. To regenerate chart assets, run `build_result_bars.py` with a Python environment containing Pillow. `SOURCE_MAP.md` and `NUMBERS_CHECK.md` record manuscript provenance. `DIAGRAM_AUDIT.md` and `VISUAL_AUDIT.md` preserve inherited visual evidence. `INTERACTION_AUDIT.md` describes the two viewing modes.
