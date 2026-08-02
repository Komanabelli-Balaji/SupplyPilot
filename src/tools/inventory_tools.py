from langchain.tools import tool

from environment.runtime import get_env


@tool
def get_inventory(actor: str) -> int:
    """
    Returns the current inventory of an actor.

    Valid actors:
    - Retailer
    - Distributor
    - Factory
    """
    env = get_env()
    return env.get_inventory(actor)
