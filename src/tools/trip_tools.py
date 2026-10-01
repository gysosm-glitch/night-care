"""start_trip / check_arrival: record a trip home and check that the user arrived."""
from src.tools import data_store
from src.tools.timeutil import to_minutes

TIME_ERROR = "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."
LATE_AFTER = 10  # minutes past the ETA before a trip counts as overdue


def _hhmm(minutes: int) -> str:
    """Format minutes since midnight as HH:MM, wrapping past midnight."""
    minutes %= 24 * 60
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _trip_minutes(route: dict, mode: str, now: int, area: str) -> int | dict:
    """Return trip length in minutes for a mode, or an {"error": ...} dict."""
    if mode == "도보":
        return route["walk_minutes"]
    if mode == "버스" and (route["bus_line"] == "-" or now > to_minutes(route["last_bus"])):
        return {"error": f"No bus to {area} now (last bus {route['last_bus']}). Use 도보 or 택시."}
    if mode in ("버스", "택시"):
        return route["bus_minutes"]
    return {"error": f"Unknown mode '{mode}'. Use 도보, 버스, or 택시."}


def start_trip(area: str, time: str, mode: str, confirmed: bool) -> dict:
    """Save a trip home from 충북대 정문 and compute the expected arrival time and a message for a guardian. Only call with confirmed=true after the user has explicitly agreed."""
    if not confirmed:
        return {"error": "User has not confirmed. Summarize the trip and ask the user to confirm first."}
    routes = data_store.load("routes")["routes"]
    if area not in routes:
        return {"error": f"Unknown area '{area}'. Valid: {', '.join(routes)}."}
    now = to_minutes(time)
    if now is None:
        return {"error": TIME_ERROR}
    minutes = _trip_minutes(routes[area], mode, now, area)
    if isinstance(minutes, dict):
        return minutes
    eta, call_by = _hhmm(now + minutes), _hhmm(now + minutes + LATE_AFTER)
    data = data_store.load("trips")
    trip = {"id": f"T{len(data['trips']) + 1}", "area": area, "mode": mode, "depart": time, "eta": eta, "status": "on_the_way"}
    data["trips"].append(trip)
    data_store.save("trips", data)
    ride = "걸어서" if mode == "도보" else f"{mode} 타고"
    message = (f"나 {time}에 충북대 정문에서 출발해서 {area}으로 {ride} 가는 중이야. "
               f"{eta}쯤 도착 예정. {call_by}까지 연락 없으면 전화해 줘!")
    return {"saved": True, **{k: v for k, v in trip.items() if k != "status"}, "guardian_message": message}


def check_arrival(trip_id: str, time: str, arrived: bool) -> dict:
    """Mark a saved trip as arrived, or check whether it is overdue and what to do."""
    data = data_store.load("trips")
    trip = next((t for t in data["trips"] if t["id"] == trip_id), None)
    if trip is None:
        return {"error": f"Unknown trip '{trip_id}'. Call start_trip first or check the trip id."}
    now = to_minutes(time)
    if now is None:
        return {"error": TIME_ERROR}
    if arrived:
        trip["status"] = "arrived"
        data_store.save("trips", data)
        return {"id": trip_id, "status": "arrived"}
    diff = (now - to_minutes(trip["eta"]) + 720) % 1440 - 720  # minutes past ETA, across midnight
    if diff > LATE_AFTER:
        return {"id": trip_id, "status": "overdue", "eta": trip["eta"], "minutes_late": diff,
                "advice": "Ask if they are safe. Suggest contacting their guardian; if in danger, call 112."}
    return {"id": trip_id, "status": "on_the_way", "eta": trip["eta"], "minutes_left": max(0, -diff)}


START_TRIP_SCHEMA = {
    "type": "function",
    "function": {
        "name": "start_trip",
        "description": "Save a trip home from 충북대 정문 and compute the expected arrival time and a message for a guardian. Only call with confirmed=true after the user has explicitly agreed.",
        "parameters": {
            "type": "object",
            "properties": {
                "area": {"type": "string", "description": "Destination district: 개신동, 사창동, 복대동, 봉명동, or 율량동"},
                "time": {"type": "string", "description": "Departure time in 24-hour HH:MM"},
                "mode": {"type": "string", "description": "How they travel: 도보, 버스, or 택시"},
                "confirmed": {"type": "boolean", "description": "true only if the user explicitly confirmed starting this trip"},
            },
            "required": ["area", "time", "mode", "confirmed"],
        },
    },
}

CHECK_ARRIVAL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "check_arrival",
        "description": "Mark a saved trip as arrived, or check whether it is overdue and what to do.",
        "parameters": {
            "type": "object",
            "properties": {
                "trip_id": {"type": "string", "description": "Trip id from start_trip, e.g. 'T1'"},
                "time": {"type": "string", "description": "Current time in 24-hour HH:MM"},
                "arrived": {"type": "boolean", "description": "true if the user says they got home"},
            },
            "required": ["trip_id", "time", "arrived"],
        },
    },
}
