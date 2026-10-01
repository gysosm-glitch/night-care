"""Tool registry: the single place where tools are connected to the agent.

TOOL_SCHEMAS   -> sent to the LLM (what the model can SEE)
TOOL_FUNCTIONS -> used by agent.py (what actually RUNS)
"""
from src.tools.calculator import CALCULATE_SCHEMA, calculate
from src.tools.emergency_tools import GET_EMERGENCY_GUIDE_SCHEMA, get_emergency_guide
from src.tools.escort_tools import GET_ESCORT_INFO_SCHEMA, REQUEST_ESCORT_SCHEMA, get_escort_info, request_escort
from src.tools.risk_tools import ESTIMATE_WALK_RISK_SCHEMA, estimate_walk_risk
from src.tools.route_tools import GET_ROUTE_SCHEMA, get_route
from src.tools.spot_tools import FIND_SAFE_SPOTS_SCHEMA, find_safe_spots
from src.tools.taxi_tools import ESTIMATE_TAXI_COST_SCHEMA, estimate_taxi_cost
from src.tools.trip_tools import CHECK_ARRIVAL_SCHEMA, START_TRIP_SCHEMA, check_arrival, start_trip

TOOL_SCHEMAS = [
    CALCULATE_SCHEMA,
    FIND_SAFE_SPOTS_SCHEMA,
    GET_ROUTE_SCHEMA,
    ESTIMATE_WALK_RISK_SCHEMA,
    ESTIMATE_TAXI_COST_SCHEMA,
    REQUEST_ESCORT_SCHEMA,
    GET_ESCORT_INFO_SCHEMA,
    GET_EMERGENCY_GUIDE_SCHEMA,
    START_TRIP_SCHEMA,
    CHECK_ARRIVAL_SCHEMA,
]

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "find_safe_spots": find_safe_spots,
    "get_route": get_route,
    "estimate_walk_risk": estimate_walk_risk,
    "estimate_taxi_cost": estimate_taxi_cost,
    "request_escort": request_escort,
    "get_escort_info": get_escort_info,
    "get_emergency_guide": get_emergency_guide,
    "start_trip": start_trip,
    "check_arrival": check_arrival,
}
