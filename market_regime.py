def detect_market_regime(price, moving_average, momentum):
    if price > moving_average:
        regime = "BULLISH"
    elif price < moving_average:
        regime = "BEARISH"
    else:
        regime = "SIDEWAYS"

    return {
        "regime": regime,
    }
