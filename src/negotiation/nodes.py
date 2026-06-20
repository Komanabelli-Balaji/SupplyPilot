import json

from agents.distributor import distributor
from agents.factory import factory
from agents.retailer import retailer
from agents.supervisor import supervisor

def retailer_node(state):
    state_text = json.dumps(
        state["retailer_state"],
        indent=2
    )
    response = retailer.invoke({
        "messages": [{
            "role": "user",
            "content": state_text
        }]
    })

    return {
        "retailer_decision": response["structured_response"].model_dump()
    }

def distributor_node(state):

    content = f"""
Distributor State:
{json.dumps(
    state["distributor_state"],
    indent=2
)}

Retailer Request:
{state["retailer_decision"]}
"""
    
    response = distributor.invoke({
        "messages": [{
            "role": "user",
            "content": content
        }]
    })

    return {
        "distributor_decision": response["structured_response"].model_dump()
    }

def factory_node(state):

    content = f"""
Factory State:
{json.dumps(
    state["factory_state"],
    indent=2
)}

Distributor Proposal:
{state["distributor_decision"]}
"""

    response = factory.invoke({
        "messages": [{
            "role": "user",
            "content": content
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