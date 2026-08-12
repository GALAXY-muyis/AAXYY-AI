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
