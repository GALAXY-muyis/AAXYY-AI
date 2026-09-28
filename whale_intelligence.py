"""
AAXYY AI - Whale Intelligence

Classifies large blockchain transfers while keeping uncertainty explicit.

A transfer between an exchange and a wallet may indicate accumulation
or distribution, but the transfer alone does not prove a buy or sell.
"""

from dataclasses import dataclass

from address_intelligence import classify_address_role
from address_registry import AddressRegistry
from chain_intelligence import classify_chain


@dataclass
class Transfer:
    token: str
    amount_usd: float
    sender: str
    receiver: str
    timestamp: str = ""
    sender_type: str = "unknown"
    receiver_type: str = "unknown"
    chain: str = "unknown"


@dataclass
class WhaleAssessment:
    classification: str
    confidence: int
    reason: str
    sender_attribution_confidence: str = "UNKNOWN"
    receiver_attribution_confidence: str = "UNKNOWN"


def classify_transfer(
    transfer: Transfer,
    address_registry: AddressRegistry | None = None,
) -> WhaleAssessment:
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

    sender_attribution_confidence = "UNKNOWN"
    receiver_attribution_confidence = "UNKNOWN"

    chain = classify_chain(transfer.chain)

    if address_registry is not None and chain != "unknown":
        registered_sender_role = address_registry.get_role(
            transfer.sender,
            chain,
        )
        registered_receiver_role = address_registry.get_role(
            transfer.receiver,
            chain,
        )

        sender_attribution_confidence = (
            address_registry.get_confidence(
                transfer.sender,
                chain,
            )
        )
        receiver_attribution_confidence = (
            address_registry.get_confidence(
                transfer.receiver,
                chain,
            )
        )

        if registered_sender_role != "unknown":
            sender_role = registered_sender_role

        if registered_receiver_role != "unknown":
            receiver_role = registered_receiver_role

    if sender_role == "exchange" and receiver_role == "wallet":
        return WhaleAssessment(
            classification="POSSIBLE_ACCUMULATION",
            confidence=65,
            reason=(
                "Large exchange-to-wallet transfer may indicate accumulation, "
                "but the transfer alone does not prove a purchase."
            ),
            sender_attribution_confidence=sender_attribution_confidence,
            receiver_attribution_confidence=receiver_attribution_confidence,
        )

    if sender_role == "wallet" and receiver_role == "exchange":
        return WhaleAssessment(
            classification="POSSIBLE_DISTRIBUTION",
            confidence=65,
            reason=(
                "Large wallet-to-exchange transfer may indicate distribution, "
                "but the transfer alone does not prove a sale."
            ),
            sender_attribution_confidence=sender_attribution_confidence,
            receiver_attribution_confidence=receiver_attribution_confidence,
        )

    return WhaleAssessment(
        classification="WHALE_TRANSFER",
        confidence=75,
        reason=(
            "Large transfer detected, but the address roles do not provide "
            "enough evidence to classify accumulation or distribution."
        ),
        sender_attribution_confidence=sender_attribution_confidence,
        receiver_attribution_confidence=receiver_attribution_confidence,
        )
