from momentum import calculate_momentum


def test_positive_momentum():
    assert calculate_momentum(105, 100) == 5


def test_negative_momentum():
    assert calculate_momentum(95, 100) == -5


def test_zero_momentum():
    assert calculate_momentum(100, 100) == 0


def test_zero_previous_price():
    assert calculate_momentum(100, 0) == 0
