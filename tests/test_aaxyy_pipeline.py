from aaxyy_pipeline import run_aaxyy_pipeline


def test_strong_buy_pipeline():
    result = run_aaxyy_pipeline(
        price=110,
        moving_average=100,
        volume=1500,
        average_volume=1000,
        signal="BUY",
        confidence=90,
        risk_reward=3,
        momentum=10,
    )

    assert result["market_regime"] == "BULLISH"
    assert result["volume_status"] == "HIGH"
    assert result["trade_quality"]["quality"] == "STRONG"
    assert result["conflict"]["status"] == "ALIGNED"
    assert result["final_decision"] == "STRONG BUY"


def test_conflicting_buy_pipeline():
    result = run_aaxyy_pipeline(
        price=90,
        moving_average=100,
        volume=1500,
        average_volume=1000,
        signal="BUY",
        confidence=90,
        risk_reward=3,
        momentum=10,
    )

    assert result["market_regime"] == "BEARISH"
    assert result["conflict"]["status"] == "CONFLICT"
    assert result["final_decision"] == "CAUTION"


def test_hold_pipeline():
    result = run_aaxyy_pipeline(
        price=100,
        moving_average=100,
        volume=1000,
        average_volume=1000,
        signal="HOLD",
        confidence=40,
        risk_reward=1,
        momentum=0,
    )

    assert result["market_regime"] == "SIDEWAYS"
    assert result["final_decision"] == "WAIT"
