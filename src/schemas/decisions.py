from pydantic import BaseModel


class PlannerDecision(BaseModel):
    quantity: int
    reason: str