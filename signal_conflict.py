def detect_signal_conflict(
    signal,
    market_regime,
    momentum,
    volume_status,
):
    conflicts = []

    if signal == "BUY" and market_regime == "BEARISH":
        conflicts.append("BUY signal conflicts with bearish market")

    if signal == "SELL" and market_regime == "BULLISH":
        conflicts.append("SELL signal conflicts with bullish market")

    if signal == "BUY" and momentum < 0:
        conflicts.append("BUY signal conflicts with negative momentum")

    if signal == "SELL" and momentum > 0:
        conflicts.append("SELL signal conflicts with positive momentum")

    if volume_status == "LOW":
        conflicts.append("Low volume")

    if conflicts:
        status = "CONFLICT"
    else:
        status = "ALIGNED"

    return {
        "status": status,
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
    }
