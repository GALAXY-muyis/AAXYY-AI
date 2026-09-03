from trade_guard import validate_trade
from trade_setup import build_trade_setup
from risk_gate import check_risk_gate
from trading_guard import check_trading_guard
from paper_trading_executor import PaperTradingExecutor

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
def execute_approved_opportunity(
    opportunity,
    trades_today,
    consecutive_losses,
    daily_loss_percent,
    risk_percent=1.0,
    starting_balance=1000.0,
):
    """
    Safely execute an approved opportunity in paper trading only.

    No exchange order is placed here.
    """

    approval = approve_trade_opportunity(
        opportunity=opportunity,
        trades_today=trades_today,
        consecutive_losses=consecutive_losses,
        daily_loss_percent=daily_loss_percent,
    )

    if not approval["approved"]:
        return approval

    executor = PaperTradingExecutor(
        starting_balance=starting_balance,
    )

    quantity = executor.calculate_quantity(
        entry_price=opportunity["entry_price"],
        stop_loss=opportunity["stop_loss"],
        risk_percent=risk_percent,
    )

    result = executor.open_position(
        symbol=opportunity["symbol"],
        side=opportunity["signal"],
        entry_price=opportunity["entry_price"],
        quantity=quantity,
        stop_loss=opportunity.get("stop_loss"),
        take_profit=opportunity.get("take_profit"),
    )

    return {
        "approved": True,
        "status": result["status"],
        "symbol": result["symbol"],
        "side": result["side"],
        "entry_price": result["entry_price"],
        "quantity": result["quantity"],
        "stop_loss": result["stop_loss"],
        "take_profit": result["take_profit"],
    }
