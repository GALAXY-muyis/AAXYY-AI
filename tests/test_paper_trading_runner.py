from paper_trading_runner import PaperTradingRunner


def test_runner_opens_best_paper_trade(monkeypatch):
    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
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


def test_runner_rejects_when_no_valid_opportunity(monkeypatch):
    runner = PaperTradingRunner(
        symbols=["BTC"],
        starting_balance=1000,
    )

    monkeypatch.setattr(
        runner,
        "find_best_opportunity",
        lambda: None,
    )

    result = runner.open_best_paper_trade()

    assert result["status"] == "NO_TRADE"
    assert result["reason"] == "NO_VALID_OPPORTUNITY"
