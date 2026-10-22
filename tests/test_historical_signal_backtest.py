
import pytest

from historical_signal_backtest import backtest_candles


def make_candles(closes, volumes=None, opens=None, highs=None, lows=None):
    """Build valid 15-minute OHLCV candles for deterministic tests."""
    candles = []

    if volumes is None:
        volumes = [100.0] * len(closes)
    if opens is None:
        opens = list(closes)
    if highs is None:
        highs = [
            max(o, c) + 0.2
            for o, c in zip(opens, closes)
        ]
    if lows is None:
        lows = [
            min(o, c) - 0.2
            for o, c in zip(opens, closes)
        ]

    for index, (open_price, high, low, close, volume) in enumerate(
        zip(opens, highs, lows, closes, volumes)
    ):
        candles.append([
            (index + 1) * 900_000,
            float(open_price),
            float(high),
            float(low),
            float(close),
            float(volume),
        ])

    return candles


def bullish_candles(exit_high=None, exit_low=None):
    """Create a BUY signal, next-candle entry, and later exit candle."""
    closes = [
        100.0, 100.0, 100.0, 102.0, 102.0, 102.0, 102.0
    ]
    opens = [
        100.0, 100.0, 100.0, 102.0, 102.0, 102.0, 102.0
    ]
    highs = [
        100.2, 100.2, 100.2, 102.2, 102.2, 102.2, 102.2
    ]
    lows = [
        99.8, 99.8, 99.8, 101.8, 101.8, 101.8, 101.8
    ]
    volumes = [
        100.0, 100.0, 100.0, 200.0, 100.0, 100.0, 100.0
    ]

    if exit_high is not None:
        highs[5] = exit_high
    if exit_low is not None:
        lows[5] = exit_low

    return make_candles(closes, volumes, opens, highs, lows)


def bearish_candles(exit_high=None, exit_low=None):
    """Create a SELL signal, next-candle entry, and later exit candle."""
    closes = [
        100.0, 100.0, 100.0, 98.0, 98.0, 98.0, 98.0
    ]
    opens = [
        100.0, 100.0, 100.0, 98.0, 98.0, 98.0, 98.0
    ]
    highs = [
        100.2, 100.2, 100.2, 98.2, 98.2, 98.2, 98.2
    ]
    lows = [
        99.8, 99.8, 99.8, 97.8, 97.8, 97.8, 97.8
    ]
    volumes = [
        100.0, 100.0, 100.0, 200.0, 100.0, 100.0, 100.0
    ]

    if exit_high is not None:
        highs[5] = exit_high
    if exit_low is not None:
        lows[5] = exit_low

    return make_candles(closes, volumes, opens, highs, lows)


def test_returns_empty_results_when_no_trade_signal():
    candles = make_candles([100.0] * 60)

    result = backtest_candles(candles)

    assert result["trades"] == []
    assert result["summary"]["closed_trades"] == 0
    assert result["ending_balance"] == 1000.0


def test_excludes_last_candle_by_default():
    candles = make_candles([100.0 + i * 0.1 for i in range(60)])

    result = backtest_candles(candles)

    assert result["candles_used"] == 59


def test_rejects_invalid_starting_balance():
    with pytest.raises(ValueError):
        backtest_candles(
            make_candles([100.0] * 10),
            starting_balance=0,
        )


def test_rejects_invalid_candle():
    candles = make_candles([100.0] * 10)
    candles[0] = [900_000, 100, 99, 101, 100, 100]

    with pytest.raises(ValueError):
        backtest_candles(candles)


def test_backtest_does_not_change_input_candles():
    candles = bullish_candles()
    original = [candle.copy() for candle in candles]

    backtest_candles(candles, exclude_last_candle=False)

    assert candles == original


def test_summary_marks_simulation_as_paper_only():
    result = backtest_candles(
        make_candles([100.0] * 10),
        exclude_last_candle=False,
    )

    assert result["summary"]["assumptions"]["paper_trading_only"] is True


def test_opens_a_buy_trade_on_the_next_candle():
    result = backtest_candles(
        bullish_candles(exit_high=109.0, exit_low=101.0),
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["side"] == "BUY"
    assert result["trades"][0]["entry_price"] == 102.0


def test_opens_a_sell_trade_on_the_next_candle():
    result = backtest_candles(
        bearish_candles(exit_high=98.0, exit_low=91.0),
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["side"] == "SELL"
    assert result["trades"][0]["entry_price"] == 98.0


def test_buy_trade_hits_take_profit():
    candles = bullish_candles(exit_high=109.0, exit_low=101.0)

    result = backtest_candles(
        candles,
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["exit_reason"] == "TAKE_PROFIT"
    assert result["trades"][0]["exit_price"] == pytest.approx(108.12)


def test_buy_trade_hits_stop_loss():
    candles = bullish_candles(exit_high=103.0, exit_low=99.0)

    result = backtest_candles(
        candles,
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["exit_reason"] == "STOP_LOSS"
    assert result["trades"][0]["exit_price"] == pytest.approx(99.96)


def test_sell_trade_hits_take_profit():
    candles = bearish_candles(exit_high=98.0, exit_low=91.0)

    result = backtest_candles(
        candles,
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["exit_reason"] == "TAKE_PROFIT"
    assert result["trades"][0]["exit_price"] == pytest.approx(92.12)


def test_sell_trade_hits_stop_loss():
    candles = bearish_candles(exit_high=101.0, exit_low=97.0)

    result = backtest_candles(
        candles,
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["exit_reason"] == "STOP_LOSS"
    assert result["trades"][0]["exit_price"] == pytest.approx(99.96)


def test_stop_loss_wins_when_one_candle_touches_both_levels():
    candles = bullish_candles(exit_high=109.0, exit_low=99.0)

    result = backtest_candles(
        candles,
        moving_average_period=3,
        exclude_last_candle=False,
    )

    assert len(result["trades"]) == 1
    assert result["trades"][0]["exit_reason"] == "STOP_LOSS"
    assert result["trades"][0]["exit_price"] == pytest.approx(99.96)
    
    
