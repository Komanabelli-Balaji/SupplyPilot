from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from typing import Annotated
from typing_extensions import TypedDict

from agents.inventory_agent import agent
from memory.checkpoint import memory


class InventoryState(TypedDict):
    messages: Annotated[list, add_messages]


def agent_node(state: InventoryState):
    result = agent.invoke({
        "messages": state["messages"]
    })

    return {
        "messages": result["messages"]
    }


builder = StateGraph(InventoryState)

builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
builder.add_edge("agent", END)

graph = builder.compile(
    checkpointer=memory
)