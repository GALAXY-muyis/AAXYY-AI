def calculate_trade_targets(
    entry_price,
    stop_loss,
    risk_reward=3.0,
    signal="BUY",
):
    """
    Calculate take-profit from entry, stop-loss,
    and desired risk/reward ratio.
    """

    if entry_price <= 0 or stop_loss <= 0:
        return {
            "valid": False,
            "reason": "INVALID_PRICE",
        }

    if risk_reward <= 0:
        return {
            "valid": False,
            "reason": "INVALID_RISK_REWARD",
        }

    risk_per_unit = abs(
        entry_price - stop_loss
    )

    if risk_per_unit == 0:
        return {
            "valid": False,
            "reason": "ZERO_PRICE_RISK",
        }

    if signal == "BUY":
        take_profit = (
            entry_price
            + risk_per_unit * risk_reward
        )

    elif signal == "SELL":
        take_profit = (
            entry_price
            - risk_per_unit * risk_reward
        )

    else:
        return {
            "valid": False,
            "reason": "INVALID_SIGNAL",
        }

    return {
        "valid": True,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_per_unit": risk_per_unit,
        "risk_reward": risk_reward,
    }
