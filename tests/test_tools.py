"""Tool tests. No LLM needed.  Run:  python -m pytest tests"""
from src.tools.calculator import calculate


def test_calculate_ok():
    assert calculate("9900 - 1500")["result"] == 8400


def test_data_store_roundtrip():
    from src.tools import data_store
    data = data_store.load("visit_plans")
    data["plans"].append({"id": "X"})
    data_store.save("visit_plans", data)
    assert data_store.load("visit_plans")["plans"][-1]["id"] == "X"


# ---- find_open_places ----
def test_open_at_night_only_emergency():
    from src.tools.place_tools import find_open_places
    ids = {p["id"] for p in find_open_places("23:10", "내과")["places"]}
    assert ids == {"C1"}


def test_open_daytime_includes_clinic():
    from src.tools.place_tools import find_open_places
    ids = {p["id"] for p in find_open_places("10:00", "내과")["places"]}
    assert ids == {"C1", "C2"}


def test_pharmacy_open_until_midnight():
    from src.tools.place_tools import find_open_places
    ids = {p["id"] for p in find_open_places("23:30", "일반의약품")["places"]}
    assert ids == {"C5", "C6"}


def test_unknown_subject_has_hint():
    from src.tools.place_tools import find_open_places
    assert "내과" in find_open_places("23:00", "치과")["error"]


def test_bad_time():
    from src.tools.place_tools import find_open_places
    assert "error" in find_open_places("25:99", "내과")


# ---- get_route ----
def test_route_ok():
    from src.tools.route_tools import get_route
    r = get_route("사창동")
    assert r["minutes"] == 25 and r["last_bus"] == "22:30"


def test_route_last_bus_gone():
    from src.tools.route_tools import get_route
    assert get_route("사창동", "23:10")["bus_available_now"] is False
    assert get_route("사창동", "21:00")["bus_available_now"] is True


def test_route_walk_always_available():
    from src.tools.route_tools import get_route
    assert get_route("개신동", "23:50")["bus_available_now"] is True


def test_route_unknown_area():
    from src.tools.route_tools import get_route
    assert "사창동" in get_route("송정동")["error"]


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


# ---- book_visit_plan ----
def test_book_needs_confirmation():
    from src.tools import data_store
    from src.tools.plan_tools import book_visit_plan
    assert "error" in book_visit_plan("C3", "2026-10-02", "10:00", "인후통", False)
    assert data_store.load("visit_plans")["plans"] == []


def test_book_ok_saves():
    from src.tools import data_store
    from src.tools.plan_tools import book_visit_plan
    r = book_visit_plan("C3", "2026-10-02", "10:00", "인후통", True)
    assert r["saved"] is True and r["id"] == "P1"
    assert len(data_store.load("visit_plans")["plans"]) == 1


def test_book_unknown_clinic():
    from src.tools.plan_tools import book_visit_plan
    assert "find_open_places" in book_visit_plan("X9", "2026-10-02", "10:00", "x", True)["error"]


def test_book_closed_time():
    from src.tools.plan_tools import book_visit_plan
    assert "closed" in book_visit_plan("C3", "2026-10-02", "22:00", "x", True)["error"]


# ---- Registry ----
def test_registry_consistent():
    from src.tools import TOOL_FUNCTIONS, TOOL_SCHEMAS
    names = {s["function"]["name"] for s in TOOL_SCHEMAS}
    assert names == set(TOOL_FUNCTIONS) and len(names) >= 5
