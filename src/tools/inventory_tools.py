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


@tool
def add_inventory(
    actor: str,
    quantity: int,
) -> str:
    """
    Adds inventory to an actor.
    """
    env = get_env()
    env.add_inventory(actor, quantity)
    return (
        f"{quantity} units added to {actor}. "
        f"Current inventory: {env.get_inventory(actor)}"
    )


@tool
def remove_inventory(
    actor: str,
    quantity: int,
) -> str:
    """
    Removes inventory from an actor.
    """
    env = get_env()
    env.remove_inventory(actor, quantity)
    return (
        f"{quantity} units removed from {actor}. "
        f"Current inventory: {env.get_inventory(actor)}"
    )