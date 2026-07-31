from llms.provider import Provider
from prompts.system_prompt import DISTRIBUTOR_SYSTEM_PROMPT
from schemas.negotiation import NegotiationProposal
from tools.economics_tools import (
    get_annual_demand,
    get_distributor_shortage_cost,
    get_holding_cost,
    get_ordering_cost,
)
from tools.inventory_math import calculate_eoq, calculate_reorder_point
from tools.inventory_tools import get_inventory

distributor = Provider(
    tools=[
        get_inventory,
        get_ordering_cost,
        get_holding_cost,
        get_distributor_shortage_cost,
        get_annual_demand,
        calculate_eoq,
        calculate_reorder_point,
    ],
    response_format=NegotiationProposal,
    system_prompt=DISTRIBUTOR_SYSTEM_PROMPT
)     