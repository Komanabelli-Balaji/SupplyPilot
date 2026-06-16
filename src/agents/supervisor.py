from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import SUPERVISOR_SYSTEM_PROMPT
from schemas.supervisor import FinalDecision

supervisor = create_agent(
    model=get_model(),
    tools=[],
    response_format=FinalDecision,
    system_prompt=SUPERVISOR_SYSTEM_PROMPT
)