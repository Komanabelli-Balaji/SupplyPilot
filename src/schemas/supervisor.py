from pydantic import BaseModel


class FinalDecision(BaseModel):
    final_quantity: int
    rationale: str