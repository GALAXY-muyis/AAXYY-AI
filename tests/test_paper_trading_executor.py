from paper_trading_executor import PaperTradingExecutor


def test_open_buy_position():
    executor = PaperTradingExecutor(starting_balance=1000)

    trade = executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
        stop_loss=95,
        take_profit=115,
    )

    assert trade["status"] == "OPENED"
    assert trade["symbol"] == "BTC"
    assert trade["side"] == "BUY"
    assert trade["entry_price"] == 100
    assert trade["quantity"] == 2
    assert trade["stop_loss"] == 95
    assert trade["take_profit"] == 115


def test_open_sell_position():
    executor = PaperTradingExecutor(starting_balance=1000)

    trade = executor.open_position(
        symbol="BTC",
        side="SELL",
        entry_price=100,
        quantity=2,
        stop_loss=105,
        take_profit=90,
    )

    assert trade["status"] == "OPENED"
    assert trade["side"] == "SELL"


def test_buy_pnl():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    pnl = executor.calculate_pnl(110)

    assert pnl == 20


def test_sell_pnl():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="SELL",
        entry_price=100,
        quantity=2,
    )

    pnl = executor.calculate_pnl(90)

    assert pnl == 20


def test_buy_stop_loss():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
        stop_loss=95,
        take_profit=115,
    )

    trade = executor.check_exit(95)

    assert trade is not None
    assert trade["reason"] == "STOP_LOSS"
    assert trade["pnl"] == -10
    assert executor.position is None


def test_buy_take_profit():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
        stop_loss=95,
        take_profit=115,
    )

    trade = executor.check_exit(115)

    assert trade is not None
    assert trade["reason"] == "TAKE_PROFIT"
    assert trade["pnl"] == 30
    assert executor.position is None


def test_sell_stop_loss():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="SELL",
        entry_price=100,
        quantity=2,
        stop_loss=105,
        take_profit=90,
    )

    trade = executor.check_exit(105)

    assert trade is not None
    assert trade["reason"] == "STOP_LOSS"
    assert trade["pnl"] == -10
    assert executor.position is None


def test_sell_take_profit():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="SELL",
        entry_price=100,
        quantity=2,
        stop_loss=105,
        take_profit=90,
    )

    trade = executor.check_exit(90)

    assert trade is not None
    assert trade["reason"] == "TAKE_PROFIT"
    assert trade["pnl"] == 20
    assert executor.position is None


def test_close_position_updates_balance_and_history():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    trade = executor.close_position(
        exit_price=110,
        reason="MANUAL",
    )

    assert trade["pnl"] == 20
    assert trade["balance_after"] == 1020
    assert executor.balance == 1020
    assert executor.realized_pnl == 20
    assert len(executor.trade_history) == 1


def test_calculate_quantity():
    executor = PaperTradingExecutor(starting_balance=1000)

    quantity = executor.calculate_quantity(
        entry_price=100,
        stop_loss=95,
        risk_percent=2,
    )

    assert quantity == 4


def test_status_with_open_position():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    status = executor.get_status(current_price=110)

    assert status["starting_balance"] == 1000
    assert status["balance"] == 1000
    assert status["realized_pnl"] == 0
    assert status["unrealized_pnl"] == 20
    assert status["total_pnl"] == 20
    assert status["position_open"] is True
    assert status["total_trades"] == 0


def test_trade_history_returns_completed_trades():
    executor = PaperTradingExecutor(starting_balance=1000)

    executor.open_position(
        symbol="BTC",
        side="BUY",
        entry_price=100,
        quantity=2,
    )

    executor.close_position(
        exit_price=110,
        reason="TAKE_PROFIT",
    )

    history = executor.get_trade_history()

    assert len(history) == 1
    assert history[0]["symbol"] == "BTC"
    assert history[0]["side"] == "BUY"
    assert history[0]["pnl"] == 20
def test_safety_approved_opportunity_can_open_paper_position():
    from paper_trading_executor import PaperTradingExecutor

    opportunity = {
        "symbol": "ETHUSDT",
        "signal": "BUY",
        "entry_price": 3000,
        "stop_loss": 2900,
        "take_profit": 3250,
    }

    executor = PaperTradingExecutor(starting_balance=1000)

    quantity = executor.calculate_quantity(
        entry_price=opportunity["entry_price"],
        stop_loss=opportunity["stop_loss"],
        risk_percent=1.0,
    )

    result = executor.open_position(
        symbol=opportunity["symbol"],
        side=opportunity["signal"],
        entry_price=opportunity["entry_price"],
        quantity=quantity,
        stop_loss=opportunity["stop_loss"],
        take_profit=opportunity["take_profit"],
    )

    assert result["status"] == "OPENED"
    assert result["symbol"] == "ETHUSDT"
    assert result["side"] == "BUY"
    assert executor.position is not None
