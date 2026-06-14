from pydantic import BaseModel


class AgentOpinion(BaseModel):
    recommended_quantity: int
    rationale: str