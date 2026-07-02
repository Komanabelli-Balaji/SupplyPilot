from pydantic import BaseModel


class RetailerDecision(BaseModel):
    quantity: int
    rationale: str