def generate_signal(price, moving_average):
    """
    Generate a basic trading signal from price and moving average.
    """

    if price > moving_average:
        return "BUY"

    if price < moving_average:
        return "SELL"

    return "HOLD"


def analyze_market(price, moving_average, volume, average_volume):
    """
    Analyze price trend and volume to produce a structured signal.
    """

    signal = generate_signal(price, moving_average)

    if volume > average_volume:
        volume_status = "HIGH"
    else:
        volume_status = "LOW"

    if signal == "BUY" and volume_status == "HIGH":
        confidence = 80
    elif signal == "SELL" and volume_status == "HIGH":
        confidence = 80
    elif signal != "HOLD":
        confidence = 60
    else:
        confidence = 40

    return {
        "signal": signal,
        "volume_status": volume_status,
        "confidence": confidence
    }
