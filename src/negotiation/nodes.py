import json

from agents.distributor import distributor
from agents.factory import factory
from agents.retailer import retailer
from agents.supervisor import supervisor
from agents.distributor_review import distributor_review
from agents.retailer_review import retailer_review

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

    retailer_request = state["retailer_decision"]["quantity"]
    inventory = state["distributor_state"]["inventory"]
    safety_stock = state["distributor_state"]["safety_stock"]

    available = max(0, inventory - safety_stock)
    shortage = max(0, retailer_request - available)

    content = f"""
Distributor State

{json.dumps(
state["distributor_state"],
indent=2
)}

Retailer requested

{retailer_request}

Immediately available inventory

{available}

Shortage requiring factory replenishment

{shortage}

Return the shortage quantity that should be requested from the factory.
"""
    
    response = distributor.invoke({
        "messages": [{
            "role": "user",
            "content": content
        }]
    })

    decision = response["structured_response"].model_dump()

    decision["available_inventory"] = available
    decision["shortage"] = shortage

    return {
        "distributor_decision": decision
    }

def factory_node(state):

    content = f"""
Factory State:
{json.dumps(
    state["factory_state"],
    indent=2
)}

Distributor requires
{state["distributor_decision"]["shortage"]}

Produce only the requested shortage.

Return EchelonDecision.
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

def distributor_final_offer_node(state):

    shipped = state["distributor_decision"]["available_inventory"]
    factory_supply = state["factory_decision"]["quantity"]

    total = shipped + factory_supply

    return {
        "distributor_final_offer": {
            "quantity": total,
            "rationale":
                (
                    f"{shipped} shipped from distributor inventory. "
                    f"{factory_supply} supplied by factory."
                )
        }
    }

def retailer_review_node(state):
    
    content = f"""
Retailer State

{json.dumps(
state["retailer_state"],
indent=2
)}

Original Request
{state["retailer_decision"]}

Distributor Final Offer
{state["distributor_final_offer"]}

Determine whether the offer is acceptable.

Return ReviewDecision.
"""
    
    response = retailer_review.invoke({
        "messages": [{
            "role": "user",
            "content": content
        }]
    })

    return {
        "retailer_review": response["structured_response"].model_dump()
    }

def supervisor_node(state):

    content = f"""
Retailer Request

{state["retailer_decision"]}

Distributor Final Offer

{state["distributor_final_offer"]}

Retailer Review

{state["retailer_review"]}

Determine whether consensus has been reached.

Return FinalDecision.
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
