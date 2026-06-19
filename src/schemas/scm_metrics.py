from pydantic import BaseModel


class SCMMetrics(BaseModel):
    product: str
    inventory: int
    reorder_point: int
    stockout_days: float
    eoq: float
    distributor_inventory: int
    lead_time: int
    factory_inventory: int
    production_capacity: int