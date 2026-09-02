from trade_analyzer import analyze_trade


def test_analyze_trade():
    result = analyze_trade(
        110,
        100,
        2000,
        1000,
        105,
        110,
        100,
        130
    )

    assert result["signal"] == "BUY"
    assert result["volume_status"] == "HIGH"
    assert result["momentum"] > 0
    assert result["confidence"] == 90
    assert result["risk"] == 10
    assert result["reward"] == 20
    assert result["risk_reward_ratio"] == 2
def test_analyze_trade_sell():
    result = analyze_trade(
        90,
        100,
        2000,
        1000,
        95,
        90,
        100,
        70
    )

    assert result["signal"] == "SELL"
    assert result["volume_status"] == "HIGH"
    assert result["momentum"] < 0
    assert result["confidence"] == 90
    assert result["risk"] == 10
    assert result["reward"] == 20
    assert result["risk_reward_ratio"] == 2
