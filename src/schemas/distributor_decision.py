from pydantic import BaseModel


class DistributorDecision(BaseModel):
    requested_quantity: int
    available_inventory: int
    shortage: int
    quantity: int
    rationale: str