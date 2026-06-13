from pydantic import BaseModel


class PlannerDecision(BaseModel):
    recommended_quantity: int
    rationale: str