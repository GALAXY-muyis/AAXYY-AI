def validate_trade_setup(
    entry_price,
    stop_loss,
    take_profit,
    signal,
):
    """
    Validate the basic structure of a proposed trade setup.
    """

    if entry_price <= 0:
        return {
            "valid": False,
            "reason": "INVALID_ENTRY",
        }

    if stop_loss <= 0:
        return {
            "valid": False,
            "reason": "INVALID_STOP_LOSS",
        }

    if take_profit <= 0:
        return {
            "valid": False,
            "reason": "INVALID_TAKE_PROFIT",
        }

    if signal == "BUY":
        if stop_loss >= entry_price:
            return {
                "valid": False,
                "reason": "BUY_STOP_LOSS_INVALID",
            }

        if take_profit <= entry_price:
            return {
                "valid": False,
                "reason": "BUY_TAKE_PROFIT_INVALID",
            }

    elif signal == "SELL":
        if stop_loss <= entry_price:
            return {
                "valid": False,
                "reason": "SELL_STOP_LOSS_INVALID",
            }

        if take_profit >= entry_price:
            return {
                "valid": False,
                "reason": "SELL_TAKE_PROFIT_INVALID",
            }

    elif signal == "HOLD":
        return {
            "valid": True,
            "reason": "NO_TRADE_SETUP_REQUIRED",
        }

    else:
        return {
            "valid": False,
            "reason": "UNKNOWN_SIGNAL",
        }

    return {
        "valid": True,
        "reason": "TRADE_SETUP_VALID",
        }
