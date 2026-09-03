from risk_gate import check_risk_gate
from trading_guard import check_trading_guard


def test_selected_opportunity_passes_risk_gate_and_trading_guard():
    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "position_size": 1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    risk_result = check_risk_gate(
        signal=opportunity["signal"],
        risk_reward=opportunity["risk_reward"],
        stop_loss=opportunity["stop_loss"],
        entry_price=opportunity["entry_price"],
        position_size=opportunity["position_size"],
        conflict_status=opportunity["conflict_status"],
        trade_quality=opportunity["trade_quality"],
    )

    trading_result = check_trading_guard(
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    )

    approved = (
        opportunity["valid"]
        and risk_result["allowed"]
        and trading_result["allowed"]
    )

    assert risk_result["allowed"] is True
    assert trading_result["allowed"] is True
    assert approved is True
