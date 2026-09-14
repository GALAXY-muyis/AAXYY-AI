from paper_trading_runner import PaperTradingRunner


def test_monitor_open_position_reports_open_position(monkeypatch):
    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
    )

    runner.executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100.0,
        quantity=1.0,
        stop_loss=95.0,
        take_profit=110.0,
    )

    monkeypatch.setattr(
        runner.provider,
        "get_market_data",
        lambda symbol: {
            "symbol": symbol,
            "price": 105.0,
        },
    )

    result = runner.monitor_open_position()

    assert result["status"] == "POSITION_OPEN"
    assert result["symbol"] == "BTCUSDT"
    assert result["current_price"] == 105.0
    assert result["pnl"] == 5.0


def test_monitor_open_position_closes_at_take_profit(monkeypatch):
    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
    )

    runner.executor.open_position(
        symbol="BTCUSDT",
        side="BUY",
        entry_price=100.0,
        quantity=1.0,
        stop_loss=95.0,
        take_profit=110.0,
    )

    monkeypatch.setattr(
        runner.provider,
        "get_market_data",
        lambda symbol: {
            "symbol": symbol,
            "price": 110.0,
        },
    )

    result = runner.monitor_open_position()

    assert result["status"] == "PAPER_TRADE_CLOSED"
    assert result["exit"]["reason"] == "TAKE_PROFIT"
    assert result["exit"]["exit_price"] == 110.0
    assert result["exit"]["pnl"] == 10.0
    assert runner.executor.position is None
