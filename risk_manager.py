def calculate_risk(entry_price, stop_loss, take_profit):
    """
    Calculate risk, reward, and risk/reward ratio.
    """

    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)

    if risk == 0:
        return {
            "risk": 0,
            "reward": reward,
            "risk_reward_ratio": None
        }

    risk_reward_ratio = reward / risk

    return {
        "risk": risk,
        "reward": reward,
        "risk_reward_ratio": risk_reward_ratio
    }
