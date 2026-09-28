from whale_event_intelligence import analyze_whale_event
from whale_intelligence import WhaleAssessment


def test_accumulation_event():
    assessments = [
        WhaleAssessment(
            classification="POSSIBLE_ACCUMULATION",
            confidence=65,
            reason="Test accumulation.",
        ),
        WhaleAssessment(
            classification="POSSIBLE_ACCUMULATION",
            confidence=65,
            reason="Test accumulation.",
        ),
        WhaleAssessment(
            classification="POSSIBLE_DISTRIBUTION",
            confidence=65,
            reason="Test distribution.",
        ),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "POSSIBLE_ACCUMULATION_EVENT"
    assert result.transfer_count == 3
    assert result.confidence == 70


def test_distribution_event():
    assessments = [
        WhaleAssessment(
            classification="POSSIBLE_DISTRIBUTION",
            confidence=65,
            reason="Test distribution.",
        ),
        WhaleAssessment(
            classification="POSSIBLE_DISTRIBUTION",
            confidence=65,
            reason="Test distribution.",
        ),
        WhaleAssessment(
            classification="POSSIBLE_ACCUMULATION",
            confidence=65,
            reason="Test accumulation.",
        ),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "POSSIBLE_DISTRIBUTION_EVENT"
    assert result.transfer_count == 3
    assert result.confidence == 70


def test_mixed_whale_activity():
    assessments = [
        WhaleAssessment(
            classification="POSSIBLE_ACCUMULATION",
            confidence=65,
            reason="Test accumulation.",
        ),
        WhaleAssessment(
            classification="POSSIBLE_DISTRIBUTION",
            confidence=65,
            reason="Test distribution.",
        ),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "MIXED_WHALE_ACTIVITY"
    assert result.transfer_count == 2
    assert result.confidence == 60


def test_empty_assessments():
    result = analyze_whale_event([])

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.transfer_count == 0
    assert result.confidence == 0


def test_invalid_assessments_input():
    result = analyze_whale_event(None)

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.transfer_count == 0
    assert result.confidence == 0
