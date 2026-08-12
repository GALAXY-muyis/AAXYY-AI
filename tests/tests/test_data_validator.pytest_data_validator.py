from data_validator import validate_price


def test_valid_price():
    assert validate_price(100.0) is True


def test_zero_price_is_invalid():
    assert validate_price(0) is False


def test_negative_price_is_invalid():
    assert validate_price(-50) is False


def test_missing_price_is_invalid():
    assert validate_price(None) is False


def test_invalid_text_is_rejected():
    assert validate_price("100") is False
