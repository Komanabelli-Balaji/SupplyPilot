from pydantic import BaseModel


class ReviewDecision(BaseModel):
    accepted: bool
    quantity: int
    counter_offer: int
    rationale: str