from typing_extensions import TypedDict


class SCMState(TypedDict):
    metrics: dict

    retailer_decision: dict
    distributor_decision: dict
    factory_decision: dict
    
    final_decision: dict
