from pydantic import BaseModel


class SupplyChainMetrics(BaseModel):

    retailer_profit: float
    distributor_profit: float
    factory_profit: float

    retailer_holding_cost: float
    distributor_holding_cost: float
    factory_holding_cost: float

    shortage_cost: float
    overtime_cost: float

    service_level: float
    bullwhip_ratio: float

    retailer_eoq: int
    distributor_eoq: int
    factory_eoq: int

    customer_demand: int
    retailer_order: int
    factory_supply: int
    customer_served: int

    remaining_retailer_inventory: int
    remaining_distributor_inventory: int
    remaining_factory_inventory: int