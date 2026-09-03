from trade_approval import check_trade_approval


def test_trade_is_approved_when_all_safety_checks_pass():
    opportunity = {
        "signal": "BUY",
        "risk_reward": 3,
        "stop_loss": 95,
        "entry_price": 100,
        "position_size": 4,
        "conflict_status": "ALIGNED",
        "trade_quality": "STRONG",
    }

    result = check_trade_approval(
        opportunity=opportunity,
        trades_today=1,
        consecutive_losses=0,
        daily_loss_percent=1,
    )

    assert result["approved"] is True
    assert result["risk_gate"]["allowed"] is True
    assert result["trading_guard"]["allowed"] is True
