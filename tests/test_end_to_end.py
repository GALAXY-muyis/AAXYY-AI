from market_data import get_market_data
from signal_engine import analyze_market
from aaxyy_pipeline import run_aaxyy_pipeline
from paper_trading_executor import PaperTradingExecutor


def run_end_to_end_test(
    signal,
    price,
    moving_average,
    volume,
    average_volume,
    previous_price,
):
    analysis = analyze_market(
        price=price,
        moving_average=moving_average,
        volume=volume,
        average_volume=average_volume,
        previous_price=previous_price,
    )

    entry_price = price

    if signal == "BUY":
        stop_loss = entry_price * 0.98
    else:
        stop_loss = entry_price * 1.02

    result = run_aaxyy_pipeline(
        price=price,
        moving_average=moving_average,
        volume=volume,
        average_volume=average_volume,
        signal=signal,
        confidence=90,
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

    assert result["final_decision"] in (
        "STRONG BUY",
        "STRONG SELL",
    )

    executor = PaperTradingExecutor(
        starting_balance=1000
    )

    trade = executor.open_position(
        symbol="BTC",
        side=signal,
        entry_price=entry_price,
        quantity=result["position_size"],
        stop_loss=result["targets"]["stop_loss"],
        take_profit=result["targets"]["take_profit"],
    )

    assert trade["status"] == "OPENED"
    assert trade["side"] == signal
    assert executor.position is not None

    return executor


def test_aaxyy_end_to_end_buy():
    market_data = get_market_data("bitcoin")

    executor = run_end_to_end_test(
        signal="BUY",
        price=market_data["current_price"],
        moving_average=market_data["current_price"] - 1,
        volume=2000,
        average_volume=1000,
        previous_price=market_data["current_price"] - 1,
    )

    assert executor.position.side == "BUY"


def test_aaxyy_end_to_end_sell():
    market_data = get_market_data("bitcoin")

    executor = run_end_to_end_test(
        signal="SELL",
        price=market_data["current_price"],
        moving_average=market_data["current_price"] + 1,
        volume=2000,
        average_volume=1000,
        previous_price=market_data["current_price"] + 1,
    )

    assert executor.position.side == "SELL"
