from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import FINANCE_SYSTEM_PROMPT
from schemas.negotiation import AgentOpinion

finance = create_agent(
    model=get_model(),
    tools=[],
    response_format=AgentOpinion,
    system_prompt=FINANCE_SYSTEM_PROMPT
)