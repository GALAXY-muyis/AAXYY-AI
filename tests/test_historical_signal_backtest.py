
import pytest

from historical_signal_backtest import backtest_candles


def make_candles(count=65, start_price=100.0):
    candles = []

    for index in range(count):
        price = start_price + index * 0.5
        candles.append([
            (index + 1) * 900_000,
            price - 0.1,
            price + 0.2,
            price - 0.2,
            price,
            100.0,
        ])

    return candles


def test_returns_empty_results_when_no_trade_signal():
    candles = []

    for index in range(60):
        candles.append([
            (index + 1) * 900_000,
            100.0,
            100.1,
            99.9,
            100.0,
            100.0,
        ])

    result = backtest_candles(candles)

    assert result["trades"] == []
    assert result["summary"]["closed_trades"] == 0
    assert result["ending_balance"] == 1000.0


def test_excludes_last_candle_by_default():
    candles = make_candles(60)

    result = backtest_candles(candles)

    assert result["candles_used"] == 59


def test_rejects_invalid_starting_balance():
    with pytest.raises(ValueError):
        backtest_candles(make_candles(), starting_balance=0)


def test_rejects_invalid_candle():
    candles = make_candles()
    candles[0] = [900_000, 100, 99, 101, 100, 100]

    with pytest.raises(ValueError):
        backtest_candles(candles)


def test_backtest_does_not_change_input_candles():
    candles = make_candles()
    original = [candle.copy() for candle in candles]

    backtest_candles(candles)

    assert candles == original


def test_summary_marks_simulation_as_paper_only():
    result = backtest_candles(make_candles())

    assert result["summary"]["assumptions"]["paper_trading_only"] is True
  
