from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import PROCUREMENT_SYSTEM_PROMPT
from schemas.negotiation import AgentOpinion

procurement = create_agent(
    model=get_model(),
    tools=[],
    response_format=AgentOpinion,
    system_prompt=PROCUREMENT_SYSTEM_PROMPT
)