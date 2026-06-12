from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import SYSTEM_PROMPT
from tools.planning_tools import inventory_analysis
from schemas.decisions import PlannerDecision

planner = create_agent(
    model=get_model(),
    tools=[
        inventory_analysis
    ],
    response_format=PlannerDecision,
    system_prompt=SYSTEM_PROMPT
)