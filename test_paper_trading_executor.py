import pytest

from paper_trading_executor import PaperTradingExecutor


def test_executor_starts_with_correct_balance():
    executor = PaperTradingExecutor(1000)

    status = executor.get_status()

    assert status["balance"] == 1000
    assert status["realized_pnl"] == 0
    assert status["position_open"] is False


def test_calculate_quantity():
    executor = PaperTradingExecutor(1000)

    quantity = executor.calculate_quantity(
        entry_price=100,
        stop_loss=95,
        risk_percent=1,
    )

    assert quantity == pytest.approx(2)


def test_open_buy_position():
    executor = PaperTradingExecutor(1000)

    result = executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
        stop_loss=95,
        take_profit=110,
    )

    assert result["status"] == "OPENED"
    assert result["symbol"] == "BTCUSDT"
    assert result["side"] == "BUY"
    assert result["entry_price"] == 100
    assert result["quantity"] == 2


def test_buy_position_profit():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    pnl = executor.calculate_pnl(110)

    assert pnl == pytest.approx(20)


def test_buy_position_loss():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    pnl = executor.calculate_pnl(90)

    assert pnl == pytest.approx(-20)


def test_sell_position_profit():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="SELL",
        entry_price=100,
        quantity=2,
    )

    pnl = executor.calculate_pnl(90)

    assert pnl == pytest.approx(20)


def test_close_position_updates_balance():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    trade = executor.close_position(
        exit_price=110,
        reason="MANUAL",
    )

    assert trade["pnl"] == pytest.approx(20)
    assert executor.balance == pytest.approx(1020)
    assert executor.position is None


def test_buy_stop_loss_closes_position():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
        stop_loss=95,
    )

    result = executor.check_exit(94)

    assert result is not None
    assert result["reason"] == "STOP_LOSS"
    assert result["pnl"] == pytest.approx(-12)
    assert executor.position is None


def test_buy_take_profit_closes_position():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
        take_profit=110,
    )

    result = executor.check_exit(111)

    assert result is not None
    assert result["reason"] == "TAKE_PROFIT"
    assert result["pnl"] == pytest.approx(22)
    assert executor.position is None


def test_sell_stop_loss_closes_position():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="SELL",
        entry_price=100,
        quantity=2,
        stop_loss=105,
    )

    result = executor.check_exit(106)

    assert result is not None
    assert result["reason"] == "STOP_LOSS"
    assert result["pnl"] == pytest.approx(-12)
    assert executor.position is None


def test_sell_take_profit_closes_position():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="SELL",
        entry_price=100,
        quantity=2,
        take_profit=90,
    )

    result = executor.check_exit(89)

    assert result is not None
    assert result["reason"] == "TAKE_PROFIT"
    assert result["pnl"] == pytest.approx(22)
    assert executor.position is None


def test_cannot_open_two_positions():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    with pytest.raises(ValueError):
        executor.open_position(
            symbol="ETHUSDT",
            side="BUY",
            entry_price=200,
            quantity=1,
        )


def test_cannot_close_without_position():
    executor = PaperTradingExecutor(1000)

    with pytest.raises(ValueError):
        executor.close_position(100)


def test_trade_history_records_completed_trade():
    executor = PaperTradingExecutor(1000)

    executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    executor.close_position(110)

    history = executor.get_trade_history()

    assert len(history) == 1
    assert history[0]["symbol"] == "BTCUSDT"
    assert history[0]["pnl"] == pytest.approx(20)
