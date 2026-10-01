"""
AAXYY AI - Whale Persistence Intelligence

Detects whether whale behaviour persists across multiple
time-pattern observations.

This module does not make trading decisions.

Persistent activity across separate observations can provide
stronger evidence than an isolated whale pattern, but it still
does not prove that a whale bought or sold an asset.
"""

from dataclasses import dataclass


@dataclass
class WhalePersistence:
    classification: str
    observation_count: int
    accumulation_count: int
    distribution_count: int
    confidence: int
    reason: str


def analyze_whale_persistence(
    patterns,
) -> WhalePersistence:
    """
    Analyze multiple whale time-pattern observations.

    Supported classifications:
    - PERSISTENT_ACCUMULATION
    - PERSISTENT_DISTRIBUTION
    - MIXED_PERSISTENCE
    - INCONSISTENT_ACTIVITY
    - INSUFFICIENT_DATA

    The function does not make trading decisions.
    """

    if not isinstance(patterns, list):
        return WhalePersistence(
            classification="INSUFFICIENT_DATA",
            observation_count=0,
            accumulation_count=0,
            distribution_count=0,
            confidence=0,
            reason="Whale patterns must be provided as a list.",
        )

    if not patterns:
        return WhalePersistence(
            classification="INSUFFICIENT_DATA",
            observation_count=0,
            accumulation_count=0,
            distribution_count=0,
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
        accumulation_count >= 2
        and distribution_count == 0
    ):
        return WhalePersistence(
            classification="PERSISTENT_ACCUMULATION",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=80,
            reason=(
                "Possible accumulation behaviour persisted across "
                "multiple whale time-window observations."
            ),
        )

    if (
        distribution_count >= 2
        and accumulation_count == 0
    ):
        return WhalePersistence(
            classification="PERSISTENT_DISTRIBUTION",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=80,
            reason=(
                "Possible distribution behaviour persisted across "
                "multiple whale time-window observations."
            ),
        )

    if (
        accumulation_count > 0
        and distribution_count > 0
    ):
        return WhalePersistence(
            classification="MIXED_PERSISTENCE",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=60,
            reason=(
                "Whale activity persisted across multiple observations "
                "but included both accumulation and distribution patterns."
            ),
        )

    return WhalePersistence(
        classification="INCONSISTENT_ACTIVITY",
        observation_count=observation_count,
        accumulation_count=accumulation_count,
        distribution_count=distribution_count,
        confidence=30,
        reason=(
            "The observations do not contain enough repeated "
            "accumulation or distribution patterns to establish "
            "persistent behaviour."
        ),
  )
