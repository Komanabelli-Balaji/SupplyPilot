from langchain.tools import tool

from environment.runtime import get_env
from environment.scm_env import SupplyChainEnvironment


@tool
def get_retailer_policy() -> dict:
    """
    Returns the retailer inventory policy like:
    - Average demand
    - EOQ
    - Reorder Point
    """

    env: SupplyChainEnvironment = get_env()

    return {
        "average_demand": env.retailer_avg_demand(),
        "eoq": env.retailer_eoq(),
        "reorder_point": env.retailer_reorder_point(),
    }

@tool
def get_retailer_economics() -> dict:
    """
    Returns retailer's economics like:
    - Ordering cost
    - Holding cost
    - Shortage cost
    """

    env: SupplyChainEnvironment = get_env()

    return {
        "ordering_cost": env.economics()["retailer"]["ordering_cost"],
        "holding_cost": env.economics()["retailer"]["holding_cost"],
        "shortage_cost": env.economics()["retailer"]["shortage_cost"],
        "selling_price": env.economics()["retailer"]["selling_price"],
        "purchase_price": env.economics()["retailer"]["purchase_price"]
    }

@tool
def get_distributor_policy() -> dict:
    """
    Returns the distributor inventory policy like:
    - Average demand
    - EOQ
    - Reorder Point
    """

    env: SupplyChainEnvironment = get_env()

    return {
        "average_demand": env.distributor_avg_demand(),
        "eoq": env.distributor_eoq(),
        "reorder_point": env.distributor_reorder_point(),
    }

@tool
def get_distributor_economics() -> dict:
    """
    Returns distributor's economics like:
    - Ordering cost
    - Holding cost
    - Shortage cost
    """

    env: SupplyChainEnvironment = get_env()

    return {
        "ordering_cost": env.economics()["distributor"]["ordering_cost"],
        "holding_cost": env.economics()["distributor"]["holding_cost"],
        "shortage_cost": env.economics()["distributor"]["shortage_cost"],
        "selling_price": env.economics()["distributor"]["selling_price"],
        "purchase_price": env.economics()["distributor"]["purchase_price"]
    }


@tool
def get_replenishment_state() -> dict:
    """
    Returns the distributor's replenishment state after today's
    retailer shipment.

    This tool should ONLY be used during the Distributor → Factory
    negotiation.

    The projected inventory is computed assuming today's agreed
    retailer shipment has already been committed.

    Returns:
        A dictionary containing:

        - current_inventory:
            Distributor inventory before shipment.

        - retailer_order:
            Quantity committed to the retailer.

        - projected_inventory:
            Inventory remaining after serving the retailer.

        - reorder_point:
            Distributor reorder point.

        - eoq:
            Distributor Economic Order Quantity.

        - needs_replenishment:
            True if projected inventory is at or below the
            reorder point.
    """

    env: SupplyChainEnvironment = get_env()

    current_inventory = env.get_inventory("Distributor")
    retailer_order = env.pending_retailer_order
    projected_inventory = max(
        0,
        current_inventory - retailer_order,
    )

    reorder_point = env.distributor_reorder_point()
    eoq = env.distributor_eoq()

    return {
        "current_inventory": current_inventory,
        "retailer_order": retailer_order,
        "projected_inventory": projected_inventory,
        "reorder_point": reorder_point,
        "eoq": eoq,
        "needs_replenishment": (
            projected_inventory <= reorder_point
        ),
    }

@tool
def get_factory_policy() -> dict:
    """
    Returns factory inventory policy.

    Includes
    - average demand
    - EOQ
    - reorder point
    """

    env: SupplyChainEnvironment = get_env()

    return {
        "average_demand": env.factory_avg_demand(),
        "eoq": env.factory_eoq(),
        "reorder_point": env.factory_reorder_point()
    }

@tool
def get_factory_economics() -> dict:
    """
    Returns factory economics.

    Includes:
    - Inventory holding cost
    - Selling price
    - Regular production cost
    - Overtime production cost
    """

    env: SupplyChainEnvironment = get_env()

    return {
        "setup_cost": env.economics()["factory"]["setup_cost"],
        "holding_cost": env.economics()["factory"]["holding_cost"],
        "selling_price": env.economics()["factory"]["selling_price"],
        "regular_unit_cost": env.economics()["factory"]["regular_unit_cost"],
        "overtime_unit_cost": env.economics()["factory"]["overtime_unit_cost"],
    }