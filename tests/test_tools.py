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
def test_spots_real_police_only():
    from src.tools.spot_tools import find_safe_spots
    spots = find_safe_spots("봉명동", "23:30")["spots"]
    assert [s["id"] for s in spots] == ["S11"]
    assert all(s["source"] == "공공데이터" for s in spots)


def test_spots_real_police_has_phone_and_address():
    from src.tools.spot_tools import find_safe_spots
    police = find_safe_spots("사창동", "23:00")["spots"][0]
    assert police["phone"] == "043-251-1703" and "1순환로 690" in police["address"]


def test_spots_includes_real_119_center():
    from src.tools.spot_tools import find_safe_spots
    spots = {s["id"]: s for s in find_safe_spots("복대동", "02:00")["spots"]}
    assert set(spots) == {"S5", "S12"}
    assert spots["S12"]["type"] == "119안전센터" and spots["S12"]["phone"] == "043-249-9802"


def test_spots_none_in_gaesin_has_hint():
    from src.tools.spot_tools import find_safe_spots
    r = find_safe_spots("개신동", "23:00")
    assert r["spots"] == [] and "112" in r["hint"]


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
    assert "E1" in r["verify"] and "신분증" in r["verify"]
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


def test_escort_info_lists_criteria_and_checks():
    from src.tools.escort_tools import get_escort_info
    r = get_escort_info()
    assert r["hours"] == "22:00-01:00" and "예시" in r["note"]
    assert any("경력 조회" in c for c in r["staff_criteria"])
    assert any("신청 번호" in c for c in r["check_on_meet"])


def test_escort_unknown_area():
    from src.tools.escort_tools import request_escort
    assert "Valid" in request_escort("송정동", "2026-10-02", "23:00", "충북대 정문", True)["error"]


# ---- get_emergency_guide ----
def test_emergency_has_112_sms_and_police():
    from src.tools.emergency_tools import get_emergency_guide
    r = get_emergency_guide("사창동", "23:30")
    assert r["call"] == "112" and r["spots"][0]["phone"] == "043-251-1703"
    assert "사창동" in r["sms_112"] and "23:30" in r["sms_112"]


def test_emergency_custom_situation():
    from src.tools.emergency_tools import get_emergency_guide
    assert "술 취한 사람" in get_emergency_guide("개신동", "00:10", "술 취한 사람이 시비를 걸어요")["sms_112"]


def test_emergency_unknown_area_still_says_112():
    from src.tools.emergency_tools import get_emergency_guide
    assert "112" in get_emergency_guide("송정동", "23:00")["error"]


# ---- start_trip / check_arrival ----
def test_trip_needs_confirmation():
    from src.tools import data_store
    from src.tools.trip_tools import start_trip
    assert "error" in start_trip("사창동", "23:10", "택시", False)
    assert data_store.load("trips")["trips"] == []


def test_trip_taxi_eta_and_message():
    from src.tools.trip_tools import start_trip
    r = start_trip("사창동", "23:10", "택시", True)
    assert r["id"] == "T1" and r["eta"] == "23:35"
    assert "23:45까지" in r["guardian_message"]


def test_trip_walk_eta_wraps_midnight():
    from src.tools.trip_tools import start_trip
    assert start_trip("율량동", "23:30", "도보", True)["eta"] == "00:30"


def test_trip_bus_after_last_bus():
    from src.tools.trip_tools import start_trip
    assert "last bus 22:30" in start_trip("사창동", "23:10", "버스", True)["error"]


def test_trip_bad_mode():
    from src.tools.trip_tools import start_trip
    assert "도보" in start_trip("사창동", "23:10", "자전거", True)["error"]


def test_arrival_marks_done():
    from src.tools import data_store
    from src.tools.trip_tools import check_arrival, start_trip
    start_trip("사창동", "23:10", "택시", True)
    assert check_arrival("T1", "23:30", True)["status"] == "arrived"
    assert data_store.load("trips")["trips"][0]["status"] == "arrived"


def test_arrival_on_the_way_and_overdue():
    from src.tools.trip_tools import check_arrival, start_trip
    start_trip("사창동", "23:50", "택시", True)  # eta 00:15
    assert check_arrival("T1", "00:05", False)["minutes_left"] == 10
    r = check_arrival("T1", "00:30", False)
    assert r["status"] == "overdue" and r["minutes_late"] == 15


def test_arrival_unknown_trip():
    from src.tools.trip_tools import check_arrival
    assert "start_trip" in check_arrival("T9", "23:00", True)["error"]


# ---- Registry ----
def test_registry_consistent():
    from src.tools import TOOL_FUNCTIONS, TOOL_SCHEMAS
    names = {s["function"]["name"] for s in TOOL_SCHEMAS}
    assert names == set(TOOL_FUNCTIONS) and len(names) >= 5
