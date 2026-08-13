def analyze_market(price, moving_average, volume, average_volume, momentum):
    if price > moving_average:
        signal = "BUY"
    elif price < moving_average:
        signal = "SELL"
    else:
        signal = "HOLD"

    if volume > average_volume:
        volume_status = "HIGH"
    elif volume < average_volume:
        volume_status = "LOW"
    else:
        volume_status = "NORMAL"

    if signal == "BUY" and momentum > 0 and volume_status == "HIGH":
        confidence = 90
    elif signal == "BUY" and momentum > 0:
        confidence = 75
    elif signal == "BUY" and momentum < 0:
        confidence = 50
    elif signal == "BUY":
        confidence = 60
    elif signal == "SELL" and momentum < 0 and volume_status == "HIGH":
        confidence = 90
    elif signal == "SELL" and momentum < 0:
        confidence = 75
    elif signal == "SELL" and momentum > 0:
        confidence = 50
    elif signal == "SELL":
        confidence = 60
    else:
        confidence = 40

    return {
        "signal": signal,
        "volume_status": volume_status,
        "momentum": momentum,
        "confidence": confidence,
    }
    
