from pydantic import BaseModel


class FinalDecision(BaseModel):
    consensus: bool
    final_quantity: int
    rationale: str