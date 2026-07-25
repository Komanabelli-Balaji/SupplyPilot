from langchain.agents import create_agent

from llms.provider import Provider
from prompts.system_prompt import SUPERVISOR_SYSTEM_PROMPT
from schemas.supervisor import FinalDecision

supervisor = Provider(
    tools=[],
    response_format=FinalDecision,
    system_prompt=SUPERVISOR_SYSTEM_PROMPT
)