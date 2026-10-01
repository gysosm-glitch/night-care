"""get_emergency_guide: what to do right now, where to go, and a 112 text message."""
from src.tools.spot_tools import find_safe_spots

STEPS = [
    "밝고 사람 많은 큰길·가게로 이동하세요.",
    "112에 전화하세요. 말하기 어려우면 112로 문자 신고하세요.",
    "아래 지구대가 가까우면 들어가세요.",
]


def get_emergency_guide(area: str, time: str, situation: str = "누군가 따라오는 것 같아요") -> dict:
    """Get what to do right now in an emergency: short steps, open safe places in the district, and a ready-to-send 112 text message."""
    found = find_safe_spots(area, time)
    if "error" in found:
        if found["error"].startswith("Unknown area"):
            return {"error": found["error"] + " Call 112 now and say where you are."}
        return found
    spots = [{k: s[k] for k in ("name", "phone", "address") if k in s} for s in found["spots"][:2]]
    sms = f"[긴급] 청주시 {area} 부근, {time}. {situation}. 도와주세요."
    return {"call": "112", "steps": STEPS, "spots": spots, "sms_112": sms}


GET_EMERGENCY_GUIDE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_emergency_guide",
        "description": "Get what to do right now in an emergency: short steps, open safe places in the district, and a ready-to-send 112 text message.",
        "parameters": {
            "type": "object",
            "properties": {
                "area": {"type": "string", "description": "District the user is in or near: 개신동, 사창동, 복대동, 봉명동, or 율량동"},
                "time": {"type": "string", "description": "Current time in 24-hour HH:MM, e.g. '23:30'"},
                "situation": {"type": "string", "description": "Short description of what is happening, e.g. '누군가 따라오는 것 같아요'"},
            },
            "required": ["area", "time"],
        },
    },
}
