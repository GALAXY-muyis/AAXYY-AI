"""
AAXYY AI - Whale Event Intelligence

Combines multiple whale transfer assessments into a broader event.

This module does not make trading decisions.

A sequence of possible accumulation or distribution transfers
provides stronger evidence than a single transfer, but it still
does not prove that a whale bought or sold an asset.
"""

from dataclasses import dataclass


@dataclass
class WhaleEvent:
    classification: str
    transfer_count: int
    confidence: int
    reason: str
    accumulation_value_usd: float = 0.0
    distribution_value_usd: float = 0.0
    total_value_usd: float = 0.0


def analyze_whale_event(assessments) -> WhaleEvent:
    """
    Analyze multiple whale assessments as one event.

    Each assessment may optionally provide:
    - amount_usd
    - transfer

    Supported event classifications:
    - POSSIBLE_ACCUMULATION_EVENT
    - POSSIBLE_DISTRIBUTION_EVENT
    - MIXED_WHALE_ACTIVITY
    - INSUFFICIENT_DATA
    """

    if not isinstance(assessments, list):
        return WhaleEvent(
            classification="INSUFFICIENT_DATA",
            transfer_count=0,
            confidence=0,
            reason="Whale assessments must be provided as a list.",
        )

    if not assessments:
        return WhaleEvent(
            classification="INSUFFICIENT_DATA",
            transfer_count=0,
            confidence=0,
            reason="No whale assessments were provided.",
        )

    accumulation_count = 0
    distribution_count = 0
    accumulation_value_usd = 0.0
    distribution_value_usd = 0.0

    for assessment in assessments:
        classification = getattr(
            assessment,
            "classification",
            "",
        )

        amount_usd = getattr(
            assessment,
            "amount_usd",
            0.0,
        )

        if not isinstance(amount_usd, (int, float)):
            amount_usd = 0.0

        if amount_usd < 0:
            amount_usd = 0.0

        if classification == "POSSIBLE_ACCUMULATION":
            accumulation_count += 1
            accumulation_value_usd += amount_usd

        elif classification == "POSSIBLE_DISTRIBUTION":
            distribution_count += 1
            distribution_value_usd += amount_usd

    total_count = len(assessments)
    total_value_usd = (
        accumulation_value_usd + distribution_value_usd
    )

    if accumulation_count > distribution_count:
        return WhaleEvent(
            classification="POSSIBLE_ACCUMULATION_EVENT",
            transfer_count=total_count,
            confidence=70,
            reason=(
                "Multiple whale assessments show more possible "
                "accumulation activity than distribution activity."
            ),
            accumulation_value_usd=accumulation_value_usd,
            distribution_value_usd=distribution_value_usd,
            total_value_usd=total_value_usd,
        )

    if distribution_count > accumulation_count:
        return WhaleEvent(
            classification="POSSIBLE_DISTRIBUTION_EVENT",
            transfer_count=total_count,
            confidence=70,
            reason=(
                "Multiple whale assessments show more possible "
                "distribution activity than accumulation activity."
            ),
            accumulation_value_usd=accumulation_value_usd,
            distribution_value_usd=distribution_value_usd,
            total_value_usd=total_value_usd,
        )

    if accumulation_count == distribution_count and (
        accumulation_count > 0
    ):
        return WhaleEvent(
            classification="MIXED_WHALE_ACTIVITY",
            transfer_count=total_count,
            confidence=60,
            reason=(
                "Whale activity contains an equal number of possible "
                "accumulation and distribution assessments."
            ),
            accumulation_value_usd=accumulation_value_usd,
            distribution_value_usd=distribution_value_usd,
            total_value_usd=total_value_usd,
        )

    return WhaleEvent(
        classification="INSUFFICIENT_DATA",
        transfer_count=total_count,
        confidence=0,
        reason=(
            "The assessments do not contain enough accumulation or "
            "distribution evidence to classify a whale event."
        ),
        accumulation_value_usd=accumulation_value_usd,
        distribution_value_usd=distribution_value_usd,
        total_value_usd=total_value_usd,
    )
