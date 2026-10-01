"""estimate_taxi_cost: taxi fare with the night surcharge."""
from src.tools import data_store
from src.tools.timeutil import to_minutes


def estimate_taxi_cost(minutes: float, time: str) -> dict:
    """Estimate a taxi fare in KRW for a trip of N minutes, including the 20% night surcharge from 22:00 to 04:00."""
    if minutes <= 0:
        return {"error": "minutes must be positive."}
    now = to_minutes(time)
    if now is None:
        return {"error": "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."}
    t = data_store.load("taxi")
    fare = t["base_fare"] + t["per_minute"] * max(0, minutes - t["free_minutes"])
    start, end = to_minutes(t["night_from"]), to_minutes(t["night_to"])
    night = now >= start or now < end
    if night:
        fare *= 1 + t["night_rate"]
    fare = int(round(fare / t["round_to"]) * t["round_to"])
    return {"minutes": minutes, "time": time, "night": night, "fare": fare}


ESTIMATE_TAXI_COST_SCHEMA = {
    "type": "function",
    "function": {
        "name": "estimate_taxi_cost",
        "description": "Estimate a taxi fare in KRW for a trip of N minutes, including the 20% night surcharge from 22:00 to 04:00.",
        "parameters": {
            "type": "object",
            "properties": {
                "minutes": {"type": "number", "description": "Car trip length in minutes: use bus_minutes from get_route, NOT walk_minutes"},
                "time": {"type": "string", "description": "Departure time in 24-hour HH:MM, e.g. '23:10'"},
            },
            "required": ["minutes", "time"],
        },
    },
}
