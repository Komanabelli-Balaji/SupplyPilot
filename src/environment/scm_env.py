import json
from copy import deepcopy


class SupplyChainEnvironment:
    """
    Represents the dynamic state of the supply chain.

    The JSON file is loaded once during initialization.
    All subsequent changes are kept in memory.
    """

    def __init__(
        self,
        file_path: str = "src/data/supply_chain.json",
    ):
        self.file_path = file_path

        with open(self.file_path, "r") as f:
            self.state = deepcopy(json.load(f))

    # Getters

    def economics(self) -> dict:
        return self.state["economics"]

    def demand(self) -> dict:
        return self.state["demand"]

    def capacity(self) -> dict:
        return self.state["capacity"]

    def inventory(self) -> dict:
        return self.state["inventory"]

    # Inventory API

    def get_inventory(self, actor: str) -> int:
        """
        Returns the inventory of an actor.

        Valid actors:
            Retailer
            Distributor
            Factory
        """
        return self.state["inventory"][actor.lower()]

    def add_inventory(
        self,
        actor: str,
        quantity: int,
    ) -> None:
        self.state["inventory"][actor.lower()] += quantity

    def remove_inventory(
        self,
        actor: str,
        quantity: int,
    ) -> None:
        self.state["inventory"][actor.lower()] -= quantity

    def can_supply(
        self,
        actor: str,
        quantity: int,
    ) -> bool:
        """
        Returns whether the actor has sufficient inventory.
        """

        return (
            self.get_inventory(actor)
            >= quantity
        )

    # Capacity API

    def get_capacity(
        self,
        actor: str,
    ) -> int:
        return self.state["capacity"].get(
            actor.lower(),
            0,
        )

    # Demand API

    def current_demand(self) -> int:
        return self.state["demand"]["current"]

    def forecast_demand(self) -> int:
        return self.state["demand"]["forecast"]

    # Utilities

    def snapshot(self) -> dict:
        """
        Returns a deep copy of the current environment.
        Useful for logging and debugging.
        """
        return deepcopy(self.state)

    def reset(self) -> None:
        """
        Reload the initial state from disk.
        Useful for running multiple experiments.
        """

        with open(self.file_path, "r") as f:
            self.state = deepcopy(json.load(f))
