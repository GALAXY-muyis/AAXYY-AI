from trade_quality import calculate_trade_quality


def test_strong_buy_setup():
    result = calculate_trade_quality(
        signal="BUY",
        confidence=90,
        risk_reward=3,
        momentum=10,
        volume_status="HIGH",
    )

    assert result["score"] == 100
    assert result["quality"] == "STRONG"


def test_good_trade_setup():
    result = calculate_trade_quality(
        signal="BUY",
        confidence=75,
        risk_reward=2,
        momentum=5,
        volume_status="NORMAL",
    )

    assert result["score"] == 70
    assert result["quality"] == "GOOD"


def test_weak_trade_setup():
    result = calculate_trade_quality(
        signal="HOLD",
        confidence=40,
        risk_reward=1,
        momentum=0,
        volume_status="LOW",
    )

    assert result["score"] == 0
    assert result["quality"] == "WEAK"
