def calculate_trade_targets(
    entry_price,
    stop_loss,
    risk_reward_ratio,
    signal,
):
    if entry_price <= 0:
        return {
            "stop_loss": 0,
            "take_profit": 0,
            "risk_per_unit": 0,
            "risk_reward": 0,
        }

    if stop_loss <= 0:
        return {
            "stop_loss": 0,
            "take_profit": 0,
            "risk_per_unit": 0,
            "risk_reward": 0,
        }

    if risk_reward_ratio <= 0:
        return {
            "stop_loss": 0,
            "take_profit": 0,
            "risk_per_unit": 0,
            "risk_reward": 0,
        }

    risk_per_unit = abs(entry_price - stop_loss)

    if risk_per_unit == 0:
        return {
            "stop_loss": stop_loss,
            "take_profit": entry_price,
            "risk_per_unit": 0,
            "risk_reward": 0,
        }

    if signal == "BUY":
        take_profit = entry_price + (
            risk_per_unit * risk_reward_ratio
        )

    elif signal == "SELL":
        take_profit = entry_price - (
            risk_per_unit * risk_reward_ratio
        )

    else:
        take_profit = entry_price

    return {
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_per_unit": risk_per_unit,
        "risk_reward": risk_reward_ratio,
    }
