from llms.provider import Provider
from prompts.system_prompt import FACTORY_SYSTEM_PROMPT
from schemas.negotiation import NegotiationProposal
from tools.capacity_tools import get_overtime_capacity, get_regular_capacity
from tools.economics_tools import get_factory_production_cost, get_factory_selling_price
from tools.inventory_tools import get_inventory

factory = Provider(
    tools=[
        get_inventory,
        get_regular_capacity,
        get_overtime_capacity,
        get_factory_production_cost,
        get_factory_selling_price,
    ],
    response_format=NegotiationProposal,
    system_prompt=FACTORY_SYSTEM_PROMPT
)