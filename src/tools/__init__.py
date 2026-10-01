"""Tool registry: the single place where tools are connected to the agent.

TOOL_SCHEMAS   -> sent to the LLM (what the model can SEE)
TOOL_FUNCTIONS -> used by agent.py (what actually RUNS)
"""
from src.tools.calculator import CALCULATE_SCHEMA, calculate
from src.tools.escort_tools import REQUEST_ESCORT_SCHEMA, request_escort
from src.tools.risk_tools import ESTIMATE_WALK_RISK_SCHEMA, estimate_walk_risk
from src.tools.route_tools import GET_ROUTE_SCHEMA, get_route
from src.tools.spot_tools import FIND_SAFE_SPOTS_SCHEMA, find_safe_spots
from src.tools.taxi_tools import ESTIMATE_TAXI_COST_SCHEMA, estimate_taxi_cost

TOOL_SCHEMAS = [
    CALCULATE_SCHEMA,
    FIND_SAFE_SPOTS_SCHEMA,
    GET_ROUTE_SCHEMA,
    ESTIMATE_WALK_RISK_SCHEMA,
    ESTIMATE_TAXI_COST_SCHEMA,
    REQUEST_ESCORT_SCHEMA,
]

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "find_safe_spots": find_safe_spots,
    "get_route": get_route,
    "estimate_walk_risk": estimate_walk_risk,
    "estimate_taxi_cost": estimate_taxi_cost,
    "request_escort": request_escort,
}
