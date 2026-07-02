import json

from agents.retailer import retailer
from agents.distributor import distributor
from agents.factory import factory
from agents.retailer_review import retailer_review
from agents.supervisor import supervisor


def retailer_node(state):

    content = """
Determine your replenishment decision.
Use your tools before making a decision.

Return EchelonDecision.
"""

    response = retailer.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        }
    )

    return {
        "retailer_decision":
            response["structured_response"].model_dump()
    }


def distributor_node(state):

    prompt = f"""
Retailer Decision
{json.dumps(state["retailer_decision"], indent=2)}

You are the distributor.

Use your tools to
- inspect your local inventory
- inspect your safety stock
- determine how many units can be shipped immediately
- determine how many additional units must be requested from the factory

Do not assume any values.
Use your tools.

Return EchelonDecision.
"""

    response = distributor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    return {
        "distributor_decision":
            response["structured_response"].model_dump()
    }


def factory_node(state):

    prompt = f"""
Distributor Decision
{json.dumps(state["distributor_decision"], indent=2)}

You are the factory.

Use your tools to inspect
- finished goods inventory
- safety stock
- production capacity

Determine how many units you can supply.

Return EchelonDecision.
"""

    response = factory.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    return {
        "factory_decision":
            response["structured_response"].model_dump()
    }


def distributor_final_offer_node(state):

    distributor = state["distributor_decision"]

    requested = distributor["requested_quantity"]
    available = distributor["available_inventory"]

    factory_supply = 0

    if "factory_decision" in state:
        factory_supply = state["factory_decision"]["quantity"]

    final_quantity = min(
        requested,
        available + factory_supply
    )

    if factory_supply == 0:
        rationale = (
            f"{final_quantity} units will be shipped immediately "
            "from distributor inventory."
        )
    else:
        rationale = (
            f"{min(requested, available)} units will be shipped "
            "immediately from distributor inventory and "
            f"{factory_supply} units will be supplied by the factory."
        )

    return {
        "distributor_final_offer": {
            "quantity": final_quantity,
            "rationale": rationale
        }
    }

def retailer_review_node(state):

    prompt = f"""
Your Original Decision
{json.dumps(state["retailer_decision"], indent=2)}

Distributor Final Offer
{json.dumps(state["distributor_final_offer"], indent=2)}

Review the proposal.

Accept only if it is reasonable from the retailer's perspective.

Return ReviewDecision.
"""

    response = retailer_review.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    return {
        "retailer_review":
            response["structured_response"].model_dump()
    }


def supervisor_node(state):

    factory_decision = state.get(
        "factory_decision",
        {
            "quantity": 0,
            "rationale": (
                "Factory not involved because the distributor "
                "fulfilled the order from local inventory."
            )
        }
    )

    prompt = f"""
Retailer Decision
{json.dumps(state["retailer_decision"], indent=2)}

Distributor Decision
{json.dumps(state["distributor_decision"], indent=2)}

Factory Decision
{json.dumps(factory_decision, indent=2)}

Distributor Final Offer
{json.dumps(state["distributor_final_offer"], indent=2)}

Retailer Review
{json.dumps(state["retailer_review"], indent=2)}

Determine whether consensus has been reached.
Do not invent a new quantity.

Return FinalDecision.
"""

    response = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    return {
        "final_decision":
            response["structured_response"].model_dump()
    }
