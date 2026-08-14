from trade_guard import validate_trade


def filter_signal(
    signal_result,
    trades_today,
    consecutive_losses,
):
    """Apply AAXYY safety rules to a generated signal."""

    analysis = signal_result["analysis"]

    confidence = analysis["decision"]["confidence"]
    risk_reward = analysis["targets"]["risk_reward"]
    position_size = analysis["position_size"]

    risk_percent = 1.0
    leverage = 5

    guard = validate_trade(
        confidence=confidence,
        risk_percent=risk_percent,
        leverage=leverage,
        risk_reward=risk_reward,
        trades_today=trades_today,
        consecutive_losses=consecutive_losses,
    )

    return {
        "symbol": signal_result["symbol"],
        "approved": guard["approved"],
        "reason": guard["reason"],
        "position_size": position_size,
        "analysis": analysis,
    }
