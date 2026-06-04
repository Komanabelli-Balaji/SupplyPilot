from langchain.tools import tool

from environment.inventory_state import (
    load_inventory,
    save_inventory
)


@tool
def check_inventory(product: str) -> str:
    """
    Check current inventory level.
    Pass the product name (in singular form) as an argument to check the inventory for that product.
    """

    inventory = load_inventory()
    qty = inventory.get(product)

    if qty is None:
        return f"{product} not found"

    return f"{product}: {qty}"

@tool
def replenish_inventory(
    product: str,
    amount: int
) -> str:
    """
    Add inventory to a product.
    Pass the product name (in singular form) and the amount to add as arguments to replenish the inventory for that product.
    """

    inventory = load_inventory()
    inventory[product] = inventory.get(product, 0) + amount

    save_inventory(inventory)

    return f"Added {amount} units to {product}"

@tool
def consume_inventory(
    product: str,
    amount: int
) -> str:
    """
    consume inventory of a product.
    Pass the product name (in singular form) and the amount to consume as arguments to consume the inventory for that product.
    """

    inventory = load_inventory()
    current_qty = inventory.get(product)

    if current_qty is None:
        return f"{product} not found"
    
    if current_qty < amount:
        return f"Not enough {product} in inventory. Current quantity: {current_qty}"
    
    inventory[product] = current_qty - amount
    save_inventory(inventory)

    return f"Consumed {amount} units of {product}"