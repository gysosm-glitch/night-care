"""get_route: walking and bus options from 충북대 정문 to a Cheongju district."""
from src.tools import data_store
from src.tools.timeutil import to_minutes


def get_route(to: str, time: str = "") -> dict:
    """Get the walking time, streetlight and CCTV info, and the bus option from 충북대 정문 to a district."""
    routes = data_store.load("routes")["routes"]
    if to not in routes:
        return {"error": f"Unknown area '{to}'. Valid: {', '.join(routes)}."}
    r = routes[to]
    keys = ["walk_minutes", "lit_ratio", "cctv", "bus_line", "bus_minutes", "fare", "last_bus"]
    result = {"to": to, **{k: r[k] for k in keys}}
    if time:
        now = to_minutes(time)
        if now is None:
            return {"error": "Invalid time. Use 24-hour HH:MM, e.g. '23:10'."}
        has_bus = r["bus_line"] != "-"
        result["bus_available_now"] = has_bus and now <= to_minutes(r["last_bus"])
    return result


GET_ROUTE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_route",
        "description": "Get the walking time, streetlight and CCTV info, and the bus option from 충북대 정문 to a district.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Destination district: 개신동, 사창동, 복대동, 봉명동, or 율량동"},
                "time": {"type": "string", "description": "Optional current time HH:MM; if given, the result says whether the bus still runs"},
            },
            "required": ["to"],
        },
    },
}
