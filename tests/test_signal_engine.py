from signal_engine import generate_signal, analyze_market


def test_buy_signal():
    result = generate_signal(110, 100)
    assert result == "BUY"


def test_sell_signal():
    result = generate_signal(90, 100)
    assert result == "SELL"


def test_hold_signal():
    result = generate_signal(100, 100)
    assert result == "HOLD"


def test_buy_signal_with_high_volume():
    result = analyze_market(110, 100, 2000, 1000, 105)

    assert result["signal"] == "BUY"
    assert result["volume_status"] == "HIGH"
    assert result["momentum"] > 0
    assert result["confidence"] == 90


def test_sell_signal_with_high_volume():
    result = analyze_market(90, 100, 2000, 1000, 95)

    assert result["signal"] == "SELL"
    assert result["volume_status"] == "HIGH"
    assert result["momentum"] < 0
    assert result["confidence"] == 90


def test_hold_signal_with_no_momentum():
    result = analyze_market(100, 100, 1000, 1000, 100)

    assert result["signal"] == "HOLD"
    assert result["volume_status"] == "LOW"
    assert result["momentum"] == 0
    assert result["confidence"] == 40
def test_buy_with_negative_momentum_has_lower_confidence():
    result = analyze_market(110, 100, 2000, 1000, 115)

    assert result["signal"] == "BUY"
    assert result["volume_status"] == "HIGH"
    assert result["momentum"] < 0
    assert result["confidence"] == 50
    def test_sell_with_positive_momentum_has_lower_confidence():
        result = analyze_market(90, 100, 2000, 1000, 85)

    assert result["signal"] == "SELL"
    assert result["volume_status"] == "HIGH"
    assert result["momentum"] > 0
    assert result["confidence"] == 50
