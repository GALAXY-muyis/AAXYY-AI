from paper_trade_history import PaperTradeHistory
from paper_trade_report import PaperTradeReport


def test_report_is_empty_when_no_trades_exist(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    report = PaperTradeReport(history)

    result = report.generate()

    assert result["total_trades"] == 0
    assert result["winning_trades"] == 0
    assert result["losing_trades"] == 0
    assert result["win_rate"] == 0.0
    assert result["total_pnl"] == 0.0


def test_report_calculates_trade_statistics(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    history.append(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "pnl": 20.0,
        }
    )

    history.append(
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "pnl": -10.0,
        }
    )

    history.append(
        {
            "symbol": "SOLUSDT",
            "side": "BUY",
            "pnl": 0.0,
        }
    )

    report = PaperTradeReport(history)

    result = report.generate()

    assert result["total_trades"] == 3
    assert result["winning_trades"] == 1
    assert result["losing_trades"] == 1
    assert result["breakeven_trades"] == 1
    assert result["win_rate"] == 33.33333333333333
    assert result["total_pnl"] == 10.0
    assert result["average_pnl"] == 10.0 / 3


def test_report_formats_readable_output(tmp_path):
    history = PaperTradeHistory(
        tmp_path / "paper_trade_history.json"
    )

    history.append(
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "pnl": 25.0,
        }
    )

    report = PaperTradeReport(history)

    text = report.format_report()

    assert "AAXYY PAPER TRADING PERFORMANCE" in text
    assert "Total Trades: 1" in text
    assert "Winning Trades: 1" in text
    assert "Total PnL: 25.00" in text
