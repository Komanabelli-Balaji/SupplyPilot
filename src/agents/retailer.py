from llms.provider import Provider
from prompts.system_prompt import RETAILER_SYSTEM_PROMPT
from schemas.negotiation import NegotiationProposal
from tools.demand_tools import get_current_demand, get_forecast_demand
from tools.economics_tools import get_annual_demand, get_holding_cost, get_ordering_cost
from tools.inventory_math import (
    calculate_eoq,
    calculate_reorder_point,
    calculate_safety_stock,
)
from tools.inventory_tools import get_inventory

retailer = Provider(
    tools=[
        get_inventory,
        get_current_demand,
        get_forecast_demand,
        get_ordering_cost,
        get_holding_cost,
        get_annual_demand,
        calculate_eoq,
        calculate_reorder_point,
        calculate_safety_stock,
    ],
    response_format=NegotiationProposal,
    system_prompt=RETAILER_SYSTEM_PROMPT
)