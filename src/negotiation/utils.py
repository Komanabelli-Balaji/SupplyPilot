from negotiation.models import (
    NegotiationRound,
    NegotiationStatus,
)
from schemas.negotiation import NegotiationDecision


def record_round(
    history: list[NegotiationRound],
    round_no: int,
    proposer,
    decision: NegotiationDecision,
) -> None:
    """
    Store one negotiation round.
    """

    history.append(
        NegotiationRound(
            round_no=round_no,
            proposer=proposer.role,
            decision=decision,
        )
    )


def reached_agreement(
    left: NegotiationDecision,
    right: NegotiationDecision,
) -> bool:
    """
    Agreement is reached only if both
    participants accept.
    """

    return left.accepted and right.accepted


def failed(
    rounds: int,
    maximum: int,
) -> bool:

    return rounds >= maximum


def status(
    agreed: bool,
) -> NegotiationStatus:

    if agreed:
        return NegotiationStatus.AGREED

    return NegotiationStatus.FAILED