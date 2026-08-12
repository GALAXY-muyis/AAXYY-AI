from signal_engine import generate_signal


def test_buy_signal():
    assert generate_signal(110, 100) == "BUY"


def test_sell_signal():
    assert generate_signal(90, 100) == "SELL"


def test_hold_signal():
    assert generate_signal(100, 100) == "HOLD"
