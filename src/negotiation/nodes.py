import json

from agents.retailer import retailer
from agents.distributor import distributor
from agents.factory import factory
from agents.retailer_review import retailer_review
from agents.supervisor import supervisor

from tools.inventory_math import calculate_shortage


def retailer_node(state):

    content = """
Determine your replenishment decision.
Use your tools before making a decision.

Return RetailerDecision.
"""

    messages = [
        {
            "role": "user",
            "content": content
        }
    ]

    response = retailer.invoke(messages=messages)

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

Return DistributorDecision.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = distributor.invoke(messages)

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

Return FactoryDecision.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = factory.invoke(messages)

    return {
        "factory_decision":
            response["structured_response"].model_dump()
    }


def distributor_final_offer_node(state):

    distributor = state["distributor_decision"]

    requested = distributor.get("requested_quantity", 0)
    available = distributor.get("available_inventory", 0)

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

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = retailer_review.invoke(messages)

    return {
        "retailer_review":
            response["structured_response"].model_dump()
    }

def distributor_revision_node(state):

    factory_decision = state.get(
        "factory_decision",
        {
            "quantity": 0,
            "rationale": """
                Factory was not involved because the distributor
                could satisfy the order from local inventory.
                """
        }
    )

    prompt = f"""
You are the Distributor.

Original Retailer Request
{json.dumps(state["retailer_decision"], indent=2)}

Your Previous Offer
{json.dumps(state["distributor_final_offer"], indent=2)}

Retailer's Review
{json.dumps(state["retailer_review"], indent=2)}

Factory Constraints
{json.dumps(factory_decision, indent=2)}

The retailer has rejected your previous offer.

Review the retailer's objections.

You may use your tools again if you need to re-evaluate
inventory availability or shortage after revising your offer.

Do not invent inventory values.
Base your revised proposal only on tool outputs.

If you can improve your offer while respecting
your own inventory constraints and the factory's
constraints, do so.

Otherwise explain clearly why no better offer is
possible.

Return DistributorDecision.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = distributor.invoke(messages)

    decision = state["distributor_decision"].copy()
    decision.update(
        response["structured_response"].model_dump(
            exclude_unset=True
        )
    )

    available = decision["available_inventory"]

    shortage = calculate_shortage.invoke(
        {
            "requested_quantity": decision["quantity"],
            "available_inventory": available
        }
    )

    decision["requested_quantity"] = decision["quantity"]
    decision["shortage"] = shortage

    return {
        "distributor_decision": decision,
        "negotiation_round":
            state["negotiation_round"] + 1
    }

def factory_revision_node(state):

    prompt = f"""
Previous Factory Decision
{json.dumps(state["factory_decision"], indent=2)}

Revised Distributor Decision
{json.dumps(state["distributor_decision"], indent=2)}

You are the Factory.

The distributor has revised its request after
negotiation with the retailer.

Use your tools to inspect
- finished goods inventory
- safety stock
- production capacity

Determine whether you can improve your previous offer.
If you can supply more, revise your quantity.

Otherwise explain why your previous offer is still
the best feasible offer.

Return FactoryDecision.
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = factory.invoke(messages)

    return {
        "factory_decision":
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

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    response = supervisor.invoke(messages)

    return {
        "final_decision":
            response["structured_response"].model_dump()
    }
