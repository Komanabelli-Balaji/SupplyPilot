from langchain.tools import tool

from environment.scm_env import load_supply_chain


@tool
def get_distributor_state():
    """
    Retrieve the distributor's local information.

    The distributor knows only its own inventory,
    safety stock and transportation lead time.

    Returns a JSON object.
    """

    data = load_supply_chain()

    distributor = data["distributor"]

    return {
        "inventory": distributor["inventory"],
        "safety_stock": distributor["safety_stock"],
        "lead_time": distributor["lead_time"]
    }