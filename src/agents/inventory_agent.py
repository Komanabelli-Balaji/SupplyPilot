from langchain.agents import create_agent

from config.settings import MODEL
from prompts.system_prompt import SYSTEM_PROMPT
from tools.inventory_tools import (
    check_inventory,
    replenish_inventory
)

agent = create_agent(
    model=MODEL,
    tools=[
        check_inventory,
        replenish_inventory
    ],
    system_prompt=SYSTEM_PROMPT
)