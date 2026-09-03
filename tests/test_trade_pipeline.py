from risk_gate import check_risk_gate
from trading_guard import check_trading_guard


def test_selected_opportunity_passes_risk_gate_and_trading_guard():
    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "position_size": 1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    risk_result = check_risk_gate(
        signal=opportunity["signal"],
        risk_reward=opportunity["risk_reward"],
        stop_loss=opportunity["stop_loss"],
        entry_price=opportunity["entry_price"],
        position_size=opportunity["position_size"],
        conflict_status=opportunity["conflict_status"],
        trade_quality=opportunity["trade_quality"],
    )

    trading_result = check_trading_guard(
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    )

    approved = (
        opportunity["valid"]
        and risk_result["allowed"]
        and trading_result["allowed"]
    )

    assert risk_result["allowed"] is True
    assert trading_result["allowed"] is True
    assert approved is True
from trade_pipeline import approve_trade_opportunity


def test_approve_trade_opportunity_returns_safety_approved():
    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "position_size": 1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = approve_trade_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    )

    assert result["approved"] is True
    assert result["reason"] == "SAFETY_APPROVED"
def test_approve_trade_opportunity_rejects_invalid_opportunity():
    opportunity = {
        "symbol": "BTCUSDT",
        "valid": False,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 100000,
        "stop_loss": 99000,
        "position_size": 1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = approve_trade_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    )

    assert result["approved"] is False
    assert result["reason"] == "INVALID_OPPORTUNITY"
def test_approve_trade_opportunity_rejects_risk_gate_failure():
    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "position_size": 1,
        "risk_reward": 1.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = approve_trade_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
    )

    assert result["approved"] is False
    assert result["reason"] == "RISK_REWARD_TOO_LOW"
def test_approve_trade_opportunity_rejects_trading_guard_failure():
    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "position_size": 1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = approve_trade_opportunity(
        opportunity=opportunity,
        trades_today=3,
        consecutive_losses=0,
        daily_loss_percent=0,
    )

    assert result["approved"] is False
    assert "Maximum daily trade limit reached." in result["reason"]
def test_approved_opportunity_can_be_sent_to_paper_trading():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "take_profit": 3250,
        "position_size": 0.1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is True
    assert result["status"] == "OPENED"
    assert result["symbol"] == "ETHUSDT"
    assert result["side"] == "BUY"
def test_rejected_opportunity_does_not_open_paper_position():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "take_profit": 3250,
        "position_size": 0.1,
        "risk_reward": 1.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is False
    assert result["reason"] == "RISK_REWARD_TOO_LOW"
def test_trading_guard_rejection_does_not_open_paper_position():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "take_profit": 3250,
        "position_size": 0.1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=3,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is False
    assert "Maximum daily trade limit reached." in result["reason"]
def test_paper_position_preserves_opportunity_risk_targets():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "SOLUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 150,
        "stop_loss": 145,
        "take_profit": 165,
        "position_size": 0.1,
        "risk_reward": 3.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is True
    assert result["status"] == "OPENED"
    assert result["stop_loss"] == 145
    assert result["take_profit"] == 165
def test_approved_sell_opportunity_opens_paper_position():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "SOLUSDT",
        "valid": True,
        "signal": "SELL",
        "confidence": 95,
        "entry_price": 150,
        "stop_loss": 155,
        "take_profit": 135,
        "position_size": 0.1,
        "risk_reward": 3.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is True
    assert result["status"] == "OPENED"
    assert result["symbol"] == "SOLUSDT"
    assert result["side"] == "SELL"
    assert result["stop_loss"] == 155
    assert result["take_profit"] == 135
def test_paper_execution_uses_risk_based_quantity():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "BTCUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 100,
        "stop_loss": 95,
        "take_profit": 110,
        "position_size": 999,
        "risk_reward": 2.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is True
    assert result["status"] == "OPENED"
    assert result["quantity"] == 2.0
def test_invalid_stop_loss_does_not_open_paper_position():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 3000,
        "take_profit": 3300,
        "position_size": 0.1,
        "risk_reward": 3.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = execute_approved_opportunity(
        opportunity=opportunity,
        trades_today=0,
        consecutive_losses=0,
        daily_loss_percent=0,
        risk_percent=1.0,
        starting_balance=1000,
    )

    assert result["approved"] is False
    assert result["reason"] == "INVALID_STOP_LOSS"
def test_invalid_starting_balance_does_not_open_paper_position():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 2900,
        "take_profit": 3250,
        "position_size": 0.1,
        "risk_reward": 2.5,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    try:
        result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=0,
        )
    except ValueError:
        return

    assert result["approved"] is False
def test_buy_opportunity_with_wrong_side_stop_loss_is_rejected():
    from trade_pipeline import execute_approved_opportunity

    opportunity = {
        "symbol": "ETHUSDT",
        "valid": True,
        "signal": "BUY",
        "confidence": 95,
        "entry_price": 3000,
        "stop_loss": 3100,
        "take_profit": 3300,
        "position_size": 0.1,
        "risk_reward": 2.0,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    try:
        result = execute_approved_opportunity(
            opportunity=opportunity,
            trades_today=0,
            consecutive_losses=0,
            daily_loss_percent=0,
            risk_percent=1.0,
            starting_balance=1000,
        )
    except ValueError:
        return

    assert result["approved"] is False
