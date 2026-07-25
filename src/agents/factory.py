from langchain.agents import create_agent

from llms.provider import Provider
from prompts.system_prompt import FACTORY_SYSTEM_PROMPT
from schemas.factory_decision import FactoryDecision
from tools.factory_tools import get_factory_state
from tools.inventory_math import calculate_factory_supply

factory = Provider(
    tools=[
        get_factory_state,
        calculate_factory_supply
    ],
    response_format=FactoryDecision,
    system_prompt=FACTORY_SYSTEM_PROMPT
)