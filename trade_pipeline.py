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
