from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import RETAILER_SYSTEM_PROMPT
from schemas.echelon_decision import EchelonDecision

retailer = create_agent(
    model=get_model(),
    tools=[],
    response_format=EchelonDecision,
    system_prompt=RETAILER_SYSTEM_PROMPT
)