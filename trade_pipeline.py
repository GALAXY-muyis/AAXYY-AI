from trade_guard import validate_trade
from trade_setup import build_trade_setup
from risk_gate import check_risk_gate
from trading_guard import check_trading_guard


def process_trade_signal(
    account_balance,
    risk_percent,
    entry_price,
    stop_loss,
    signal,
    confidence,
    risk_reward,
    leverage,
    trades_today,
    consecutive_losses,
):
    """
    Process a signal through AAXYY's safety pipeline.

    No exchange order is placed here.
    """

    guard = validate_trade(
        confidence=confidence,
        risk_percent=risk_percent,
        leverage=leverage,
        risk_reward=risk_reward,
        trades_today=trades_today,
        consecutive_losses=consecutive_losses,
    )

    if not guard["approved"]:
        return {
            "approved": False,
            "reason": guard["reason"],
        }

    setup = build_trade_setup(
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry_price,
        stop_loss=stop_loss,
        signal=signal,
        risk_reward=risk_reward,
    )

    if not setup["valid"]:
        return {
            "approved": False,
            "reason": setup["reason"],
        }

    return {
        "approved": True,
        "reason": "TRADE_READY",
        "setup": setup,
        "leverage": leverage,
    }
def approve_trade_opportunity(
    opportunity,
    trades_today,
    consecutive_losses,
    daily_loss_percent,
):
    """
    Run a selected opportunity through AAXYY's safety gates.

    No exchange order is placed here.
    """

    if not opportunity.get("valid", False):
        return {
            "approved": False,
            "reason": "INVALID_OPPORTUNITY",
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

    if not risk_result["allowed"]:
        return {
            "approved": False,
            "reason": risk_result["reason"],
        }

    trading_result = check_trading_guard(
        trades_today=trades_today,
        consecutive_losses=consecutive_losses,
        daily_loss_percent=daily_loss_percent,
    )

    if not trading_result["allowed"]:
        return {
            "approved": False,
            "reason": trading_result["reasons"],
        }

    return {
        "approved": True,
        "reason": "SAFETY_APPROVED",
    }
