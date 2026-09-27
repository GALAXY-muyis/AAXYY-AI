"""
AAXYY AI - Whale Intelligence

Classifies large blockchain transfers while keeping uncertainty explicit.

A transfer between an exchange and a wallet may indicate accumulation
or distribution, but the transfer alone does not prove a buy or sell.
"""

from dataclasses import dataclass

from address_intelligence import classify_address_role


@dataclass
class Transfer:
    token: str
    amount_usd: float
    sender: str
    receiver: str
    timestamp: str = ""
    sender_type: str = "unknown"
    receiver_type: str = "unknown"


@dataclass
class WhaleAssessment:
    classification: str
    confidence: int
    reason: str


def classify_transfer(transfer: Transfer) -> WhaleAssessment:
    """Classify a blockchain transfer for whale-intelligence purposes."""

    if not isinstance(transfer, Transfer):
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=0,
            reason="Transfer data is invalid.",
        )

    if not transfer.token:
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=0,
            reason="Token is missing.",
        )

    if transfer.amount_usd < 0:
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=0,
            reason="Transfer amount cannot be negative.",
        )

    if not transfer.sender or not transfer.receiver:
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=0,
            reason="Sender or receiver address is missing.",
        )

    if transfer.sender == transfer.receiver:
        return WhaleAssessment(
            classification="NORMAL_TRANSFER",
            confidence=100,
            reason="Sender and receiver are the same address.",
        )

    if transfer.amount_usd < 100_000:
        return WhaleAssessment(
            classification="NORMAL_TRANSFER",
            confidence=90,
            reason="Transfer is below the whale threshold.",
        )

    sender_role = classify_address_role(transfer.sender_type)
    receiver_role = classify_address_role(transfer.receiver_type)

    if sender_role == "exchange" and receiver_role == "wallet":
        return WhaleAssessment(
            classification="POSSIBLE_ACCUMULATION",
            confidence=65,
            reason=(
                "Large exchange-to-wallet transfer may indicate accumulation, "
                "but the transfer alone does not prove a purchase."
            ),
        )

    if sender_role == "wallet" and receiver_role == "exchange":
        return WhaleAssessment(
            classification="POSSIBLE_DISTRIBUTION",
            confidence=65,
            reason=(
                "Large wallet-to-exchange transfer may indicate distribution, "
                "but the transfer alone does not prove a sale."
            ),
        )

    return WhaleAssessment(
        classification="WHALE_TRANSFER",
        confidence=75,
        reason=(
            "Large transfer detected, but the address roles do not provide "
            "enough evidence to classify accumulation or distribution."
        ),
    )
