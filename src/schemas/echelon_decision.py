from pydantic import BaseModel


class EchelonDecision(BaseModel):
    quantity: int
    rationale: str
