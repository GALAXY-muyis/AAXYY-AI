from paper_trade_history import PaperTradeHistory


def test_history_starts_empty(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    assert history.load() == []


def test_history_saves_and_loads_trade(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    trade = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "entry_price": 76445.0,
        "exit_price": 76000.0,
        "quantity": 0.01,
        "pnl": 4.45,
        "reason": "TAKE_PROFIT",
        "balance_after": 1004.45,
    }

    history.append(trade)

    assert history.load() == [trade]


def test_history_preserves_multiple_trades(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    first_trade = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "pnl": 10.0,
    }

    second_trade = {
        "symbol": "ETHUSDT",
        "side": "BUY",
        "pnl": -5.0,
    }

    history.append(first_trade)
    history.append(second_trade)

    assert history.load() == [
        first_trade,
        second_trade,
  ]
