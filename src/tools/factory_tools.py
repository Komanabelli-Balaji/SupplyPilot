from langchain.tools import tool

from environment.scm_env import load_supply_chain


@tool
def get_factory_state():
    """
    Retrieve the factory's local information.

    The factory knows only its own finished goods
    inventory, safety stock and production capacity.

    Returns a JSON object.
    """

    data = load_supply_chain()

    factory = data["factory"]

    return {
        "finished_goods_inventory":
            factory["finished_goods_inventory"],

        "safety_stock":
            factory["safety_stock"],

        "production_capacity":
            factory["production_capacity"]
    }