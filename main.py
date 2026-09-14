from paper_trading_runner import PaperTradingRunner


def main():
    print("AAXYY AI")
    print("Trade Less. Trade Better.")
    print("------------------------------")

    runner = PaperTradingRunner(
        symbols=None,
        starting_balance=1000,
    )

    try:
        result = runner.open_best_paper_trade()

        print("\nAAXYY PAPER TRADING")
        print("------------------------------")

        if result["status"] == "PAPER_TRADE_OPENED":
            trade = result["trade"]

            print("Status: PAPER TRADE OPENED")
            print(f"Symbol: {trade['symbol']}")
            print(f"Side: {trade['side']}")
            print(f"Entry Price: {trade['entry_price']}")
            print(f"Quantity: {trade['quantity']}")
            print(f"Stop Loss: {trade['stop_loss']}")
            print(f"Take Profit: {trade['take_profit']}")

            monitoring = runner.monitor_until_exit(
                max_checks=5,
                interval_seconds=60,
            )

            print("\nPAPER TRADE MONITOR")
            print("------------------------------")

            if monitoring["status"] == "PAPER_TRADE_CLOSED":
                exit_result = monitoring["exit"]

                print("Status: PAPER TRADE CLOSED")
                print(f"Reason: {exit_result['reason']}")
                print(f"Exit Price: {exit_result['exit_price']}")
                print(f"PnL: {exit_result['pnl']:.2f}")
                print(
                    f"Balance: "
                    f"{exit_result['balance_after']:.2f}"
                )

            elif monitoring["status"] == "MONITORING_LIMIT_REACHED":
                last_status = monitoring["last_status"]

                print("Status: MONITORING LIMIT REACHED")
                print(
                    f"Last Status: "
                    f"{last_status['status']}"
                )

                if last_status["status"] == "POSITION_OPEN":
                    print(
                        f"Current Price: "
                        f"{last_status['current_price']}"
                    )
                    print(
                        f"Unrealized PnL: "
                        f"{last_status['pnl']:.2f}"
                    )

                else:
            print("Status: NO PAPER TRADE")
            print(f"Reason: {result['reason']}")

            diagnostic = result.get("diagnostic")

            if diagnostic:
                print("\nAAXYY SCAN DIAGNOSTIC")
                print("------------------------------")
                print(
                    f"Markets Scanned: "
                    f"{diagnostic.get('markets_scanned')}"
                )
                print(
                    f"Opportunities Found: "
                    f"{diagnostic.get('opportunities_found')}"
                )

                candidates = diagnostic.get(
                    "top_candidates",
                    [],
                )

                if candidates:
                    print("\nTOP CANDIDATES")

                    for candidate in candidates:
                        print(
                            f"{candidate.get('symbol')} | "
                            f"Signal: {candidate.get('signal')} | "
                            f"Confidence: "
                            f"{candidate.get('confidence')} | "
                            f"Quality: "
                            f"{candidate.get('trade_quality')} | "
                            f"RR: "
                            f"{candidate.get('risk_reward')} | "
                            f"Score: "
                            f"{candidate.get('scan_score')} | "
                            f"Valid: "
                            f"{candidate.get('valid')} | "
                            f"Decision: "
                            f"{candidate.get('final_decision')}"
                        )

    except Exception as error:
        print("\nAAXYY AI ERROR")
        print("------------------------------")
        print(error)


if __name__ == "__main__":
    main()
