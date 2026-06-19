from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import FACTORY_SYSTEM_PROMPT
from schemas.echelon_decision import EchelonDecision

factory = create_agent(
    model=get_model(),
    tools=[],
    response_format=EchelonDecision,
    system_prompt=FACTORY_SYSTEM_PROMPT
)