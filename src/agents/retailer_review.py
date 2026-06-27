from langchain.agents import create_agent

from llms.provider import get_model
from prompts.system_prompt import RETAILER_REVIEW_SYSTEM_PROMPT
from schemas.review import ReviewDecision

retailer_review = create_agent(
    model=get_model(),
    tools=[],
    response_format=ReviewDecision,
    system_prompt=RETAILER_REVIEW_SYSTEM_PROMPT
)