import math

from langchain.tools import tool


@tool
def calculate_eoq(
    annual_demand: float,
    ordering_cost: float,
    holding_cost: float
) -> float:
    """
    Calculate Economic Order Quantity.
    The arguments of the function are annual_demand, ordering_cost and holding_cost.
    Return value of the function is the eoq value with a precision of 2 decimal places.
    """

    eoq = math.sqrt(
        (2 * annual_demand * ordering_cost) / holding_cost
    )

    return round(eoq, 2)


@tool
def calculate_reorder_point(
    daily_demand: float,
    lead_time: int
) -> float:
    """
    Calculate reorder point.
    Arguments of the function are daily_demand and lead_time.
    Returns the reorder point.
    """

    return (daily_demand * lead_time)


@tool
def days_until_stockout(
    inventory: int,
    daily_demand: float
) -> float:
    """
    Estimate days until stockout.
    Arguments of the function are inventory level and daily_demand.
    Returns the estimated no of days till the next stockout
    """

    if daily_demand <= 0:
        return float("inf")

    return round(inventory / daily_demand, 2)