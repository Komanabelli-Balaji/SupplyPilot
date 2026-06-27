from pydantic import BaseModel


class ReviewDecision(BaseModel):
    accepted: bool
    quantity: int
    rationale: str