"""Render source-checked, baseline-relative result charts for the offline deck.

Only presentation assets are generated; no detector, tracker, or evaluation is run.
The values below are copied from the named result slides and NUMBERS_CHECK.md.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

if sys.argv[1:] != ["--check"]:
    from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
OUT = HERE / "assets" / "results"
REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SCALE = 2
WIDTH, HEIGHT = 1480, 550
INK = "#17243D"
MUTED = "#64748B"
BASE = "#A9B6C9"
PURPLE = "#4F46E5"
TEAL = "#0D9488"
GOOD = "#087F5B"
BAD = "#B45309"
LINE = "#E0E7EF"


def M(name: str, baseline: float, result: float, higher: bool = True):
    return dict(name=name, baseline=baseline, result=result, higher=higher)


def S(id: str, after: str, title: str, intro: str, source: str, note: str,
      baseline_label: str, result_label: str, rows: list[dict], color: str = PURPLE):
    return dict(id=id, after=after, title=title, intro=intro, source=source,
                note=note, baseline_label=baseline_label, result_label=result_label,
                rows=rows, color=color)


SPECS = [
    S("old-ablation", "Ablation result", "Original AC-MOT: validation bars",
      "The full original controller improves tracking quality but costs some speed.",
      "Original AC-MOT ablation · VisDrone validation · source result table",
      "This is the original component study, not the later frozen test set.",
      "OLD-A0", "OLD-A3", [M("MOTA", 17.633, 18.165), M("HOTA", 29.837, 33.064),
      M("IDF1", 30.892, 36.296), M("IDS", 283, 271, False)]),
    S("old-test", "Old AC-MOT on the test set", "Original AC-MOT: held-out bars",
      "The original controller beats the fixed baseline on the 17 test videos.",
      "Historical VisDrone test-dev · assets/data/results.js · testdev.rows",
      "Different from the paper's later YOLO11m experiment. Speed is in the preceding table.",
      "Baseline", "Old AC-MOT", [M("MOTA", 19.729, 23.236), M("HOTA", 28.430, 32.698),
      M("IDF1", 32.724, 39.516), M("IDS", 1235, 1061, False)]),
    S("v1-test", "V1 on the test set", "V1: quality gains vs fixed baseline",
      "Frozen Trial 24 gives the largest quality gain on VisDrone test-dev.",
      "Historical VisDrone test-dev · assets/data/results.js · testdev.rows",
      "The ID-switch difference is not statistically secure; see the paired interval slide.",
      "Baseline", "V1", [M("MOTA", 19.729, 26.948), M("HOTA", 28.430, 33.835),
      M("IDF1", 32.724, 41.546), M("IDS", 1235, 1184, False)]),
    S("v2-test", "V2 on the test set", "V2: identity gains vs fixed baseline",
      "Frozen Trial 22 improves over baseline; V1 remains better on quality.",
      "Historical VisDrone test-dev · assets/data/results.js · testdev.rows",
      "Compare V1 and V2 separately: V2 trades some quality for fewer switches and more speed.",
      "Baseline", "V2", [M("MOTA", 19.729, 23.792), M("HOTA", 28.430, 31.218),
      M("IDF1", 32.724, 37.870), M("IDS", 1235, 919, False)]),
    S("uav-v1", "UAVDT with zero tuning", "UAVDT: V1 vs its own baseline",
      "The frozen quality profile also works on unseen drone videos.",
      "Historical UAVDT external test · assets/data/results.js · uavdt.rows",
      "Quality and IDs improve, but V1 is slower than the UAVDT baseline.",
      "Baseline", "V1", [M("MOTA", 13.841, 17.399), M("HOTA", 24.085, 28.390),
      M("IDF1", 27.887, 34.453), M("IDS", 558, 321, False)]),
    S("uav-v2", "UAVDT with zero tuning", "UAVDT: V2 vs its own baseline",
      "The frozen identity profile also works on unseen drone videos.",
      "Historical UAVDT external test · assets/data/results.js · uavdt.rows",
      "Both frozen profiles improve over baseline; V1 has higher quality, V2 fewer switches.",
      "Baseline", "V2", [M("MOTA", 13.841, 16.118), M("HOTA", 24.085, 26.930),
      M("IDF1", 27.887, 32.014), M("IDS", 558, 308, False)]),
    S("u2-val", "U2MOT validation comparison", "U2MOT validation: a mixed result",
      "Quality and false alarms improve, while missed objects increase.",
      "U2MOT transfer · VisDrone validation · source result table",
      "The missed-object count rises from 7,091 to 7,726; this trade-off remains visible.",
      "U2MOT", "+ AC-MOT", [M("MOTA", 75.1273, 75.4738), M("IDF1", 75.5578, 76.5775),
      M("IDS", 1947, 1908, False), M("FP", 8837, 7992, False)]),
    S("u2-test", "U2MOT final test", "U2MOT final test: fewer IDs and FP",
      "MOTA slips slightly; identity switches and false alarms fall.",
      "U2MOT transfer · frozen VisDrone test-dev · source result table",
      "Missed objects rise from 63,241 to 64,801. Do not describe this as an overall win.",
      "U2MOT", "+ AC-MOT", [M("MOTA", 53.9000, 53.7668), M("IDF1", 69.8000, 69.8494),
      M("IDS", 1239, 1152, False), M("FP", 41385, 40155, False)]),

    S("p1-vis-bt-quality", "Paper 1 full VisDrone results", "Paper 1: ByteTrack quality on VisDrone",
      "The frozen controller improves three quality scores and reduces ID switches.",
      "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
      "MOTA's relative percentage is large because the fixed MOTA starts at 9.876.",
      "Fixed", "AC-MOT", [M("HOTA", 41.586, 44.523), M("MOTA", 9.876, 27.871),
      M("IDF1", 48.569, 53.929), M("IDS", 1341, 1016, False)]),
    S("p1-vis-bt-errors", "Paper 1 full VisDrone results", "Paper 1: ByteTrack errors and recall",
      "Fewer false alarms come with more missed objects and lower recall.",
      "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
      "A lower FP count is good; a higher FN count is a real cost.",
      "Fixed", "AC-MOT", [M("FP", 39274, 24892, False), M("FN", 24121, 25902, False),
      M("Precision", 54.849, 64.852), M("Recall", 66.419, 63.940)]),
    S("p1-vis-oa-quality", "Paper 1 full VisDrone results", "Paper 1: OATrack quality on VisDrone",
      "The same frozen controller improves a second tracker too.",
      "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
      "OATrack starts stronger than ByteTrack; compare each host only with its own fixed run.",
      "Fixed", "AC-MOT", [M("HOTA", 46.770, 48.095), M("MOTA", 28.165, 34.483),
      M("IDF1", 57.107, 59.364), M("IDS", 773, 604, False)]),
    S("p1-vis-oa-errors", "Paper 1 full VisDrone results", "Paper 1: OATrack errors and recall",
      "False alarms, misses and ID switches all fall for OATrack.",
      "Paper1_V12_JAIS.pdf · frozen VisDrone result table · NUMBERS_CHECK.md",
      "The OATrack FN interval crosses zero, so avoid a strong claim about that decrease.",
      "Fixed", "AC-MOT", [M("FP", 25394, 21400, False), M("FN", 25432, 25057, False),
      M("Precision", 64.628, 68.609), M("Recall", 64.594, 65.116)]),
    S("p1-uav-bt-quality", "Paper 1 full UAVDT results", "Paper 1: ByteTrack quality on UAVDT",
      "The frozen controller raises MOTA from a negative starting score.",
      "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
      "MOTA relative % is undefined because its fixed baseline is negative; +17.601 points is valid.",
      "Fixed", "AC-MOT", [M("HOTA", 45.923, 47.004), M("MOTA", -1.573, 16.028),
      M("IDF1", 58.400, 61.767), M("IDS", 601, 486, False)]),
    S("p1-uav-bt-errors", "Paper 1 full UAVDT results", "Paper 1: ByteTrack UAVDT trade-off",
      "False alarms fall, but missed objects rise and recall falls.",
      "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
      "This is an external test with no retuning; selectivity costs must remain visible.",
      "Fixed", "AC-MOT", [M("FP", 279616, 212077, False), M("FN", 66050, 73702, False),
      M("Precision", 49.571, 55.751), M("Recall", 80.625, 78.381)]),
    S("p1-uav-oa-quality", "Paper 1 full UAVDT results", "Paper 1: OATrack quality on UAVDT",
      "MOTA and IDF1 rise, while HOTA is almost unchanged.",
      "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
      "HOTA falls slightly; do not call it an improvement.",
      "Fixed", "AC-MOT", [M("HOTA", 47.728, 47.640), M("MOTA", 19.607, 22.873),
      M("IDF1", 62.101, 62.931), M("IDS", 517, 486, False)]),
    S("p1-uav-oa-errors", "Paper 1 full UAVDT results", "Paper 1: OATrack UAVDT trade-off",
      "False alarms fall, but missed objects rise and recall falls.",
      "Paper1_V12_JAIS.pdf · frozen UAVDT result table · NUMBERS_CHECK.md",
      "Both paper hosts have the same missed-object direction on UAVDT.",
      "Fixed", "AC-MOT", [M("FP", 197937, 183669, False), M("FN", 75612, 78774, False),
      M("Precision", 57.270, 58.800), M("Recall", 77.820, 76.893)]),

    S("p2-mot17", "Paper 2 MOT17 results", "Paper 2: MOT17 host comparison",
      "SCL helps OC-SORT while compatible two-stage hosts stay unchanged.",
      "Paper2_V71.pdf · MOT17 result table · NUMBERS_CHECK.md",
      "The first three panels use floor 0.01; the last uses floor 0.10. Rounded HOTA bars differ by 0.47, while the paper reports 0.46.",
      "Host", "+ SCL", [M("HOTA · floor .01", 66.43, 67.04), M("MOTA · floor .01", 74.67, 75.94),
      M("IDS · floor .01", 211, 203, False), M("HOTA · floor .10", 66.44, 66.91)], TEAL),
    S("p2-kitti-bt", "Paper 2 KITTI RT-DETR results", "Paper 2: KITTI RT-DETR + ByteTrack",
      "SCL helps the tracker use a replacement detector's scores.",
      "Paper2_V71.pdf · KITTI RT-DETR-L table · NUMBERS_CHECK.md",
      "Only the score interface changes. Small point-difference rounding may differ from the paper's paired estimates.",
      "Host", "+ SCL", [M("HOTA", 50.73, 51.64), M("MOTA", 47.27, 53.24),
      M("IDF1", 64.98, 68.86), M("IDS", 686, 389, False)], TEAL),
    S("p2-kitti-bot", "Paper 2 KITTI RT-DETR results", "Paper 2: KITTI RT-DETR + BoT-SORT",
      "SCL improves quality and reduces ID switches for this host too.",
      "Paper2_V71.pdf · KITTI RT-DETR-L table · NUMBERS_CHECK.md",
      "Sequence 0020 is excluded from both runs because the host stops with a numerical error.",
      "Host", "+ SCL", [M("MOTA", 48.25, 56.11), M("IDF1", 67.74, 70.85),
      M("IDS", 476, 250, False)], TEAL),
    S("p2-kitti-oc", "Paper 2 KITTI OC-SORT results", "Paper 2: KITTI YOLOv8n + OC-SORT",
      "SCL recovers useful weak boxes for a single-stage tracker.",
      "Paper2_V71.pdf · KITTI OC-SORT table · NUMBERS_CHECK.md",
      "False negatives fall by 5,310. The paper reports IDF1 +9.60; rounded bar values differ by 9.59.",
      "Host", "+ SCL", [M("HOTA", 36.27, 44.18), M("MOTA", 33.99, 43.39),
      M("IDF1", 50.46, 60.05)], TEAL),
    S("p2-score-shift", "Paper 2 score shift robustness", "Paper 2: repair a shifted score scale",
      "Changing score values without changing their order can break a host.",
      "Paper2_V71.pdf · score-transform table · NUMBERS_CHECK.md",
      "For 0.5s, the host HOTA is zero; relative percentages are undefined, not infinite.",
      "Host", "+ SCL", [M("ByteTrack · s³ HOTA", 60.92, 65.81), M("OC-SORT · s³ HOTA", 58.34, 66.60),
      M("ByteTrack · 0.5s HOTA", 0, 66.17), M("OC-SORT · 0.5s HOTA", 0, 66.72)], TEAL),
    S("p2-otsu", "Paper 2 Otsu baselines", "Paper 2: SCL vs a simple threshold",
      "SCL beats the stronger simple threshold in all three KITTI cells.",
      "Paper2_V71.pdf · Otsu comparator table · NUMBERS_CHECK.md",
      "Each panel compares SCL with that same cell's t2 baseline; cells are not pooled.",
      "t₂", "SCL", [M("OC-SORT · YOLOv8n HOTA", 41.09, 44.18),
      M("ByteTrack · half RT-DETR HOTA", 49.50, 51.79),
      M("OC-SORT · half YOLOv8n HOTA", 43.56, 46.30)], TEAL),
    S("p2-act", "Paper 2 ACT comparison", "Paper 2: SCL vs the ACT comparator",
      "SCL is higher in all three reported HOTA comparisons.",
      "Paper2_V71.pdf · ACT comparison table · NUMBERS_CHECK.md",
      "Each cell uses its own ACT result. The first rounded bars differ by 2.02, while the paper reports +2.01.",
      "ACT", "SCL", [M("KITTI · ByteTrack HOTA", 49.77, 51.79),
      M("KITTI · OC-SORT HOTA", 36.24, 46.30), M("UAVDT · ByteTrack HOTA", 29.01, 30.83),
      M("UAVDT RT-DETR · MOTA", 5.34, 27.99)], TEAL),
    S("p2-pd", "Paper 2 unseen trackers", "Paper 2: PD-SORT on MOT17",
      "A predeclared unseen single-stage host improves with SCL.",
      "Paper2_V71.pdf · frozen PD-SORT test · NUMBERS_CHECK.md",
      "All seven sequences improve in HOTA. Rounded MOTA bars differ by 1.12; the paper reports +1.13.",
      "Host", "+ SCL", [M("HOTA", 68.01, 68.62), M("MOTA", 75.19, 76.31),
      M("IDF1", 81.03, 81.85)], TEAL),
    S("p2-hybrid", "Paper 2 unseen trackers", "Paper 2: Hybrid-SORT stays unchanged",
      "A compatible two-stage host produces identical output with SCL.",
      "Paper2_V71.pdf · frozen Hybrid-SORT test · NUMBERS_CHECK.md",
      "No measured gain is the intended compatibility result for this host.",
      "Host", "+ SCL", [M("HOTA", 66.70, 66.70), M("MOTA", 75.52, 75.52),
      M("IDF1", 77.56, 77.56), M("IDS", 259, 259, False)], TEAL),
    S("p2-uav-rtdetr", "Paper 2 UAVDT results", "Paper 2: UAVDT RT-DETR + ByteTrack",
      "Frozen SCL transfers to unseen drone videos with a replacement detector.",
      "Paper2_V71.pdf · UAVDT RT-DETR-L test · NUMBERS_CHECK.md",
      "The MOTA baseline is only 3.29; the large relative percentage needs its +24.70-point context.",
      "Host", "+ SCL", [M("MOTA", 3.29, 27.99), M("IDF1", 48.59, 54.33),
      M("IDS", 1041, 455, False)], TEAL),
    S("p2-uav-yolo", "Paper 2 UAVDT results", "Paper 2: UAVDT YOLOv8n + ByteTrack",
      "The same frozen layer also helps a second detector–host pair.",
      "Paper2_V71.pdf · UAVDT YOLOv8n test · NUMBERS_CHECK.md",
      "Rounded HOTA bars differ by 1.78; the paper reports +1.77. Its paired interval remains on the preceding slide.",
      "Host", "+ SCL", [M("HOTA", 29.05, 30.83), M("IDF1", 34.52, 38.49),
      M("IDS", 719, 393, False)], TEAL),
]


def is_count(name: str) -> bool:
    return name.split(" ")[0] in {"IDS", "FP", "FN"}


def is_score(name: str) -> bool:
    return any(x in name for x in ("HOTA", "MOTA", "IDF1", "Precision", "Recall"))


def number(value: float, metric: str) -> str:
    if is_count(metric):
        return f"{int(value):,}"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def delta_label(row: dict) -> tuple[str, str, bool | None]:
    base, result = row["baseline"], row["result"]
    diff = result - base
    good = (diff > 0) if row["higher"] else (diff < 0)
    if diff == 0:
        return "0% change vs baseline", "No change", None
    if base <= 0:
        relative = "Relative % undefined: baseline is zero or negative"
    else:
        pct = abs(100 * diff / base)
        precision = 2 if pct < 1 else 1
        word = ("higher" if diff > 0 else "lower") if row["higher"] else ("more" if diff > 0 else "fewer")
        relative = f"{pct:.{precision}f}% {word} vs baseline"
    absolute = abs(diff)
    if is_count(row["name"]):
        change = f"{int(round(absolute)):,} {'more' if diff > 0 else 'fewer'}"
    elif is_score(row["name"]):
        change = f"{'+' if diff > 0 else '−'}{number(absolute, row['name'])} points"
    else:
        change = f"{'+' if diff > 0 else '−'}{number(absolute, row['name'])}"
    return relative, change, good


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else REGULAR, size * SCALE)


def render(spec: dict) -> None:
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), "#FFFFFF")
    draw = ImageDraw.Draw(image)
    P = lambda x: round(x * SCALE)
    def box(x0, y0, x1, y1, fill, radius=0, outline=None, width=1):
        draw.rounded_rectangle((P(x0), P(y0), P(x1), P(y1)), radius=P(radius),
                               fill=fill, outline=outline, width=P(width))
    def text(x, y, value, size=20, color=INK, bold=False):
        draw.text((P(x), P(y)), value, font=font(size, bold), fill=color)
    def wrap(value, max_width, size=20, bold=False):
        words, lines, line = value.split(), [], ""
        for word in words:
            candidate = (line + " " + word).strip()
            if draw.textlength(candidate, font=font(size, bold)) <= P(max_width):
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    for i in range(4):
        x0 = 6 + (i % 2) * 738
        y0 = 4 + (i // 2) * 272
        x1, y1 = x0 + 724, y0 + 263
        box(x0, y0, x1, y1, "#FFFFFF", 17, LINE)
        if i >= len(spec["rows"]):
            box(x0 + 16, y0 + 16, x1 - 16, y1 - 16, "#F6F8FC", 13)
            text(x0 + 31, y0 + 35, "READ THIS RESULT", 17, MUTED, True)
            for j, line in enumerate(wrap(spec["note"], 645, 22, False)[:6]):
                text(x0 + 31, y0 + 81 + j * 33, line, 22, INK)
            continue
        row = spec["rows"][i]
        label = row["name"]
        text(x0 + 26, y0 + 19, label, 26, INK, True)
        base, result = row["baseline"], row["result"]
        min_v, max_v = min(0, base, result), max(0, base, result)
        if min_v == max_v:
            max_v = 1
        lo = min_v * (1.08 if min_v < 0 else 1)
        hi = max_v * 1.07
        left, right = x0 + 174, x0 + 600
        zero = left + (0 - lo) / (hi - lo) * (right - left)
        draw.line((P(zero), P(y0 + 63), P(zero), P(y0 + 160)), fill="#B8C5D5", width=P(2))
        for j, (lab, value, color) in enumerate(((spec["baseline_label"], base, BASE),
                                                 (spec["result_label"], result, spec["color"]))):
            yy = y0 + 71 + j * 56
            text(x0 + 26, yy - 2, lab, 19, MUTED if j == 0 else INK, j == 1)
            dest = left + (value - lo) / (hi - lo) * (right - left)
            a, b = min(zero, dest), max(zero, dest)
            if value != 0:
                if b - a < 4:
                    b = a + 4
                box(a, yy - 4, b, yy + 28, color, 7)
            text(x0 + 612, yy - 2, number(value, label), 20, INK, j == 1)
        relative, absolute, good = delta_label(row)
        status = GOOD if good is True else BAD if good is False else MUTED
        box(x0 + 17, y0 + 177, x1 - 17, y1 - 15, "#EFF8F4" if good is True else "#FFF7E9" if good is False else "#F3F5F8", 10)
        text(x0 + 29, y0 + 185, relative, 21, status, True)
        text(x0 + 29, y0 + 216, absolute, 19, INK)
    image.save(OUT / f"{spec['id']}.png", optimize=True)


def check_source_values() -> None:
    source = (HERE / "index.html").read_text(encoding="utf-8")
    for spec in SPECS:
        pattern = r'<section class="slide"[^>]*data-title="' + re.escape(spec["after"]) + r'"[^>]*>.*?</section>'
        match = re.search(pattern, source, flags=re.S)
        if not match:
            raise AssertionError(f"Missing source slide: {spec['after']}")
        visible = html.unescape(re.sub(r"<[^>]+>", " ", match.group()))
        visible = visible.replace("−", "-").replace(",", "")
        for row in spec["rows"]:
            for value in (row["baseline"], row["result"]):
                token = number(value, row["name"]).replace(",", "").replace("−", "-")
                if token not in visible:
                    raise AssertionError(f"{spec['id']}: {token} absent from {spec['after']}")


def build() -> None:
    ids = [s["id"] for s in SPECS]
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate chart ID")
    check_source_values()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for spec in SPECS:
        render(spec)
        alt = "; ".join(f"{r['name']}: {number(r['baseline'], r['name'])} to {number(r['result'], r['name'])}, {delta_label(r)[0]}" for r in spec["rows"])
        manifest.append({k: spec[k] for k in ("id", "after", "title", "intro", "source", "note")}
                        | {"image": f"assets/results/{spec['id']}.png", "alt": alt})
    (OUT / "manifest.js").write_text("window.ACMOT_RESULT_BARS = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    print(f"OK: {len(SPECS)} chart slides generated; every baseline/result value appears on its source slide.")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        check_source_values()
        assert len(list(OUT.glob("*.png"))) == len(SPECS)
        assert (OUT / "manifest.js").is_file()
        print(f"OK: {len(SPECS)} source-checked chart images and manifest present.")
    else:
        build()
