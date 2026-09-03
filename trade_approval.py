from risk_gate import check_risk_gate
from trading_guard import check_trading_guard


def check_trade_approval(
    opportunity,
    trades_today,
    consecutive_losses,
    daily_loss_percent,
):
    """Approve a trade only when all safety checks pass."""

    risk_gate_result = check_risk_gate(
        signal=opportunity["signal"],
        risk_reward=opportunity["risk_reward"],
        stop_loss=opportunity["stop_loss"],
        entry_price=opportunity["entry_price"],
        position_size=opportunity["position_size"],
        conflict_status=opportunity["conflict_status"],
        trade_quality=opportunity["trade_quality"],
    )

    trading_guard_result = check_trading_guard(
        trades_today=trades_today,
        consecutive_losses=consecutive_losses,
        daily_loss_percent=daily_loss_percent,
    )

    approved = (
        risk_gate_result["allowed"]
        and trading_guard_result["allowed"]
    )

    return {
        "approved": approved,
        "risk_gate": risk_gate_result,
        "trading_guard": trading_guard_result,
    }
