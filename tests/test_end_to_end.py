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
    executor = run_end_to_end_test(
        signal="BUY",
        price=100,
        moving_average=99,
        volume=2000,
        average_volume=1000,
        previous_price=99,
    )

    assert executor.position.side == "BUY"


def test_aaxyy_end_to_end_sell():
    executor = run_end_to_end_test(
        signal="SELL",
        price=100,
        moving_average=101,
        volume=2000,
        average_volume=1000,
        previous_price=101,
    )

    assert executor.position.side == "SELL"


def test_aaxyy_buy_trade_hits_take_profit():
    executor = run_end_to_end_test(
        signal="BUY",
        price=100,
        moving_average=99,
        volume=2000,
        average_volume=1000,
        previous_price=99,
    )

    take_profit = executor.position.take_profit

    result = executor.check_exit(take_profit)

    assert result is not None
    assert result["reason"] == "TAKE_PROFIT"
    assert result["exit_price"] == take_profit
    assert result["pnl"] > 0
    assert executor.position is None
    assert executor.balance > executor.starting_balance


def test_aaxyy_sell_trade_hits_stop_loss():
    executor = run_end_to_end_test(
        signal="SELL",
        price=100,
        moving_average=101,
        volume=2000,
        average_volume=1000,
        previous_price=101,
    )

    stop_loss = executor.position.stop_loss

    result = executor.check_exit(stop_loss)

    assert result is not None
    assert result["reason"] == "STOP_LOSS"
    assert result["exit_price"] == stop_loss
    assert result["pnl"] < 0
    assert executor.position is None
    assert executor.balance < executor.starting_balance
