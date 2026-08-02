import json
from pathlib import Path

from agents.distributor_df import distributor_df
from agents.distributor_rd import distributor_rd
from agents.factory import factory
from agents.retailer import retailer
from negotiation.engine import NegotiationEngine
from negotiation.prompts import build_messages
from negotiation.settlement import settlement
from schemas.factory_offer import FactoryExecutionPlan
from state.scm_state import SCMState


def customer_retailer_node(state: SCMState):
    print("===== Customer → Retailer =====")

    env = state["env"]

    demand = env.generate_customer_demand()
    inventory = env.get_inventory("Retailer")

    served = min(inventory, demand)

    env.remove_inventory(
        "Retailer",
        served,
    )

    remaining_inventory = env.get_inventory("Retailer")
    reorder_point = env.retailer_reorder_point()

    print(f"Demand: {demand}")
    print(f"Served: {served}")
    print(f"Remaining Inventory: {remaining_inventory}")

    return {
        "customer_demand": demand,
        "customer_served": served,
        "skip_retailer_negotiation": (
            remaining_inventory > reorder_point
        ),
    }

def retailer_distributor_node(state: SCMState):
    print("===== Retailer ↔ Distributor =====")

    engine = NegotiationEngine(
        initiator=retailer,
        responder=distributor_rd,
        initiator_role="Retailer",
        responder_role="Distributor",
        initiator_prompt="""
You are the Retailer.

This is the first proposal.
There is no previous proposal to accept.
Set accepted = false.

Use your tools.
Determine your desired replenishment quantity and unit price.

Negotiate until an agreement is reached or the maximum number of rounds is exceeded.
""",
        responder_prompt="""
You are the Distributor.

If you agree with the previous proposal,
set accepted = true and repeat the agreed quantity.

Otherwise,
set accepted = false and provide a counter proposal.

Use your tools.
Evaluate the retailer proposal and make a counter proposal if necessary.
""",
    )

    result = engine.run()

    Path("src/debug").mkdir(exist_ok=True)

    with open("src/debug/rd_result.json", "w") as f:
        json.dump(result.model_dump(), f, indent=4)

    print("✓ Retailer ↔ Distributor completed")

    print(
        f"Negotiation successful: {result.success}, "
        f"Rounds: {result.total_rounds}, "
        f"Agreed quantity: {result.agreed_quantity}"
    )

    env = state["env"]
    env.set_pending_retailer_order(result.agreed_quantity)

    return {
        "rd_result": result,
    }


def distributor_factory_node(state: SCMState):
    print("===== Distributor ↔ Factory =====")
    
    env = state["env"]

    inventory = env.get_inventory("Distributor")
    retailer_order = state["rd_result"].agreed_quantity

    remaining_inventory = inventory - retailer_order
    reorder_point = env.distributor_reorder_point()

    if remaining_inventory > reorder_point:
        return {
            "df_result": None,
            "factory_plan": None,
        }

    required_quantity = env.distributor_eoq()

    engine = NegotiationEngine(
        initiator=distributor_df,
        responder=factory,
        initiator_role="Distributor",
        responder_role="Factory",
        initiator_prompt=f"""
Retailer-distributor negotiation has completed.

Current distributor inventory:
{remaining_inventory}

Distributor reorder point:
{reorder_point}

Desired replenishment quantity (EOQ):
{required_quantity}

This is the first proposal to factory.
There is no previous proposal to accept.
Set accepted = false.

Negotiate ONLY this replenishment quantity.
Prices are fixed.
""",
        responder_prompt="""
You are the Factory.

If you agree with the previous proposal,
set accepted = true and repeat the agreed quantity.

Otherwise,
set accepted = false and provide a counter proposal.

Negotiate ONLY quantity.
Before responding, consult your tools for:

- current inventory
- factory inventory policy
- production capacities
- factory economics

Consider:

- current finished-goods inventory
- regular production capacity
- overtime production capacity

Do not negotiate prices.
Counter only when the requested quantity is infeasible or economically unreasonable.
Return ONLY the required schema.
""",
    )

    result = engine.run()

    with open("src/debug/df_result.json", "w") as f:
        json.dump(result.model_dump(), f, indent=4)

    print("✓ Distributor ↔ Factory results")

    if not result.success:
        return {
            "df_result": result,
            "factory_plan": None,
        }

    plan = factory.invoke_with_schema(
        messages=build_messages(
            f"""
Generate a FactoryExecutionPlan.

Distributor replenishment request:
{required_quantity}

Follow this production policy.

Step 1
Ship as much as possible from finished-goods inventory.

Step 2
If additional units are required, use regular production.

Step 3
If regular production is insufficient, use overtime production.

Step 4
After today's shipment, evaluate the remaining factory inventory.

If the remaining inventory is below the reorder point, use any remaining production capacity to replenish inventory toward the EOQ.

Never exceed:

- finished-goods inventory
- regular production capacity
- overtime production capacity

Return ONLY the FactoryExecutionPlan.
""",
            [],
        ),
        response_format=FactoryExecutionPlan,
    )

    with open("src/debug/factory_plan.json", "w") as f:
        json.dump(plan.model_dump(), f, indent=4)

    print("✓ Distributor ↔ Factory completed")

    return {
        "df_result": result,
        "factory_plan": plan,
    }

def settlement_node(state: SCMState):
    print("===== Settlement =====")

    result = settlement(state)

    with open("src/debug/metrics.json", "w") as f:
        json.dump(result["metrics"].model_dump(), f, indent=4)

    print("✓ Settlement completed")

    return {
        "metrics": result["metrics"],
    }


# Routing functions

def needs_retailer_negotiation(state: SCMState) -> str:

    if state["skip_retailer_negotiation"]:
        return "settlement"

    return "retailer"

def needs_factory(state: SCMState) -> str:
    """
    Determines whether the distributor should negotiate with the factory.

    Returns:
        "factory"     -> run distributor-factory negotiation
        "settlement"  -> skip directly to settlement
    """

    env = state["env"]

    inventory = env.get_inventory("Distributor")
    retailer_order = state["rd_result"].agreed_quantity

    remaining_inventory = inventory - retailer_order
    reorder_point = env.distributor_reorder_point()

    if remaining_inventory <= reorder_point:
        return "factory"

    return "settlement"
