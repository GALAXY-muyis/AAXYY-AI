from trading_guard import check_trading_guard


def test_trade_is_allowed():
    result = check_trading_guard(
        trades_today=1,
        consecutive_losses=0,
        daily_loss_percent=1,
    )

    assert result["allowed"] is True
    assert result["reasons"] == []


def test_maximum_trades_blocks_trading():
    result = check_trading_guard(
        trades_today=3,
        consecutive_losses=0,
        daily_loss_percent=1,
    )

    assert result["allowed"] is False
    assert "Maximum daily trade limit reached." in result["reasons"]


def test_consecutive_losses_block_trading():
    result = check_trading_guard(
        trades_today=1,
        consecutive_losses=3,
        daily_loss_percent=1,
    )

    assert result["allowed"] is False
    assert "Maximum consecutive loss limit reached." in result["reasons"]


def test_daily_loss_limit_blocks_trading():
    result = check_trading_guard(
        trades_today=1,
        consecutive_losses=0,
        daily_loss_percent=5,
    )

    assert result["allowed"] is False
    assert "Maximum daily loss limit reached." in result["reasons"]
