from schemas.metrics import SupplyChainMetrics
from state.scm_state import SCMState


def settlement(state: SCMState) -> SCMState:

    env = state["env"]

    rd_result = state["rd_result"]
    factory_plan = state["factory_plan"]

    economics = env.economics()

    retailer = economics["retailer"]
    distributor = economics["distributor"]
    factory = economics["factory"]

    # -------------------------------------------------------
    # Current inventories
    # -------------------------------------------------------

    retailer_inventory = env.get_inventory("Retailer")
    distributor_inventory = env.get_inventory("Distributor")
    factory_inventory = env.get_inventory("Factory")

    # -------------------------------------------------------
    # Negotiated quantities
    # -------------------------------------------------------

    retailer_order = rd_result.agreed_quantity if rd_result is not None else 0

    factory_supply = 0
    if factory_plan is not None:
        factory_supply = (
            factory_plan.inventory_supply
            + factory_plan.regular_supply
            + factory_plan.overtime_supply
        )

    # -------------------------------------------------------
    # Factory executes production plan
    # -------------------------------------------------------

    factory_production_cost = 0.0
    overtime_cost = 0.0

    if factory_plan is not None:
        inventory_supply = factory_plan.inventory_supply
        regular_supply = factory_plan.regular_supply
        overtime_supply = factory_plan.overtime_supply

        regular_replenishment = factory_plan.regular_replenishment
        overtime_replenishment = factory_plan.overtime_replenishment

        # Consume only finished-goods inventory

        env.remove_inventory(
            "Factory",
            inventory_supply,
        )

        # Produce inventory replenishment for future days

        env.add_inventory(
            "Factory",
            regular_replenishment
            + overtime_replenishment,
        )

        produced = (
            regular_supply + overtime_supply
            + regular_replenishment + overtime_replenishment
        )

        factory_production_cost = (produced > 0) * factory["setup_cost"]

        factory_production_cost += (
            (regular_supply + regular_replenishment)
            * factory_plan.regular_unit_cost
            + (overtime_supply + overtime_replenishment)
            * factory_plan.overtime_unit_cost
        )

        overtime_cost = (overtime_supply + overtime_replenishment) * (
            factory_plan.overtime_unit_cost - factory_plan.regular_unit_cost
        )

    # -------------------------------------------------------
    # Distributor receives factory shipment
    # -------------------------------------------------------

    env.add_inventory(
        "Distributor",
        factory_supply,
    )

    distributor_inventory = env.get_inventory("Distributor")

    # -------------------------------------------------------
    # Distributor fulfills retailer order
    # -------------------------------------------------------

    shipped_to_retailer = min(
        retailer_order,
        distributor_inventory,
    )

    env.remove_inventory(
        "Distributor",
        shipped_to_retailer,
    )

    env.add_inventory(
        "Retailer",
        shipped_to_retailer,
    )

    # -------------------------------------------------------
    # Customer service statistics
    # -------------------------------------------------------

    customer_demand = state["customer_demand"]
    customer_served = state["customer_served"]

    shortage = max(
        0,
        customer_demand - customer_served,
    )

    # -------------------------------------------------------
    # Remaining inventories
    # -------------------------------------------------------

    retailer_inventory = env.get_inventory("Retailer")
    distributor_inventory = env.get_inventory("Distributor")
    factory_inventory = env.get_inventory("Factory")

    # -------------------------------------------------------
    # Holding costs
    # -------------------------------------------------------

    retailer_holding_cost = retailer_inventory * (retailer["holding_cost"]/365)
    distributor_holding_cost = distributor_inventory * (distributor["holding_cost"]/365)
    factory_holding_cost = factory_inventory * (factory["holding_cost"]/365)

    # -------------------------------------------------------
    # Shortage cost
    # -------------------------------------------------------

    shortage_cost = shortage * retailer["shortage_cost"]

    # -------------------------------------------------------
    # Revenues
    # -------------------------------------------------------

    retailer_revenue = customer_served * retailer["selling_price"]
    distributor_revenue = shipped_to_retailer * distributor["selling_price"]
    factory_revenue = factory_supply * factory["selling_price"]

    # -------------------------------------------------------
    # Purchase costs
    # -------------------------------------------------------

    distributor_purchase_cost = factory_supply * distributor["purchase_price"]

    # -------------------------------------------------------
    # Profits
    # -------------------------------------------------------

    retailer_profit = retailer_revenue - retailer_holding_cost - shortage_cost
    
    distributor_profit = (
        distributor_revenue - distributor_purchase_cost - distributor_holding_cost
    )

    factory_profit = factory_revenue - factory_production_cost - factory_holding_cost

    # -------------------------------------------------------
    # KPIs
    # -------------------------------------------------------

    service_level = customer_served / customer_demand if customer_demand > 0 else 1.0

    bullwhip_ratio = env.bullwhip_effect()

    # -------------------------------------------------------
    # Save metrics
    # -------------------------------------------------------

    env.update_inventory_policy(
        customer_demand,
        "retailer",
    )
    env.update_inventory_policy(
        retailer_order,
        "distributor",
    )
    env.update_inventory_policy(
        factory_supply,
        "factory",
    )

    state["metrics"] = SupplyChainMetrics(
        retailer_profit=retailer_profit,
        distributor_profit=distributor_profit,
        factory_profit=factory_profit,

        retailer_holding_cost=retailer_holding_cost,
        distributor_holding_cost=distributor_holding_cost,
        factory_holding_cost=factory_holding_cost,

        shortage_cost=shortage_cost,
        overtime_cost=overtime_cost,

        service_level=service_level,
        bullwhip_ratio=bullwhip_ratio,

        retailer_eoq = env.retailer_eoq(),
        distributor_eoq = env.distributor_eoq(),
        factory_eoq = env.factory_eoq(),

        customer_demand=customer_demand,
        retailer_order=retailer_order,
        factory_supply=factory_supply,
        customer_served=customer_served,

        remaining_retailer_inventory=retailer_inventory,
        remaining_distributor_inventory=distributor_inventory,
        remaining_factory_inventory=factory_inventory,
    )

    return state
