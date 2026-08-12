from signal_engine import generate_signal, analyze_market


def test_buy_signal():
    assert generate_signal(110, 100) == "BUY"


def test_sell_signal():
    assert generate_signal(90, 100) == "SELL"


def test_hold_signal():
    assert generate_signal(100, 100) == "HOLD"
def test_buy_signal_with_high_volume():
    result = analyze_market(110, 100, 2000, 1000)

    assert result["signal"] == "BUY"
    assert result["volume_status"] == "HIGH"
    assert result["confidence"] == 80


def test_sell_signal_with_high_volume():
    result = analyze_market(90, 100, 2000, 1000)

    assert result["signal"] == "SELL"
    assert result["volume_status"] == "HIGH"
    assert result["confidence"] == 80


def test_hold_signal():
    result = analyze_market(100, 100, 1000, 1000)

    assert result["signal"] == "HOLD"
    assert result["volume_status"] == "LOW"
    assert result["confidence"] == 40
