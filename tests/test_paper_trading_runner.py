from paper_trading_runner import PaperTradingRunner
from paper_trade_history import PaperTradeHistory


def test_runner_opens_best_paper_trade(monkeypatch, tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
        history=history,
    )

    opportunity = {
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "price": 110.0,
        "position_size": 10.0,
        "final_decision": "STRONG BUY",
        "targets": {
            "stop_loss": 100.0,
            "take_profit": 140.0,
        },
        "scan_score": 100,
    }

    monkeypatch.setattr(
        runner,
        "find_best_opportunity",
        lambda: opportunity,
    )

    result = runner.open_best_paper_trade()

    assert result["status"] == "PAPER_TRADE_OPENED"
    assert result["trade"]["symbol"] == "BTCUSDT"
    assert result["trade"]["side"] == "BUY"
    assert runner.executor.position is not None

    assert history.load() == []


def test_runner_rejects_when_no_valid_opportunity(
    monkeypatch,
    tmp_path,
):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
        history=history,
    )

    monkeypatch.setattr(
        runner,
        "find_best_opportunity",
        lambda: None,
    )

    result = runner.open_best_paper_trade()

    assert result["status"] == "NO_TRADE"
    assert result["reason"] == "NO_VALID_OPPORTUNITY"
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
        history=history,
    )

    result = runner.open_best_paper_trade()

    assert result["status"] == "NO_TRADE"
    assert result["reason"] == "NO_VALID_OPPORTUNITY"


def test_runner_records_only_closed_trade(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
        history=history,
    )

    opportunity = {
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "price": 110.0,
        "position_size": 10.0,
        "final_decision": "STRONG BUY",
        "targets": {
            "stop_loss": 100.0,
            "take_profit": 140.0,
        },
        "scan_score": 100,
    }

    monkeypatch = __import__("pytest").MonkeyPatch()

    monkeypatch.setattr(
        runner,
        "find_best_opportunity",
        lambda: opportunity,
    )

    result = runner.open_best_paper_trade()

    assert result["status"] == "PAPER_TRADE_OPENED"
    assert history.load() == []

    runner.provider.get_market_data = lambda symbol: {
        "price": 140.0,
    }

    result = runner.monitor_open_position()

    assert result["status"] == "PAPER_TRADE_CLOSED"

    saved_trades = history.load()

    assert len(saved_trades) == 1
    assert saved_trades[0]["symbol"] == "BTCUSDT"
    assert saved_trades[0]["reason"] == "TAKE_PROFIT"

    monkeypatch.undo()
