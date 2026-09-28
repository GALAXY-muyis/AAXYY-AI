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


def analyze_whale_event(assessments) -> WhaleEvent:
    """
    Analyze multiple whale assessments as one event.

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

    accumulation_count = sum(
        assessment.classification == "POSSIBLE_ACCUMULATION"
        for assessment in assessments
    )

    distribution_count = sum(
        assessment.classification == "POSSIBLE_DISTRIBUTION"
        for assessment in assessments
    )

    total_count = len(assessments)

    if accumulation_count > distribution_count:
        return WhaleEvent(
            classification="POSSIBLE_ACCUMULATION_EVENT",
            transfer_count=total_count,
            confidence=70,
            reason=(
                "Multiple whale assessments show more possible "
                "accumulation activity than distribution activity."
            ),
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
        )

    return WhaleEvent(
        classification="INSUFFICIENT_DATA",
        transfer_count=total_count,
        confidence=0,
        reason=(
            "The assessments do not contain enough accumulation or "
            "distribution evidence to classify a whale event."
        ),
  )
