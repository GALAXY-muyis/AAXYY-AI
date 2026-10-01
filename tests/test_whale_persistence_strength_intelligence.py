from dataclasses import dataclass

from whale_persistence_strength_intelligence import (
    analyze_whale_persistence_strength,
)


@dataclass
class Pattern:
    classification: str


def make_pattern(classification):
    return Pattern(
        classification=classification,
    )


def test_strong_persistent_accumulation():
    patterns = [
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
    ]

    result = analyze_whale_persistence_strength(patterns)

    assert result.classification == "STRONG_PERSISTENT_ACCUMULATION"
    assert result.observation_count == 4
    assert result.dominant_count == 4
    assert result.consistency_percent == 100.0
    assert result.confidence == 85


def test_moderate_persistent_accumulation():
    patterns = [
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("WHALE_ACTIVITY_IN_WINDOW"),
    ]

    result = analyze_whale_persistence_strength(patterns)

    assert result.classification == "MODERATE_PERSISTENT_ACCUMULATION"
    assert result.observation_count == 3
    assert result.dominant_count == 2
    assert result.consistency_percent == 200 / 3
    assert result.confidence == 70


def test_strong_persistent_distribution():
    patterns = [
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
    ]

    result = analyze_whale_persistence_strength(patterns)

    assert result.classification == "STRONG_PERSISTENT_DISTRIBUTION"
    assert result.observation_count == 4
    assert result.dominant_count == 4
    assert result.consistency_percent == 100.0
    assert result.confidence == 85


def test_moderate_persistent_distribution():
    patterns = [
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
        make_pattern("WHALE_ACTIVITY_IN_WINDOW"),
    ]

    result = analyze_whale_persistence_strength(patterns)

    assert result.classification == "MODERATE_PERSISTENT_DISTRIBUTION"
    assert result.observation_count == 3
    assert result.dominant_count == 2
    assert result.consistency_percent == 200 / 3
    assert result.confidence == 70


def test_mixed_persistence():
    patterns = [
        make_pattern("REPEATED_ACCUMULATION_IN_WINDOW"),
        make_pattern("REPEATED_DISTRIBUTION_IN_WINDOW"),
    ]

    result = analyze_whale_persistence_strength(patterns)

    assert result.classification == "MIXED_PERSISTENCE"
    assert result.observation_count == 2
    assert result.dominant_count == 1
    assert result.consistency_percent == 50.0
    assert result.confidence == 60


def test_insufficient_data():
    patterns = [
        make_pattern("WHALE_ACTIVITY_IN_WINDOW"),
    ]

    result = analyze_whale_persistence_strength(patterns)

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 1
    assert result.dominant_count == 0
    assert result.consistency_percent == 0.0
    assert result.confidence == 0


def test_empty_patterns():
    result = analyze_whale_persistence_strength([])

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 0
    assert result.confidence == 0


def test_invalid_patterns_input():
    result = analyze_whale_persistence_strength(None)

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.observation_count == 0
    assert result.confidence == 0
