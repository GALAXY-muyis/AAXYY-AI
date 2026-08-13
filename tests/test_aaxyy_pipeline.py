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
        account_balance=1000,
        risk_percent=2,
        entry_price=110,
        stop_loss=105,
    )

    assert result["market_regime"] == "BULLISH"
    assert result["volume_status"] == "HIGH"
    assert result["trade_quality"]["quality"] == "STRONG"
    assert result["conflict"]["status"] == "ALIGNED"

    assert result["position_size"] == 4
    assert result["targets"]["stop_loss"] == 105
    assert result["targets"]["risk_per_unit"] == 5
    assert result["targets"]["take_profit"] == 125

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
        account_balance=1000,
        risk_percent=2,
        entry_price=90,
        stop_loss=85,
    )

    assert result["market_regime"] == "BEARISH"
    assert result["conflict"]["status"] == "CONFLICT"
    assert result["position_size"] == 4
    assert result["targets"]["take_profit"] == 105
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
        account_balance=1000,
        risk_percent=2,
        entry_price=100,
        stop_loss=95,
    )

    assert result["market_regime"] == "SIDEWAYS"
    assert result["position_size"] == 8
    assert result["targets"]["take_profit"] == 100
    assert result["final_decision"] == "WAIT"
