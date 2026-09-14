from paper_trade_performance import PaperTradePerformance


def test_empty_performance():
    performance = PaperTradePerformance()

    assert performance.total_trades() == 0
    assert performance.winning_trades() == 0
    assert performance.losing_trades() == 0
    assert performance.breakeven_trades() == 0
    assert performance.win_rate() == 0.0
    assert performance.total_pnl() == 0.0
    assert performance.average_pnl() == 0.0
    assert performance.profit_factor() == 0.0
    assert performance.best_trade() is None
    assert performance.worst_trade() is None


def test_performance_statistics():
    trades = [
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "pnl": 20.0,
        },
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "pnl": -10.0,
        },
        {
            "symbol": "SOLUSDT",
            "side": "BUY",
            "pnl": 30.0,
        },
        {
            "symbol": "XRPUSDT",
            "side": "SELL",
            "pnl": 0.0,
        },
    ]

    performance = PaperTradePerformance(trades)

    assert performance.total_trades() == 4
    assert performance.winning_trades() == 2
    assert performance.losing_trades() == 1
    assert performance.breakeven_trades() == 1
    assert performance.win_rate() == 50.0
    assert performance.total_pnl() == 40.0
    assert performance.average_pnl() == 10.0
    assert performance.profit_factor() == 5.0


def test_best_and_worst_trade():
    trades = [
        {
            "symbol": "BTCUSDT",
            "pnl": 15.0,
        },
        {
            "symbol": "ETHUSDT",
            "pnl": -8.0,
        },
        {
            "symbol": "SOLUSDT",
            "pnl": 25.0,
        },
    ]

    performance = PaperTradePerformance(trades)

    assert performance.best_trade()["symbol"] == "SOLUSDT"
    assert performance.best_trade()["pnl"] == 25.0

    assert performance.worst_trade()["symbol"] == "ETHUSDT"
    assert performance.worst_trade()["pnl"] == -8.0


def test_summary_contains_all_metrics():
    trades = [
        {
            "symbol": "BTCUSDT",
            "pnl": 10.0,
        },
        {
            "symbol": "ETHUSDT",
            "pnl": -5.0,
        },
    ]

    performance = PaperTradePerformance(trades)

    summary = performance.summary()

    assert summary["total_trades"] == 2
    assert summary["winning_trades"] == 1
    assert summary["losing_trades"] == 1
    assert summary["breakeven_trades"] == 0
    assert summary["win_rate"] == 50.0
    assert summary["total_pnl"] == 5.0
    assert summary["average_pnl"] == 2.5
    assert summary["profit_factor"] == 2.0
    assert summary["best_trade"]["symbol"] == "BTCUSDT"
    assert summary["worst_trade"]["symbol"] == "ETHUSDT"
