from dataclasses import dataclass

from whale_persistence_intelligence import (
    analyze_whale_persistence,
)


@dataclass
class Pattern:
    classification: str


def make_pattern(classification):
    return Pattern(
        classification=classification,
    )


def test_persistent_accumulation():
    patterns = [
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
    ]

    result = analyze_whale_persistence(patterns)

    assert result.classification == "PERSISTENT_ACCUMULATION"
    assert result.observation_count == 3
    assert result.accumulation_count == 3
    assert result.distribution_count == 0
    assert result.confidence == 80


def test_persistent_distribution():
    patterns = [
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
    ]

    result = analyze_whale_persistence(patterns)

    assert result.classification == "PERSISTENT_DISTRIBUTION"
    assert result.observation_count == 2
    assert result.accumulation_count == 0
    assert result.distribution_count == 2
    assert result.confidence == 80


def test_mixed_persistence():
    patterns = [
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
    ]

    result = analyze_whale_persistence(patterns)

    assert result.classification == "MIXED_PERSISTENCE"
    assert result.observation_count == 2
    assert result.accumulation_count == 1
    assert result.distribution_count == 1
    assert result.confidence == 60


def test_inconsistent_activity():
    patterns = [
        make_pattern("WHALE_ACTIVITY_IN_WINDOW"),
        make_pattern("WHALE_ACTIVITY_IN_WINDOW"),
    ]

    result = analyze_whale_persistence(patterns)

    assert result.classification == "INCONSISTENT_ACTIVITY"
    assert result.observation_count == 2
    assert result.accumulation_count == 0
    assert result.distribution_count == 0
    assert result.confidence == 30


def test_unrelated_pattern_is_inconsistent():
    patterns = [
        make_pattern("NO_WHALE_ACTIVITY"),
        make_pattern("UNKNOWN_PATTERN"),
    ]

    result = analyze_whale_persistence(patterns)

    assert result.classification == "INCONSISTENT_ACTIVITY"
    assert result.observation_count == 2
    assert result.confidence == 30


def test_empty_patterns():
    result = analyze_whale_persistence([])

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 0
    assert result.confidence == 0


def test_invalid_patterns_input():
    result = analyze_whale_persistence(None)

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 0
    assert result.confidence == 0
