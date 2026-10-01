"""
AAXYY AI - Whale Persistence Strength Intelligence

Measures the strength and consistency of persistent whale behaviour.

This module does not make trading decisions.

Persistence strength describes how consistently the observed
time-window patterns support accumulation or distribution.
It does not prove that a whale bought or sold an asset.
"""

from dataclasses import dataclass


@dataclass
class WhalePersistenceStrength:
    classification: str
    observation_count: int
    dominant_count: int
    consistency_percent: float
    confidence: int
    reason: str


def analyze_whale_persistence_strength(
    patterns,
) -> WhalePersistenceStrength:
    """
    Measure the consistency of whale behaviour across patterns.

    Supported classifications:
    - STRONG_PERSISTENT_ACCUMULATION
    - MODERATE_PERSISTENT_ACCUMULATION
    - STRONG_PERSISTENT_DISTRIBUTION
    - MODERATE_PERSISTENT_DISTRIBUTION
    - MIXED_PERSISTENCE
    - INSUFFICIENT_DATA

    The function does not make trading decisions.
    """

    if not isinstance(patterns, list):
        return WhalePersistenceStrength(
            classification="INSUFFICIENT_DATA",
            observation_count=0,
            dominant_count=0,
            consistency_percent=0.0,
            confidence=0,
            reason="Whale patterns must be provided as a list.",
        )

    if not patterns:
        return WhalePersistenceStrength(
            classification="INSUFFICIENT_DATA",
            observation_count=0,
            dominant_count=0,
            consistency_percent=0.0,
            confidence=0,
            reason="No whale patterns were provided.",
        )

    accumulation_count = 0
    distribution_count = 0

    for pattern in patterns:
        classification = getattr(
            pattern,
            "classification",
            "",
        )

        if classification == "REPEATED_ACCUMULATION_IN_WINDOW":
            accumulation_count += 1

        elif classification == "REPEATED_DISTRIBUTION_IN_WINDOW":
            distribution_count += 1

    observation_count = len(patterns)

    if (
        accumulation_count > 0
        and distribution_count > 0
    ):
        return WhalePersistenceStrength(
            classification="MIXED_PERSISTENCE",
            observation_count=observation_count,
            dominant_count=max(
                accumulation_count,
                distribution_count,
            ),
            consistency_percent=(
                max(
                    accumulation_count,
                    distribution_count,
                )
                / observation_count
            ) * 100,
            confidence=60,
            reason=(
                "Persistent whale observations contain both possible "
                "accumulation and distribution patterns."
            ),
        )

    if accumulation_count >= 2:
        consistency_percent = (
            accumulation_count / observation_count
        ) * 100

        if consistency_percent >= 75:
            classification = "STRONG_PERSISTENT_ACCUMULATION"
            confidence = 85
            reason = (
                "Possible accumulation is consistently observed across "
                "most whale time-window patterns."
            )
        else:
            classification = "MODERATE_PERSISTENT_ACCUMULATION"
            confidence = 70
            reason = (
                "Possible accumulation persists across multiple whale "
                "time-window patterns but is not fully consistent."
            )

        return WhalePersistenceStrength(
            classification=classification,
            observation_count=observation_count,
            dominant_count=accumulation_count,
            consistency_percent=consistency_percent,
            confidence=confidence,
            reason=reason,
        )

    if distribution_count >= 2:
        consistency_percent = (
            distribution_count / observation_count
        ) * 100

        if consistency_percent >= 75:
            classification = "STRONG_PERSISTENT_DISTRIBUTION"
            confidence = 85
            reason = (
                "Possible distribution is consistently observed across "
                "most whale time-window patterns."
            )
        else:
            classification = "MODERATE_PERSISTENT_DISTRIBUTION"
            confidence = 70
            reason = (
                "Possible distribution persists across multiple whale "
                "time-window patterns but is not fully consistent."
            )

        return WhalePersistenceStrength(
            classification=classification,
            observation_count=observation_count,
            dominant_count=distribution_count,
            consistency_percent=consistency_percent,
            confidence=confidence,
            reason=reason,
        )

    return WhalePersistenceStrength(
        classification="INSUFFICIENT_DATA",
        observation_count=observation_count,
        dominant_count=0,
        consistency_percent=0.0,
        confidence=0,
        reason=(
            "The observations do not contain enough repeated "
            "accumulation or distribution patterns to measure "
            "persistence strength."
        ),
            )
