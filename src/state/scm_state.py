from typing_extensions import TypedDict


class SCMState(TypedDict):
    retailer_state: dict
    distributor_state: dict
    factory_state: dict

    retailer_decision: dict
    distributor_decision: dict
    factory_decision: dict
    
    final_decision: dict
