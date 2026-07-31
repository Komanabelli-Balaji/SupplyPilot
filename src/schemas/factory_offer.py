from pydantic import BaseModel


class FactoryExecutionPlan(BaseModel):
    inventory_supply: int
    regular_production: int
    overtime_production: int

    regular_unit_cost: float
    overtime_unit_cost: float

    lead_time: int
