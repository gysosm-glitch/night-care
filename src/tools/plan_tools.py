"""book_visit_plan: save a clinic visit plan (write tool, needs user confirmation)."""
from src.tools import data_store
from src.tools.timeutil import to_minutes


def book_visit_plan(clinic_id: str, date: str, time: str, note: str, confirmed: bool) -> dict:
    """Save a clinic visit plan. Only call with confirmed=true after the user has explicitly agreed."""
    if not confirmed:
        return {"error": "User has not confirmed. Ask the user to confirm first, then call again with confirmed=true."}
    places = data_store.load("places")["places"]
    clinic = next((p for p in places if p["id"] == clinic_id), None)
    if clinic is None:
        return {"error": f"Unknown clinic '{clinic_id}'. Call find_open_places to get valid ids."}
    t = to_minutes(time)
    if t is None:
        return {"error": "Invalid time. Use 24-hour HH:MM, e.g. '10:00'."}
    if not (to_minutes(clinic["open"]) <= t < to_minutes(clinic["close"])):
        return {"error": f"{clinic['name']} is closed at {time} (open {clinic['open']}-{clinic['close']}). Pick another time."}
    data = data_store.load("visit_plans")
    plan_id = f"P{len(data['plans']) + 1}"
    data["plans"].append({"id": plan_id, "clinic_id": clinic_id, "date": date, "time": time, "note": note})
    data_store.save("visit_plans", data)
    return {"saved": True, "id": plan_id, "clinic": clinic["name"], "date": date, "time": time}


BOOK_VISIT_PLAN_SCHEMA = {
    "type": "function",
    "function": {
        "name": "book_visit_plan",
        "description": "Save a clinic visit plan. Only call with confirmed=true after the user has explicitly agreed.",
        "parameters": {
            "type": "object",
            "properties": {
                "clinic_id": {"type": "string", "description": "Clinic id from find_open_places, e.g. 'C3'"},
                "date": {"type": "string", "description": "Visit date YYYY-MM-DD"},
                "time": {"type": "string", "description": "Visit time in 24-hour HH:MM"},
                "note": {"type": "string", "description": "Short reason for the visit, e.g. '인후통'"},
                "confirmed": {"type": "boolean", "description": "true only if the user explicitly confirmed this plan"},
            },
            "required": ["clinic_id", "date", "time", "note", "confirmed"],
        },
    },
}
