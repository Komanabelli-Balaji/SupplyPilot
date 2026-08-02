from llms.provider import Provider
from prompts.system_prompt import DISTRIBUTOR_SYSTEM_PROMPT
from schemas.negotiation import NegotiationProposal
from tools.economics_tools import (
    get_distributor_economics,
    get_distributor_policy,
)
from tools.inventory_tools import get_inventory

distributor_rd = Provider(
    tools=[
        get_inventory,
        get_distributor_policy,
        get_distributor_economics,
    ],
    response_format=NegotiationProposal,
    system_prompt=DISTRIBUTOR_SYSTEM_PROMPT
)     