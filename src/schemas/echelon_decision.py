from pydantic import BaseModel


class EchelonDecision(BaseModel):
    recommended_quantity: int
    rationale: str
