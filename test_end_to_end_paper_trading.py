from signal_engine import analyze_market
from aaxyy_pipeline import run_aaxyy_pipeline
from paper_trading_executor import PaperTradingExecutor


def test_end_to_end_paper_trading_flow():
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

    result = run_aaxyy_pipeline(
        price=price,
        moving_average=moving_average,
        volume=volume,
        average_volume=average_volume,
        signal=analysis["signal"],
        confidence=analysis["confidence"],
        risk_reward=3,
        momentum=analysis["momentum"],
        account_balance=1000,
        risk_percent=2,
        entry_price=price,
        stop_loss=105,
    )

    assert analysis["signal"] == "BUY"
    assert result["final_decision"] == "STRONG BUY"
    assert result["risk_gate"]["allowed"] is True
    assert result["trading_guard"]["allowed"] is True

    executor = PaperTradingExecutor(
        starting_balance=1000
    )

    trade = executor.open_position(
        symbol="BTC",
        side=analysis["signal"],
        entry_price=price,
        quantity=result["position_size"],
        stop_loss=result["targets"]["stop_loss"],
        take_profit=result["targets"]["take_profit"],
    )

    assert trade["status"] == "OPENED"
    assert trade["symbol"] == "BTC"
    assert trade["side"] == "BUY"

    status = executor.get_status(
        current_price=price
    )

    assert status["position_open"] is True
    assert status["total_trades"] == 0
