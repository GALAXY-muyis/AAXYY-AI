from market_data import get_market_data
from signal_engine import analyze_market
from aaxyy_pipeline import run_aaxyy_pipeline
from paper_trading_executor import PaperTradingExecutor


def test_aaxyy_end_to_end_paper_trade():
    market_data = get_market_data("bitcoin")

    analysis = analyze_market(
        price=market_data["current_price"],
        moving_average=market_data["moving_average"],
        volume=market_data["current_volume"],
        average_volume=market_data["average_volume"],
        previous_price=market_data["previous_price"],
    )

    entry_price = market_data["current_price"]

    if analysis["signal"] == "BUY":
        stop_loss = entry_price * 0.98
    elif analysis["signal"] == "SELL":
        stop_loss = entry_price * 1.02
    else:
        stop_loss = entry_price

    result = run_aaxyy_pipeline(
        price=entry_price,
        moving_average=market_data["moving_average"],
        volume=market_data["current_volume"],
        average_volume=market_data["average_volume"],
        signal=analysis["signal"],
        confidence=analysis["confidence"],
        risk_reward=3,
        momentum=analysis["momentum"],
        account_balance=1000,
        risk_percent=2,
        entry_price=entry_price,
        stop_loss=stop_loss,
    )

    assert "final_decision" in result
    assert "risk_gate" in result
    assert "trading_guard" in result

    if result["final_decision"] in ("STRONG BUY", "STRONG SELL"):
        executor = PaperTradingExecutor(
            starting_balance=1000
        )

        trade = executor.open_position(
            symbol="BTC",
            side=analysis["signal"],
            entry_price=entry_price,
            quantity=result["position_size"],
            stop_loss=result["targets"]["stop_loss"],
            take_profit=result["targets"]["take_profit"],
        )

        assert trade["status"] == "OPENED"
        assert executor.position is not None
