from typing_extensions import TypedDict


class SCMState(TypedDict):
    retailer_decision: dict
    distributor_decision: dict
    factory_decision: dict

    distributor_final_offer: dict
    retailer_review: dict
    
    final_decision: dict

    negotiation_round: int
    max_rounds: int
    consensus: bool
