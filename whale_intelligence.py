from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Transfer:
    """A normalized blockchain asset transfer."""

    token: str
    amount_usd: float
    sender: str
    receiver: str
    timestamp: Optional[str] = None


@dataclass(frozen=True)
class WhaleAssessment:
    """Explainable assessment of a large wallet movement."""

    classification: str
    confidence: int
    reason: str


def classify_transfer(
    transfer: Transfer,
    whale_threshold_usd: float = 100_000,
) -> WhaleAssessment:
    """
    Classify a large transfer without making a trading decision.

    Possible classifications:
    - WHALE_TRANSFER
    - WHALE_ACCUMULATION
    - WHALE_DISTRIBUTION
    - NORMAL_TRANSFER
    - INVALID_DATA
    """

    if transfer.amount_usd < 0:
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=100,
            reason="Transfer value cannot be negative.",
        )

    if not transfer.token:
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=100,
            reason="Token is required.",
        )

    if not transfer.sender or not transfer.receiver:
        return WhaleAssessment(
            classification="INVALID_DATA",
            confidence=100,
            reason="Sender and receiver are required.",
        )

    if transfer.sender == transfer.receiver:
        return WhaleAssessment(
            classification="NORMAL_TRANSFER",
            confidence=100,
            reason="Sender and receiver are the same address.",
        )

    if transfer.amount_usd < whale_threshold_usd:
        return WhaleAssessment(
            classification="NORMAL_TRANSFER",
            confidence=100,
            reason="Transfer is below the configured whale threshold.",
        )

    return WhaleAssessment(
        classification="WHALE_TRANSFER",
        confidence=75,
        reason=(
            f"Large {transfer.token} transfer detected: "
            f"${transfer.amount_usd:,.2f}."
        ),
    )
