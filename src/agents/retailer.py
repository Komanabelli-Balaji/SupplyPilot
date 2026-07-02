from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import RETAILER_SYSTEM_PROMPT
from schemas.retailer_decision import RetailerDecision
from tools.retailer_tools import get_retailer_state
from tools.inventory_math import (
    calculate_eoq, 
    calculate_reorder_point,
    calculate_stockout_days
)

retailer = create_agent(
    model=get_model(),
    tools=[
        get_retailer_state,
        calculate_eoq,
        calculate_reorder_point,
        calculate_stockout_days
    ],
    response_format=RetailerDecision,
    system_prompt=RETAILER_SYSTEM_PROMPT
)