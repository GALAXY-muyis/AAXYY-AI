def make_trade_decision(
    signal,
    confidence,
    trade_quality,
    market_regime,
):
    if signal == "HOLD":
        decision = "WAIT"

    elif trade_quality == "STRONG" and confidence >= 80:
        if signal == "BUY" and market_regime == "BULLISH":
            decision = "STRONG BUY"
        elif signal == "SELL" and market_regime == "BEARISH":
            decision = "STRONG SELL"
        else:
            decision = "CAUTION"

    elif trade_quality == "GOOD" and confidence >= 65:
        decision = signal

    else:
        decision = "CAUTION"

    return {
        "decision": decision,
        "signal": signal,
        "confidence": confidence,
        "trade_quality": trade_quality,
        "market_regime": market_regime,
    }
