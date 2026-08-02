from llms.provider import Provider
from prompts.system_prompt import DISTRIBUTOR_SYSTEM_PROMPT
from schemas.negotiation import NegotiationProposal
from tools.economics_tools import (
    get_distributor_economics,
    get_distributor_policy,
    get_replenishment_state,
)

distributor_df = Provider(
    tools=[
        get_replenishment_state,
        get_distributor_policy,
        get_distributor_economics,
    ],
    response_format=NegotiationProposal,
    system_prompt=DISTRIBUTOR_SYSTEM_PROMPT
)     