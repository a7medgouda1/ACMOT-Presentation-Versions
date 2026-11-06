"""Build Paper Presentation v01 from the immutable v88 Big Presentation copy.

The target folder must already be a byte-for-byte copy of v88.  This script
only edits the new Paper Presentation family; it never writes to v88.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "versions" / "v01-paper-presentation-hybrid-buttons"
INDEX = TARGET / "index.html"
RESULTS = TARGET / "assets" / "data" / "results.js"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def slide(title: str, kicker: str, heading: str, body: str, notes: str,
          sec: int, secname: str, explain: str = "", footer: str = "") -> str:
    ex = f' data-explain="{explain}"' if explain else ""
    foot = f'<footer class="s-foot"><span class="prov">{footer}</span></footer>' if footer else ""
    return f'''<section class="slide" data-sec="{sec}" data-secname="{secname}" data-title="{title}"{ex}>
  <header class="s-head"><div class="kicker">{kicker}</div><h2>{heading}</h2></header>
  <div class="s-body col">{body}</div>
  <aside class="notes"><p><b>Say:</b> "{notes}"</p></aside>
  {foot}
</section>'''


def divider(sec: int, roman: str, heading: str, subtitle: str, notes: str) -> str:
    return f'''<section class="slide divider" id="sec-{sec}" data-sec="{sec}" data-secname="{roman} · {heading}" data-title="Section {roman}">
  <div class="dv-text"><div class="dv-num">{roman}</div><div class="dv-kicker">Section {roman}</div>
    <h1>{heading}</h1><p>{subtitle}</p></div>
  <aside class="notes"><p><b>Say:</b> "{notes}"</p></aside>
</section>'''


s = INDEX.read_text()

# Title and document metadata.
s = s.replace(
    "<title>AC-MOT — Real-Time Object Detection and Tracking (Big Presentation 50)</title>",
    "<title>AC-MOT — Calibration Versus Scene Switching (Paper Presentation v01)</title>",
)
s = s.replace("Master's thesis · Computer Vision", "Journal Paper Presentation · Master's Research")
s = s.replace("Real-Time Object Detection and Tracking", "Calibration Versus Scene Switching", 1)
s = s.replace(
    "Adaptive Control for Real-Time Multi-Object Tracking",
    "Calibration Versus Scene Switching of Detector Operating Points for Aerial Multi-Object Tracking",
    1,
)
s = s.replace(
    '"My thesis is about real-time object detection and tracking. The system is called AC-MOT. It looks at how hard each scene is and changes the detector settings to match."',
    '"This presentation asks a stricter question. AC-MOT improves strongly over a default pipeline, but we test whether that gain comes from calibration or from changing settings from frame to frame."',
    1,
)

# Twelve-part paper-aligned outline. Ranges are omitted because explanation pages
# are optional and the engine computes the final slide count at runtime.
outline = '''<div class="ol-ppt paper-outline">
      <button class="ol-row" data-goto="sec-1"><span class="n">I</span><span class="t"><h3>Introduction and MOT Fundamentals</h3><p>Detection, tracking and evaluation metrics</p></span></button>
      <button class="ol-row" data-goto="sec-2"><span class="n">II</span><span class="t"><h3>Related Work</h3><p>Detector and tracker choices</p></span></button>
      <button class="ol-row" data-goto="sec-3"><span class="n">III</span><span class="t"><h3>Fixed Operating-Point Problem</h3><p>One detector setting for changing aerial scenes</p></span></button>
      <button class="ol-row" data-goto="sec-4"><span class="n">IV</span><span class="t"><h3>AC-MOT Controller and SCI</h3><p>Five cues, one score and detector-side control</p></span></button>
      <button class="ol-row" data-goto="sec-5"><span class="n">V</span><span class="t"><h3>Initial Controller and Ablations</h3><p>Historical development evidence</p></span></button>
      <button class="ol-row" data-goto="sec-6"><span class="n">VI</span><span class="t"><h3>Validation-Driven Calibration</h3><p>Screening, temporal sweep, Quality profile Q and Balanced profile B</p></span></button>
      <button class="ol-row" data-goto="sec-8"><span class="n">VII</span><span class="t"><h3>Held-Out Evidence and UAVDT</h3><p>Locked tests, paired bootstrap and zero-tuning transfer</p></span></button>
      <button class="ol-row" data-goto="sec-9"><span class="n">VIII</span><span class="t"><h3>Calibration vs Scene Switching</h3><p>Matched static anchor and gain decomposition</p></span></button>
      <button class="ol-row" data-goto="sec-10"><span class="n">IX</span><span class="t"><h3>Why Switching Did or Did Not Help</h3><p>Resolution budget and cue-utility audit</p></span></button>
      <button class="ol-row" data-goto="sec-11"><span class="n">X</span><span class="t"><h3>Cross-Pipeline Evidence</h3><p>U2MOT and SparseTrack</p></span></button>
      <button class="ol-row" data-goto="sec-12"><span class="n">XI</span><span class="t"><h3>Limitations</h3><p>Protocol, implementation and generalization boundaries</p></span></button>
      <button class="ol-row" data-goto="sec-13"><span class="n">XII</span><span class="t"><h3>Contributions and Conclusion</h3><p>Calibrate first, then prove adaptation adds value</p></span></button>
    </div>'''
pat = re.compile(r'<div class="ol-ppt">.*?</div>\s*</div>\s*<aside class="notes">', re.S)
m = pat.search(s)
if not m:
    raise RuntimeError("outline not found")
s = s[:m.start()] + outline + '\n  </div>\n  <aside class="notes">' + s[m.end():]
s = s.replace(
    '"The story goes in the order the work happened: the problem and the baseline, the first heuristic design and its ablation, V1, V2, and finally the statistics and UAVDT."',
    '"The first half keeps the development journey. The second half asks the paper question: after calibration, does scene-by-scene switching add measurable value?"',
    1,
)

# Paper terminology while retaining the historical name at first introduction.
s = s.replace("V1 Trial 24", "Quality profile Q")
s = s.replace("V2 Trial 22", "Balanced profile B")
s = re.sub(r'\bV1\b', 'Q', s)
s = re.sub(r'\bV2\b', 'B', s)
s = s.replace("VI · Q optimization", "VI · Validation-driven calibration")
s = s.replace("VII · B multi-objective", "VI · Validation-driven calibration")
s = s.replace("Q Selection on the Validation Set", "Quality Profile Q (Historical V1, Optuna Trial 24)")
s = s.replace("Why Q Was Created", "Why Balanced Profile B Was Created")

# Correct what Optuna selected. The five cues were pre-defined; the search
# selected weights and controller parameters.
s = s.replace(
    "Optuna searches the SCI weights and the detector rules together.",
    "The five cues were defined from aerial failure modes. Optuna searches their weights and the detector rules together.",
)
s = s.replace(
    "Optuna automatically selected the five cues",
    "The cue set was defined first; Optuna selected its weights",
)
s = s.replace(
    "Gains come from our method, not from a bigger model",
    "Differences are not caused by changing the detector model",
)

# Remove the old U2MOT and conclusion main path, replacing it with the final
# journal-attribution story. The existing Thank-you slide remains unchanged.
start = s.index('<section class="slide divider" id="sec-9"')
end = s.index('<section class="slide divider" data-sec="0" data-secname="Questions"')

paper_slides = []
paper_slides.append(divider(9, "VIII", "Calibration Versus Scene Switching",
    "The controller beats the default. Now we test whether calibration or frame-to-frame switching explains the gain.",
    "This is the central attribution section of the journal paper."))

paper_slides.append(slide(
    "The important question changed", "Section VIII · Held-out attribution",
    "The Important Question Changed",
    '''<div class="g3 grow">
      <div class="kpi"><div class="l">Default static</div><div class="v" data-bind="paper.main.defaultHota" data-dec="2"></div><div class="s">HOTA</div></div>
      <div class="kpi hi"><div class="l">Adaptive Q</div><div class="v" data-bind="paper.main.qHota" data-dec="2"></div><div class="s">HOTA · +5.41</div></div>
      <div class="card sec"><h3>But why?</h3><p>A better result can come from <b>better calibration</b>, from <b>scene-by-scene switching</b>, or from both.</p></div>
    </div><div class="flow"><div class="node good">Better result</div><div class="arr"></div><div class="node hot">A · calibration</div><div class="node hot">B · switching</div></div>''',
    "Adaptive Q gained 5.41 HOTA over the default. That gain is real, but this comparison alone cannot tell us why it happened.",
    9, "VIII · Calibration vs switching", "x-attribution|Explain the Attribution Test",
    "Held-out VisDrone test-dev · custom class-agnostic protocol"))

paper_slides.append(slide(
    "What Optuna learned", "Section VIII · Behavior of Quality profile Q",
    "What Did Optuna Actually Learn?",
    '''<div class="g2 grow"><div class="card"><h3>11 optimized parameters</h3><p>5 cue weights + 4 confidence/NMS endpoints + 2 resolution thresholds.</p><p>The cue set itself was defined before optimization.</p></div><div class="card sec"><h3>Dominant result</h3><p>The two resolution thresholds explained most validation-MOTA variation. Every cue weight had relatively low importance.</p></div></div>
    <div class="callout">Q spends almost all frames near <b>960 px</b>, <b>confidence ≈ 0.34</b> and <b>NMS = 0.35</b>. The optimized adaptive controller became almost static.</div>''',
    "Optuna did not discover the five cues. It tuned their weights and the controller. The selected policy then stayed close to one operating point on most frames.",
    9, "VIII · Calibration vs switching", "x-attribution#2|Why Q Became Almost Static",
    "Validation analysis · parameter importance and controller trace"))

paper_slides.append(slide(
    "Matched static anchor", "Section VIII · Post-hoc attribution",
    "Matched Static Anchor: Hold the Learned Operating Point Fixed",
    '''<div class="g3 grow"><div class="card"><h3>Adaptive Q</h3><div class="big" data-bind="paper.main.qHota" data-dec="2"></div><p>HOTA</p></div><div class="card sec"><h3>Matched static</h3><div class="big" data-bind="paper.main.staticHota" data-dec="2"></div><p>HOTA</p></div><div class="card"><h3>Difference</h3><div class="big" data-bind="paper.main.deltaHota" data-dec="2"></div><p>95% CI [−0.25, +0.06]</p></div></div>
    <div class="flow"><div class="node io">conf 0.35</div><div class="node io">NMS 0.35</div><div class="node io">960 px</div><div class="node io">same tuned tracker</div></div>
    <div class="callout warn"><b>No measurable held-out difference.</b> The interval includes zero. The matched static anchor was evaluated post hoc after the frozen comparison for attribution.</div>''',
    "The static anchor uses the operating point discovered during validation. Once it is fixed at that point, switching adds no measurable held-out HOTA under the present sample size.",
    9, "VIII · Calibration vs switching", "x-attribution#3|How to Read the Confidence Interval",
    "Post-hoc attribution · held-out VisDrone test-dev · paired bootstrap"))

paper_slides.append(slide(
    "Calibration decomposition", "Section VIII · Validation decomposition",
    "Where Did the Gain Come From?",
    '''<div class="flow" style="align-items:stretch"><div class="node io">H0<br><small>default detector + default tracker</small></div><div class="arr"></div><div class="node hot">H1<br><small>same detector point + tuned tracker</small><br><b>+1.03 HOTA</b></div><div class="arr"></div><div class="node good">C0<br><small>calibrated detector point + tuned tracker</small><br><b>+5.21 HOTA further</b></div></div>
    <div class="g2 grow"><div class="callout">A smaller part came from the tuned tracker profile.</div><div class="callout sec">Most of the gain came from the detector operating point.</div></div>''',
    "This decomposition is on validation. It shows a smaller tracker-profile gain and a much larger detector operating-point gain.",
    9, "VIII · Calibration vs switching", "x-attribution|Explain the Attribution Test",
    "Validation ablation · calibration decomposition"))

paper_slides.append(slide(
    "Calibration versus switching result", "Section VIII · Main result",
    "The Large Gain Was Real — but Mainly Calibration",
    '''<div class="g3 grow"><div class="kpi"><div class="l">Default</div><div class="v">28.43</div></div><div class="kpi hi"><div class="l">Adaptive Q</div><div class="v">33.84</div></div><div class="kpi hi"><div class="l">Matched static</div><div class="v">33.93</div></div></div>
    <div class="meaning"><div class="tag">Journal-paper conclusion</div><p>The controller beat the default strongly, but once the static system used the operating point found on validation, frame-to-frame switching added no measurable held-out accuracy.</p></div>''',
    "The smart system looked good because it found a better pair of shoes. Once we kept those good shoes on all the time, changing shoes every few frames did not help.",
    9, "VIII · Calibration vs switching", "x-attribution|Explain the Attribution Test",
    "Held-out result plus post-hoc attribution"))

paper_slides.append(divider(10, "IX", "Why Switching Did or Did Not Help",
    "A separate cue-utility audit tests whether the scene cues identify the exact frames where a higher operating point pays off.",
    "The audit is a later experiment and is not numerically identical to Quality profile Q."))

paper_slides.append(slide(
    "Cue audit design", "Section IX · Exploratory audit",
    "Do the Cues Know When Switching Helps?",
    '''<div class="g3 grow"><div class="card"><h3>Detectors</h3><p>YOLOv8n and RT-DETR-L</p></div><div class="card"><h3>Tracker</h3><p>ByteTrack</p></div><div class="card"><h3>Resolutions</h3><p>640 / 736 / 832</p></div></div>
    <div class="callout">The same seven development sequences were used. The target was the <b>frame-wise benefit of 832 over 640</b>, not scene difficulty alone.</div>''',
    "A cue can describe a hard frame without predicting that changing resolution on that frame will improve tracking. This audit tests the second question directly.",
    10, "IX · Cue utility", "x-cue-audit|Explain the Cue-Utility Audit",
    "Exploratory validation audit · separate from Q"))

paper_slides.append(slide(
    "Cue audit findings", "Section IX · Exploratory audit",
    "Simple Cues Did Not Reliably Predict Switching Benefit",
    '''<div class="g2 grow"><div class="card"><h3>Correlation</h3><p>No causal cue reached <b>|Spearman| ≥ 0.3</b> consistently. Signs changed between sequences and detectors.</p></div><div class="card"><h3>Policy test</h3><p>No individual cue or SCI rule beat random high-resolution allocation on both detectors.</p></div></div>
    <div class="callout warn">Scene difficulty and switching benefit are different targets.</div>''',
    "The cues can describe darkness, blur or crowding, but they did not reliably tell us the exact frames where the larger detector input creates a tracking gain.",
    10, "IX · Cue utility", "x-cue-audit#2|Audit Statistics and Controls",
    "Exploratory validation audit · two detectors"))

paper_slides.append(slide(
    "Pixel budget example", "Section IX · Compute-aware reading",
    "A Gain Can Also Mean More Pixels",
    '''<div class="g2 grow"><div class="kpi hi"><div class="l">Tiny-object rule · YOLOv8n</div><div class="v">+1.26</div><div class="s">HOTA · +19% pixel budget</div></div><div class="kpi"><div class="l">Same rule · RT-DETR-L</div><div class="v">−0.45</div><div class="s">HOTA</div></div></div>
    <div class="callout">The hand-designed adaptive-resolution result also raised mean resolution from about <b>640 to 722/725 px</b>. The gain is therefore better explained by spending more pixels than by selecting the correct frames.</div>''',
    "When a policy uses more high-resolution frames, quality may rise because the average pixel budget rises. A fair switching claim needs a compute-matched control.",
    10, "IX · Cue utility", "x-cue-audit#3|Learned Cue Audit",
    "Exploratory validation audit · compute-budget qualification"))

paper_slides.append(slide(
    "Data-driven cue audit", "Section IX · LOSO and permutation checks",
    "What Signals Repeated Across Sequences?",
    '''<div class="g2 grow"><div class="card sec"><h3>Repeatable signal</h3><p>Detector-output cues, tracker-state cues and image-motion cues.</p></div><div class="card"><h3>Not consistent</h3><p>Edge, brightness and blur.</p></div></div>
    <div class="callout">Leave-one-sequence-out cross-validation and permutation null testing found useful signals, but learned controllers still did not reliably beat fixed global parameters on held-out sequences.</div>''',
    "The audit points toward richer detector and tracker state, but it does not establish a new successful controller. That negative result is part of the evidence.",
    10, "IX · Cue utility", "x-cue-audit#3|Learned Cue Audit",
    "Exploratory audit · LOSO cross-validation · permutation null"))

paper_slides.append(divider(11, "X", "Cross-Pipeline Evidence",
    "The same attribution question is checked on U2MOT and SparseTrack without claiming that one unchanged controller transfers everywhere.",
    "The pipelines share an outcome pattern, not one frozen controller."))

paper_slides.append(slide(
    "U2MOT study design", "Section X · Supplementary held-out study",
    "U2MOT: Same Design Family, Separately Recalibrated",
    '''<div class="flow"><div class="node io">YOLOX-X</div><div class="arr"></div><div class="node hot">U2MOT</div><div class="arr"></div><div class="node good">recalibrated controller</div></div>
    <div class="g2 grow"><div class="card"><h3>What changed</h3><p>SCI boundaries were recalibrated and U2MOT-specific detector actions were used.</p></div><div class="card sec"><h3>Comparator</h3><p>Author-calibrated static operating point — not the matched static anchor used for Q.</p></div></div>
    <div class="note">U2MOT source: Liu et al., <i>Uncertainty-aware Unsupervised Multi-Object Tracking</i>, ICCV 2023.</div>''',
    "This is not Quality profile Q transferred unchanged. It is a separately recalibrated member of the same controller design family.",
    11, "X · Cross-pipeline evidence", "x-u2mot|Explain the U2MOT Study",
    "Supplementary cross-pipeline study · VisDrone test-dev"))

paper_slides.append(slide(
    "U2MOT held-out rescore", "Section X · Post-hoc TrackEval rescore",
    "U2MOT Held-Out Result: No Measurable HOTA Change",
    '''<div class="g3 grow"><div class="kpi"><div class="l">Author static</div><div class="v" data-bind="paper.u2mot.baseHota" data-dec="2"></div><div class="s">HOTA</div></div><div class="kpi"><div class="l">Controller</div><div class="v" data-bind="paper.u2mot.controllerHota" data-dec="2"></div><div class="s">HOTA</div></div><div class="kpi"><div class="l">Difference</div><div class="v" data-bind="paper.u2mot.deltaHota" data-dec="2"></div><div class="s">CI [−0.31,+0.22]</div></div></div>
    <table class="tbl"><tr><th>Metric</th><th>Static</th><th>Controller</th></tr><tr><td>MOTA</td><td>53.87</td><td>53.77</td></tr><tr><td>IDF1</td><td>69.78</td><td>69.85</td></tr><tr><td>IDS</td><td>1,239</td><td>1,152</td></tr><tr><td>FP</td><td>41,385</td><td>40,155</td></tr><tr><td>FN</td><td>63,241</td><td>64,801</td></tr></table>
    <div class="callout warn">W/T/L = 9/0/8. No matched test-dev timing exists, so no held-out speed-improvement claim is made.</div>''',
    "The post-hoc TrackEval rescore gives minus 0.06 HOTA with an interval that includes zero. Identity switches and false positives fall, while false negatives rise.",
    11, "X · Cross-pipeline evidence", "x-u2mot#2|Read the U2MOT Trade-off",
    "Post-hoc TrackEval HOTA rescore · held-out · 17 sequences"))

paper_slides.append(slide(
    "SparseTrack study design", "Section X · Supplementary validation study",
    "SparseTrack: A Minimal NMS-Switching Test",
    '''<div class="flow"><div class="node io">YOLOX + SparseTrack</div><div class="arr"></div><div class="node hot">smoothed edge cue</div><div class="arr"></div><div class="node good">NMS 0.70 or 0.80</div></div>
    <div class="g2 grow"><div class="card"><h3>Data</h3><p>MOT17 validation half · seven sequences.</p></div><div class="card"><h3>Important limit</h3><p>The threshold was selected on these same sequences. There is no held-out SparseTrack score.</p></div></div>''',
    "SparseTrack is supporting validation evidence only. It tests one cue controlling one detector parameter.",
    11, "X · Cross-pipeline evidence", "x-sparse|Explain the SparseTrack Study",
    "Supplementary validation evidence · in-sample"))

paper_slides.append(slide(
    "SparseTrack results", "Section X · Supplementary validation study",
    "SparseTrack: The Comparator Changes the Conclusion",
    '''<table class="tbl"><tr><th>Comparison</th><th>Adaptive</th><th>Static</th><th>ΔHOTA</th><th>95% CI</th><th>W/T/L</th></tr><tr><td>Predeclared static 0.75</td><td>69.10</td><td>68.96</td><td class="good">+0.13</td><td>[+0.02,+0.24]</td><td>6/0/1</td></tr><tr><td>Default static 0.70</td><td>69.10</td><td>69.17</td><td>−0.07</td><td>[−0.54,+0.19]</td><td>4/0/3</td></tr></table>
    <div class="callout">Small in-sample gain over static 0.75, but no measurable gain over the tracker’s default 0.70 static setting.</div>''',
    "The adaptive rule beats the predeclared 0.75 comparator slightly, but it does not beat the tracker default. This is why comparator choice matters.",
    11, "X · Cross-pipeline evidence", "x-sparse#2|SparseTrack Limits",
    "Supplementary MOT17 validation evidence · not held-out"))

paper_slides.append(slide(
    "Cross-pipeline summary", "Section X · Comparison",
    "Does the Finding Repeat on Other Pipelines?",
    '''<table class="tbl" style="font-size:22px"><tr><th>Pipeline</th><th>Split and comparator</th><th>ΔHOTA</th><th>95% CI</th><th>Reading</th></tr><tr><td>YOLOv8n + ByteTrack</td><td>VisDrone held-out · Q vs matched static</td><td>−0.09</td><td>[−0.25,+0.06]</td><td>No measurable change</td></tr><tr><td>YOLOX-X + U2MOT</td><td>VisDrone held-out · recalibrated controller vs author static</td><td>−0.06</td><td>[−0.31,+0.22]</td><td>No measurable change</td></tr><tr><td>YOLOX + SparseTrack</td><td>MOT17 validation only · adaptive vs 0.75 / default 0.70</td><td>+0.13 / −0.07</td><td>[+0.02,+0.24] / [−0.54,+0.19]</td><td>Comparator-sensitive</td></tr></table>
    <div class="meaning"><div class="tag">Main message</div><p>The pipelines share an outcome pattern; they do not share one unchanged controller.</p></div>''',
    "Across pipelines, adaptive control does not show a reliable extra gain once the static comparator is calibrated or already strong.",
    11, "X · Cross-pipeline evidence", "x-attribution|Explain the Attribution Test",
    "Held-out and supplementary evidence shown separately"))

paper_slides.append(divider(12, "XI", "Limitations",
    "The evidence is useful only when its protocol, implementation and generalization boundaries are visible.",
    "These limits are part of the scientific result, not hidden footnotes."))

paper_slides.append(slide(
    "ByteTrack implementation caveat", "Section XI · Implementation boundary",
    "How ByteTrack Behaved in These Experiments",
    '''<div class="g2 grow"><div class="card"><h3>Standard ByteTrack</h3><p>Uses a high-score first association and a low-score second association.</p></div><div class="card sec"><h3>This implementation</h3><p>Detections below the controller confidence threshold were removed before ByteTrack. Every controller threshold was at least the tracker high threshold.</p></div></div>
    <div class="callout warn">The low-score second association received no input. The experiments mainly characterize the first association stage plus tuned buffer and matching settings.</div>''',
    "The early ByteTrack slide explains the standard algorithm. This later caveat explains how the specific AC-MOT filtering changed the available inputs.",
    12, "XI · Limitations", "x-limitations|Explain the Method Limits",
    "Implementation-specific methodology caveat"))

paper_slides.append(slide(
    "Study limitations", "Section XI · Scope of claims",
    "What This Study Does Not Prove",
    '''<div class="g2 grow"><div class="card"><ul><li>One main YOLOv8n + ByteTrack pipeline.</li><li>Custom class-agnostic VisDrone research protocol, not an official leaderboard result.</li><li>Matched static anchor is post-hoc attribution.</li><li>Seven validation sequences.</li><li>No exactly compute-matched random/static resolution allocation in the main pipeline.</li></ul></div><div class="card"><ul><li>Supplementary pipelines reduce, but do not remove, the generalization limit.</li><li>Processing FPS excludes JPEG decoding.</li><li>A T4 GPU is not an embedded flight computer.</li><li>Some provenance limits are documented.</li><li>SparseTrack evidence is in-sample.</li></ul></div></div>''',
    "The conclusions are bounded by the evaluation protocol, the small validation sample, the post-hoc static anchor and the lack of a compute-matched main control.",
    12, "XI · Limitations", "x-limitations#2|Claim Boundaries",
    "Paper-aligned limitations"))

paper_slides.append(divider(13, "XII", "Contributions and Conclusion",
    "The contribution is an attribution method and an auditable negative result, not a generic adaptive-superiority claim.",
    "We end with what the work establishes and the practical lesson."))

paper_slides.append(slide(
    "Final contributions", "Section XII · Contributions",
    "Main Contributions",
    '''<div class="g2 grow"><div class="card sec"><h3>1 · Attribution</h3><p>Separates calibration gain from scene-switching gain.</p></div><div class="card sec"><h3>2 · Controlled evidence</h3><p>Locked held-out test, matched static control, paired bootstrap and zero-tuning UAVDT.</p></div><div class="card sec"><h3>3 · Auditable instrument</h3><p>Causal, training-free controller with label-free cue normalization and validation-only selection.</p></div><div class="card sec"><h3>4 · Cross-pipeline evidence</h3><p>Checks the same attribution question with U2MOT and SparseTrack without claiming one unchanged controller.</p></div></div>''',
    "The strongest contribution is the controlled attribution framework: compare adaptation with a calibrated static operating point before assigning the gain to switching.",
    13, "XII · Conclusion", "x-contributions|Explain the Contributions",
    "Final journal-paper contributions"))

paper_slides.append(slide(
    "Final conclusion", "Section XII · Conclusion",
    "Calibration Explains Most of the Gain",
    '''<div class="meaning"><div class="tag">Final conclusion</div><p><b>AC-MOT strongly improves over a default pipeline, but controlled attribution shows that most of the gain comes from calibration of the detector operating point and tracker profile rather than from frame-to-frame scene switching.</b></p></div>
    <div class="callout">Switching can help in some operating ranges or against some static settings, but its benefit must be demonstrated against a calibrated static baseline and on held-out data.</div>''',
    "The improvement over default is real. The matched static experiment changes the explanation of that improvement: calibration explains most of it.",
    13, "XII · Conclusion", "x-conclusion|Explain the Final Conclusion",
    "Final scientific conclusion"))

paper_slides.append(slide(
    "Practical lesson", "Section XII · Methodological takeaway",
    "Calibrate First, Then Prove Adaptation Adds Value",
    '''<div class="flow" style="flex-wrap:wrap;row-gap:16px"><div class="node io">Default</div><div class="arr"></div><div class="node hot">Calibrate</div><div class="arr"></div><div class="node good">Strong gain</div><div class="arr"></div><div class="node hot">Test switching against calibrated static</div><div class="arr"></div><div class="node io">Does adaptation add more?</div></div>
    <div class="callout sec">Any adaptive MOT method should be compared with a well-calibrated static operating point before improvement is attributed to adaptation itself.</div>''',
    "This workflow is the transferable lesson of the study. A default baseline is not enough to prove an adaptive mechanism.",
    13, "XII · Conclusion", "x-conclusion#2|A Reusable Evaluation Recipe",
    "Methodological takeaway"))

paper_slides.append(slide(
    "Future work", "Section XII · Future work",
    "What Should Come Next?",
    '''<div class="g2 grow"><div class="card"><h3>Compute-matched controls</h3><p>Compare switching with random and static policies using the same average pixel budget.</p></div><div class="card"><h3>Richer causal signals</h3><p>Use detector output, tracker state and image motion to predict benefit, then validate on unseen sequences.</p></div><div class="card"><h3>Embedded evaluation</h3><p>Measure end-to-end latency, including decoding, on the target device.</p></div><div class="card"><h3>Radar-assisted tracking</h3><p>Fuse radar position and speed with image detections to support identity through occlusion, blur and camera motion.</p></div></div>''',
    "Future work should first fix the experimental controls: equal compute, unseen sequences and end-to-end device timing. Radar fusion remains a separate tracking direction.",
    13, "XII · Conclusion", "x-paper-future|Explain the Future Work",
    "Future work · not completed experiments"))

s = s[:start] + "\n\n".join(paper_slides) + "\n\n" + s[end:]

# Replace outdated explanation decks and add paper-specific deep dives. Existing
# educational decks stay in place.
lines = s.splitlines()
drop_ids = ("x-u2mot", "x-conclusion", "x-contributions")
lines = [line for line in lines if not any(f'id="{deck}"' in line for deck in drop_ids)]
s = "\n".join(lines) + "\n"

extra_decks = r'''
<div class="xdeck" id="x-attribution" data-label="Calibration versus switching">
<section class="xpage" data-sec="9" data-title="Attribution design"><header class="s-head"><div class="kicker">Attribution · 1 of 3</div><h2>Why the Default Comparison Is Not Enough</h2></header><div class="s-body col"><div class="flow"><div class="node io">Default detector point</div><div class="arr"></div><div class="node hot">Q changes tracker profile + operating point + switching</div><div class="arr"></div><div class="node good">Observed gain</div></div><div class="callout">This comparison bundles several changes. The matched static anchor keeps the tuned tracker and operating point but removes switching.</div></div><aside class="notes"><p><b>Say:</b> "The matched static control isolates the extra effect of frame-to-frame switching."</p></aside></section>
<section class="xpage" data-sec="9" data-title="Q behavior"><header class="s-head"><div class="kicker">Attribution · 2 of 3</div><h2>Why Q Suggested a Static Control</h2></header><div class="s-body col"><div class="g3 grow"><div class="kpi"><div class="l">Input size</div><div class="v">≈960</div><div class="s">almost all frames</div></div><div class="kpi"><div class="l">Confidence</div><div class="v">≈0.34</div></div><div class="kpi"><div class="l">NMS</div><div class="v">0.35</div></div></div><div class="callout">The optimized policy behaved almost like one static operating point, so that point became the natural attribution control.</div></div></section>
<section class="xpage" data-sec="9" data-title="CI reading"><header class="s-head"><div class="kicker">Attribution · 3 of 3</div><h2>What the Confidence Interval Allows Us to Say</h2></header><div class="s-body col"><div class="g2 grow"><div class="card"><h3>Measured difference</h3><p>Q − matched static = −0.09 HOTA.</p></div><div class="card"><h3>95% interval</h3><p>[−0.25,+0.06] includes zero.</p></div></div><div class="callout warn">Correct wording: <b>no measurable held-out difference under the present sample size</b>. Incorrect wording: proven equal or statistically equivalent.</div></div></section>
</div>

<div class="xdeck" id="x-cue-audit" data-label="Cue-utility audit">
<section class="xpage" data-sec="10" data-title="Audit target"><header class="s-head"><div class="kicker">Cue audit · 1 of 3</div><h2>Difficulty Is Not the Same as Treatment Benefit</h2></header><div class="s-body col"><div class="g2 grow"><div class="card"><h3>Difficulty question</h3><p>Is this frame crowded, dark or blurred?</p></div><div class="card sec"><h3>Switching question</h3><p>Will using 832 instead of 640 improve tracking on this frame?</p></div></div><div class="callout">The audit evaluates the second question directly.</div></div></section>
<section class="xpage" data-sec="10" data-title="Audit controls"><header class="s-head"><div class="kicker">Cue audit · 2 of 3</div><h2>How the Audit Avoided an Easy Win</h2></header><div class="s-body col"><div class="g3 grow"><div class="card"><h3>Two detectors</h3><p>YOLOv8n and RT-DETR-L.</p></div><div class="card"><h3>Random allocation</h3><p>Checks whether the rule beats spending the same high-resolution budget randomly.</p></div><div class="card"><h3>Sequence checks</h3><p>Correlation signs and policy gains are checked separately across sequences.</p></div></div></div></section>
<section class="xpage" data-sec="10" data-title="Learned audit"><header class="s-head"><div class="kicker">Cue audit · 3 of 3</div><h2>What the Data-Driven Audit Found</h2></header><div class="s-body col"><div class="flow"><div class="node io">Leave one sequence out</div><div class="arr"></div><div class="node hot">Select signals on the others</div><div class="arr"></div><div class="node hot">Permutation null</div><div class="arr"></div><div class="node good">Test the held-out sequence</div></div><div class="callout">Repeatable signals appeared mainly in detector output, tracker state and image motion. Learned controllers still did not reliably beat fixed global parameters.</div></div></section>
</div>

<div class="xdeck" id="x-u2mot" data-label="U2MOT attribution study">
<section class="xpage" data-sec="11" data-title="U2MOT provenance"><header class="s-head"><div class="kicker">U2MOT · 1 of 2</div><h2>What Was Reused and What Was Recalibrated?</h2></header><div class="s-body col"><div class="g2 grow"><div class="card"><h3>Same design family</h3><p>Scene cues and controller idea come from AC-MOT.</p></div><div class="card sec"><h3>Not the same controller</h3><p>Regime boundaries and detector actions were recalibrated for YOLOX-X + U2MOT.</p></div></div><div class="note">Comparator: author-calibrated static operating point.</div></div></section>
<section class="xpage" data-sec="11" data-title="U2MOT tradeoff"><header class="s-head"><div class="kicker">U2MOT · 2 of 2</div><h2>How to Read the U2MOT Trade-off</h2></header><div class="s-body col"><div class="g3 grow"><div class="card"><h3>HOTA</h3><p>55.00 → 54.94; Δ −0.06; interval includes zero.</p></div><div class="card"><h3>Identity / FP</h3><p>IDS −87 and FP −1,230.</p></div><div class="card"><h3>Misses</h3><p>FN +1,560.</p></div></div><div class="callout warn">No matched held-out timing was recorded, so this slide makes no test-dev speed claim.</div></div></section>
</div>

<div class="xdeck" id="x-sparse" data-label="SparseTrack study">
<section class="xpage" data-sec="11" data-title="SparseTrack comparator"><header class="s-head"><div class="kicker">SparseTrack · 1 of 2</div><h2>Why Two Static Comparators Matter</h2></header><div class="s-body col"><div class="g2 grow"><div class="card"><h3>Predeclared 0.75</h3><p>Adaptive gains +0.13 HOTA with a positive interval.</p></div><div class="card sec"><h3>Tracker default 0.70</h3><p>Adaptive is −0.07 HOTA and the interval includes zero.</p></div></div><div class="callout">A favorable comparator is not enough; the default and best static choices must also be visible.</div></div></section>
<section class="xpage" data-sec="11" data-title="SparseTrack limits"><header class="s-head"><div class="kicker">SparseTrack · 2 of 2</div><h2>Why This Is Supporting Evidence Only</h2></header><div class="s-body col"><ul><li>The threshold was selected on the same seven validation sequences.</li><li>There is no held-out SparseTrack result.</li><li>The rule switches only NMS between 0.70 and 0.80.</li><li>The result cannot support a cross-dataset generalization claim.</li></ul></div></section>
</div>

<div class="xdeck" id="x-limitations" data-label="Study limitations">
<section class="xpage" data-sec="12" data-title="Method limits"><header class="s-head"><div class="kicker">Limitations · 1 of 2</div><h2>Main Design Limits</h2></header><div class="s-body col"><div class="g2 grow"><div class="card"><h3>Attribution</h3><p>The matched static anchor is post hoc, not predeclared before the frozen Q test.</p></div><div class="card"><h3>Compute</h3><p>The main pipeline lacks an exactly compute-matched random or static resolution control.</p></div></div></div></section>
<section class="xpage" data-sec="12" data-title="Claim limits"><header class="s-head"><div class="kicker">Limitations · 2 of 2</div><h2>How the Claim Is Bounded</h2></header><div class="s-body col"><div class="callout">The study supports an attribution finding under the stated protocols. It does not establish a universal controller, official VisDrone leaderboard result, embedded real-time operation or held-out SparseTrack generalization.</div></div></section>
</div>

<div class="xdeck" id="x-conclusion" data-label="Paper conclusion">
<section class="xpage" data-sec="13" data-title="Conclusion logic"><header class="s-head"><div class="kicker">Conclusion · 1 of 2</div><h2>The Logic in One Line</h2></header><div class="s-body col"><div class="flow"><div class="node io">Default</div><div class="arr"></div><div class="node hot">Adaptive gain</div><div class="arr"></div><div class="node hot">Matched static control</div><div class="arr"></div><div class="node good">Attribution</div></div><div class="callout">The strong default-to-Q gain is mainly a calibration gain; switching must be tested as an additional treatment.</div></div></section>
<section class="xpage" data-sec="13" data-title="Evaluation recipe"><header class="s-head"><div class="kicker">Conclusion · 2 of 2</div><h2>A Reusable Evaluation Recipe</h2></header><div class="s-body col"><div class="xsteps col"><div class="node io">Calibrate a strong static operating point on validation</div><div class="xdown">↓</div><div class="node">Freeze the adaptive policy and static control</div><div class="xdown">↓</div><div class="node">Evaluate both on held-out sequences</div><div class="xdown">↓</div><div class="node good">Use paired uncertainty and report compute budget</div></div></div></section>
</div>

<div class="xdeck" id="x-contributions" data-label="Paper contributions">
<section class="xpage" data-sec="13" data-title="Contribution logic"><header class="s-head"><div class="kicker">Contributions</div><h2>Why Attribution Is the Main Contribution</h2></header><div class="s-body col"><div class="g2 grow"><div class="card"><h3>Common comparison</h3><p>Adaptive policy versus an untuned default.</p></div><div class="card sec"><h3>Stronger comparison</h3><p>Adaptive policy versus a calibrated static operating point using the same tracker profile.</p></div></div><div class="callout">The stronger control changes the scientific explanation from adaptive superiority to calibration-first attribution.</div></div></section>
</div>

<div class="xdeck" id="x-paper-future" data-label="Paper future work">
<section class="xpage" data-sec="13" data-title="Future controls"><header class="s-head"><div class="kicker">Future work</div><h2>The Next Decisive Experiments</h2></header><div class="s-body col"><div class="g3 grow"><div class="card"><h3>Equal compute</h3><p>Match the average pixel budget across adaptive, random and static policies.</p></div><div class="card"><h3>Unseen sequences</h3><p>Select benefit-predicting signals on development data and test once on held-out sequences.</p></div><div class="card"><h3>Target hardware</h3><p>Measure decoding, inference, association and control together.</p></div></div></div></section>
</div>
'''
s = s.replace('<div class="xdeck" id="x-pictures"', extra_decks + '\n<div class="xdeck" id="x-pictures"', 1)

INDEX.write_text(s)

# Centralized paper-aligned results and executable assertions.
r = RESULTS.read_text()
paper_data = r'''

/* Journal-paper attribution registry. These values are deliberately separate
   from the historical development blocks above. */
window.ACMOT.paper = {
  main: {
    prov: 'Held-out VisDrone test-dev plus post-hoc matched-static attribution',
    defaultHota: 28.43, qHota: 33.84, staticHota: 33.93,
    gainVsDefault: 5.41, deltaHota: -0.09, ci95: [-0.25, 0.06],
    matchedStatic: { confidence: 0.35, nms: 0.35, resolution: 960 }
  },
  calibration: { trackerGainHota: 1.03, detectorGainHota: 5.21 },
  uavdt: { defaultHota: 24.08, qHota: 28.39, deltaHota: 4.30 },
  u2mot: {
    prov: 'Post-hoc TrackEval HOTA rescore of frozen held-out outputs',
    baseHota: 55.00, controllerHota: 54.94, deltaHota: -0.06,
    ci95: [-0.31, 0.22], wtl: [9, 0, 8],
    base: { mota: 53.87, idf1: 69.78, ids: 1239, fp: 41385, fn: 63241 },
    controller: { mota: 53.77, idf1: 69.85, ids: 1152, fp: 40155, fn: 64801 }
  },
  sparseTrack: {
    prov: 'MOT17 validation only; in-sample supporting evidence',
    adaptiveHota: 69.10, static075Hota: 68.96, delta075: 0.13,
    ci075: [0.02, 0.24], wtl075: [6, 0, 1],
    static070Hota: 69.17, delta070: -0.07,
    ci070: [-0.54, 0.19], wtl070: [4, 0, 3]
  }
};

(function assertPaperNumbers(P) {
  var checks = [
    ['Q HOTA', P.main.qHota, 33.84], ['matched static HOTA', P.main.staticHota, 33.93],
    ['matched delta', P.main.deltaHota, -0.09], ['UAVDT default', P.uavdt.defaultHota, 24.08],
    ['UAVDT Q', P.uavdt.qHota, 28.39], ['U2MOT static', P.u2mot.baseHota, 55.00],
    ['U2MOT controller', P.u2mot.controllerHota, 54.94], ['U2MOT delta', P.u2mot.deltaHota, -0.06],
    ['SparseTrack static .75', P.sparseTrack.static075Hota, 68.96],
    ['SparseTrack adaptive', P.sparseTrack.adaptiveHota, 69.10],
    ['SparseTrack delta .75', P.sparseTrack.delta075, 0.13],
    ['SparseTrack static .70', P.sparseTrack.static070Hota, 69.17],
    ['SparseTrack delta .70', P.sparseTrack.delta070, -0.07]
  ];
  checks.forEach(function (c) {
    if (Math.abs(c[1] - c[2]) > 1e-9) throw new Error('Paper result mismatch: ' + c[0]);
  });
})(window.ACMOT.paper);
'''
if "window.ACMOT.paper" not in r:
    r = r.rstrip() + paper_data + "\n"
RESULTS.write_text(r)

print(f"Built {TARGET}")
