from market_regime import detect_market_regime
from trade_quality import calculate_trade_quality
from signal_conflict import detect_signal_conflict
from trade_decision import make_trade_decision


def run_aaxyy_pipeline(
    price,
    moving_average,
    volume,
    average_volume,
    signal,
    confidence,
    risk_reward,
    momentum,
):
    market = detect_market_regime(
        price,
        moving_average,
        momentum,
    )

    if volume > average_volume:
        volume_status = "HIGH"
    elif volume < average_volume:
        volume_status = "LOW"
    else:
        volume_status = "NORMAL"

    quality = calculate_trade_quality(
        signal=signal,
        confidence=confidence,
        risk_reward=risk_reward,
        momentum=momentum,
        volume_status=volume_status,
    )

    conflict = detect_signal_conflict(
        signal=signal,
        market_regime=market["regime"],
        momentum=momentum,
        volume_status=volume_status,
    )

    decision = make_trade_decision(
        signal=signal,
        confidence=confidence,
        trade_quality=quality["quality"],
        market_regime=market["regime"],
    )

    if conflict["status"] == "CONFLICT":
        final_decision = "CAUTION"
    else:
        final_decision = decision["decision"]

    return {
        "market_regime": market["regime"],
        "volume_status": volume_status,
        "trade_quality": quality,
        "conflict": conflict,
        "decision": decision,
        "final_decision": final_decision,
  }
