from paper_trade_report import PaperTradeReport
from paper_trading_runner import PaperTradingRunner
from paper_trading_state import PaperTradingState


print("AAXYY AI")
print("Trade Less. Trade Better.")
print("------------------------------")
print()

print("AAXYY PAPER TRADING")
print("------------------------------")

runner = PaperTradingRunner(
    symbols=None,
    starting_balance=1000,
    state=PaperTradingState(),
)

result = runner.open_best_paper_trade()

print(f"Status: {result['status']}")

should_monitor = result["status"] == "PAPER_TRADE_OPENED"

if (
    result["status"] == "NO_TRADE"
    and result.get("reason") == "POSITION_ALREADY_OPEN"
):
    should_monitor = True

if should_monitor:

    if result["status"] == "PAPER_TRADE_OPENED":
        trade = result["trade"]

        print(f"Symbol: {trade['symbol']}")
        print(f"Side: {trade['side']}")
        print(f"Entry Price: {trade['entry_price']}")
        print(f"Quantity: {trade['quantity']}")
        print(f"Stop Loss: {trade['stop_loss']}")
        print(f"Take Profit: {trade['take_profit']}")

    else:
        position = runner.executor.position

        print("RESTORED PAPER POSITION")
        print("------------------------------")
        print(f"Symbol: {position.symbol}")
        print(f"Side: {position.side}")
        print(f"Entry Price: {position.entry_price}")
        print(f"Quantity: {position.quantity}")
        print(f"Stop Loss: {position.stop_loss}")
        print(f"Take Profit: {position.take_profit}")

    print()
    print("PAPER TRADE MONITOR")
    print("------------------------------")

    monitor_result = runner.monitor_until_exit(
        max_checks=5,
        interval_seconds=60,
    )

    print(f"Status: {monitor_result['status']}")

    if monitor_result.get("last_status"):
        last_status = monitor_result["last_status"]

        print(f"Last Status: {last_status['status']}")

        if "current_price" in last_status:
            print(
                f"Current Price: "
                f"{last_status['current_price']}"
            )

        if "pnl" in last_status:
            print(
                f"Unrealized PnL: "
                f"{last_status['pnl']:.2f}"
            )

    if monitor_result.get("exit"):
        exit_result = monitor_result["exit"]

        print(f"Exit Price: {exit_result['exit_price']}")
        print(f"Realized PnL: {exit_result['pnl']:.2f}")
        print(f"Exit Reason: {exit_result['reason']}")

elif result["status"] == "NO_TRADE":
    print(f"Reason: {result['reason']}")

    diagnostic = result.get("diagnostic", {})

    print(
        f"Markets Scanned: "
        f"{diagnostic.get('markets_scanned', 0)}"
    )

    print(
        f"Opportunities Found: "
        f"{diagnostic.get('opportunities_found', 0)}"
    )

print()
print("PAPER TRADING PERFORMANCE")
print("------------------------------")

report = PaperTradeReport()
performance = report.generate()

print(f"Total Trades: {performance['total_trades']}")
print(
    f"Winning Trades: "
    f"{performance['winning_trades']}"
)
print(
    f"Losing Trades: "
    f"{performance['losing_trades']}"
)
print(
    f"Breakeven Trades: "
    f"{performance['breakeven_trades']}"
)
print(
    f"Win Rate: "
    f"{performance['win_rate']:.2f}%"
)
print(
    f"Total PnL: "
    f"{performance['total_pnl']:.2f}"
)
print(
    f"Average PnL: "
    f"{performance['average_pnl']:.2f}"
)
print(
    f"Profit Factor: "
    f"{performance['profit_factor']}"
)
