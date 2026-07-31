import math

from langchain.tools import tool


@tool
def calculate_eoq(
    annual_demand: float,
    ordering_cost: float,
    holding_cost: float,
) -> float:
    """
    Calculates Economic Order Quantity.
    """
    return math.sqrt(
        (2 * annual_demand * ordering_cost)
        / holding_cost
    )


@tool
def calculate_reorder_point(
    demand: float,
    lead_time: float,
) -> float:
    """
    Calculates reorder point.
    """
    return demand * lead_time


@tool
def calculate_safety_stock(
    max_daily_demand: float,
    average_daily_demand: float,
    max_lead_time: float,
    average_lead_time: float,
) -> float:
    """
    Calculates safety stock.
    """
    return (
        max_daily_demand
        * max_lead_time
        -
        average_daily_demand
        * average_lead_time
    )