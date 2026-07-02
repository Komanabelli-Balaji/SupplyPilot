from langchain.tools import tool
import math


@tool
def calculate_eoq(
    annual_demand: float,
    ordering_cost: float,
    holding_cost: float
) -> float:
    """
    Calculate the Economic Order Quantity (EOQ).

    Arguments:
    - annual_demand
    - ordering_cost
    - holding_cost

    Returns:
    EOQ rounded to two decimal places.
    """

    return round(
        math.sqrt(
            (2 * annual_demand * ordering_cost)
            / holding_cost
        ),
        2
    )


@tool
def calculate_reorder_point(
    daily_demand: float,
    lead_time: int
) -> float:
    """
    Calculate reorder point.

    Arguments:
    - daily_demand
    - lead_time

    Returns:
    Inventory level at which replenishment should begin.
    """

    return daily_demand * lead_time


@tool
def calculate_stockout_days(
    inventory: int,
    daily_demand: float
) -> float:
    """
    Estimate the number of days until stockout.

    Arguments:
    - inventory
    - daily_demand

    Returns:
    Number of days until inventory reaches zero.
    """

    if daily_demand <= 0:
        return float("inf")

    return round(
        inventory / daily_demand,
        2
    )


@tool
def calculate_available_inventory(
    inventory: int,
    safety_stock: int
) -> int:
    """
    Calculate the inventory available for shipment while
    preserving safety stock.

    Arguments:
    - inventory
    - safety_stock

    Returns:
    Inventory immediately available for customer orders.
    """

    return max(
        0,
        inventory - safety_stock
    )


@tool
def calculate_shortage(
    requested_quantity: int,
    available_inventory: int
) -> int:
    """
    Calculate the quantity that cannot be fulfilled immediately from the distributor's available inventory.

    Arguments:
    - requested_quantity: quantity requested by the retailer.
    - available_inventory: inventory available after preserving safety stock.

    Returns:
    The shortage that must be requested from the factory.

    This tool performs only the mathematical calculation.
    It does not decide whether the distributor should place the request.
    """

    return max(
        0,
        requested_quantity - available_inventory
    )


@tool
def calculate_factory_supply(
    requested_quantity: int,
    finished_goods_inventory: int,
    safety_stock: int,
    production_capacity: int
) -> int:
    """
    Calculate the maximum quantity the factory can supply immediately.

    Arguments:
    - requested_quantity
    - finished_goods_inventory
    - safety_stock
    - production_capacity

    The calculation first uses finished goods inventory while preserving safety stock.
    If additional supply is required, production capacity is used.

    Returns:
    The maximum feasible supply quantity.

    This tool performs only the calculation.
    It does not decide whether the factory should accept or reject a request.
    """

    available_inventory = max(
        0,
        finished_goods_inventory - safety_stock
    )

    return min(
        requested_quantity,
        available_inventory + production_capacity
    )