from dataclasses import dataclass

from whale_time_pattern_intelligence import (
    analyze_whale_time_pattern,
)


@dataclass
class Assessment:
    classification: str
    timestamp: str


def make_assessment(classification, timestamp):
    return Assessment(
        classification=classification,
        timestamp=timestamp,
    )


def test_repeated_accumulation_inside_time_window():
    assessments = [
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T09:00:00",
        ),
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T10:00:00",
        ),
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T11:30:00",
        ),
    ]

    result = analyze_whale_time_pattern(
        assessments,
        4,
        "2026-09-29T12:00:00",
    )

    assert result.classification == (
        "REPEATED_ACCUMULATION_IN_WINDOW"
    )
    assert result.window_hours == 4
    assert result.assessment_count == 3
    assert result.accumulation_count == 3
    assert result.distribution_count == 0
    assert result.confidence == 70


def test_repeated_distribution_inside_time_window():
    assessments = [
        make_assessment(
            "POSSIBLE_DISTRIBUTION",
            "2026-09-29T09:30:00",
        ),
        make_assessment(
            "POSSIBLE_DISTRIBUTION",
            "2026-09-29T11:00:00",
        ),
    ]

    result = analyze_whale_time_pattern(
        assessments,
        4,
        "2026-09-29T12:00:00",
    )

    assert result.classification == (
        "REPEATED_DISTRIBUTION_IN_WINDOW"
    )
    assert result.assessment_count == 2
    assert result.accumulation_count == 0
    assert result.distribution_count == 2
    assert result.confidence == 70


def test_mixed_pattern_inside_time_window():
    assessments = [
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T10:00:00",
        ),
        make_assessment(
            "POSSIBLE_DISTRIBUTION",
            "2026-09-29T11:00:00",
        ),
    ]

    result = analyze_whale_time_pattern(
        assessments,
        4,
        "2026-09-29T12:00:00",
    )

    assert result.classification == "MIXED_PATTERN_IN_WINDOW"
    assert result.assessment_count == 2
    assert result.accumulation_count == 1
    assert result.distribution_count == 1
    assert result.confidence == 60


def test_old_activity_is_excluded_from_time_pattern():
    assessments = [
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T05:00:00",
        ),
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T11:00:00",
        ),
    ]

    result = analyze_whale_time_pattern(
        assessments,
        4,
        "2026-09-29T12:00:00",
    )

    assert result.classification == "WHALE_ACTIVITY_IN_WINDOW"
    assert result.assessment_count == 1
    assert result.accumulation_count == 1
    assert result.distribution_count == 0


def test_no_whale_activity_in_window():
    assessments = [
        make_assessment(
            "POSSIBLE_ACCUMULATION",
            "2026-09-29T05:00:00",
        )
    ]

    result = analyze_whale_time_pattern(
        assessments,
        1,
        "2026-09-29T12:00:00",
    )

    assert result.classification == "NO_WHALE_ACTIVITY"
    assert result.assessment_count == 0
    assert result.confidence == 0


def test_invalid_input():
    result = analyze_whale_time_pattern(
        None,
        4,
        "2026-09-29T12:00:00",
    )

    assert result.classification == "INVALID_DATA"
    assert result.assessment_count == 0
    assert result.confidence == 0
