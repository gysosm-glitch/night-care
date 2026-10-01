"""estimate_walk_risk: score how risky it is to walk home at a given time."""
from src.tools import data_store
from src.tools.timeutil import in_window, to_minutes


def _risk_points(r: dict, now: int) -> list:
    """Return (points, reason) pairs for one route at one time. See the formula in docs/03_tool_spec.md."""
    hour = 40 if in_window(now, "22:00", "04:00") else 20 if (
        in_window(now, "20:00", "22:00") or in_window(now, "04:00", "06:00")) else 0
    return [
        (hour, "심야 시간" if hour == 40 else "늦은 시간"),
        (round((1 - r["lit_ratio"]) * 30), f"가로등 {round(r['lit_ratio'] * 100)}%"),
        (max(0, 10 - r["cctv"]) * 2, f"CCTV {r['cctv']}대"),
        (10 if in_window(now, r["busy_until"], "06:00") else 0, "인적 드묾"),
        (10 if r["walk_minutes"] > 20 else 0, f"도보 {r['walk_minutes']}분"),
    ]


def estimate_walk_risk(area: str, time: str) -> dict:
    """Score the risk (0-100) of walking from 충북대 정문 to a district at a given time, based on hour, streetlights, CCTV and foot traffic."""
    routes = data_store.load("routes")["routes"]
    if area not in routes:
        return {"error": f"Unknown area '{area}'. Valid: {', '.join(routes)}."}
    now = to_minutes(time)
    if now is None:
        return {"error": "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."}
    points = _risk_points(routes[area], now)
    score = min(100, sum(p for p, _ in points))
    level = "높음" if score >= 60 else "보통" if score >= 30 else "낮음"
    reasons = [reason for p, reason in points if p > 0]
    return {"area": area, "time": time, "score": score, "level": level, "reasons": reasons}


ESTIMATE_WALK_RISK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "estimate_walk_risk",
        "description": "Score the risk (0-100) of walking from 충북대 정문 to a district at a given time, based on hour, streetlights, CCTV and foot traffic.",
        "parameters": {
            "type": "object",
            "properties": {
                "area": {"type": "string", "description": "Destination district: 개신동, 사창동, 복대동, 봉명동, or 율량동"},
                "time": {"type": "string", "description": "Departure time in 24-hour HH:MM, e.g. '23:10'"},
            },
            "required": ["area", "time"],
        },
    },
}
