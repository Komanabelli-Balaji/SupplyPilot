import json
from pathlib import Path

from agents.distributor import distributor
from agents.factory import factory
from agents.retailer import retailer
from negotiation.engine import NegotiationEngine
from negotiation.prompts import build_messages
from negotiation.settlement import settlement
from schemas.factory_offer import FactoryExecutionPlan


def retailer_distributor_node(state):
    print("===== Retailer ↔ Distributor =====")

    engine = NegotiationEngine(
        initiator=retailer,
        responder=distributor,
        initiator_role="Retailer",
        responder_role="Distributor",
        initiator_prompt="""
You are the Retailer.

Use your tools.
Determine your desired replenishment quantity and unit price.

Negotiate until an agreement is reached or the maximum number of rounds is exceeded.
""",
        responder_prompt="""
You are the Distributor.

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

    return {
        "rd_result": result,
    }


def distributor_factory_node(state):
    print("===== Distributor ↔ Factory =====")

    rd = state["rd_result"]

    engine = NegotiationEngine(
        initiator=distributor,
        responder=factory,
        initiator_role="Distributor",
        responder_role="Factory",
        initiator_prompt=f"""
The retailer-distributor negotiation has completed.

Agreed Quantity:
{rd.agreed_quantity}

Negotiate ONLY the quantity.

Prices are fixed.
Use your tools.
""",
        responder_prompt="""
You are the Factory.

Negotiate ONLY quantity.

Consider:

- inventory
- production capacity
- overtime production
- lead time

Prices are fixed.
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

The negotiated quantity is:
{result.agreed_quantity}

Return ONLY the execution plan.
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

def settlement_node(state):
    print("===== Settlement =====")

    result = settlement(state)

    with open("src/debug/metrics.json", "w") as f:
        json.dump(result["metrics"].model_dump(), f, indent=4)

    print("✓ Settlement completed")

    return {
        "metrics": result["metrics"],
    }


def needs_factory(state) -> str:
    """
    Determines whether the distributor should negotiate with the factory.

    Returns:
        "factory"     -> run distributor-factory negotiation
        "settlement"  -> skip directly to settlement
    """

    env = state["env"]
    rd = state["rd_result"]

    requested = rd.agreed_quantity
    available = env.get_inventory("Distributor")

    if requested > available:
        return "factory"

    return "settlement"
