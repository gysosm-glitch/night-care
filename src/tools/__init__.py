"""Tool registry: the single place where tools are connected to the agent.

TOOL_SCHEMAS   -> sent to the LLM (what the model can SEE)
TOOL_FUNCTIONS -> used by agent.py (what actually RUNS)
"""
from src.tools.calculator import CALCULATE_SCHEMA, calculate
from src.tools.place_tools import FIND_OPEN_PLACES_SCHEMA, find_open_places
from src.tools.plan_tools import BOOK_VISIT_PLAN_SCHEMA, book_visit_plan
from src.tools.route_tools import GET_ROUTE_SCHEMA, get_route
from src.tools.taxi_tools import ESTIMATE_TAXI_COST_SCHEMA, estimate_taxi_cost

TOOL_SCHEMAS = [
    CALCULATE_SCHEMA,
    FIND_OPEN_PLACES_SCHEMA,
    GET_ROUTE_SCHEMA,
    ESTIMATE_TAXI_COST_SCHEMA,
    BOOK_VISIT_PLAN_SCHEMA,
]

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "find_open_places": find_open_places,
    "get_route": get_route,
    "estimate_taxi_cost": estimate_taxi_cost,
    "book_visit_plan": book_visit_plan,
}
