from langchain.tools import tool

from environment.inventory_state import (
    load_inventory,
    save_inventory
)


@tool
def check_inventory(product: str) -> str:
    """
    Check current inventory level and the reorder point of the product.
    Pass the product name (in singular form) as an argument to check the inventory for that product.
    The output is a string that contains the current inventory level and the reorder point for the product.
    """

    inventory = load_inventory()
    product_info = inventory.get(product)

    if product_info is None:
        return f"{product} not found"

    return f"{product}: {product_info['quantity']} (Reorder Point: {product_info['reorder_point']})"

@tool
def replenish_inventory(
    product: str,
    amount: int
) -> str:
    """
    Add inventory to a product.
    Pass the product name (in singular form) and the amount to add as arguments to replenish the inventory for that product.
    Use this tool when you were explicitly told to add inventory for a product, 
    or when the quantity is below the reorder point and you want to add inventory to bring it back to a healthy level.
    The output is a string that confirms the amount added to the inventory for the product.
    """

    inventory = load_inventory()
    product_info = inventory.get(product)

    if product_info is None:
        return f"{product} not found"

    product_info["quantity"] += amount
    save_inventory(inventory)

    return f"Added {amount} units to {product}"

@tool
def consume_inventory(
    product: str,
    amount: int
) -> str:
    """
    Consume inventory of a product.
    Pass the product name (in singular form) and the amount to consume as arguments to consume the inventory for that product.
    If the inventory level is below the reorder point after consuming, replenish the inventory to bring it back to a healthy level.
    The output is a string that confirms the amount consumed from the inventory for the product and the reorder point.
    """

    inventory = load_inventory()
    product_info = inventory.get(product)

    if product_info is None:
        return f"{product} not found"

    current_qty = product_info["quantity"]

    if current_qty < amount:
        return f"Not enough {product} in inventory. Current quantity: {current_qty}"

    product_info["quantity"] -= amount
    save_inventory(inventory)

    return f"Consumed {amount} units of {product} from inventory. Current quantity: {product_info['quantity']} (Reorder Point: {product_info['reorder_point']})"

@tool
def place_order(
    product: str,
    amount: int
) -> str:
    """
    Place an order for a product.
    Pass the product name (in singular form) and the amount to order as arguments to place an order for that product.
    Use this tool when you want to place an order for a product, but it is not urgent and does not need to be replenished immediately.
    The output is a string that confirms the amount ordered for the product.
    """

    return f"Placed an order for {amount} units of {product}"