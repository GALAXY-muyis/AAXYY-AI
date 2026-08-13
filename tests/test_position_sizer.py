from position_sizer import calculate_position_size


def test_position_size_with_one_percent_risk():
    result = calculate_position_size(1000, 1, 100, 95)

    assert result == 2


def test_position_size_with_two_percent_risk():
    result = calculate_position_size(1000, 2, 100, 95)

    assert result == 4


def test_position_size_with_larger_stop_distance():
    result = calculate_position_size(1000, 1, 100, 90)

    assert result == 1


def test_zero_account_balance_returns_zero():
    result = calculate_position_size(0, 1, 100, 95)

    assert result == 0


def test_zero_risk_returns_zero():
    result = calculate_position_size(1000, 0, 100, 95)

    assert result == 0


def test_same_entry_and_stop_returns_zero():
    result = calculate_position_size(1000, 1, 100, 100)

    assert result == 0
