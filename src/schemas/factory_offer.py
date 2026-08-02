from pydantic import BaseModel


class FactoryExecutionPlan(BaseModel):
    inventory_supply: int
    regular_supply: int
    overtime_supply: int

    regular_replenishment: int
    overtime_replenishment: int

    regular_unit_cost: float
    overtime_unit_cost: float

    lead_time: int
