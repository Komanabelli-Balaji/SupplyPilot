from langchain.tools import tool

from environment.runtime import get_env


@tool
def get_ordering_cost() -> float:
    """
    Returns ordering cost.
    """
    env = get_env()
    return env.economics()["ordering_cost"]


@tool
def get_holding_cost() -> float:
    """
    Returns inventory holding cost.
    """
    env = get_env()
    return env.economics()["holding_cost"]


@tool
def get_retailer_shortage_cost() -> float:
    """
    Returns retailer shortage cost.
    """
    env = get_env()
    return env.economics()["retailer_shortage_cost"]


@tool
def get_distributor_shortage_cost() -> float:
    """
    Returns distributor shortage cost.
    """
    env = get_env()
    return env.economics()["distributor_shortage_cost"]


@tool
def get_factory_production_cost() -> float:
    """
    Returns normal production cost.
    """
    env = get_env()
    return env.economics()["factory_production_cost"]


@tool
def get_factory_selling_price() -> float:
    """
    Returns factory selling price.
    """
    env = get_env()
    return env.economics()["factory_selling_price"]


@tool
def get_distributor_purchase_price() -> float:
    """
    Returns distributor purchase price.
    """
    env = get_env()
    return env.economics()["distributor_purchase_price"]


@tool
def get_distributor_selling_price() -> float:
    """
    Returns distributor selling price.
    """
    env = get_env()
    return env.economics()["distributor_selling_price"]


@tool
def get_retailer_selling_price() -> float:
    """
    Returns retailer selling price.
    """
    env = get_env()
    return env.economics()["retailer_selling_price"]


@tool
def get_annual_demand() -> int:
    """
    Returns annual demand used in EOQ.
    """
    env = get_env()
    return env.economics()["annual_demand"]