def check_risk_gate(
    signal,
    risk_reward,
    stop_loss,
    entry_price,
    position_size,
    conflict_status,
    trade_quality,
):
    if signal == "HOLD":
        return {
            "allowed": False,
            "reason": "NO_TRADE_SIGNAL",
        }

    if entry_price == stop_loss:
        return {
            "allowed": False,
            "reason": "INVALID_STOP_LOSS",
        }

    if position_size <= 0:
        return {
            "allowed": False,
            "reason": "INVALID_POSITION_SIZE",
        }

    if risk_reward < 2:
        return {
            "allowed": False,
            "reason": "RISK_REWARD_TOO_LOW",
        }

    if conflict_status == "CONFLICT":
        return {
            "allowed": False,
            "reason": "SIGNAL_CONFLICT",
        }

    if trade_quality == "WEAK":
        return {
            "allowed": False,
            "reason": "TRADE_QUALITY_TOO_LOW",
        }

    return {
        "allowed": True,
        "reason": "TRADE ALLOWED",
  }
