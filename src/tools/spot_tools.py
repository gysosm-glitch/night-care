"""find_safe_spots: police boxes, 24-hour stores and 안심지킴이집 open right now."""
from src.tools import data_store
from src.tools.timeutil import in_window, to_minutes

TIME_ERROR = "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."


def find_safe_spots(area: str, time: str) -> dict:
    """Find safe spots (police boxes, 24-hour convenience stores, 안심지킴이집) open at a given time in a district."""
    areas = list(data_store.load("routes")["routes"])
    if area not in areas:
        return {"error": f"Unknown area '{area}'. Valid: {', '.join(areas)}."}
    now = to_minutes(time)
    if now is None:
        return {"error": TIME_ERROR}
    keys = ["id", "name", "type", "address", "phone", "source"]
    spots = [
        {**{k: s[k] for k in keys if k in s}, "open_until": s["close"]}
        for s in data_store.load("safe_spots")["spots"]
        if s["area"] == area and in_window(now, s["open"], s["close"])
    ]
    result = {"area": area, "time": time, "spots": spots}
    if not spots:
        result["hint"] = "No safe spot open now. Call 112 in an emergency."
    return result


FIND_SAFE_SPOTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "find_safe_spots",
        "description": "Find safe spots (police boxes, 24-hour convenience stores, 안심지킴이집) open at a given time in a district.",
        "parameters": {
            "type": "object",
            "properties": {
                "area": {"type": "string", "description": "District: 개신동, 사창동, 복대동, 봉명동, or 율량동"},
                "time": {"type": "string", "description": "Current time in 24-hour HH:MM, e.g. '23:10'"},
            },
            "required": ["area", "time"],
        },
    },
}
