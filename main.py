from paper_trade_report import PaperTradeReport
from paper_trading_runner import PaperTradingRunner
from paper_trading_state import PaperTradingState
from paper_trade_history import PaperTradeHistory


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

if result["status"] == "NO_TRADE":
    print(f"Reason: {result.get('reason', 'NOT_PROVIDED')}")

diagnostic = result.get("diagnostic", {})

print()
print("MARKET SCAN DIAGNOSTICS")
print("------------------------------")
print(f"Markets Requested: {diagnostic.get('markets_scanned', len(runner.symbols))}")
print(f"Markets Analyzed: {len(runner.last_opportunities)}")

valid_count = sum(
    1
    for candidate in runner.last_opportunities
    if candidate.get("valid", False)
)

print(f"Valid Opportunities: {valid_count}")
print(f"Opportunities Found: {len(runner.last_opportunities)}")

if diagnostic.get("best_opportunity"):
    print(f"Best Opportunity: {diagnostic['best_opportunity']}")

print()
print("LEADING CANDIDATE DECISION DIAGNOSTICS")
print("------------------------------")

if not runner.last_opportunities:
    print("No candidates reached pipeline analysis.")
else:
    for number, candidate in enumerate(
        runner.last_opportunities[:10],
        start=1,
    ):
        quality = candidate.get("trade_quality")

        if isinstance(quality, dict):
            quality = quality.get("quality", quality)

        conflict = candidate.get("conflict", {})
        risk_gate = candidate.get("risk_gate", {})
        trading_guard = candidate.get("trading_guard", {})
        decision = candidate.get("decision", {})

        print()
        print(
            f"Candidate {number}: "
            f"{candidate.get('symbol', 'UNKNOWN')}"
        )

        print(
            f"  Signal: {candidate.get('signal')} | "
            f"Confidence: {candidate.get('confidence')}"
        )

        print(
            f"  Valid: {candidate.get('valid')} | "
            f"Final Decision: {candidate.get('final_decision')} | "
            f"Score: {candidate.get('scan_score')}"
        )

        print(
            f"  Trade Quality: {quality} | "
            f"Risk-Reward: {candidate.get('risk_reward')}"
        )

        print(
            f"  Market Regime: {candidate.get('market_regime')} | "
            f"Volume: {candidate.get('volume_status')}"
        )

        print(
            "  SIGNAL CONFLICT: "
            f"{conflict if conflict else 'No conflict details returned'}"
        )

        print(
            "  RISK GATE: "
            f"{risk_gate if risk_gate else 'No risk-gate details returned'}"
        )

        print(
            "  TRADING GUARD: "
            f"{trading_guard if trading_guard else 'No trading-guard details returned'}"
        )

        print(f"  DECISION ENGINE: {decision}")

        print(
            "  FINAL CANDIDATE DECISION: "
            f"{candidate.get('final_decision', 'NOT_PROVIDED')}"
        )

        print("------------------------------")


should_monitor = (
    result["status"] == "PAPER_TRADE_OPENED"
    or (
        result["status"] == "NO_TRADE"
        and result.get("reason") == "POSITION_ALREADY_OPEN"
    )
)

if should_monitor:
    if result["status"] == "PAPER_TRADE_OPENED":
        trade = result["trade"]

        print()
        print("NEW PAPER POSITION")
        print("------------------------------")
        print(f"Symbol: {trade['symbol']}")
        print(f"Side: {trade['side']}")
        print(f"Entry Price: {trade['entry_price']}")
        print(f"Quantity: {trade['quantity']}")
        print(f"Stop Loss: {trade['stop_loss']}")
        print(f"Take Profit: {trade['take_profit']}")
    else:
        position = runner.executor.position

        print()
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
            print(f"Current Price: {last_status['current_price']}")

        if "pnl" in last_status:
            print(f"Unrealized PnL: {last_status['pnl']:.2f}")

    if monitor_result.get("exit"):
        exit_result = monitor_result["exit"]

        print(f"Exit Price: {exit_result['exit_price']}")
        print(f"Realized PnL: {exit_result['pnl']:.2f}")
        print(f"Exit Reason: {exit_result['reason']}")


print()
print("PAPER TRADING PERFORMANCE")
print("------------------------------")

report = PaperTradeReport()
performance = report.generate()

print(f"Total Trades: {performance['total_trades']}")
print(f"Winning Trades: {performance['winning_trades']}")
print(f"Losing Trades: {performance['losing_trades']}")
print(f"Breakeven Trades: {performance['breakeven_trades']}")
print(f"Win Rate: {performance['win_rate']:.2f}%")
print(f"Total PnL: {performance['total_pnl']:.2f}")
print(f"Average PnL: {performance['average_pnl']:.2f}")
print(f"Profit Factor: {performance['profit_factor']}")

print()
print("PAPER TRADE HISTORY")
print("------------------------------")

history = PaperTradeHistory()
trades = history.load()

print(f"History Records: {len(trades)}")

if not trades:
    print("No completed paper trades recorded.")
else:
    for number, trade in enumerate(trades, start=1):
        print(f"Trade {number}")
        print(f"Symbol: {trade.get('symbol')}")
        print(f"Side: {trade.get('side')}")
        print(f"Entry Price: {trade.get('entry_price')}")
        print(f"Exit Price: {trade.get('exit_price')}")
        print(f"Quantity: {trade.get('quantity')}")
        print(f"PnL: {trade.get('pnl')}")
        print(f"Reason: {trade.get('reason')}")
        print(f"Balance After: {trade.get('balance_after')}")
        print("------------------------------")
