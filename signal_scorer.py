def calculate_signal_score(
    trend_score,
    momentum_score,
    volume_score,
    risk_reward_score,
    conflict_score,
):
    """
    Calculate the overall AAXYY AI signal score.

    Maximum score: 100.
    """

    trend_score = max(0, min(trend_score, 30))
    momentum_score = max(0, min(momentum_score, 25))
    volume_score = max(0, min(volume_score, 20))
    risk_reward_score = max(0, min(risk_reward_score, 15))
    conflict_score = max(0, min(conflict_score, 10))

    total_score = (
        trend_score
        + momentum_score
        + volume_score
        + risk_reward_score
        + conflict_score
    )

    if total_score >= 85:
        decision = "STRONG"
    elif total_score >= 70:
        decision = "GOOD"
    elif total_score >= 50:
        decision = "CAUTION"
    else:
        decision = "WEAK"

    return {
        "score": total_score,
        "decision": decision,
        "breakdown": {
            "trend": trend_score,
            "momentum": momentum_score,
            "volume": volume_score,
            "risk_reward": risk_reward_score,
            "conflict": conflict_score,
        },
  }
