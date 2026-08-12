from momentum import calculate_momentum


def generate_signal(price, moving_average):
    """
    Generate a basic trading signal from price and moving average.
    """

    if price > moving_average:
        return "BUY"

    if price < moving_average:
        return "SELL"

    return "HOLD"


def analyze_market(
    price,
    moving_average,
    volume,
    average_volume,
    previous_price
):
    """
    Analyze trend, volume, and momentum.
    """

    signal = generate_signal(price, moving_average)

    if volume > average_volume:
        volume_status = "HIGH"
    else:
        volume_status = "LOW"

    momentum = calculate_momentum(price, previous_price)

    if signal == "BUY":
    if momentum > 0 and volume_status == "HIGH":
        confidence = 90
    elif momentum > 0:
        confidence = 75
    elif momentum < 0:
        confidence = 50
    else:
        confidence = 60

elif signal == "SELL":
    if momentum < 0 and volume_status == "HIGH":
        confidence = 90
    elif momentum < 0:
        confidence = 75
    elif momentum > 0:
        confidence = 50
    else:
        confidence = 60

else:
    confidence = 40

    return {
        "signal": signal,
        "volume_status": volume_status,
        "momentum": momentum,
        "confidence": confidence
    }
