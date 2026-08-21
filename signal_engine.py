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


def explain_signal(signal, volume_status, momentum, confidence):
    """
    Explain why AAXYY generated a trading signal.
    """

    reasons = []

    if signal == "BUY":
        reasons.append("Price is above the moving average.")
    elif signal == "SELL":
        reasons.append("Price is below the moving average.")
    else:
        reasons.append("Price is at the moving average.")

    if momentum > 0:
        reasons.append("Momentum is positive.")
    elif momentum < 0:
        reasons.append("Momentum is negative.")
    else:
        reasons.append("Momentum is neutral.")

    if volume_status == "HIGH":
        reasons.append("Volume is above average and confirms activity.")
    elif volume_status == "LOW":
        reasons.append("Volume is below average, reducing confirmation.")
    else:
        reasons.append("Volume is around average.")

    if confidence >= 90:
        strength = "VERY STRONG"
    elif confidence >= 75:
        strength = "STRONG"
    elif confidence >= 50:
        strength = "MODERATE"
    else:
        strength = "WEAK"

    return {
        "strength": strength,
        "reasons": reasons,
        "summary": " ".join(reasons),
    }


def analyze_market(
    price,
    moving_average,
    volume,
    average_volume,
    previous_price,
):
    """
    Analyze market conditions using price, moving average,
    volume and price momentum.
    """

    signal = generate_signal(
        price,
        moving_average,
    )

        if volume > average_volume:
        volume_status = "HIGH"
    else:
        volume_status = "LOW"

    momentum = price - previous_price
    if momentum < 0 and signal == "BUY":
        signal = "SELL"
elif momentum > 0 and signal == "SELL":
    signal = "BUY"

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

    explanation = explain_signal(
        signal,
        volume_status,
        momentum,
        confidence,
    )

    return {
        "signal": signal,
        "volume_status": volume_status,
        "momentum": momentum,
        "confidence": confidence,
        "explanation": explanation,
        }
    
