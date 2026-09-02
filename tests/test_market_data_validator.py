from market_data_validator import validate_market_data


def test_valid_market_data():
    result = validate_market_data(
        price=100,
        moving_average=95,
        volume=1000,
        average_volume=900,
    )

    assert result["valid"] is True
    assert result["reason"] == "MARKET_DATA_VALID"


def test_invalid_price():
    result = validate_market_data(
        price=0,
        moving_average=95,
        volume=1000,
        average_volume=900,
    )

    assert result["valid"] is False
    assert result["reason"] == "INVALID_PRICE"


def test_invalid_moving_average():
    result = validate_market_data(
        price=100,
        moving_average=0,
        volume=1000,
        average_volume=900,
    )

    assert result["valid"] is False
    assert result["reason"] == "INVALID_MOVING_AVERAGE"


def test_invalid_volume():
    result = validate_market_data(
        price=100,
        moving_average=95,
        volume=-1,
        average_volume=900,
    )

    assert result["valid"] is False
    assert result["reason"] == "INVALID_VOLUME"


def test_invalid_average_volume():
    result = validate_market_data(
        price=100,
        moving_average=95,
        volume=1000,
        average_volume=0,
    )

    assert result["valid"] is False
    assert result["reason"] == "INVALID_AVERAGE_VOLUME"


def test_zero_volume():
    result = validate_market_data(
        price=100,
        moving_average=95,
        volume=0,
        average_volume=900,
    )

    assert result["valid"] is False
    assert result["reason"] == "NO_VOLUME"
