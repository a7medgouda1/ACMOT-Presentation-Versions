"""Build offline SVG teaching figures and source-checked charts for v123.

All measured values below are transcribed from the two supplied manuscripts.
Other numbers are explicitly illustrative in the slide captions.
"""

from __future__ import annotations

from html import escape
from pathlib import Path


OUT = Path(__file__).resolve().parents[1] / "assets" / "beginner"
OUT.mkdir(parents=True, exist_ok=True)
INK = "#10203A"
MUTED = "#52637B"
GRID = "#D8E1EC"
P1 = "#4F46E5"
P2 = "#0D9488"
HOST = "#94A3B8"
GOOD = "#15803D"
BAD = "#B91C1C"


def tag(name: str, attrs: dict[str, object], body: str = "") -> str:
    a = " ".join(f'{k.replace("_", "-")}="{escape(str(v), quote=True)}"' for k, v in attrs.items())
    return f"<{name} {a}>{body}</{name}>"


def text(x: float, y: float, words: str, size: int = 27, weight: int = 700,
         fill: str = INK, anchor: str = "start") -> str:
    return tag("text", {"x": x, "y": y, "font-size": size, "font-weight": weight,
                        "fill": fill, "text-anchor": anchor}, escape(words))


def rect(x: float, y: float, w: float, h: float, fill: str = "#FFFFFF",
         stroke: str = GRID, radius: int = 18, sw: int = 3) -> str:
    return tag("rect", {"x": x, "y": y, "width": w, "height": h, "rx": radius,
                         "fill": fill, "stroke": stroke, "stroke-width": sw})


def line(x1: float, y1: float, x2: float, y2: float, stroke: str = GRID,
         sw: int = 3, dash: str | None = None) -> str:
    attrs: dict[str, object] = {"x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                "stroke": stroke, "stroke-width": sw}
    if dash:
        attrs["stroke-dasharray"] = dash
    return tag("line", attrs)


def circle(x: float, y: float, r: float, fill: str, stroke: str = "none", sw: int = 2) -> str:
    return tag("circle", {"cx": x, "cy": y, "r": r, "fill": fill,
                           "stroke": stroke, "stroke-width": sw})


def box(x: int, y: int, w: int, h: int, title: str, detail: str,
        accent: str = P1, tint: str = "#F3F2FF") -> str:
    return (rect(x, y, w, h, tint, accent) + text(x + 22, y + 47, title, 31, 800) +
            text(x + 22, y + 87, detail, 23, 600, MUTED))


def save(name: str, body: str, description: str) -> None:
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1480 480" '
           f'role="img" aria-label="{escape(description, quote=True)}">'
           '<style>text{font-family:Inter,Arial,sans-serif}</style>' + body + '</svg>')
    (OUT / name).write_text(svg, encoding="utf-8")


def pair_chart(name: str, metric: str, dataset: str, pairs: list[tuple[str, float, float]],
               maximum: float, method: str, accent: str, integer: bool = False) -> None:
    """Honest paired bars: zero baseline, one metric, one dataset, exact labels."""
    left, width = 480, 830
    p = [text(45, 44, f"{metric} · {dataset}", 28, 800),
         rect(850, 12, 24, 22, HOST, HOST, 3, 0), text(885, 31, "Host", 20, 700),
         rect(1070, 12, 24, 22, accent, accent, 3, 0), text(1105, 31, f"With {method}", 20, 700)]
    for tick in (0, maximum / 2, maximum):
        x = left + width * tick / maximum
        p += [line(x, 73, x, 429, GRID, 2, "7 8"),
              text(x, 461, f"{tick:,.0f}" if integer else f"{tick:.0f}", 18, 600, MUTED, "middle")]
    for i, (label, before, after) in enumerate(pairs):
        y = 110 + i * (105 if len(pairs) == 3 else 150)
        p += [text(40, y + 40, label, 25, 800),
              rect(left, y, width * before / maximum, 31, HOST, HOST, 3, 0),
              rect(left, y + 44, width * after / maximum, 31, accent, accent, 3, 0),
              text(1350, y + 25, f"{before:,.0f}" if integer else f"{before:.2f}", 22, 800, INK),
              text(1350, y + 70, f"{after:,.0f}" if integer else f"{after:.2f}", 22, 800, accent)]
    save(name, "".join(p), f"{metric} on {dataset}, host versus host with {method}, with zero baseline")


