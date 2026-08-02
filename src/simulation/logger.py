from pathlib import Path

import pandas as pd

from schemas.metrics import SupplyChainMetrics


class SimulationLogger:

    def __init__(self):
        self.rows = []

    def log_day(
        self,
        day: int,
        metrics: SupplyChainMetrics,
    ):
        self.rows.append(
            {
                "day": day,

                # Profits
                "retailer_profit": metrics.retailer_profit,
                "distributor_profit": metrics.distributor_profit,
                "factory_profit": metrics.factory_profit,

                # Costs
                "retailer_holding_cost": metrics.retailer_holding_cost,
                "distributor_holding_cost": metrics.distributor_holding_cost,
                "factory_holding_cost": metrics.factory_holding_cost,
                "shortage_cost": metrics.shortage_cost,
                "overtime_cost": metrics.overtime_cost,

                # KPIs
                "service_level": metrics.service_level,
                "bullwhip_ratio": metrics.bullwhip_ratio,

                # Policies
                "retailer_eoq": metrics.retailer_eoq,
                "distributor_eoq": metrics.distributor_eoq,
                "factory_eoq": metrics.factory_eoq,

                # Flows
                "customer_demand": metrics.customer_demand,
                "customer_served": metrics.customer_served,
                "retailer_order": metrics.retailer_order,
                "factory_supply": metrics.factory_supply,

                # Inventories
                "retailer_inventory": metrics.remaining_retailer_inventory,
                "distributor_inventory": metrics.remaining_distributor_inventory,
                "factory_inventory": metrics.remaining_factory_inventory,
            }
        )

    def save(
        self,
        filename: str,
    ):

        output_dir = Path("src/simulation/reports")

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        pd.DataFrame(self.rows).to_csv(
            output_dir/filename,
            index=False,
        )