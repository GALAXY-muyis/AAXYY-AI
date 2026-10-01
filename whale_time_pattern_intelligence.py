"""
AAXYY AI - Whale Time Pattern Intelligence

Combines whale time-window analysis with behavioural pattern analysis.

This module does not make trading decisions.

The purpose is to identify repeated whale activity concentrated
within a defined time window.
"""

from dataclasses import dataclass

from whale_behaviour_pattern_intelligence import (
    analyze_whale_behaviour_pattern,
)
from whale_time_window_intelligence import analyze_time_window


@dataclass
class WhaleTimePattern:
    classification: str
    window_hours: int
    assessment_count: int
    accumulation_count: int
    distribution_count: int
    confidence: int
    start_time: str
    end_time: str
    reason: str


def analyze_whale_time_pattern(
    assessments,
    window_hours,
    end_time,
) -> WhaleTimePattern:
    """
    Analyze whale behaviour inside a defined time window.

    Supported classifications:
    - REPEATED_ACCUMULATION_IN_WINDOW
    - REPEATED_DISTRIBUTION_IN_WINDOW
    - MIXED_PATTERN_IN_WINDOW
    - WHALE_ACTIVITY_IN_WINDOW
    - NO_WHALE_ACTIVITY
    - INVALID_DATA

    This function does not make trading decisions.
    """

    time_window = analyze_time_window(
        assessments,
        window_hours,
        end_time,
    )

    if time_window.classification == "INVALID_DATA":
        return WhaleTimePattern(
            classification="INVALID_DATA",
            window_hours=window_hours,
            assessment_count=0,
            accumulation_count=0,
            distribution_count=0,
            confidence=0,
            start_time="",
            end_time="",
            reason="Invalid whale time-window data.",
        )

    if time_window.classification == "NO_WHALE_ACTIVITY":
        return WhaleTimePattern(
            classification="NO_WHALE_ACTIVITY",
            window_hours=window_hours,
            assessment_count=0,
            accumulation_count=0,
            distribution_count=0,
            confidence=0,
            start_time=time_window.start_time,
            end_time=time_window.end_time,
            reason="No whale activity was detected inside the time window.",
        )

    start_time = time_window.start_time
    end_time_value = time_window.end_time

    window_assessments = []

    for assessment in assessments:
        timestamp = getattr(
            assessment,
            "timestamp",
            "",
        )

        try:
            from datetime import datetime

            assessment_time = datetime.fromisoformat(timestamp)
            start_datetime = datetime.fromisoformat(start_time)
            end_datetime = datetime.fromisoformat(end_time_value)
        except (TypeError, ValueError):
            continue

        if start_datetime <= assessment_time <= end_datetime:
            window_assessments.append(assessment)

    behaviour = analyze_whale_behaviour_pattern(
        window_assessments,
    )

    if behaviour.classification == "REPEATED_ACCUMULATION":
        return WhaleTimePattern(
            classification="REPEATED_ACCUMULATION_IN_WINDOW",
            window_hours=window_hours,
            assessment_count=behaviour.observation_count,
            accumulation_count=behaviour.accumulation_count,
            distribution_count=behaviour.distribution_count,
            confidence=behaviour.confidence,
            start_time=start_time,
            end_time=end_time_value,
            reason=(
                "Repeated possible accumulation activity was detected "
                "inside the defined whale time window."
            ),
        )

    if behaviour.classification == "REPEATED_DISTRIBUTION":
        return WhaleTimePattern(
            classification="REPEATED_DISTRIBUTION_IN_WINDOW",
            window_hours=window_hours,
            assessment_count=behaviour.observation_count,
            accumulation_count=behaviour.accumulation_count,
            distribution_count=behaviour.distribution_count,
            confidence=behaviour.confidence,
            start_time=start_time,
            end_time=end_time_value,
            reason=(
                "Repeated possible distribution activity was detected "
                "inside the defined whale time window."
            ),
        )

    if behaviour.classification == "MIXED_PATTERN":
        return WhaleTimePattern(
            classification="MIXED_PATTERN_IN_WINDOW",
            window_hours=window_hours,
            assessment_count=behaviour.observation_count,
            accumulation_count=behaviour.accumulation_count,
            distribution_count=behaviour.distribution_count,
            confidence=behaviour.confidence,
            start_time=start_time,
            end_time=end_time_value,
            reason=(
                "Both possible accumulation and distribution activity "
                "were detected inside the defined whale time window."
            ),
        )

    return WhaleTimePattern(
        classification="WHALE_ACTIVITY_IN_WINDOW",
        window_hours=window_hours,
        assessment_count=behaviour.observation_count,
        accumulation_count=behaviour.accumulation_count,
        distribution_count=behaviour.distribution_count,
        confidence=behaviour.confidence,
        start_time=start_time,
        end_time=end_time_value,
        reason=(
            "Whale activity was detected inside the defined time window, "
            "but repeated behaviour was not established."
        ),
  )
