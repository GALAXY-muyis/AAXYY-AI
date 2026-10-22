
"""Isolated historical backtest for AAXYY AI's 15-minute signal rules.

Input candles use Bitget format:
[timestamp_ms, open, high, low, close, volume, ...].

The final candle is excluded by default because it may still be forming.
This module never reads or writes paper-trading state/history and never
places orders.
"""

from datetime import datetime, timezone
from math import isfinite


def _read_candle(candle):
    if len(candle) < 6:
        raise ValueError(
            "Each candle must contain timestamp, OHLC, and volume."
        )

    timestamp = int(candle[0])
    values = [float(candle[index]) for index in range(1, 6)]
    open_price, high, low, close, volume = values

    if not all(isfinite(value) for value in values):
        raise ValueError("Candle values must be finite numbers.")

    if min(open_price, high, low, close) <= 0 or volume < 0:
        raise ValueError(
            "Prices must be positive and volume cannot be negative."
        )

    if high < max(open_price, close, low):
        raise ValueError("Candle high value is inconsistent.")

    if low > min(open_price, close, high):
        raise ValueError("Candle low value is inconsistent.")

    return {
        "timestamp": timestamp,
        "open": open_price,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }


def backtest_candles(
    candles,
    starting_balance=1000.0,
    moving_average_period=50,
    stop_loss_fraction=0.02,
    risk_reward_ratio=3.0,
    risk_percent=2.0,
    estimated_cost_bps_per_side=10.0,
    max_trades_per_utc_day=3,
    max_consecutive_losses=3,
    max_daily_loss_percent=5.0,
    exclude_last_candle=True,
):
    """Backtest the current high-confidence trend signal on OHLCV candles.

    Signals are evaluated at candle close using a rolling mean that includes
    that close, matching the current provider's calculation. Only signals
    with matching momentum and above-average volume are eligible.

    Entry is at the next candle's open. The default stop-loss is 2% from
    entry, with a take-profit three times the stop distance. If both levels
    touch in one candle, the stop-loss is assumed to occur first.

    Trading costs are estimates applied to entry and exit notional.
    Results are simulations, not evidence of future profitability.
    """

    if starting_balance <= 0:
        raise ValueError("starting_balance must be positive.")

    if moving_average_period < 2:
        raise ValueError("moving_average_period must be at least 2.")

    if not 0 < stop_loss_fraction < 1:
        raise ValueError(
            "stop_loss_fraction must be between 0 and 1."
        )

    if risk_reward_ratio <= 0 or risk_percent <= 0:
        raise ValueError(
            "risk_reward_ratio and risk_percent must be positive."
        )

    if estimated_cost_bps_per_side < 0:
        raise ValueError(
            "estimated_cost_bps_per_side cannot be negative."
        )

    if max_trades_per_utc_day < 1 or max_consecutive_losses < 1:
        raise ValueError("Trade and loss limits must be at least 1.")

    parsed = [_read_candle(candle) for candle in candles]
    parsed.sort(key=lambda item: item["timestamp"])

    deduplicated = {}
    for candle in parsed:
        deduplicated[candle["timestamp"]] = candle

    data = [
        deduplicated[key]
        for key in sorted(deduplicated)
    ]

    if exclude_last_candle and data:
        data = data[:-1]

    balance = float(starting_balance)
    trades = []
    total_costs = 0.0
    trades_by_day = {}
    daily_start_balance = {}
    daily_realized_pnl = {}
    consecutive_losses = 0

    index = moving_average_period - 1

    while index + 1 < len(data):
        signal_candle = data[index]

        day = datetime.fromtimestamp(
            signal_candle["timestamp"] / 1000,
            tz=timezone.utc,
        ).date().isoformat()

        daily_start_balance.setdefault(day, balance)
        daily_realized_pnl.setdefault(day, 0.0)

        if (
            trades_by_day.get(day, 0)
            >= max_trades_per_utc_day
        ):
            index += 1
            continue

        if consecutive_losses >= max_consecutive_losses:
            index += 1
            continue

        if daily_start_balance[day] > 0:
            daily_loss_percent = (
                max(0.0, -daily_realized_pnl[day])
                / daily_start_balance[day]
                * 100
            )

            if daily_loss_percent >= max_daily_loss_percent:
                index += 1
                continue

        window = data[
            index - moving_average_period + 1:index + 1
        ]

        closes = [item["close"] for item in window]
        volumes = [item["volume"] for item in window]

        price = signal_candle["close"]
        previous_price = (
            data[index - 1]["close"] if index > 0 else price
        )

        moving_average = sum(closes) / len(closes)
        average_volume = sum(volumes) / len(volumes)
        momentum = price - previous_price

        side = None

        if price > moving_average:
            if (
                momentum > 0
                and signal_candle["volume"] > average_volume
            ):
                side = "BUY"

        elif price < moving_average:
            if (
                momentum < 0
                and signal_candle["volume"] > average_volume
            ):
                side = "SELL"

        if side is None:
            index += 1
            continue

        # Do not enter at the signal candle's close. Use the next open.
        entry_index = index + 1
        entry_candle = data[entry_index]
        entry = entry_candle["open"]

        if side == "BUY":
            stop = entry * (1 - stop_loss_fraction)
            target = entry + (entry - stop) * risk_reward_ratio
            direction = 1.0
        else:
            stop = entry * (1 + stop_loss_fraction)
            target = entry - (stop - entry) * risk_reward_ratio
            direction = -1.0

        if target <= 0:
            index += 1
            continue

        risk_budget = balance * risk_percent / 100.0
        quantity = risk_budget / abs(entry - stop)

        exit_price = None
        exit_reason = None
        exit_index = None

        for future_index in range(entry_index, len(data)):
            candle = data[future_index]

            if side == "BUY":
                hit_stop = candle["low"] <= stop
                hit_target = candle["high"] >= target
            else:
                hit_stop = candle["high"] >= stop
                hit_target = candle["low"] <= target

            # Conservative assumption: stop-loss wins if both are touched.
            if hit_stop:
                # Model a stop gap at the worse opening price.
                if side == "BUY" and candle["open"] < stop:
                    exit_price = candle["open"]
                elif side == "SELL" and candle["open"] > stop:
                    exit_price = candle["open"]
                else:
                    exit_price = stop

                exit_reason = "STOP_LOSS"
                exit_index = future_index
                break

            if hit_target:
                exit_price = target
                exit_reason = "TAKE_PROFIT"
                exit_index = future_index
                break

        if exit_price is None:
            # Do not invent an exit if the historical data ends first.
            break

        gross_pnl = (
            (exit_price - entry) * quantity * direction
        )

        entry_cost = (
            entry * quantity
            * estimated_cost_bps_per_side / 10000.0
        )

        exit_cost = (
            exit_price * quantity
            * estimated_cost_bps_per_side / 10000.0
        )

        costs = entry_cost + exit_cost
        net_pnl = gross_pnl - costs

        balance += net_pnl
        total_costs += costs

        trades_by_day[day] = trades_by_day.get(day, 0) + 1
        daily_realized_pnl[day] = (
            daily_realized_pnl.get(day, 0.0) + net_pnl
        )

        if net_pnl < 0:
            consecutive_losses += 1
        else:
            consecutive_losses = 0

        trades.append({
            "side": side,
            "signal_time": datetime.fromtimestamp(
                signal_candle["timestamp"] / 1000,
                tz=timezone.utc,
            ).isoformat(),
            "entry_time": datetime.fromtimestamp(
                entry_candle["timestamp"] / 1000,
                tz=timezone.utc,
            ).isoformat(),
            "exit_time": datetime.fromtimestamp(
                data[exit_index]["timestamp"] / 1000,
                tz=timezone.utc,
            ).isoformat(),
            "entry_price": entry,
            "stop_loss": stop,
            "take_profit": target,
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "quantity": quantity,
            "gross_pnl": gross_pnl,
            "estimated_costs": costs,
            "net_pnl": net_pnl,
            "balance_after": balance,
        })

        # One position at a time: resume only after this position exits.
        index = exit_index + 1

    wins = sum(
        1 for trade in trades if trade["net_pnl"] > 0
    )
    losses = sum(
        1 for trade in trades if trade["net_pnl"] < 0
    )

    gross_total = sum(
        trade["gross_pnl"] for trade in trades
    )
    net_total = sum(
        trade["net_pnl"] for trade in trades
    )

    gross_wins = sum(
        trade["gross_pnl"]
        for trade in trades
        if trade["gross_pnl"] > 0
    )
    gross_losses = -sum(
        trade["gross_pnl"]
        for trade in trades
        if trade["gross_pnl"] < 0
    )

    net_wins = sum(
        trade["net_pnl"]
        for trade in trades
        if trade["net_pnl"] > 0
    )
    net_losses = -sum(
        trade["net_pnl"]
        for trade in trades
        if trade["net_pnl"] < 0
    )

    summary = {
        "closed_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "win_rate_percent": (
            wins / len(trades) * 100 if trades else 0.0
        ),
        "gross_pnl": gross_total,
        "estimated_costs": total_costs,
        "net_pnl": net_total,
        "gross_profit_factor": (
            gross_wins / gross_losses if gross_losses else None
        ),
        "net_profit_factor": (
            net_wins / net_losses if net_losses else None
        ),
        "assumptions": {
            "moving_average_period": moving_average_period,
            "entry": "next candle open after signal candle closes",
            "stop_loss_percent_from_entry": (
                stop_loss_fraction * 100
            ),
            "risk_reward_ratio": risk_reward_ratio,
            "risk_percent_of_equity": risk_percent,
            "estimated_cost_bps_per_side": (
                estimated_cost_bps_per_side
            ),
            "both_stop_and_target_touched": "stop-loss first",
            "last_candle_excluded": exclude_last_candle,
            "paper_trading_only": True,
        },
    }

    return {
        "candles_used": len(data),
        "starting_balance": float(starting_balance),
        "ending_balance": balance,
        "trades": trades,
        "summary": summary,
    }
