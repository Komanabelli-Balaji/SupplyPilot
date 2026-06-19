import json

from agents.distributor import distributor
from agents.factory import factory
from agents.retailer import retailer
from agents.supervisor import supervisor

def retailer_node(state):
    metrics_text = json.dumps(
        state["metrics"],
        indent=2
    )
    response = retailer.invoke({
        "messages": [{
            "role": "user",
            "content": metrics_text
        }]
    })

    return {
        "retailer_decision": response["structured_response"].model_dump()
    }

def distributor_node(state):
    metrics_text = json.dumps(
        state["metrics"],
        indent=2
    )
    response = distributor.invoke({
        "messages": [{
            "role": "user",
            "content": metrics_text
        }]
    })

    return {
        "distributor_decision": response["structured_response"].model_dump()
    }

def factory_node(state):
    metrics_text = json.dumps(
        state["metrics"],
        indent=2
    )
    response = factory.invoke({
        "messages": [{
            "role": "user",
            "content": metrics_text
        }]
    })

    return {
        "factory_decision": response["structured_response"].model_dump()
    }

def supervisor_node(state):

    content = f"""
Retailer:
{state["retailer_decision"]}

Distributor:
{state["distributor_decision"]}

Factory:
{state["factory_decision"]}

Find a consensus quantity.
"""

    response = supervisor.invoke({
        "messages": [{
            "role": "user",
            "content": content
        }]
    })

    return {
        "final_decision": response["structured_response"].model_dump()
    }