from signal_engine import analyze_market
from aaxyy_pipeline import run_aaxyy_pipeline
from paper_trading_executor import PaperTradingExecutor


def main():
    print("AAXYY AI")
    print("Trade Less. Trade Better.")
    print("------------------------------")

    # Sample market data for demonstration.
    # No real exchange orders are sent.
    price = 110
    moving_average = 100
    volume = 1500
    average_volume = 1000
    previous_price = 105

    analysis = analyze_market(
        price=price,
        moving_average=moving_average,
        volume=volume,
        average_volume=average_volume,
        previous_price=previous_price,
    )

    print("\nMARKET ANALYSIS")
    print("----------------")
    print(f"Signal: {analysis['signal']}")
    print(f"Confidence: {analysis['confidence']}")
    print(f"Momentum: {analysis['momentum']}")
    print(f"Volume Status: {analysis['volume_status']}")
    print(f"Explanation: {analysis['explanation']['summary']}")

    risk_reward = 3
    account_balance = 1000
    risk_percent = 2
    entry_price = price
    stop_loss = 105

    result = run_aaxyy_pipeline(
        price=price,
        moving_average=moving_average,
        volume=volume,
        average_volume=average_volume,
        signal=analysis["signal"],
        confidence=analysis["confidence"],
        risk_reward=risk_reward,
        momentum=analysis["momentum"],
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry_price,
        stop_loss=stop_loss,
    )

    print("\nAAXYY PIPELINE")
    print("----------------")
    print(f"Market Regime: {result['market_regime']}")
    print(f"Trade Quality: {result['trade_quality']['quality']}")
    print(f"Final Decision: {result['final_decision']}")

    if result["final_decision"] in ("STRONG BUY", "STRONG SELL"):
        executor = PaperTradingExecutor(
            starting_balance=account_balance
        )

        side = analysis["signal"]

        trade = executor.open_position(
            symbol="BTC",
            side=side,
            entry_price=entry_price,
            quantity=result["position_size"],
            stop_loss=result["targets"]["stop_loss"],
            take_profit=result["targets"]["take_profit"],
        )

        print("\nPAPER TRADE")
        print("----------------")
        print("Status: PAPER POSITION OPENED")
        print(f"Symbol: {trade['symbol']}")
        print(f"Side: {trade['side']}")
        print(f"Entry Price: {trade['entry_price']}")
        print(f"Quantity: {trade['quantity']}")
        print(f"Stop Loss: {trade['stop_loss']}")
        print(f"Take Profit: {trade['take_profit']}")

    else:
        print("\nPAPER TRADE")
        print("----------------")
        print("No paper trade opened.")
        print(f"Reason: {result['final_decision']}")


if __name__ == "__main__":
    main()
