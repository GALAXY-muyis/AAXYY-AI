def check_trading_guard(
    trades_today,
    consecutive_losses,
    daily_loss_percent,
    max_trades=3,
    max_consecutive_losses=3,
    max_daily_loss_percent=5,
):
    """
    Check whether AAXYY AI is allowed to open a new trade.
    """

    reasons = []

    if trades_today >= max_trades:
        reasons.append("Maximum daily trade limit reached.")

    if consecutive_losses >= max_consecutive_losses:
        reasons.append("Maximum consecutive loss limit reached.")

    if daily_loss_percent >= max_daily_loss_percent:
        reasons.append("Maximum daily loss limit reached.")

    if reasons:
        allowed = False
    else:
        allowed = True

    return {
        "allowed": allowed,
        "reasons": reasons,
        "trades_today": trades_today,
        "consecutive_losses": consecutive_losses,
        "daily_loss_percent": daily_loss_percent,
    }
