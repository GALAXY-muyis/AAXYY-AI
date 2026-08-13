from trade_decision import make_trade_decision


def test_strong_buy_decision():
    result = make_trade_decision(
        signal="BUY",
        confidence=90,
        trade_quality="STRONG",
        market_regime="BULLISH",
    )

    assert result["decision"] == "STRONG BUY"


def test_strong_sell_decision():
    result = make_trade_decision(
        signal="SELL",
        confidence=90,
        trade_quality="STRONG",
        market_regime="BEARISH",
    )

    assert result["decision"] == "STRONG SELL"


def test_hold_decision_waits():
    result = make_trade_decision(
        signal="HOLD",
        confidence=50,
        trade_quality="MODERATE",
        market_regime="SIDEWAYS",
    )

    assert result["decision"] == "WAIT"


def test_good_buy_decision():
    result = make_trade_decision(
        signal="BUY",
        confidence=75,
        trade_quality="GOOD",
        market_regime="BULLISH",
    )

    assert result["decision"] == "BUY"


def test_conflicting_market_regime_causes_caution():
    result = make_trade_decision(
        signal="BUY",
        confidence=90,
        trade_quality="STRONG",
        market_regime="BEARISH",
    )

    assert result["decision"] == "CAUTION"
