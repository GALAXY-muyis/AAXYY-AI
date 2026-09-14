from paper_trading_runner import PaperTradingRunner


def main():
    print("AAXYY AI")
    print("Trade Less. Trade Better.")
    print("------------------------------")

    runner = PaperTradingRunner(
        symbols=[
            "BTC",
            "ETH",
            "SOL",
        ],
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

        else:
            print("Status: NO PAPER TRADE")
            print(f"Reason: {result['reason']}")

    except Exception as error:
        print("\nAAXYY AI ERROR")
        print("------------------------------")
        print(error)


if __name__ == "__main__":
    main()
