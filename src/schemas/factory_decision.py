from pydantic import BaseModel


class FactoryDecision(BaseModel):
    quantity: int
    rationale: str