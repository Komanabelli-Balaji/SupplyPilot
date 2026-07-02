from langchain.tools import tool

from environment.scm_env import load_supply_chain


@tool
def get_retailer_state():
    """
    Retrieve the retailer's local information.

    The retailer only knows its own inventory,
    daily demand, reorder point and purchasing
    economics.

    Returns a JSON object.
    """

    data = load_supply_chain()

    retailer = data["retailer"]
    economics = data["economics"]
    distributor = data["distributor"]

    return {
        "product": data["product"],
        "inventory": retailer["inventory"],
        "daily_demand": retailer["daily_demand"],
        "reorder_point": retailer["reorder_point"],
        "annual_demand": economics["annual_demand"],
        "ordering_cost": economics["ordering_cost"],
        "holding_cost": economics["holding_cost"],
        "lead_time": distributor["lead_time"]
    }