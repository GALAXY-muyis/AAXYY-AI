def calculate_trade_quality(
    signal,
    confidence,
    risk_reward,
    momentum,
    volume_status,
):
    score = 0

    # Signal confidence
    if confidence >= 80:
        score += 30
    elif confidence >= 65:
        score += 20
    elif confidence >= 50:
        score += 10

    # Risk/reward
    if risk_reward >= 3:
        score += 30
    elif risk_reward >= 2:
        score += 20
    elif risk_reward >= 1.5:
        score += 10

    # Momentum
    if signal == "BUY" and momentum > 0:
        score += 20
    elif signal == "SELL" and momentum < 0:
        score += 20

    # Volume
    if volume_status == "HIGH":
        score += 20
    elif volume_status == "NORMAL":
        score += 10

    if score >= 80:
        quality = "STRONG"
    elif score >= 60:
        quality = "GOOD"
    elif score >= 40:
        quality = "MODERATE"
    else:
        quality = "WEAK"

    return {
        "score": score,
        "quality": quality,
    }
