"""
Engine Calculator API
---------------------
Vercel serverless function — receives bore, stroke, fuel via GET params
and returns all tuning calculations as JSON.

Usage:
  GET /api/calculate?bore=57&stroke=58.7&fuel=95
"""

import math
import json
import os
from urllib.parse import parse_qs

_HTML_PATH = os.path.join(os.path.dirname(__file__), "index.html")


# ─── Pure calculation functions (easy to read & test) ─────────────────────────

def calc_displacement(bore_mm: float, stroke_mm: float) -> float:
    """Cylinder displacement in cc."""
    return (math.pi / 4) * (bore_mm ** 2) * stroke_mm / 1000


def calc_valve_sizes(bore_mm: float) -> dict:
    """Recommended valve diameters based on bore size."""
    return {
        "intake_mm":  round(bore_mm * 0.50, 1),
        "exhaust_mm": round(bore_mm * 0.42, 1),
        "throttle_mm": round(bore_mm * 0.60, 1),
    }


def calc_bore_stroke_character(bore_mm: float, stroke_mm: float) -> dict:
    """Classify engine character from bore/stroke ratio."""
    ratio = bore_mm / stroke_mm
    if ratio < 0.9:
        character = "Long Stroke"
        note = "High torque at low RPM — good for street use"
    elif ratio > 1.1:
        character = "Over Square"
        note = "High RPM capability — good for performance builds"
    else:
        character = "Square"
        note = "Balanced torque and RPM"
    return {"ratio": round(ratio, 3), "character": character, "note": note}


FUEL_SPECS = {
    "95":  {"label": "Gasohol 95", "cr": 10.5, "afr_stoich": 14.7, "injector_mult": 1.0, "ignition_btdc": 34},
    "E20": {"label": "E20",        "cr": 11.5, "afr_stoich": 13.8, "injector_mult": 1.2, "ignition_btdc": 35},
    "E85": {"label": "E85",        "cr": 13.0, "afr_stoich":  9.8, "injector_mult": 1.3, "ignition_btdc": 38},
}


def calc_fuel_specs(cc: float, fuel: str) -> dict:
    """Compression ratio, chamber size, injector size for a given fuel."""
    if fuel not in FUEL_SPECS:
        raise ValueError(f"Unknown fuel '{fuel}'. Choose from: {list(FUEL_SPECS)}")
    spec = FUEL_SPECS[fuel]
    return {
        "fuel_label":       spec["label"],
        "compression_ratio": spec["cr"],
        "chamber_cc":       round(cc / (spec["cr"] - 1), 2),
        "injector_cc_min":  round(cc * spec["injector_mult"]),
        "afr_stoich":       spec["afr_stoich"],
        "ignition_btdc":    spec["ignition_btdc"],
    }


def calc_performance_estimate(cc: float, bore_mm: float, stroke_mm: float, cr: float) -> dict:
    """Rough performance estimates for a single-cylinder 4-stroke — guidance only."""
    bs_ratio = bore_mm / stroke_mm

    if bs_ratio > 1.05:
        peak_rpm = 11000
        cam_dur = "270–285°"
        valve_lift = round(bore_mm * 0.28, 1)
    elif bs_ratio < 0.90:
        peak_rpm = 8000
        cam_dur = "250–260°"
        valve_lift = round(bore_mm * 0.24, 1)
    else:
        peak_rpm = 9500
        cam_dur = "260–270°"
        valve_lift = round(bore_mm * 0.26, 1)

    # 4-stroke power: P(W) = BMEP(Pa) × Vd(m³) × (RPM/60) / 2
    # Simplified: kW = BMEP_kPa × cc × RPM / 120,000,000
    bmep_kpa = 900 + (cr - 10) * 30           # tuned NA single ~9–11 bar
    kw_est = (bmep_kpa * cc * peak_rpm) / 120_000_000
    hp_est = kw_est / 0.7457
    torq_est = (kw_est * 9549) / peak_rpm     # Nm

    return {
        "hp_estimate":   round(hp_est, 1),
        "torque_nm":     round(torq_est, 1),
        "peak_rpm":      peak_rpm,
        "cam_duration":  cam_dur,
        "valve_lift_mm": valve_lift,
    }


# ─── WSGI app (Vercel Python runtime entrypoint) ──────────────────────────────

def _compute(params: dict) -> tuple[int, dict]:
    try:
        bore = float(params["bore"][0])
        stroke = float(params["stroke"][0])
        fuel = params.get("fuel", [None])[0]

        if bore <= 0 or stroke <= 0:
            raise ValueError("bore and stroke must be positive numbers")

        cc = calc_displacement(bore, stroke)
        result = {
            "displacement_cc": round(cc, 2),
            "valves": calc_valve_sizes(bore),
            "engine": calc_bore_stroke_character(bore, stroke),
        }
        if fuel:
            fuel_result = calc_fuel_specs(cc, fuel)
            result["fuel"] = fuel_result
            result["performance"] = calc_performance_estimate(
                cc, bore, stroke, fuel_result["compression_ratio"]
            )
        return 200, result
    except KeyError as e:
        return 400, {"error": f"Missing parameter: {e}"}
    except (ValueError, TypeError, IndexError) as e:
        return 400, {"error": str(e)}


def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")

    if path.startswith("/api/calculate"):
        qs = environ.get("QUERY_STRING", "")
        status_code, data = _compute(parse_qs(qs))
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        status = f"{status_code} {'OK' if status_code == 200 else 'Bad Request'}"
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Access-Control-Allow-Origin", "*"),
            ("Content-Length", str(len(body))),
        ]
        start_response(status, headers)
        return [body]

    with open(_HTML_PATH, "rb") as f:
        body = f.read()
    start_response("200 OK", [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ])
    return [body]
