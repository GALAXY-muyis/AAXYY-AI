def create_signal_report(filtered_signal):
    """Create a standardized AAXYY AI signal report."""

    analysis = filtered_signal["analysis"]

    targets = analysis["targets"]
    decision = analysis["decision"]

    return {
        "symbol": filtered_signal["symbol"],
        "signal": decision["signal"],
        "decision": analysis["final_decision"],
        "approved": filtered_signal["approved"],
        "reason": filtered_signal["reason"],
        "confidence": decision["confidence"],
        "market_regime": analysis["market_regime"],
        "volume_status": analysis["volume_status"],
        "trade_quality": analysis["trade_quality"]["quality"],
        "conflict_status": analysis["conflict"]["status"],
        "entry_price": targets["stop_loss"] + targets["risk_per_unit"]
        if decision["signal"] == "BUY"
        else targets["stop_loss"] - targets["risk_per_unit"],
        "stop_loss": targets["stop_loss"],
        "take_profit": targets["take_profit"],
        "risk_reward": targets["risk_reward"],
        "position_size": filtered_signal["position_size"],
    }
