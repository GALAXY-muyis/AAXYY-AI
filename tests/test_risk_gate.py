from risk_gate import check_risk_gate


def test_strong_trade_is_allowed():
    result = check_risk_gate(
        signal="BUY",
        risk_reward=3,
        stop_loss=95,
        entry_price=100,
        position_size=4,
        conflict_status="ALIGNED",
        trade_quality="STRONG",
    )

    assert result["allowed"] is True
    assert result["reason"] == "TRADE ALLOWED"


def test_trade_below_two_to_one_risk_reward_is_rejected():
    result = check_risk_gate(
        signal="BUY",
        risk_reward=1.5,
        stop_loss=95,
        entry_price=100,
        position_size=4,
        conflict_status="ALIGNED",
        trade_quality="STRONG",
    )

    assert result["allowed"] is False
    assert result["reason"] == "RISK_REWARD_TOO_LOW"


def test_zero_stop_distance_is_rejected():
    result = check_risk_gate(
        signal="BUY",
        risk_reward=3,
        stop_loss=100,
        entry_price=100,
        position_size=4,
        conflict_status="ALIGNED",
        trade_quality="STRONG",
    )

    assert result["allowed"] is False
    assert result["reason"] == "INVALID_STOP_LOSS"


def test_hold_signal_is_rejected():
    result = check_risk_gate(
        signal="HOLD",
        risk_reward=3,
        stop_loss=95,
        entry_price=100,
        position_size=4,
        conflict_status="ALIGNED",
        trade_quality="STRONG",
    )

    assert result["allowed"] is False
    assert result["reason"] == "NO_TRADE_SIGNAL"


def test_conflicting_trade_is_rejected():
    result = check_risk_gate(
        signal="BUY",
        risk_reward=3,
        stop_loss=95,
        entry_price=100,
        position_size=4,
        conflict_status="CONFLICT",
        trade_quality="STRONG",
    )

    assert result["allowed"] is False
    assert result["reason"] == "SIGNAL_CONFLICT"


def test_weak_trade_is_rejected():
    result = check_risk_gate(
        signal="BUY",
        risk_reward=3,
        stop_loss=95,
        entry_price=100,
        position_size=4,
        conflict_status="ALIGNED",
        trade_quality="WEAK",
    )

    assert result["allowed"] is False
    assert result["reason"] == "TRADE_QUALITY_TOO_LOW"
