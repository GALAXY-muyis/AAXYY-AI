from risk_manager import calculate_risk


def test_risk_reward_ratio():
    result = calculate_risk(100, 95, 110)

    assert result["risk"] == 5
    assert result["reward"] == 10
    assert result["risk_reward_ratio"] == 2


def test_zero_risk():
    result = calculate_risk(100, 100, 110)

    assert result["risk"] == 0
    assert result["reward"] == 10
    assert result["risk_reward_ratio"] is None
