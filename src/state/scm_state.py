from typing import TypedDict

from environment.scm_env import SupplyChainEnvironment
from schemas.factory_offer import FactoryExecutionPlan
from schemas.metrics import SupplyChainMetrics
from schemas.negotiation import NegotiationResult


class SCMState(TypedDict):

    env: SupplyChainEnvironment
    rd_result: NegotiationResult | None
    df_result: NegotiationResult | None
    factory_plan: FactoryExecutionPlan | None
    metrics: SupplyChainMetrics | None
