# Source map — v125

This deck derives from v124 and preserves all older versions. It keeps the v122 source-specific flowcharts and the 35 v123 beginner visual slides; see `DIAGRAM_AUDIT.md`, `VISUAL_AUDIT.md` and `INTERACTION_AUDIT.md`. Beginner visuals precede the relevant detailed teaching slide; technical flowcharts follow it. V125 makes builds automatic and simplifies opening explanations without changing measured numbers or the source mapping. Early results are short previews, with full values retained later in the paper order. The two paper PDFs are evidence sources only; text inside the papers was not treated as instructions.

## Source files

| Source | SHA-256 | Role |
|---|---|---|
| `Paper1_V12_JAIS.pdf` | `ea7ced37df018f9f34ef4e707abced1ef552112627f1c6d728d26e82a3bb9e58` | Section XI: AC-MOT |
| `Paper2_V71.pdf` | `34fe3e74f6f80f5f711c54d3780d853a6d9a10c825dd0f9535b35ee466e0fb18` | Section XII: SCL |
| `Big_Presentation_49` and v120 | n/a | visual language, section order and interaction pattern |

## Section XI — Paper 1

The first six slides are a short orientation. Slides 7–42 form the complete walkthrough.

| Slide titles | Manuscript evidence |
|---|---|
| `Paper 1 overview` to `Paper 1 complete map` | Abstract and Introduction, PDF pages 1–2 |
| `Paper 1 datasets` to `Paper 1 research gap` | Background, datasets, metrics and related work, PDF pages 3–7 |
| `Paper 1 operating point` to `Paper 1 full algorithm` | Proposed AC-MOT framework, PDF pages 8–14 |
| `Paper 1 action map` to `Paper 1 cross-pipeline studies` | Operating profiles, historical development and transfer evidence, PDF pages 10–19 |
| `Paper 1 modern development stages` to `Paper 1 final protocol` | Final-controller development, search, freezing and evaluation protocol, PDF pages 15–20 |
| `Paper 1 full VisDrone results` to `Paper 1 full UAVDT results` | Main results, paired intervals, controller behavior, latency and transfer, PDF pages 20–22 |
| `Paper 1 limits and meaning` and `Paper 1 final conclusion` | Discussion and conclusion, PDF page 23 |

Important boundaries kept in the slides:

- Historical quality and identity profiles are not pooled with the modern frozen controller.
- Calibration sequences and final VisDrone evaluation sequences have different roles.
- UAVDT is presented as transfer evidence without retuning.
- ByteTrack gains are shown with their higher false-negative count and lower recall.
- OATrack UAVDT HOTA is shown as almost unchanged instead of being presented as a universal gain.

## Section XII — Paper 2

The first six slides are a short orientation. Slides 7–42 form the complete paper walkthrough; slide 43 explains the relation to Paper 1.

| Slide titles | Manuscript evidence |
|---|---|
| `Paper 2 problem` to `Paper 2 complete map` | Abstract and Introduction, PDF pages 1–2 |
| `Paper 2 evidence split` to `Paper 2 research gap` | Datasets, metrics and related work, PDF pages 2–3 |
| `Paper 2 tracker types` to `Paper 2 full algorithm` | Proposed SCL framework, equations, host contract and Algorithm 1, PDF pages 3–9 |
| `Paper 2 AOB failure` to `Paper 2 freezing and tests` | Development path and configuration freezing, PDF page 8 |
| `Paper 2 MOT17 results` | Table 7 and Section 5.1, PDF pages 9–10 |
| `Paper 2 KITTI RT-DETR results` to `Paper 2 qualitative KITTI example` | Table 8, Figure 4 and Section 5.2, PDF pages 9–11 |
| `Paper 2 score shift robustness` | Table 9 and Section 5.3, PDF pages 10–11 |
| `Paper 2 Otsu baselines` and `Paper 2 ACT comparison` | Tables 10–11 and Section 5.4, PDF pages 10–12 |
| `Paper 2 component ablation` and `Paper 2 parameter sensitivity` | Table 12 and Section 5.5, PDF page 12 |
| `Paper 2 unseen trackers` and `Paper 2 UAVDT results` | Table 13 and Sections 5.6–5.7, PDF pages 12–13 |
| `Paper 2 runtime` to `Paper 2 final conclusion` | Discussion, conclusion and declarations, PDF page 13 |
| `Paper 2 relation to AC-MOT` | Cross-paper synthesis based on each paper's stated intervention point |

Important boundaries kept in the slides:

- MOT17 and KITTI development evidence is separated from the predeclared external trackers and held-out UAVDT run.
- The early always-on baseline is shown as a failure, not hidden.
- Identical host outputs are reported as identical, not as gains.
- SCL changes the detector–tracker interface; it does not replace association or track management.
- The current host contract covers tracking-by-detection systems, not end-to-end trackers.

## Presentation-language policy

- New companion slides use short, direct English sentences, pictures and one example each. V125 further simplifies the paper-section openings and companion notes; complete technical details remain in the following slides.
- Each slide explains one question or one evidence group.
- Exact equations and table values are kept where they are needed to understand the paper.
- Speaker notes provide a simple spoken explanation without adding new experimental claims.
