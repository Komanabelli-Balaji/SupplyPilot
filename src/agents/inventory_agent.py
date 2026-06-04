from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import SYSTEM_PROMPT
from tools.inventory_tools import (
    check_inventory,
    consume_inventory,
    replenish_inventory
)

agent = create_agent(
    model=get_model(),
    tools=[
        check_inventory,
        consume_inventory,
        replenish_inventory
    ],
    system_prompt=SYSTEM_PROMPT
)