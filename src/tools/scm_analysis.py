import math

from environment.scm_env import load_supply_chain


def scm_analysis():
    data = load_supply_chain()

    retailer = data["retailer"]
    distributor = data["distributor"]
    factory = data["factory"]
    economics = data["economics"]

    inventory = retailer["inventory"]

    stockout_days = inventory / retailer["daily_demand"]

    eoq = math.sqrt(
        (2 * economics["annual_demand"] * economics["ordering_cost"])
        /
        economics["holding_cost"]
    )

    return {
        "product": data["product"],
        "inventory": inventory,
        "reorder_point": retailer["reorder_point"],
        "stockout_days": round(stockout_days, 2),
        "eoq": round(eoq, 2),
        "distributor_inventory": distributor["inventory"],
        "distributor_safety_stock": distributor["safety_stock"],
        "lead_time": distributor["lead_time"],
        "factory_inventory": factory["finished_goods_inventory"],
        "factory_safety_stock": factory["safety_stock"],
        "production_capacity": factory["production_capacity"]
    }