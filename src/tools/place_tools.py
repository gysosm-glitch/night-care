"""find_open_places: which clinics/pharmacies are open right now."""
from src.tools import data_store
from src.tools.timeutil import to_minutes

TIME_ERROR = "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."


def find_open_places(time: str, subject: str) -> dict:
    """Find clinics and pharmacies open at a given time for a given medical subject."""
    now = to_minutes(time)
    if now is None:
        return {"error": TIME_ERROR}
    places = data_store.load("places")["places"]
    valid = sorted({s for p in places for s in p["subjects"]})
    if subject not in valid:
        return {"error": f"No place for '{subject}'. Valid subjects: {', '.join(valid)}."}
    found = [
        {"id": p["id"], "name": p["name"], "type": p["type"], "area": p["area"], "open_until": p["close"]}
        for p in places
        if subject in p["subjects"] and to_minutes(p["open"]) <= now < to_minutes(p["close"])
    ]
    return {"time": time, "subject": subject, "places": found}


FIND_OPEN_PLACES_SCHEMA = {
    "type": "function",
    "function": {
        "name": "find_open_places",
        "description": "Find clinics and pharmacies open at a given time for a given medical subject.",
        "parameters": {
            "type": "object",
            "properties": {
                "time": {"type": "string", "description": "Current time in 24-hour HH:MM, e.g. '23:10'"},
                "subject": {"type": "string", "description": "Medical subject: 내과, 소아과, 정형외과, 외과, 이비인후과, 일반의약품, or 상비약"},
            },
            "required": ["time", "subject"],
        },
    },
}
