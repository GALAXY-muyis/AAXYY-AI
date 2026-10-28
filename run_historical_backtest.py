
"""Run an isolated, paper-only backtest on public Bitget historical candles.

This script never loads, changes, or writes AAXYY paper-trading state/history.
It does not place orders. Results are historical simulations, not forecasts.
"""

import argparse
from datetime import datetime, timedelta, timezone

from bitget_market_data_provider import BitgetMarketDataProvider
from historical_signal_backtest import backtest_candles


DEFAULT_SYMBOLS = ("BTC", "ETH", "SOL", "XRP")
MAX_DAYS = 90


def _money(value):
    return f"${value:,.2f}"


def _profit_factor(trades):
    wins = sum(
        trade["net_pnl"]
        for trade in trades
        if trade["net_pnl"] > 0
    )
    losses = -sum(
        trade["net_pnl"]
        for trade in trades
        if trade["net_pnl"] < 0
    )

    if losses == 0:
        return "N/A (no net losses observed)"

    return f"{wins / losses:.2f}"


def _max_closed_trade_drawdown(starting_balance, trades):
    """Return realized-equity peak-to-trough drawdown in dollars and percent."""
    peak = float(starting_balance)
    worst_dollars = 0.0
    worst_percent = 0.0

    for trade in trades:
        equity = float(trade["balance_after"])
        peak = max(peak, equity)
        drawdown = peak - equity
        drawdown_percent = (
            drawdown / peak * 100 if peak > 0 else 0.0
        )
        worst_dollars = max(worst_dollars, drawdown)
        worst_percent = max(worst_percent, drawdown_percent)

    return worst_dollars, worst_percent


def _print_group(label, trades):
    wins = sum(1 for trade in trades if trade["net_pnl"] > 0)
    losses = sum(1 for trade in trades if trade["net_pnl"] < 0)
    net_pnl = sum(trade["net_pnl"] for trade in trades)
    costs = sum(trade["estimated_costs"] for trade in trades)
    win_rate = wins / len(trades) * 100 if trades else 0.0

    print(
        f"  {label}: trades={len(trades)}, wins={wins}, "
        f"losses={losses}, win_rate={win_rate:.2f}%, "
        f"net_pnl={_money(net_pnl)}, "
        f"estimated_costs={_money(costs)}, "
        f"net_profit_factor={_profit_factor(trades)}"
    )


def run_backtest(symbols, days=30, ending_at=None):
    """Fetch real public candles and print per-symbol and per-side metrics."""
    if not 1 <= days <= MAX_DAYS:
        raise ValueError(f"days must be between 1 and {MAX_DAYS}.")

    if not symbols:
        raise ValueError("At least one symbol must be supplied.")

    end_time = ending_at or datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days)
    start_ms = int(start_time.timestamp() * 1000)
    end_ms = int(end_time.timestamp() * 1000)

    provider = BitgetMarketDataProvider(
        granularity="15m",
        limit=1000,
    )
    failures = 0

    print("AAXYY HISTORICAL BACKTEST — SIMULATION ONLY")
    print("No live orders. Paper-trading state/history are not accessed.")
    print(
        f"Period requested (UTC): {start_time.isoformat()} "
        f"to {end_time.isoformat()}"
    )
    print(f"Symbols: {', '.join(symbol.upper() for symbol in symbols)}")
    print("Assumptions: 15m candles, 2% stop, 3R target, 2% equity risk,")
    print(
        "             estimated trading costs 10 bps per side, "
        "stop-first on ambiguous candles."
    )
    print(
        "Drawdown is based on closed-trade equity, "
        "not intratrade mark-to-market."
    )
    print("-" * 72)

    for requested_symbol in symbols:
        symbol = requested_symbol.upper()
        if symbol.endswith("USDT"):
            symbol = symbol[:-4]

        try:
            candles = provider.get_historical_candles(
                symbol,
                start_time=start_ms,
                end_time=end_ms,
                limit=1000,
            )

            if len(candles) < 60:
                raise ValueError(
                    f"Only {len(candles)} candles returned; at least "
                    "60 are required for a useful initial run."
                )

            result = backtest_candles(candles)
            trades = result["trades"]
            summary = result["summary"]

            drawdown_dollars, drawdown_percent = (
                _max_closed_trade_drawdown(
                    result["starting_balance"],
                    trades,
                )
            )

            print(f"\n{symbol}USDT")
            print(f"  Candles used: {result['candles_used']}")
            print(
                f"  Closed trades: {summary['closed_trades']} | "
                f"Wins: {summary['wins']} | "
                f"Losses: {summary['losses']} | "
                f"Win rate: {summary['win_rate_percent']:.2f}%"
            )
            print(
                f"  Gross PnL: {_money(summary['gross_pnl'])} | "
                f"Estimated costs: "
                f"{_money(summary['estimated_costs'])} | "
                f"Net PnL: {_money(summary['net_pnl'])}"
            )
            print(
                f"  Ending balance from $1,000: "
                f"{_money(result['ending_balance'])}"
            )
            print(f"  Net profit factor: {_profit_factor(trades)}")
            print(
                f"  Max closed-trade drawdown: "
                f"{_money(drawdown_dollars)} "
                f"({drawdown_percent:.2f}%)"
            )

            _print_group(
                "BUY",
                [
                    trade for trade in trades
                    if trade["side"] == "BUY"
                ],
            )
            _print_group(
                "SELL",
                [
                    trade for trade in trades
                    if trade["side"] == "SELL"
                ],
            )

            if not trades:
                print(
                    "  NOTE: No completed trades were produced; "
                    "this is not proof of profitability."
                )

        except Exception as error:
            failures += 1
            print(f"\n{symbol}USDT: BACKTEST FAILED — {error}")

    print(
        "\nBacktest finished. Historical simulation is not a guarantee "
        "of future results."
    )

    return 1 if failures == len(symbols) else 0


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run AAXYY's isolated historical backtest on public "
            "Bitget 15m candles."
        )
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=list(DEFAULT_SYMBOLS),
        help="Base symbols to test (default: BTC ETH SOL XRP).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help=f"Historical period in days, from 1 to {MAX_DAYS} (default: 30).",
    )
    args = parser.parse_args()

    try:
        return run_backtest(args.symbols, days=args.days)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
