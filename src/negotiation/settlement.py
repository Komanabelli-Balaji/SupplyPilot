from schemas.metrics import SupplyChainMetrics
from state.scm_state import SCMState


def settlement(state: SCMState) -> SCMState:

    env = state["env"]

    rd_result = state["rd_result"]
    df_result = state["df_result"]
    factory_plan = state["factory_plan"]

    economics = env.economics()

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

    factory_supply = df_result.agreed_quantity if df_result is not None else 0

    customer_demand = env.current_demand()

    # -------------------------------------------------------
    # Factory executes production plan
    # -------------------------------------------------------

    factory_production_cost = 0.0
    overtime_cost = 0.0

    if factory_plan is not None:
        inventory_supply = factory_plan.inventory_supply
        regular_production = factory_plan.regular_production
        overtime_production = factory_plan.overtime_production

        # Consume only finished-goods inventory

        env.remove_inventory(
            "Factory",
            inventory_supply,
        )

        factory_production_cost = (
            regular_production * factory_plan.regular_unit_cost
            + overtime_production * factory_plan.overtime_unit_cost
        )

        overtime_cost = overtime_production * (
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
    # Retailer fulfills customer demand
    # -------------------------------------------------------

    retailer_inventory = env.get_inventory("Retailer")

    customer_served = min(
        retailer_inventory,
        customer_demand,
    )

    env.remove_inventory(
        "Retailer",
        customer_served,
    )

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

    retailer_holding_cost = retailer_inventory * economics["holding_cost"]
    distributor_holding_cost = distributor_inventory * economics["holding_cost"]
    factory_holding_cost = factory_inventory * economics["factory_inventory_cost"]

    # -------------------------------------------------------
    # Shortage cost
    # -------------------------------------------------------

    shortage_cost = shortage * economics["retailer_shortage_cost"]

    # -------------------------------------------------------
    # Revenues
    # -------------------------------------------------------

    retailer_revenue = customer_served * economics["retailer_selling_price"]
    distributor_revenue = shipped_to_retailer * economics["distributor_selling_price"]
    factory_revenue = factory_supply * economics["factory_selling_price"]

    # -------------------------------------------------------
    # Purchase costs
    # -------------------------------------------------------

    distributor_purchase_cost = factory_supply * economics["distributor_purchase_price"]

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

    bullwhip_ratio = retailer_order / customer_demand if customer_demand > 0 else 1.0

    # -------------------------------------------------------
    # Save metrics
    # -------------------------------------------------------

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
        customer_demand=customer_demand,
        retailer_order=retailer_order,
        factory_supply=factory_supply,
        customer_served=customer_served,
        remaining_retailer_inventory=retailer_inventory,
        remaining_distributor_inventory=distributor_inventory,
        remaining_factory_inventory=factory_inventory,
    )

    return state
