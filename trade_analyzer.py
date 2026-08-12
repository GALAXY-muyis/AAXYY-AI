from signal_engine import analyze_market
from risk_manager import calculate_risk


def analyze_trade(
    price,
    moving_average,
    volume,
    average_volume,
    entry_price,
    stop_loss,
    take_profit
):
    """
    Combine market analysis and risk management
    into one trading-analysis result.
    """

    market = analyze_market(
        price,
        moving_average,
        volume,
        average_volume
    )

    risk = calculate_risk(
        entry_price,
        stop_loss,
        take_profit
    )

    return {
        "signal": market["signal"],
        "volume_status": market["volume_status"],
        "confidence": market["confidence"],
        "risk": risk["risk"],
        "reward": risk["reward"],
        "risk_reward_ratio": risk["risk_reward_ratio"]
    }
