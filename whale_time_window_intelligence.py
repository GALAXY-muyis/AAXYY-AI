"""
AAXYY AI - Whale Time Window Intelligence

Groups whale assessments into meaningful time windows.

This module does not make trading decisions.

Time-window analysis helps distinguish isolated whale activity
from activity concentrated within a defined period.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class WhaleTimeWindow:
    window_hours: int
    assessment_count: int
    start_time: str
    end_time: str
    classification: str


def analyze_time_window(
    assessments,
    window_hours,
    end_time,
) -> WhaleTimeWindow:
    """
    Analyze whale assessments inside a defined time window.

    Supported windows include:
    - 1 hour
    - 4 hours
    - 24 hours

    The function does not make trading decisions.
    """

    if not isinstance(assessments, list):
        return WhaleTimeWindow(
            window_hours=window_hours,
            assessment_count=0,
            start_time="",
            end_time="",
            classification="INVALID_DATA",
        )

    if not isinstance(window_hours, int) or window_hours <= 0:
        return WhaleTimeWindow(
            window_hours=window_hours,
            assessment_count=0,
            start_time="",
            end_time="",
            classification="INVALID_DATA",
        )

    try:
        end_datetime = datetime.fromisoformat(end_time)
    except (TypeError, ValueError):
        return WhaleTimeWindow(
            window_hours=window_hours,
            assessment_count=0,
            start_time="",
            end_time="",
            classification="INVALID_DATA",
        )

    start_datetime = end_datetime - timedelta(
        hours=window_hours
    )

    valid_assessments = []

    for assessment in assessments:
        timestamp = getattr(
            assessment,
            "timestamp",
            "",
        )

        try:
            assessment_time = datetime.fromisoformat(timestamp)
        except (TypeError, ValueError):
            continue

        if start_datetime <= assessment_time <= end_datetime:
            valid_assessments.append(assessment)

    if not valid_assessments:
        classification = "NO_WHALE_ACTIVITY"
    else:
        classification = "WHALE_ACTIVITY_DETECTED"

    return WhaleTimeWindow(
        window_hours=window_hours,
        assessment_count=len(valid_assessments),
        start_time=start_datetime.isoformat(),
        end_time=end_datetime.isoformat(),
        classification=classification,
    )
