from whale_event_intelligence import analyze_whale_event
from whale_intelligence import Transfer, classify_transfer


def make_assessment(
    classification,
    amount_usd,
):
    transfer = Transfer(
        token="ETH",
        amount_usd=amount_usd,
        sender="0xSENDER",
        receiver="0xRECEIVER",
        sender_type="exchange"
        if classification == "POSSIBLE_ACCUMULATION"
        else "wallet",
        receiver_type="wallet"
        if classification == "POSSIBLE_ACCUMULATION"
        else "exchange",
    )

    return classify_transfer(transfer)


def test_accumulation_event():
    assessments = [
        make_assessment("POSSIBLE_ACCUMULATION", 100_000),
        make_assessment("POSSIBLE_ACCUMULATION", 500_000),
        make_assessment("POSSIBLE_DISTRIBUTION", 200_000),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "POSSIBLE_ACCUMULATION_EVENT"
    assert result.transfer_count == 3
    assert result.confidence == 70
    assert result.accumulation_value_usd == 600_000
    assert result.distribution_value_usd == 200_000
    assert result.total_value_usd == 800_000
    assert result.net_flow_usd == 400_000
    assert result.flow_strength == 50.0


def test_distribution_event():
    assessments = [
        make_assessment("POSSIBLE_DISTRIBUTION", 700_000),
        make_assessment("POSSIBLE_DISTRIBUTION", 300_000),
        make_assessment("POSSIBLE_ACCUMULATION", 100_000),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "POSSIBLE_DISTRIBUTION_EVENT"
    assert result.transfer_count == 3
    assert result.confidence == 70
    assert result.accumulation_value_usd == 100_000
    assert result.distribution_value_usd == 1_000_000
    assert result.total_value_usd == 1_100_000
    assert result.net_flow_usd == -900_000
    assert result.flow_strength == 81.81818181818183


def test_mixed_whale_activity():
    assessments = [
        make_assessment("POSSIBLE_ACCUMULATION", 500_000),
        make_assessment("POSSIBLE_DISTRIBUTION", 500_000),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "MIXED_WHALE_ACTIVITY"
    assert result.transfer_count == 2
    assert result.confidence == 60
    assert result.accumulation_value_usd == 500_000
    assert result.distribution_value_usd == 500_000
    assert result.total_value_usd == 1_000_000
    assert result.net_flow_usd == 0
    assert result.flow_strength == 0.0


def test_value_flow_can_override_transfer_count():
    assessments = [
        make_assessment("POSSIBLE_ACCUMULATION", 100_000),
        make_assessment("POSSIBLE_ACCUMULATION", 100_000),
        make_assessment("POSSIBLE_DISTRIBUTION", 2_000_000),
    ]

    result = analyze_whale_event(assessments)

    assert result.classification == "POSSIBLE_DISTRIBUTION_EVENT"
    assert result.net_flow_usd == -1_800_000
    assert result.flow_strength == 81.81818181818183


def test_empty_assessments():
    result = analyze_whale_event([])

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.transfer_count == 0
    assert result.confidence == 0
    assert result.total_value_usd == 0.0
    assert result.net_flow_usd == 0.0
    assert result.flow_strength == 0.0


def test_invalid_assessments_input():
    result = analyze_whale_event(None)

    assert result.classification == "INSUFFICIENT_DATA"
    assert result.transfer_count == 0
    assert result.confidence == 0
    assert result.total_value_usd == 0.0
    assert result.net_flow_usd == 0.0
    assert result.flow_strength == 0.0
