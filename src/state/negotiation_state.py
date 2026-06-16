from typing_extensions import TypedDict


class NegotiationState(TypedDict):
    observation: str
    planner_opinion: dict
    procurement_opinion: dict
    finance_opinion: dict
    final_decision: dict