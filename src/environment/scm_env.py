import json
import math
import random
import statistics
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

        self._initialize_policy()
        self._pending_retailer_order = 0

    def _initialize_policy(self) -> None:
        retailer_avg = self.state["policy"]["retailer"]["average_demand"]
        distributor_avg = self.state["policy"]["distributor"]["average_demand"]
        factory_avg = self.state["policy"]["factory"]["average_demand"]

        self.state["policy"]["retailer"]["eoq"] = (
            self.calculate_eoq(retailer_avg, "retailer")
        )

        self.state["policy"]["distributor"]["eoq"] = (
            self.calculate_eoq(distributor_avg, "distributor")
        )

        self.state["policy"]["factory"]["eoq"] = (
            self.calculate_eoq(factory_avg, "factory")
        )

    @property
    def pending_retailer_order(self):
        return self._pending_retailer_order

    def set_pending_retailer_order(self, quantity):
        self._pending_retailer_order = quantity

    # Getters

    def economics(self) -> dict:
        return self.state["economics"]

    def capacity(self) -> dict:
        return self.state["capacity"]

    def inventory(self) -> dict:
        return self.state["inventory"]

    # Policy Getters

    def retailer_avg_demand(self) -> int:
        return self.state["policy"]["retailer"]["average_demand"]

    def distributor_avg_demand(self) -> int:
        return self.state["policy"]["distributor"]["average_demand"]

    def factory_avg_demand(self) -> int:
        return self.state["policy"]["factory"]["average_demand"]

    def retailer_eoq(self) -> int:
        return self.state["policy"]["retailer"]["eoq"]

    def distributor_eoq(self) -> int:
        return self.state["policy"]["distributor"]["eoq"]

    def factory_eoq(self) -> int:
        return self.state["policy"]["factory"]["eoq"]

    def retailer_reorder_point(self) -> int:
        return self.state["policy"]["retailer"]["reorder_point"]

    def distributor_reorder_point(self) -> int:
        return self.state["policy"]["distributor"]["reorder_point"]
    
    def factory_reorder_point(self) -> int:
        return self.state["policy"]["factory"]["reorder_point"] 

    # EOQ

    def calculate_eoq(
        self,
        demand: float,
        actor: str,
    ) -> int:

        economics = self.state["economics"][actor.lower()]

        if actor == "factory":
            fixed_cost = economics["setup_cost"]
        else:
            fixed_cost = economics["ordering_cost"]
            
        holding = economics["holding_cost"]

        return round(
            math.sqrt(
                2 * demand * fixed_cost / holding
            )
        )

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

    # KIPs

    def bullwhip_effect(self) -> float:
        retailer_history = self.state["history"]["retailer"]
        distributor_history = self.state["history"]["distributor"]

        if len(retailer_history) > 1:
            demand_variance = statistics.variance(retailer_history)
            order_variance = statistics.variance(distributor_history)

            if demand_variance > 0:
                return order_variance / demand_variance
            else:
                return 1.0

        else:
            return 1.0

    # Utilities

    def generate_customer_demand(self) -> int:
        """
        Generates customer demand.
        Replace this later with a probability distribution.
        """

        demand = random.randint(120, 180)
        return demand

    def update_inventory_policy(
        self,
        demand: int,
        role: str,
    ) -> None:

        history = self.state["history"][role]
        history.append(demand)

        window = self.state["policy"]["window_size"]

        if len(history) > window:
            history.pop(0)
        
        avg_demand = sum(history) / len(history)

        self.state["policy"][role]["average_demand"] = avg_demand
        self.state["policy"][role]["eoq"] = (
            self.calculate_eoq(avg_demand, role)
        )

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
