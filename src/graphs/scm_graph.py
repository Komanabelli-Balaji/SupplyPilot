from langgraph.graph import  StateGraph, START, END

from state.scm_state import SCMState
from negotiation.nodes import (
    retailer_node,
    distributor_node,
    factory_node,
    supervisor_node
)

builder = StateGraph(SCMState)

builder.add_node("retailer", retailer_node)
builder.add_node("distributor", distributor_node)
builder.add_node("factory", factory_node)
builder.add_node("supervisor", supervisor_node)

builder.add_edge(START, "retailer")
builder.add_edge("retailer", "distributor")
builder.add_edge("distributor", "factory")
builder.add_edge("factory", "supervisor")
builder.add_edge("supervisor", END)

graph = builder.compile()
