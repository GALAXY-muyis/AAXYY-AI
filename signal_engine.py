def generate_signal(price, moving_average):
    """
    Generate a basic trading signal from price vs moving average.
    """
    if price > moving_average:
        return "BUY"
    elif price < moving_average:
        return "SELL"
    else:
        return "HOLD"


def analyze_market(
    price,
    moving_average,
    volume,
    average_volume,
    previous_price
):
    """
    Analyze market conditions using price, moving average,
    volume and price momentum.

    Momentum is calculated internally as:
        momentum = price - previous_price
    """

    # 1. Basic trading signal
    signal = generate_signal(price, moving_average)

    # 2. Volume status
    if volume > average_volume:
        volume_status = "HIGH"
    elif volume < average_volume:
        volume_status = "LOW"
    else:
        volume_status = "NORMAL"

    # 3. Calculate momentum
    momentum = price - previous_price

    # 4. Determine confidence
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

    # 5. Return complete analysis
    return {
        "signal": signal,
        "volume_status": volume_status,
        "momentum": momentum,
        "confidence": confidence,
    }
    
