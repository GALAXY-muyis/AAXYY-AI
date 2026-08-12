from data_validator import validate_price


def test_valid_price():
    assert validate_price(100.0) is True


def test_zero_price_is_invalid():
    assert validate_price(0) is False


def test_negative_price_is_invalid():
    assert validate_price(-50) is False
