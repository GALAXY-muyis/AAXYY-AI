def generate_signal(price, moving_average):
    if price > moving_average:
        return "BUY"
    elif price < moving_average:
        return "SELL"
    else:
        return "HOLD"


def analyze_market(price, moving_average, volume, average_volume, momentum):
    # 1. Determine basic signal
    if price > moving_average:
        signal = "BUY"
    elif price < moving_average:
        signal = "SELL"
    else:
        signal = "HOLD"

    # 2. Determine volume status
    if volume > average_volume:
        volume_status = "HIGH"
    elif volume < average_volume:
        volume_status = "LOW"
    else:
        volume_status = "NORMAL"

    # 3. Determine confidence
    if signal == "BUY":
        if momentum > 0 and volume_status == "HIGH":
            confidence = 90
        elif momentum > 0:
            confidence = 75
        elif momentum < 0:
            confidence = 50
        else:
            confidence = 40

    elif signal == "SELL":
        if momentum < 0 and volume_status == "HIGH":
            confidence = 90
        elif momentum < 0:
            confidence = 75
        elif momentum > 0:
            confidence = 50
        else:
            confidence = 40

    else:
        confidence = 40

    # 4. Return complete analysis
    return {
        "signal": signal,
        "volume_status": volume_status,
        "momentum": momentum,
        "confidence": confidence
    }
    
