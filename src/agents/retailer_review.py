from langchain.agents import create_agent

from llms.provider import Provider
from prompts.system_prompt import RETAILER_REVIEW_SYSTEM_PROMPT
from schemas.review import ReviewDecision

retailer_review = Provider(
    tools=[],
    response_format=ReviewDecision,
    system_prompt=RETAILER_REVIEW_SYSTEM_PROMPT
)