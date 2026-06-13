from langchain.tools import tool

from environment.inventory_state import load_inventory
from tools.eoq_tools import (
    calculate_eoq,
    calculate_reorder_point,
    days_until_stockout
)


@tool
def inventory_analysis(product: str):
    """
    Analyze inventory and return
    planning metrics for a product.
    """

    inventory = load_inventory()
    info = inventory.get(product)

    if info is None:
        return f"{product} not found"

    eoq = calculate_eoq.invoke({
        "annual_demand": info["annual_demand"],
        "ordering_cost": info["ordering_cost"],
        "holding_cost": info["holding_cost"]
    })

    rop = calculate_reorder_point.invoke({
        "daily_demand": info["daily_demand"],
        "lead_time": info["lead_time"]
    })

    stockout = days_until_stockout.invoke({
        "inventory": info["inventory"],
        "daily_demand": info["daily_demand"]
    })

    return {
        "inventory": info["inventory"],
        "eoq": eoq,
        "reorder_point": rop,
        "stockout_days": stockout
    }

def needs_replenishment(analysis: dict):
    """
    Determine if replenishment is needed based on inventory analysis.
    The argument is the output of inventory_analysis tool.
    Output is a boolean indicating if inventory is below reorder point.
    """
    return (
        analysis["inventory"]
        < analysis["reorder_point"]
    )