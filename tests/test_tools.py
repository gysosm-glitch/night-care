"""Tool tests. No LLM needed.  Run:  python -m pytest tests"""
from src.tools.calculator import calculate


def test_calculate_ok():
    assert calculate("9400 - 1500")["result"] == 7900


def test_data_store_roundtrip():
    from src.tools import data_store
    data = data_store.load("escort")
    data["requests"].append({"id": "X"})
    data_store.save("escort", data)
    assert data_store.load("escort")["requests"][-1]["id"] == "X"


def test_time_window_crosses_midnight():
    from src.tools.timeutil import in_window, to_minutes
    assert in_window(to_minutes("00:30"), "22:00", "01:00")
    assert not in_window(to_minutes("01:00"), "22:00", "01:00")
    assert in_window(to_minutes("12:00"), "00:00", "24:00")


# ---- find_safe_spots ----
def test_spots_late_night_bongmyeong():
    from src.tools.spot_tools import find_safe_spots
    ids = {s["id"] for s in find_safe_spots("봉명동", "23:30")["spots"]}
    assert ids == {"S7", "S8", "S11"}


def test_spots_safe_house_after_midnight():
    from src.tools.spot_tools import find_safe_spots
    assert {s["id"] for s in find_safe_spots("봉명동", "00:30")["spots"]} == {"S7", "S8", "S11"}
    assert {s["id"] for s in find_safe_spots("봉명동", "01:30")["spots"]} == {"S7", "S11"}


def test_spots_closed_safe_house_excluded():
    from src.tools.spot_tools import find_safe_spots
    assert {s["id"] for s in find_safe_spots("복대동", "23:30")["spots"]} == {"S5"}


def test_spots_real_police_has_phone_and_address():
    from src.tools.spot_tools import find_safe_spots
    police = next(s for s in find_safe_spots("사창동", "23:00")["spots"] if s["type"] == "지구대")
    assert police["source"] == "공공데이터"
    assert police["phone"] == "043-251-1703" and "1순환로 690" in police["address"]


def test_spots_fake_spot_has_no_phone():
    from src.tools.spot_tools import find_safe_spots
    store = find_safe_spots("개신동", "23:00")["spots"][0]
    assert store["source"] == "가상" and "phone" not in store


def test_spots_unknown_area_has_hint():
    from src.tools.spot_tools import find_safe_spots
    assert "사창동" in find_safe_spots("송정동", "23:00")["error"]


def test_spots_bad_time():
    from src.tools.spot_tools import find_safe_spots
    assert "error" in find_safe_spots("개신동", "25:99")


# ---- get_route ----
def test_route_ok():
    from src.tools.route_tools import get_route
    r = get_route("사창동")
    assert r["walk_minutes"] == 40 and r["cctv"] == 5 and r["last_bus"] == "22:30"


def test_route_last_bus_gone():
    from src.tools.route_tools import get_route
    assert get_route("사창동", "23:10")["bus_available_now"] is False
    assert get_route("사창동", "21:00")["bus_available_now"] is True


def test_route_no_bus_in_gaesin():
    from src.tools.route_tools import get_route
    r = get_route("개신동", "23:50")
    assert r["bus_line"] == "-" and r["bus_available_now"] is False


def test_route_unknown_area():
    from src.tools.route_tools import get_route
    assert "사창동" in get_route("송정동")["error"]


# ---- estimate_walk_risk ----
def test_risk_high_sachang_night():
    from src.tools.risk_tools import estimate_walk_risk
    r = estimate_walk_risk("사창동", "23:10")
    assert r["score"] == 82 and r["level"] == "높음"
    assert "인적 드묾" in r["reasons"]


def test_risk_medium_gaesin_night():
    from src.tools.risk_tools import estimate_walk_risk
    r = estimate_walk_risk("개신동", "23:10")
    assert r["score"] == 43 and r["level"] == "보통"


def test_risk_low_daytime():
    from src.tools.risk_tools import estimate_walk_risk
    r = estimate_walk_risk("개신동", "15:00")
    assert r["score"] == 3 and r["level"] == "낮음"


def test_risk_capped_at_100():
    from src.tools.risk_tools import estimate_walk_risk
    assert estimate_walk_risk("율량동", "02:00")["score"] <= 100


def test_risk_unknown_area():
    from src.tools.risk_tools import estimate_walk_risk
    assert "Valid" in estimate_walk_risk("송정동", "23:00")["error"]


# ---- estimate_taxi_cost ----
def test_taxi_day():
    from src.tools.taxi_tools import estimate_taxi_cost
    r = estimate_taxi_cost(25, "14:00")
    assert r["night"] is False and r["fare"] == 7800


def test_taxi_night_surcharge():
    from src.tools.taxi_tools import estimate_taxi_cost
    r = estimate_taxi_cost(25, "23:10")
    assert r["night"] is True and r["fare"] == 9400


def test_taxi_after_midnight_is_night():
    from src.tools.taxi_tools import estimate_taxi_cost
    assert estimate_taxi_cost(10, "03:30")["night"] is True
    assert estimate_taxi_cost(10, "04:00")["night"] is False


def test_taxi_bad_minutes():
    from src.tools.taxi_tools import estimate_taxi_cost
    assert "error" in estimate_taxi_cost(0, "23:00")


# ---- request_escort ----
def test_escort_needs_confirmation():
    from src.tools import data_store
    from src.tools.escort_tools import request_escort
    assert "error" in request_escort("사창동", "2026-10-02", "23:00", "충북대 정문", False)
    assert data_store.load("escort")["requests"] == []


def test_escort_ok_saves():
    from src.tools import data_store
    from src.tools.escort_tools import request_escort
    r = request_escort("사창동", "2026-10-02", "23:00", "충북대 정문", True)
    assert r["saved"] is True and r["id"] == "E1"
    assert len(data_store.load("escort")["requests"]) == 1


def test_escort_after_midnight_ok():
    from src.tools.escort_tools import request_escort
    assert request_escort("율량동", "2026-10-02", "00:30", "충북대 정문", True)["saved"] is True


def test_escort_outside_service_hours():
    from src.tools.escort_tools import request_escort
    assert "22:00-01:00" in request_escort("사창동", "2026-10-02", "20:00", "충북대 정문", True)["error"]


def test_escort_bad_date():
    from src.tools.escort_tools import request_escort
    assert "error" in request_escort("사창동", "내일", "23:00", "충북대 정문", True)


def test_escort_unknown_area():
    from src.tools.escort_tools import request_escort
    assert "Valid" in request_escort("송정동", "2026-10-02", "23:00", "충북대 정문", True)["error"]


# ---- Registry ----
def test_registry_consistent():
    from src.tools import TOOL_FUNCTIONS, TOOL_SCHEMAS
    names = {s["function"]["name"] for s in TOOL_SCHEMAS}
    assert names == set(TOOL_FUNCTIONS) and len(names) >= 5
