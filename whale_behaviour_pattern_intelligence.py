"""
AAXYY AI - Whale Behaviour Pattern Intelligence

Detects repeated whale activity patterns across multiple assessments.

This module does not make trading decisions.

Repeated possible accumulation or distribution activity may provide
stronger evidence of a behavioural pattern than an isolated event,
but it still does not prove that a whale bought or sold an asset.
"""

from dataclasses import dataclass


@dataclass
class WhaleBehaviourPattern:
    classification: str
    observation_count: int
    accumulation_count: int
    distribution_count: int
    confidence: int
    reason: str


def analyze_whale_behaviour_pattern(
    assessments,
) -> WhaleBehaviourPattern:
    """
    Analyze whale assessments for repeated behavioural patterns.

    Supported classifications:
    - REPEATED_ACCUMULATION
    - REPEATED_DISTRIBUTION
    - MIXED_PATTERN
    - ISOLATED_ACTIVITY
    - INSUFFICIENT_DATA

    The function does not make trading decisions.
    """

    if not isinstance(assessments, list):
        return WhaleBehaviourPattern(
            classification="INSUFFICIENT_DATA",
            observation_count=0,
            accumulation_count=0,
            distribution_count=0,
            confidence=0,
            reason="Whale assessments must be provided as a list.",
        )

    if not assessments:
        return WhaleBehaviourPattern(
            classification="INSUFFICIENT_DATA",
            observation_count=0,
            accumulation_count=0,
            distribution_count=0,
            confidence=0,
            reason="No whale assessments were provided.",
        )

    accumulation_count = 0
    distribution_count = 0

    for assessment in assessments:
        classification = getattr(
            assessment,
            "classification",
            "",
        )

        if classification == "POSSIBLE_ACCUMULATION":
            accumulation_count += 1

        elif classification == "POSSIBLE_DISTRIBUTION":
            distribution_count += 1

    observation_count = len(assessments)

    if (
        accumulation_count >= 2
        and distribution_count == 0
    ):
        return WhaleBehaviourPattern(
            classification="REPEATED_ACCUMULATION",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=70,
            reason=(
                "Multiple possible accumulation observations were "
                "detected without observed distribution activity."
            ),
        )

    if (
        distribution_count >= 2
        and accumulation_count == 0
    ):
        return WhaleBehaviourPattern(
            classification="REPEATED_DISTRIBUTION",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=70,
            reason=(
                "Multiple possible distribution observations were "
                "detected without observed accumulation activity."
            ),
        )

    if (
        accumulation_count > 0
        and distribution_count > 0
    ):
        return WhaleBehaviourPattern(
            classification="MIXED_PATTERN",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=60,
            reason=(
                "Both possible accumulation and possible "
                "distribution activity were observed."
            ),
        )

    if observation_count > 0:
        return WhaleBehaviourPattern(
            classification="ISOLATED_ACTIVITY",
            observation_count=observation_count,
            accumulation_count=accumulation_count,
            distribution_count=distribution_count,
            confidence=30,
            reason=(
                "The observations do not contain enough repeated "
                "accumulation or distribution activity to establish "
                "a behavioural pattern."
            ),
        )

    return WhaleBehaviourPattern(
        classification="INSUFFICIENT_DATA",
        observation_count=observation_count,
        accumulation_count=accumulation_count,
        distribution_count=distribution_count,
        confidence=0,
        reason=(
            "The assessments do not contain enough valid whale "
            "activity evidence."
        ),
      )
