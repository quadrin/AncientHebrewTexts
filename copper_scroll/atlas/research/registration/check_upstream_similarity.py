"""Exploratory printed-plan alignment; no geographic coordinates or accuracy claim."""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fit(source, destination):
    a, b = [complex(*p) for p in source]
    c, d = [complex(*p) for p in destination]
    multiplier = (d - c) / (b - a)
    return multiplier, c - multiplier * a


def xy(z):
    return [round(z.real, 6), round(z.imag, 6)]


source = [[355, 1238], [419, 1265]]
destination = [[186, 675], [239, 698]]
intake = [253, 1200]
rock = [74, 650]
junction_source = [305, 1220]
junction_destination = [149, 666]
multiplier, offset = fit(source, destination)
projected = multiplier * complex(*intake) + offset
junction = multiplier * complex(*junction_source) + offset
pixels_per_m = 173 / 50
rng = random.Random(21)
trials = []
scales = []


def jitter(p):
    return [v + rng.uniform(-4, 4) for v in p]


for _ in range(20000):
    src = [jitter(p) for p in source]
    dst = [jitter(p) for p in destination]
    point = jitter(intake)
    k, t = fit(src, dst)
    q = k * complex(*point) + t
    trials.append([q.real, q.imag, abs(q - complex(*rock)) / pixels_per_m])
    scales.append(abs(k))

output = {
    "reviewed": "2026-09-28",
    "purpose": "Test shared upstream sector on printed plans; not GPS or a feature-position solution",
    "source_frame": "Ilan–Amit 1989 p.283 Fig.1 in 1190-pixel-wide page image; origin top-left; y down",
    "destination_frame": "Reeder–Jol 2006 p.229 Fig.4; 1380x1044 pixels; origin top-left; y down",
    "anchor_order": ["western short tunnel approximate centre", "eastern long tunnel approximate centre"],
    "source_anchors_px": source,
    "destination_anchors_px": destination,
    "intake_source_px": intake,
    "rock_destination_px": rock,
    "junction_source_px": junction_source,
    "junction_destination_px": junction_destination,
    "baseline": {
        "complex_multiplier_real_imag": xy(multiplier),
        "translation_real_imag": xy(offset),
        "scale": abs(multiplier),
        "scale_bar_ratio": 173 / 180,
        "intake_projected_destination_px": xy(projected),
        "drawing_implied_rock_separation_m": abs(projected - complex(*rock)) / pixels_per_m,
        "junction_projected_destination_px": xy(junction),
        "junction_discrepancy_px": abs(junction - complex(*junction_destination)),
        "junction_discrepancy_drawing_m": abs(junction - complex(*junction_destination)) / pixels_per_m,
        "validation": "Two fitted anchors give zero residual by construction. Junction identity is uncertain and is not independent surveyed control.",
    },
    "sensitivity": {
        "seed": 21,
        "trials": 20000,
        "perturbation": "Independent uniform +/-4 pixels per axis on four anchors and intake; analyst-chosen, not calibrated measurement error",
        "projected_x_sampled_range": [min(p[0] for p in trials), max(p[0] for p in trials)],
        "projected_y_sampled_range": [min(p[1] for p in trials), max(p[1] for p in trials)],
        "rock_separation_drawing_m_sampled_range": [min(p[2] for p in trials), max(p[2] for p in trials)],
        "scale_sampled_range": [min(scales), max(scales)],
        "interpretation": "Sampled extrema only; not confidence intervals or exhaustive bounds. Original map distortion and rock-pick uncertainty omitted.",
    },
    "decision": "Consistent with shared collection sector; insufficient to identify intake with boulder or publish geographic geometry",
}

if __name__ == "__main__":
    (HERE / "upstream_similarity.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output["baseline"], indent=2))
