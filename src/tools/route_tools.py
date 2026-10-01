"""get_route: how to get from 충북대 정문 to a Cheongju district."""
from src.tools import data_store
from src.tools.timeutil import to_minutes


def get_route(to: str, time: str = "") -> dict:
    """Get the travel mode, minutes, fare and last bus from 충북대 정문 to a district."""
    routes = data_store.load("routes")["routes"]
    if to not in routes:
        return {"error": f"Unknown area '{to}'. Valid: {', '.join(routes)}."}
    r = routes[to]
    result = {"to": to, "mode": r["mode"], "line": r["line"], "minutes": r["minutes"],
              "fare": r["fare"], "last_bus": r["last_bus"]}
    if time:
        now = to_minutes(time)
        if now is None:
            return {"error": "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."}
        result["bus_available_now"] = r["mode"] == "도보" or now <= to_minutes(r["last_bus"])
    return result


GET_ROUTE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_route",
        "description": "Get the travel mode, minutes, fare and last bus from 충북대 정문 to a district.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Destination district: 사창동, 복대동, 개신동, or 율량동"},
                "time": {"type": "string", "description": "Optional current time HH:MM; if given, the result says whether the bus still runs"},
            },
            "required": ["to"],
        },
    },
}
