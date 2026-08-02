from langgraph.graph import END, START, StateGraph

from negotiation.nodes import (
    customer_retailer_node,
    distributor_factory_node,
    needs_factory,
    needs_retailer_negotiation,
    retailer_distributor_node,
    settlement_node,
)
from state.scm_state import SCMState

builder = StateGraph(SCMState)

builder.add_node("customer_retailer", customer_retailer_node)
builder.add_node("retailer_distributor", retailer_distributor_node)
builder.add_node("distributor_factory", distributor_factory_node)
builder.add_node("settlement", settlement_node)

builder.add_edge(START, "customer_retailer")

builder.add_conditional_edges(
    "customer_retailer",
    needs_retailer_negotiation,
    {
        "retailer": "retailer_distributor",
        "settlement": "settlement",
    },
)

builder.add_conditional_edges(
    "retailer_distributor",
    needs_factory,
    {
        "factory": "distributor_factory",
        "settlement": "settlement",
    },
)

builder.add_edge("distributor_factory", "settlement")
builder.add_edge("settlement", END)

graph = builder.compile()
