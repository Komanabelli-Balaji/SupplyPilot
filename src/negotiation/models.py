from enum import Enum

from pydantic import BaseModel

from schemas.negotiation import NegotiationDecision


class NegotiationRole(str, Enum):
    RETAILER = "Retailer"
    DISTRIBUTOR = "Distributor"
    FACTORY = "Factory"


class NegotiationStatus(str, Enum):
    AGREED = "agreed"
    FAILED = "failed"
    ONGOING = "ongoing"


class NegotiationRound(BaseModel):
    """
    Represents one proposal made by one participant.
    """

    round_no: int
    proposer: NegotiationRole
    decision: NegotiationDecision


class NegotiationResult(BaseModel):
    """
    Final output of an entire negotiation.
    """

    status: NegotiationStatus
    agreed_quantity: int
    agreed_price: float
    rounds: list[NegotiationRound]