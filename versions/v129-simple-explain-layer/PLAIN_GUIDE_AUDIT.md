# Plain-English reading guide audit — v129

Parent: `../v127-results-bar-charts/`. This version adds a non-destructive reading layer. The 276-slide main sequence, 17 optional detailed-explanation panels (59 pages), paper figures, results and source-linked bar charts are retained.

## Coverage and interaction

- Every main slide has one guide entry with a simple point and a section-level story position. The guide is available in both Still and Interactive views through the toolbar or E key.
- Every optional detail page has one guide entry in Interactive view. The Plain words button and E key work inside the detail panel; Esc returns to that page before closing the detail panel.
- Guides reuse existing authored beginner notes, diagram notes, chart introductions, main-idea text, speaker notes, examples and caution labels where present. Eight detail pages led by equations, tables or drawings have short human-written restatements of the rule already visible on that page.
- The guide labels an example or next step only when one is available. It does not invent an experiment, calculate a metric, or state that one comparison's baseline applies to another.

## Scientific and presentation boundary

All original numbers, formulas, comparison groups, negative outcomes, confidence intervals and source labels remain on the slides. The Plain words panel is a way into the material, not a substitute for the complete technical slide or paper. The 27 v127 result bars and their rounding/zero-baseline caveats are unchanged. No inference, tracking, retuning or new experiment was run.

This version does **not** rewrite every sentence on the 276 slides and does **not** create the optional 20-minute route proposed during the earlier work. The full presentation remains long and should be rehearsed or curated to match the actual talk time.

## Checks

`check_modes_browser.js` asserts all 276 slide guides and all 59 detail-page guides are populated from authored content, exercises E and the toolbar button in both viewing modes, checks return navigation inside a detail panel, and verifies representative source-checked bar charts still render and fit. `check_diagrams.js`, `check_beginner_visuals.js`, `check_interactivity.js`, and `build_result_bars.py --check` preserve inherited visual, rule and result checks.
