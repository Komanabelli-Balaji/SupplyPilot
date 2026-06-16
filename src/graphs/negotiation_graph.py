from langgraph.graph import  StateGraph, START, END

from state.negotiation_state import NegotiationState
from negotiation.nodes import (
    planner_node,
    procurement_node,
    finance_node,
    supervisor_node
)

builder = StateGraph(NegotiationState)

builder.add_node("planner", planner_node)
builder.add_node("procurement", procurement_node)
builder.add_node("finance", finance_node)
builder.add_node("supervisor", supervisor_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "procurement")
builder.add_edge("procurement", "finance")
builder.add_edge("finance", "supervisor")
builder.add_edge("supervisor", END)

graph = builder.compile()
