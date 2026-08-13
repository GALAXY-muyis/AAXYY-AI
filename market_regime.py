def detect_market_regime(price, moving_average, momentum):
    if price > moving_average and momentum > 0:
        regime = "BULLISH"
    elif price < moving_average and momentum < 0:
        regime = "BEARISH"
    else:
        regime = "SIDEWAYS"

    return {
        "regime": regime,
    }
