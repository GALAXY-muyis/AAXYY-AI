from market_data import get_market_data
from signal_engine import analyze_market
from aaxyy_pipeline import run_aaxyy_pipeline
from paper_trading_executor import PaperTradingExecutor


def main():
    print("AAXYY AI")
    print("Trade Less. Trade Better.")
    print("------------------------------")

    coin_id = "bitcoin"

    try:
        market_data = get_market_data(coin_id)

        price = market_data["current_price"]
        previous_price = market_data["previous_price"]
        moving_average = market_data["moving_average"]
        volume = market_data["current_volume"]
        average_volume = market_data["average_volume"]

        analysis = analyze_market(
            price=price,
            moving_average=moving_average,
            volume=volume,
            average_volume=average_volume,
            previous_price=previous_price,
        )

        print("\nMARKET ANALYSIS")
        print("----------------")
        print(f"Coin: {coin_id.upper()}")
        print(f"Price: ${price:,.2f}")
        print(f"Moving Average: ${moving_average:,.2f}")
        print(f"Signal: {analysis['signal']}")
        print(f"Confidence: {analysis['confidence']}")
        print(f"Momentum: {analysis['momentum']}")
        print(f"Volume Status: {analysis['volume_status']}")
        print(f"Explanation: {analysis['explanation']['summary']}")

        risk_reward = 3
        account_balance = 1000
        risk_percent = 2
        entry_price = price

        if analysis["signal"] == "BUY":
            stop_loss = entry_price * 0.98
        elif analysis["signal"] == "SELL":
            stop_loss = entry_price * 1.02
        else:
            stop_loss = entry_price

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
        print(f"Risk Gate: {result['risk_gate']['allowed']}")
        print(f"Trading Guard: {result['trading_guard']['allowed']}")
        print(f"Final Decision: {result['final_decision']}")

        if result["final_decision"] in ("STRONG BUY", "STRONG SELL"):
            executor = PaperTradingExecutor(
                starting_balance=account_balance
            )

            side = analysis["signal"]

            trade = executor.open_position(
                symbol=coin_id.upper(),
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

    except Exception as error:
        print("\nAAXYY AI ERROR")
        print("----------------")
        print(error)


if __name__ == "__main__":
    main()
