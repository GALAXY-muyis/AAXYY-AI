from market_regime import detect_market_regime


def test_bullish_market():
    result = detect_market_regime(
        price=110,
        moving_average=100,
        momentum=10,
    )

    assert result["regime"] == "BULLISH"


def test_bearish_market():
    result = detect_market_regime(
        price=90,
        moving_average=100,
        momentum=-10,
    )

    assert result["regime"] == "BEARISH"


def test_sideways_market():
    result = detect_market_regime(
        price=100,
        moving_average=100,
        momentum=0,
    )

    assert result["regime"] == "SIDEWAYS"
