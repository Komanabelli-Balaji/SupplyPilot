from agents.planner import planner
from agents.procurement import procurement
from agents.finance import finance
from agents.supervisor import supervisor

def planner_node(state):
    response = planner.invoke({
        "messages": [{
            "role": "user",
            "content": state["observation"]
        }]
    })

    return {
        "planner_opinion": response["structured_response"]
    }

def procurement_node(state):
    response = procurement.invoke({
        "messages": [{
            "role": "user",
            "content": state["observation"]
        }]
    })

    return {
        "procurement_opinion": response["structured_response"]
    }

def finance_node(state):
    response = finance.invoke({
        "messages": [{
            "role": "user",
            "content": state["observation"]
        }]
    })

    return {
        "finance_opinion": response["structured_response"]
    }

def supervisor_node(state):

    content = f"""
Planner Recommendation:
{state["planner_opinion"]}

Procurement Recommendation:
{state["procurement_opinion"]}

Finance Recommendation:
{state["finance_opinion"]}

Choose a final quantity.
"""

    response = supervisor.invoke({
        "messages": [{
            "role": "user",
            "content": content
        }]
    })

    return {
        "final_decision": response["structured_response"]
    }