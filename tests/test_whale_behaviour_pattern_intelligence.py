from dataclasses import dataclass

from whale_behaviour_pattern_intelligence import (
    analyze_whale_behaviour_pattern,
)


@dataclass
class Assessment:
    classification: str


def make_assessment(classification):
    return Assessment(
        classification=classification,
    )


def test_repeated_accumulation():
    assessments = [
        make_assessment("POSSIBLE_ACCUMULATION"),
        make_assessment("POSSIBLE_ACCUMULATION"),
        make_assessment("POSSIBLE_ACCUMULATION"),
    ]

    result = analyze_whale_behaviour_pattern(assessments)

    assert result.classification == "REPEATED_ACCUMULATION"
    assert result.observation_count == 3
    assert result.accumulation_count == 3
    assert result.distribution_count == 0
    assert result.confidence == 70


def test_repeated_distribution():
    assessments = [
        make_assessment("POSSIBLE_DISTRIBUTION"),
        make_assessment("POSSIBLE_DISTRIBUTION"),
    ]

    result = analyze_whale_behaviour_pattern(assessments)

    assert result.classification == "REPEATED_DISTRIBUTION"
    assert result.observation_count == 2
    assert result.accumulation_count == 0
    assert result.distribution_count == 2
    assert result.confidence == 70


def test_mixed_pattern():
    assessments = [
        make_assessment("POSSIBLE_ACCUMULATION"),
        make_assessment("POSSIBLE_DISTRIBUTION"),
    ]

    result = analyze_whale_behaviour_pattern(assessments)

    assert result.classification == "MIXED_PATTERN"
    assert result.observation_count == 2
    assert result.accumulation_count == 1
    assert result.distribution_count == 1
    assert result.confidence == 60


def test_isolated_activity():
    assessments = [
        make_assessment("POSSIBLE_ACCUMULATION"),
    ]

    result = analyze_whale_behaviour_pattern(assessments)

    assert result.classification == "ISOLATED_ACTIVITY"
    assert result.observation_count == 1
    assert result.accumulation_count == 1
    assert result.distribution_count == 0
    assert result.confidence == 30


def test_unrelated_activity_is_isolated():
    assessments = [
        make_assessment("WHALE_TRANSFER"),
        make_assessment("NORMAL_TRANSFER"),
    ]

    result = analyze_whale_behaviour_pattern(assessments)

    assert result.classification == "ISOLATED_ACTIVITY"
    assert result.observation_count == 2
    assert result.accumulation_count == 0
    assert result.distribution_count == 0


def test_empty_assessments():
    result = analyze_whale_behaviour_pattern([])

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 0
    assert result.confidence == 0


def test_invalid_assessments_input():
    result = analyze_whale_behaviour_pattern(None)

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 0
    assert result.confidence == 0