def single_chart(name: str, title: str, values: list[tuple[str, float]],
                 maximum: float, accent: str, suffix: str = "") -> None:
    left, width = 600, 720
    p = [text(45, 45, title, 28, 800)]
    for tick in (0, maximum / 2, maximum):
        x = left + width * tick / maximum
        p += [line(x, 70, x, 430, GRID, 2, "7 8"),
              text(x, 460, f"{tick:g}{suffix}", 18, 600, MUTED, "middle")]
    gap = 350 / len(values)
    for i, (label, value) in enumerate(values):
        y = 100 + i * gap
        p += [text(45, y + 36, label, 24, 800),
              rect(left, y, width * value / maximum, 47, accent, accent, 5, 0),
              text(1350, y + 35, f"{value:.2f}{suffix}", 22, 800, accent)]
    save(name, "".join(p), title + "; bars start at zero")


def make_charts() -> None:
    pair_chart("p1-visdrone-fp.svg", "False alarms (FP) — lower is better", "VisDrone validation",
               [("ByteTrack", 39274, 24892), ("OATrack", 25394, 21400)], 45000, "AC-MOT", P1, True)
    pair_chart("p1-visdrone-fn.svg", "Missed objects (FN) — lower is better", "VisDrone validation",
               [("ByteTrack", 24121, 25902), ("OATrack", 25432, 25057)], 30000, "AC-MOT", P1, True)
    pair_chart("p1-uavdt-fp.svg", "False alarms (FP) — lower is better", "UAVDT transfer",
               [("ByteTrack", 279616, 212077), ("OATrack", 197937, 183669)], 300000, "AC-MOT", P1, True)
    pair_chart("p1-uavdt-fn.svg", "Missed objects (FN) — lower is better", "UAVDT transfer",
               [("ByteTrack", 66050, 73702), ("OATrack", 75612, 78774)], 90000, "AC-MOT", P1, True)
    pair_chart("p2-aob-hota.svg", "HOTA — early always-on design", "MOT17 development",
               [("SparseTrack", 68.88, 64.72), ("Boost online", 68.49, 62.61),
                ("Boost + GBI", 71.73, 66.35)], 80, "AOB", BAD)
    pair_chart("p2-kitti-oc-hota.svg", "HOTA — one-score-gate OC-SORT", "KITTI · YOLOv8n",
               [("OC-SORT", 36.27, 44.18)], 50, "SCL", P2)
    pair_chart("p2-kitti-rt-mota.svg", "MOTA — new detector, same trackers", "KITTI · RT-DETR-L",
               [("ByteTrack", 47.27, 53.24), ("BoT-SORT", 48.25, 56.11)], 65, "SCL", P2)
    pair_chart("p2-uavdt-mota.svg", "MOTA — frozen SCL on unseen drone video", "UAVDT · RT-DETR-L",
               [("ByteTrack", 3.29, 27.99)], 35, "SCL", P2)
    pair_chart("p2-uavdt-hota.svg", "HOTA — frozen SCL on unseen drone video", "UAVDT · YOLOv8n",
               [("ByteTrack", 29.05, 30.83)], 35, "SCL", P2)
    single_chart("p2-runtime.svg", "Paper timing sample: detector and SCL (ms per frame)",
                 [("Detector", 42.0), ("SCL", 2.95)], 45, P2)
    single_chart("p2-ablation.svg", "Largest HOTA loss when one part is removed · different test cells",
                 [("Weak-box recovery", 3.35), ("Noisy-mode gate", 2.44),
                  ("Rank remapping", 1.67), ("Motion tolerance", 0.14)], 4, P2)

    # Actual paired HOTA intervals from Paper 1: a zero-anchored effect plot.
    p = [text(45, 45, "VisDrone HOTA gain with 95% paired intervals", 28, 800)]
    x0, scale = 510, 210
    for tick in (0, 1, 2, 3, 4):
        x = x0 + tick * scale
        p += [line(x, 80, x, 420, GRID, 2, "7 8"), text(x, 456, str(tick), 19, 700, MUTED, "middle")]
    for i, (label, gain, low, high) in enumerate([
        ("ByteTrack", 2.937, 2.356, 3.375), ("OATrack", 1.325, 0.200, 2.264)]):
        y = 165 + i * 180
        p += [text(50, y + 9, label, 27, 800), line(x0 + low * scale, y, x0 + high * scale, y, P1, 9),
              line(x0 + low * scale, y - 18, x0 + low * scale, y + 18, P1, 5),
              line(x0 + high * scale, y - 18, x0 + high * scale, y + 18, P1, 5),
              circle(x0 + gain * scale, y, 15, P1),
              text(1340, y + 8, f"+{gain:.3f}", 24, 800, P1)]
    save("p1-visdrone-hota-interval.svg", "".join(p),
         "Two positive VisDrone HOTA differences with paired 95 percent intervals and zero reference")

    # Paper 1 state use is part-to-whole; each bar sums to 100%.
    p = [text(45, 43, "Share of frames in each controller state", 28, 800)]
    colors = ["#16A34A", "#F59E0B", BAD]
    for j, (label, values) in enumerate([("ByteTrack", [7.4, 30.1, 62.5]),
                                         ("OATrack", [7.4, 33.3, 59.3])]):
        y, x = 115 + j * 155, 350
        p.append(text(45, y + 43, label, 27, 800))
        for k, value in enumerate(values):
            w = 900 * value / 100
            p.append(rect(x, y, w, 74, colors[k], colors[k], 0, 0))
            if w > 95:
                p.append(text(x + w / 2, y + 47, f"{value:.1f}%", 24, 800, "#FFFFFF", "middle"))
            x += w
    for i, (label, c) in enumerate(zip(("LOW", "MEDIUM", "HIGH"), colors)):
        x = 445 + i * 285
        p += [rect(x, 430, 26, 23, c, c, 2, 0), text(x + 40, 449, label, 19, 700)]
    save("p1-state-share.svg", "".join(p), "Two 100 percent stacked bars for actual controller state use")

    # Paper 2 frame counts: three different count types, all on one zero-based scale.
    p = [text(45, 42, "How many objects were followed in three KITTI frames", 28, 800)]
    colors = [HOST, BAD, P2]
    names = ["Labelled", "Host", "Host + SCL"]
    for i, (frame, vals) in enumerate([(92, [13, 5, 6]), (97, [12, 5, 6]), (102, [10, 6, 9])]):
        y = 95 + i * 120
        p.append(text(35, y + 53, f"Frame {frame}", 23, 800))
        for j, val in enumerate(vals):
            yy = y + j * 29
            p += [rect(430, yy, 750 * val / 15, 21, colors[j], colors[j], 2, 0),
                  text(1230, yy + 19, str(val), 22, 800, colors[j])]
    for j, name in enumerate(names):
        x = 420 + j * 290
        p += [rect(x, 450, 20, 17, colors[j], colors[j], 2, 0), text(x + 30, 466, name, 18, 700)]
    save("p2-kitti-three-frames.svg", "".join(p),
         "KITTI frames 92, 97 and 102: labelled object counts, host tracks and host plus SCL tracks")


