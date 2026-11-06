# Paper Presentation v01

This presentation is derived from:

`v88-big-presentation-hybrid-buttons`

`v88` closes the historical Big Presentation series. `v01` starts the
journal-paper-aligned Paper Presentation series.

## Scientific focus

The presentation is aligned with the final attribution story:

> Calibration Versus Scene Switching of Detector Operating Points for Aerial
> Multi-Object Tracking

It keeps the educational foundation and development history from the Big
Presentation, then asks the central journal-paper question: how much of the
improvement over the default comes from a better calibrated operating point,
and how much comes from frame-to-frame switching?

## Major changes from v88

- Reframes historical V1 as **Quality profile Q** and V2 as **Balanced profile B**.
- Preserves the pre-Optuna screening, temporal sweep, Optuna and bootstrap explanations.
- Adds the held-out matched static anchor and the calibration decomposition.
- Adds the separate cue-utility audit and its compute-budget qualification.
- Rewrites U2MOT using the post-hoc TrackEval HOTA rescore and removes the unsupported held-out speed claim.
- Adds the SparseTrack validation-only comparison with both static comparators.
- Adds the ByteTrack implementation caveat and paper-aligned limitations.
- Replaces the final contributions and conclusion with the calibration-versus-switching finding.
- Centralizes the critical paper numbers in `assets/data/results.js` and checks them at load time.

## Evidence labels

Numerical slides distinguish historical development, validation, held-out,
post-hoc attribution, supplementary cross-pipeline evidence and exploratory
audit evidence. The custom VisDrone evaluation is class-agnostic and is not an
official leaderboard result.

## Run locally

Open `index.html` directly, or serve this folder with a small local HTTP server.
All presentation assets are local and the deck does not require an external CDN.
