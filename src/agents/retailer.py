from llms.provider import Provider
from prompts.system_prompt import RETAILER_SYSTEM_PROMPT
from schemas.negotiation import NegotiationProposal
from tools.economics_tools import (
    get_retailer_economics,
    get_retailer_policy,
)
from tools.inventory_tools import get_inventory

retailer = Provider(
    tools=[
        get_inventory,
        get_retailer_policy,
        get_retailer_economics,
    ],
    response_format=NegotiationProposal,
    system_prompt=RETAILER_SYSTEM_PROMPT
)