def make_figures() -> None:
    # Every SVG below is a schematic or made-up arithmetic example, never a paper screenshot.
    def roadmap(name: str, title: str, steps: list[tuple[str, str]], accent: str) -> None:
        p = [text(45, 44, title, 29, 800)]
        for i, (label, detail) in enumerate(steps):
            x = 45 + i * 290
            p += [rect(x, 132, 250, 225, "#F4F3FF" if accent == P1 else "#E7F8F5", accent),
                  circle(x + 125, 176, 27, accent),
                  text(x + 125, 186, str(i + 1), 25, 800, "#FFFFFF", "middle"),
                  text(x + 125, 248, label, 25, 800, INK, "middle"),
                  text(x + 125, 290, detail, 20, 700, MUTED, "middle")]
            if i < 4:
                p += [line(x + 252, 246, x + 286, 246, accent, 5),
                      tag("polygon", {"points": f"{x+286},246 {x+275},238 {x+275},254", "fill": accent})]
        p += [text(740, 432, "We will see one picture, one example and then the exact rule for each step.",
                   24, 700, MUTED, "middle")]
        save(name, "".join(p), title + "; five steps shown from left to right")

    roadmap("p1-roadmap.svg", "Paper 1: from changing scenes to tested tracking", [
        ("Watch video", "The scene changes"), ("Read clues", "Image + old tracks"),
        ("Pick a state", "LOW / MEDIUM / HIGH"), ("Run host", "Detect, then track"),
        ("Test fairly", "New videos, same rules")], P1)
    roadmap("p2-roadmap.svg", "Paper 2: from detector scores to the same tracker", [
        ("Read scores", "Current boxes"), ("Look back", "Earlier 10 frames"),
        ("Choose mode", "Cold / clean / noisy"), ("Repair if needed", "Keep or remap"),
        ("Run host", "Original tracker")], P2)

    p = [text(45, 43, "The same useful box can fall below a fixed tracker gate", 28, 800),
         box(65, 115, 390, 130, "Old detector score: 0.90", "Useful car box", P2, "#E7F8F5"),
         box(545, 115, 390, 130, "New score: 0.45", "Same box; score is halved", "#D97706", "#FFF6DC"),
         box(1025, 115, 390, 130, "Host gate: 0.70", "0.45 cannot start a track", BAD, "#FEEBEC"),
         line(455, 180, 535, 180, P2, 6), line(935, 180, 1015, 180, P2, 6),
         box(280, 315, 920, 110, "SCL checks whether the score scale still fits.",
             "If repair is needed, it adapts before the unchanged tracker runs.", P2, "#E7F8F5")]
    save("p2-score-mismatch.svg", "".join(p), "Made-up Paper 2 score-halving example: score 0.9 becomes 0.45 below tracker gate 0.7")

    p = [text(45, 43, "Six numbers answer six different questions", 28, 800)]
    metric_cards = [
        ("HOTA", "Find the objects", "and keep their IDs"),
        ("MOTA", "Fewer misses, false alarms", "and ID swaps"),
        ("IDF1", "Keep the same ID", "on the same object"),
        ("FP", "A wrong box", "with no real object"),
        ("FN", "A real object", "with no box"),
        ("IDS", "One object changes", "its ID number"),
    ]
    for i, (name, first, second) in enumerate(metric_cards):
        x, y = 45 + (i % 3) * 475, 95 + (i // 3) * 183
        p += [rect(x, y, 435, 153, "#F7F9FC", P1 if i < 3 else P2),
              text(x + 20, y + 47, name, 31, 800, P1 if i < 3 else P2),
              text(x + 20, y + 94, first, 20, 700),
              text(x + 20, y + 121, second, 20, 700)]
    save("metrics-plain.svg", "".join(p), "Plain-English meanings of HOTA MOTA IDF1 false positives false negatives and ID switches")

    p = [text(45, 49, "Previous tracker boxes are clues about the next scene", 28, 800)]
    for i in range(20):
        x, y = 75 + (i % 10) * 112, 100 + (i // 10) * 115
        tiny = i < 12
        p += [rect(x, y, 38 if tiny else 66, 42 if tiny else 77,
                   "#EDEBFF" if tiny else "#D5D1FF", P1, 5, 3)]
    p += [box(90, 343, 580, 104, "Crowd = 20 ÷ 30 = 0.67", "20 boxes are being followed"),
          box(750, 343, 620, 104, "Tiny share = 12 ÷ 20 = 0.60", "12 boxes are smaller than 32 × 32")]
    save("p1-box-clues.svg", "".join(p), "Illustrative twenty boxes, twelve tiny, showing crowd and tiny ratio")

    p = [text(45, 44, "Keep the last seven crowd readings", 28, 800)]
    values = [0.2, 0.3, 0.3, 0.4, 0.4, 0.5, 0.7]
    for i, v in enumerate(values):
        x = 65 + i * 195
        p += [rect(x, 180, 145, 170, "#F4F3FF", P1),
              rect(x + 18, 320 - v * 170, 109, v * 170, P1, P1, 3, 0),
              text(x + 72, 385, f"{v:.1f}", 26, 800, INK, "middle")]
    p += [text(740, 457, "Average = 2.8 ÷ 7 = 0.40 · only crowd readings go into this average", 24, 800, P1, "middle")]
    save("p1-seven-crowds.svg", "".join(p), "Made-up seven crowd readings averaging to zero point four")

    p = [text(45, 45, "Read the crowd score from left to right", 28, 800),
         line(130, 210, 1350, 210, P1, 10)]
    for value, label, col in [(0, "0", MUTED), (0.297, "0.297", "#D97706"),
                              (0.511, "0.511", BAD), (1, "1", MUTED)]:
        x = 130 + 1220 * value
        p += [line(x, 170, x, 255, col, 5), text(x, 147, label, 24, 800, col, "middle")]
    p += [box(70, 290, 400, 115, "LOW", "No higher rule is true", GOOD, "#E9F8EE"),
          box(530, 290, 400, 115, "MEDIUM", "SCI above 0.297", "#D97706", "#FFF6DC"),
          box(990, 290, 400, 115, "HIGH", "SCI above 0.511", BAD, "#FEEBEC"),
          text(740, 458, "Tiny share above 0.50 can request HIGH even when SCI is lower.", 23, 700, MUTED, "middle")]
    save("p1-target-scale.svg", "".join(p), "Paper 1 SCI thresholds with a separate tiny-object guard")

    p = [text(45, 42, "A sudden drop might mean lost tracks", 28, 800),
         box(65, 110, 440, 122, "Before: 20 tracks", "Remember this recent peak"),
         box(575, 110, 360, 122, "Now: 6 tracks", "6 is less than 8 = 40% of 20", BAD, "#FEEBEC"),
         box(1010, 110, 400, 122, "Short HIGH request", "Only up to 3 analysis steps", BAD, "#FEEBEC"),
         line(505, 171, 565, 171, P1, 6), line(935, 171, 1000, 171, P1, 6),
         box(245, 300, 1000, 105, "This is a safety check, not proof that the scene got easier.",
             "The 30-frame dwell rule can still delay a change.")]
    save("p1-track-drop.svg", "".join(p), "Made-up twenty to six track-drop example for recovery probe")

    p = [text(45, 43, "Entering HIGH and leaving HIGH use different limits", 28, 800),
         line(150, 205, 1330, 205, P1, 9)]
    for v, label, col in [(0.50, "Hold HIGH above 0.50", "#D97706"),
                          (0.511, "Enter HIGH above 0.511", BAD)]:
        x = 150 + 1180 * (v - 0.47) / 0.07
        p += [line(x, 165, x, 250, col, 5), text(x, 145 if v == 0.50 else 280, label, 23, 800, col, "middle")]
    p += [box(80, 340, 570, 105, "SCI = 0.505 · already HIGH", "Stay HIGH for now", GOOD, "#E9F8EE"),
          box(800, 340, 580, 105, "SCI = 0.505 · currently MEDIUM", "Do not enter HIGH from SCI alone", BAD, "#FEEBEC")]
    save("p1-hold-band.svg", "".join(p), "Illustrative SCI value between entry and hold thresholds")

    p = [text(45, 45, "A requested state can wait until 30 frames have passed", 28, 800),
         line(130, 195, 1350, 195, P1, 8)]
    events = [(1, "Start LOW", GOOD), (11, "Want MEDIUM", "#D97706"),
              (21, "Still wait", MUTED), (31, "Move allowed", GOOD),
              (41, "Want HIGH", "#D97706"), (61, "Move allowed", GOOD)]
    for i, (f, label, color) in enumerate(events):
        x = 130 + i * 244
        p += [circle(x, 195, 15, color), text(x, 145, f"Frame {f}", 22, 800, color, "middle"),
              text(x, 254, label, 20, 700, INK, "middle")]
    p += [box(220, 335, 1040, 105, "The detector and tracker still run on every frame.",
              "Only the controller state is held between allowed changes.")]
    save("p1-dwell-timeline.svg", "".join(p), "Made-up frame timeline showing the 30-frame dwell rule")

    p = [text(45, 44, "The state name describes the scene — not the image size", 28, 800)]
    for i, (name, size, nms, score, color, tint) in enumerate([
        ("LOW", "1536", "0.70", "0.10", GOOD, "#E9F8EE"),
        ("MEDIUM", "1280", "0.45", "0.40", "#D97706", "#FFF6DC"),
        ("HIGH", "1088", "0.60", "0.40", BAD, "#FEEBEC")]):
        x = 50 + i * 475
        p += [rect(x, 100, 420, 300, tint, color), text(x + 25, 150, name, 32, 800, color),
              text(x + 25, 222, f"Image size: {size}", 28, 700),
              text(x + 25, 286, f"NMS limit: {nms}", 26, 700),
              text(x + 25, 350, f"Keep-box score: {score}", 24, 700)]
    p += [text(740, 456, "These three actions were selected together in the paper's final search.", 23, 700, MUTED, "middle")]
    save("p1-action-cards.svg", "".join(p), "Paper 1 frozen action triplets, including smaller input in HIGH state")

    p = [text(45, 45, "A tracker only sees boxes above its score limits", 28, 800)]
    for i, (name, floor, match, start, color) in enumerate([
        ("ByteTrack", .10, .60, .70, P2), ("OC-SORT", .60, .60, .60, BAD)]):
        y = 125 + i * 190
        p += [text(45, y + 10, name, 28, 800), line(340, y, 1310, y, color, 9)]
        if name == "OC-SORT":
            x = 340 + 970 * floor
            p += [circle(x, y, 13, color),
                  text(x, y + 49, "floor = match = new track = 0.60", 19, 800, color, "middle")]
        else:
            for v, label in [(floor, "usable floor"), (match, "match"), (start, "new track")]:
                x = 340 + 970 * v
                p += [circle(x, y, 13, color), text(x, y - 27 if label == "match" else y + 48,
                                                   f"{label} {v:.2f}", 18, 700, color, "middle")]
    save("p2-host-score-lines.svg", "".join(p), "Paper 2 ByteTrack and OC-SORT score gates from host contract")

    p = [text(45, 43, "Logit changes spacing, not the order of boxes", 28, 800)]
    for i, (score, logit) in enumerate([("0.1", "−2.2"), ("0.5", "0"), ("0.9", "+2.2")]):
        x = 100 + i * 470
        p += [rect(x, 105, 350, 270, "#E7F8F5", P2),
              text(x + 175, 170, f"Score {score}", 29, 800, INK, "middle"),
              text(x + 175, 250, "↓", 43, 800, P2, "middle"),
              text(x + 175, 330, f"Logit {logit}", 29, 800, P2, "middle")]
    p += [text(740, 448, "Low stays low; middle stays middle; high stays high.", 24, 700, MUTED, "middle")]
    save("p2-logit-points.svg", "".join(p), "Score 0.1 0.5 and 0.9 map to approximately minus 2.2 zero and plus 2.2 logits")

    p = [text(45, 43, "A real clean example from the paper: 916 earlier boxes", 28, 800)]
    for i, (label, count, color, tint) in enumerate([
        ("Background-like", 653, HOST, "#F1F5F9"),
        ("Uncertain", 88, "#D97706", "#FFF6DC"),
        ("Confident", 175, P2, "#E7F8F5")]):
        y = 110 + i * 106
        p += [text(45, y + 38, label, 26, 800), rect(420, y, 850 * count / 700, 56, color, color, 5, 0),
              text(1350, y + 38, str(count), 26, 800, color)]
    p += [text(740, 455, "The two splits separate weak, uncertain and strong scores from past frames.", 23, 700, MUTED, "middle")]
    save("p2-otsu-groups.svg", "".join(p), "Paper 2 actual clean-window counts: 653 background 88 uncertain 175 confident")

    p = [text(45, 43, "Use the median confident share seen so far", 28, 800)]
    for i, (label, value, col) in enumerate([("Clean example", .63, P2), ("Noisy example", .42, BAD)]):
        y = 155 + i * 150
        p += [text(45, y + 7, label, 26, 800, col),
              line(420, y, 1320, y, GRID, 12),
              line(870, y - 34, 870, y + 34, "#D97706", 4),
              circle(420 + 900 * value, y, 18, col),
              text(420 + 900 * value, y - 30, f"{value:.2f}", 23, 800, col, "middle")]
    p += [text(870, 90, "0.50 decision line", 23, 800, "#D97706", "middle"),
          text(740, 450, "No valid split yet? Use COLD mode and the host's own limits.", 24, 700, MUTED, "middle")]
    save("p2-mode-gauge.svg", "".join(p), "Paper 2 clean and noisy median confident shares 0.63 and 0.42")

    p = [text(45, 43, "Noisy mode gives two groups new score ranges", 28, 800)]
    for i, (label, rng, formula, example, col, tint) in enumerate([
        ("Uncertain", "0.10 to below 0.50", "0.1 + 0.4 × rank", "rank 0.3 → 0.22", "#D97706", "#FFF6DC"),
        ("Confident", "0.50 to below 1.00", "0.5 + 0.5 × rank", "rank 0.8 → 0.90", P2, "#E7F8F5")]):
        x = 75 + i * 710
        p += [rect(x, 110, 625, 280, tint, col), text(x + 30, 165, label, 31, 800, col),
              text(x + 30, 230, rng, 25, 700), text(x + 30, 290, formula, 25, 700),
              text(x + 30, 355, example, 27, 800, col)]
    p += [text(740, 452, "Order is kept; the new scores are not calibrated probabilities.", 23, 700, MUTED, "middle")]
    save("p2-rank-bands.svg", "".join(p), "Made-up percentile examples for Paper 2's exact noisy-mode score formulas")

    p = [text(45, 43, "Two close people can have overlapping boxes", 28, 800),
         rect(150, 95, 650, 325, "#F1F5F9", GRID),
         rect(285, 145, 230, 230, "none", P2, 8, 6),
         rect(405, 135, 240, 240, "none", "#D97706", 8, 6),
         text(300, 130, "Track A", 24, 800, P2), text(500, 120, "Track B", 24, 800, "#D97706"),
         box(860, 120, 515, 110, "Different old tracks?", "Keep both boxes if yes", P2, "#E7F8F5"),
         box(860, 275, 515, 110, "No second-track support?", "Remove the weaker duplicate", BAD, "#FEEBEC")]
    save("p2-two-people.svg", "".join(p), "Schematic two overlapping people supported by different previous tracks")

    p = [text(45, 43, "A weak box can be rescued only when every check passes", 28, 800),
         rect(100, 105, 535, 305, "#F1F5F9", GRID),
         rect(215, 175, 200, 155, "none", P2, 8, 6),
         rect(235, 185, 200, 155, "none", "#D97706", 8, 6),
         text(140, 145, "Old track", 24, 800, P2),
         text(405, 370, "Weak new box", 24, 800, "#D97706"),
         box(730, 95, 640, 125, "Same foreground object?", "Overlap at least 0.50; no usable box covers it", P2, "#E7F8F5"),
         box(730, 275, 640, 125, "Host would otherwise miss it?", "Raise score just above its usable floor", P2, "#E7F8F5")]
    save("p2-weak-rescue.svg", "".join(p), "Schematic track and weak box with Paper 2 recovery checks")

    p = [text(45, 43, "More camera movement may allow less box overlap", 28, 800)]
    for i, (label, host_tol, min_iou, shift, color, tint) in enumerate([
        ("Cold or clean", "m = 0.80", "minimum IoU = 0.20", 100, HOST, "#F1F5F9"),
        ("Noisy, motion ratio 2", "m = 0.90", "minimum IoU = 0.10", 123, P2, "#E7F8F5")]):
        x = 75 + i * 710
        bx = x + 170
        p += [rect(x, 95, 625, 320, tint, color),
              text(x + 315, 145, label, 28, 800, color, "middle"),
              rect(bx, 180, 150, 145, "none", MUTED, 4, 5),
              rect(bx + shift, 180, 150, 145, "none", color, 4, 5),
              text(x + 315, 365, host_tol + " · " + min_iou, 25, 800, color, "middle")]
    p += [text(740, 455, "Boxes are a sketch of the overlap rule; the frozen host still makes the match.", 22, 700, MUTED, "middle")]
    save("p2-motion-rings.svg", "".join(p), "Schematic boxes showing minimum IoU point two or point one under mode-gated motion tolerance")


if __name__ == "__main__":
    make_charts()
    make_figures()
    print(f"Wrote {len(list(OUT.glob('*.svg')))} beginner visuals to {OUT}")
