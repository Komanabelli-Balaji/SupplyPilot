from negotiation.prompts import build_messages
from schemas.negotiation import (
    NegotiationProposal,
    NegotiationResult,
    NegotiationTurn,
)


class NegotiationEngine:

    def __init__(
        self,
        initiator,
        responder,
        initiator_role: str,
        responder_role: str,
        initiator_prompt: str,
        responder_prompt: str,
        max_rounds: int = 3,
    ):

        self.initiator = initiator
        self.responder = responder

        self.initiator_role = initiator_role
        self.responder_role = responder_role

        self.initiator_prompt = initiator_prompt
        self.responder_prompt = responder_prompt

        self.max_rounds = max_rounds


    def _agreed(
        self,
        first: NegotiationProposal,
        second: NegotiationProposal,
    ) -> bool:

        return (
            first.accepted
            and second.accepted
            and first.proposed_quantity == second.proposed_quantity
        )


    def run(self) -> NegotiationResult:

        history: list[NegotiationTurn] = []

        current = self.initiator.invoke(
            build_messages(
                self.initiator_prompt,
                history,
            )
        )

        for round_number in range(1, self.max_rounds + 1):

            history.append(
                NegotiationTurn(
                    round_number=round_number,
                    proposer=self.initiator_role,
                    proposal=current,
                )
            )

            counter = self.responder.invoke(
                build_messages(
                    self.responder_prompt,
                    history,
                )
            )

            history.append(
                NegotiationTurn(
                    round_number=round_number,
                    proposer=self.responder_role,
                    proposal=counter,
                )
            )

            if self._agreed(current, counter):

                return NegotiationResult(
                    success=True,
                    agreed_quantity=current.proposed_quantity,
                    turns=history,
                    total_rounds=round_number,
                )

            current = self.initiator.invoke(
                build_messages(
                    self.initiator_prompt,
                    history,
                )
            )

        return NegotiationResult(
            success=False,
            agreed_quantity=0,
            turns=history,
            total_rounds=self.max_rounds,
        )
