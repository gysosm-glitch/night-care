"""request_escort: save a 안심귀가 escort request (write tool, needs user confirmation)."""
from datetime import datetime

from src.tools import data_store
from src.tools.timeutil import in_window, to_minutes


def _valid_date(text: str) -> bool:
    """True if text is a real date in YYYY-MM-DD."""
    try:
        datetime.strptime(str(text), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def request_escort(area: str, date: str, time: str, meet_point: str, confirmed: bool) -> dict:
    """Save a 안심귀가 escort request. Only call with confirmed=true after the user has explicitly agreed."""
    if not confirmed:
        return {"error": "User has not confirmed. Summarize the request and ask the user to confirm first."}
    areas = list(data_store.load("routes")["routes"])
    if area not in areas:
        return {"error": f"Unknown area '{area}'. Valid: {', '.join(areas)}."}
    now = to_minutes(time)
    if now is None or not _valid_date(date):
        return {"error": "Invalid date/time. Use YYYY-MM-DD and HH:MM."}
    data = data_store.load("escort")
    s = data["service"]
    if not in_window(now, s["start"], s["end"]):
        return {"error": f"Escort runs {s['start']}-{s['end']} only. Pick a time in that window or suggest a taxi."}
    req = {"id": f"E{len(data['requests']) + 1}", "area": area, "date": date, "time": time, "meet_point": meet_point}
    data["requests"].append(req)
    data_store.save("escort", data)
    return {"saved": True, **req}


REQUEST_ESCORT_SCHEMA = {
    "type": "function",
    "function": {
        "name": "request_escort",
        "description": "Save a 안심귀가 escort request. Only call with confirmed=true after the user has explicitly agreed.",
        "parameters": {
            "type": "object",
            "properties": {
                "area": {"type": "string", "description": "Destination district: 개신동, 사창동, 복대동, 봉명동, or 율량동"},
                "date": {"type": "string", "description": "Date YYYY-MM-DD"},
                "time": {"type": "string", "description": "Meeting time in 24-hour HH:MM (service runs 22:00-01:00)"},
                "meet_point": {"type": "string", "description": "Where to meet the escort, e.g. '충북대 정문'"},
                "confirmed": {"type": "boolean", "description": "true only if the user explicitly confirmed this request"},
            },
            "required": ["area", "date", "time", "meet_point", "confirmed"],
        },
    },
}
