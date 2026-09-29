from dataclasses import dataclass

from whale_time_window_intelligence import analyze_time_window


@dataclass
class TimestampedAssessment:
    timestamp: str


def make_assessment(timestamp):
    return TimestampedAssessment(
        timestamp=timestamp,
    )


def test_one_hour_window_detects_recent_whale_activity():
    end_time = "2026-09-29T12:00:00"

    assessments = [
        make_assessment("2026-09-29T11:30:00"),
    ]

    result = analyze_time_window(
        assessments,
        1,
        end_time,
    )

    assert result.window_hours == 1
    assert result.assessment_count == 1
    assert result.classification == "WHALE_ACTIVITY_DETECTED"
    assert result.start_time == "2026-09-29T11:00:00"
    assert result.end_time == end_time


def test_old_whale_activity_is_outside_window():
    end_time = "2026-09-29T12:00:00"

    assessments = [
        make_assessment("2026-09-29T09:00:00"),
    ]

    result = analyze_time_window(
        assessments,
        1,
        end_time,
    )

    assert result.assessment_count == 0
    assert result.classification == "NO_WHALE_ACTIVITY"


def test_four_hour_window_detects_multiple_events():
    end_time = "2026-09-29T12:00:00"

    assessments = [
        make_assessment("2026-09-29T09:00:00"),
        make_assessment("2026-09-29T10:30:00"),
        make_assessment("2026-09-29T11:45:00"),
    ]

    result = analyze_time_window(
        assessments,
        4,
        end_time,
    )

    assert result.window_hours == 4
    assert result.assessment_count == 3
    assert result.classification == "WHALE_ACTIVITY_DETECTED"


def test_twenty_four_hour_window():
    end_time = "2026-09-29T12:00:00"

    assessments = [
        make_assessment("2026-09-28T13:00:00"),
        make_assessment("2026-09-29T08:00:00"),
    ]

    result = analyze_time_window(
        assessments,
        24,
        end_time,
    )

    assert result.window_hours == 24
    assert result.assessment_count == 2
    assert result.classification == "WHALE_ACTIVITY_DETECTED"


def test_empty_assessments():
    result = analyze_time_window(
        [],
        1,
        "2026-09-29T12:00:00",
    )

    assert result.assessment_count == 0
    assert result.classification == "NO_WHALE_ACTIVITY"


def test_invalid_assessments():
    result = analyze_time_window(
        None,
        1,
        "2026-09-29T12:00:00",
    )

    assert result.assessment_count == 0
    assert result.classification == "INVALID_DATA"


def test_invalid_window():
    result = analyze_time_window(
        [],
        0,
        "2026-09-29T12:00:00",
    )

    assert result.classification == "INVALID_DATA"


def test_invalid_end_time():
    result = analyze_time_window(
        [],
        1,
        "invalid-time",
    )

    assert result.classification == "INVALID_DATA"


def test_invalid_assessment_timestamp_is_ignored():
    assessments = [
        make_assessment("not-a-valid-timestamp"),
        make_assessment("2026-09-29T11:30:00"),
    ]

    result = analyze_time_window(
        assessments,
        1,
        "2026-09-29T12:00:00",
    )

    assert result.assessment_count == 1
    assert result.classification == "WHALE_ACTIVITY_DETECTED"
