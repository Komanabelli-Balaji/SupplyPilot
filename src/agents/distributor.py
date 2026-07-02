from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import DISTRIBUTOR_SYSTEM_PROMPT
from schemas.distributor_decision import DistributorDecision
from tools.distributor_tools import get_distributor_state
from tools.inventory_math import (
    calculate_available_inventory,
    calculate_shortage
)

distributor = create_agent(
    model=get_model(),
    tools=[
        get_distributor_state,
        calculate_available_inventory,
        calculate_shortage
    ],
    response_format=DistributorDecision,
    system_prompt=DISTRIBUTOR_SYSTEM_PROMPT
)     