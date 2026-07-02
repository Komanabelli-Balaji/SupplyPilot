from langgraph.graph import  StateGraph, START, END

from state.scm_state import SCMState
from negotiation.nodes import (
    retailer_node,
    distributor_node,
    factory_node,
    supervisor_node,
    distributor_final_offer_node,
    retailer_review_node,
    distributor_revision_node
)

def distributor_route(state):
    if state["distributor_decision"].get("shortage", 0) > 0:
        return "factory"

    return "offer"

def supervisor_route(state):
    if state["final_decision"]["consensus"]:
        return "done"

    if (state["negotiation_round"] >= state["max_rounds"]):
        return "done"

    return "retry"

builder = StateGraph(SCMState)

builder.add_node("retailer", retailer_node)
builder.add_node("distributor", distributor_node)
builder.add_node("factory", factory_node)
builder.add_node("distributor_offer", distributor_final_offer_node)
builder.add_node("retailer_review", retailer_review_node)
builder.add_node("distributor_revision", distributor_revision_node)
builder.add_node("supervisor", supervisor_node)

builder.add_edge(START, "retailer")
builder.add_edge("retailer", "distributor")

builder.add_conditional_edges(
    "distributor",
    distributor_route,
    {
        "factory": "factory",
        "offer": "distributor_offer"
    }
)

builder.add_edge("factory", "distributor_offer")
builder.add_edge("distributor_offer", "retailer_review")
builder.add_edge("retailer_review", "supervisor")

builder.add_conditional_edges(
    "supervisor",
    supervisor_route,
    {
        "done": END,
        "retry": "distributor_revision"
    }
)

builder.add_edge("distributor_revision", "distributor_offer")

graph = builder.compile()
