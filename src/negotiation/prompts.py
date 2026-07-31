from langchain_core.messages import HumanMessage

from schemas.negotiation import NegotiationTurn


def proposal_to_text(turn: NegotiationTurn) -> str:
    proposal = turn.proposal

    constraints = (
        "\n".join(f"- {c}" for c in proposal.constraints)
        if proposal.constraints
        else "None"
    )

    return f"""
Round {turn.round_number}

Speaker:
{turn.proposer}

Accepted:
{proposal.accepted}

Proposed Quantity:
{proposal.proposed_quantity}

Reasoning:
{proposal.reasoning}

Constraints:
{constraints}

Comments:
{proposal.comments}
""".strip()


def build_messages(
    initial_prompt: str,
    history: list[NegotiationTurn],
):
    """
    Build the complete conversation sent to the LLM.

    The system prompt is already attached inside Provider.
    We only provide the user-side negotiation context.
    """

    text = initial_prompt

    if history:
        text += "\n\nNegotiation History\n"
        text += "\n\n".join(
            proposal_to_text(turn)
            for turn in history
        )

    return [HumanMessage(content=text)]