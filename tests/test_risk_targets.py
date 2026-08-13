from risk_targets import calculate_trade_targets


def test_buy_trade_targets():
    result = calculate_trade_targets(
        entry_price=100,
        stop_loss=95,
        risk_reward_ratio=2,
        signal="BUY",
    )

    assert result["stop_loss"] == 95
    assert result["risk_per_unit"] == 5
    assert result["take_profit"] == 110
    assert result["risk_reward"] == 2


def test_sell_trade_targets():
    result = calculate_trade_targets(
        entry_price=100,
        stop_loss=105,
        risk_reward_ratio=2,
        signal="SELL",
    )

    assert result["stop_loss"] == 105
    assert result["risk_per_unit"] == 5
    assert result["take_profit"] == 90
    assert result["risk_reward"] == 2


def test_invalid_entry_price():
    result = calculate_trade_targets(
        entry_price=0,
        stop_loss=95,
        risk_reward_ratio=2,
        signal="BUY",
    )

    assert result["take_profit"] == 0
    assert result["risk_per_unit"] == 0


def test_zero_risk_distance():
    result = calculate_trade_targets(
        entry_price=100,
        stop_loss=100,
        risk_reward_ratio=2,
        signal="BUY",
    )

    assert result["risk_per_unit"] == 0
    assert result["take_profit"] == 100
