from market_regime import detect_market_regime
from trade_quality import calculate_trade_quality
from signal_conflict import detect_signal_conflict
from trade_decision import make_trade_decision
from position_sizer import calculate_position_size
from risk_targets import calculate_trade_targets
from risk_gate import check_risk_gate


def run_aaxyy_pipeline(
    price,
    moving_average,
    volume,
    average_volume,
    signal,
    confidence,
    risk_reward,
    momentum,
    account_balance,
    risk_percent,
    entry_price,
    stop_loss,
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

    position_size = calculate_position_size(
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry_price,
        stop_loss=stop_loss,
    )

    targets = calculate_trade_targets(
        entry_price=entry_price,
        stop_loss=stop_loss,
        risk_reward_ratio=risk_reward,
        signal=signal,
    )

    risk_gate = check_risk_gate(
        signal=signal,
        risk_reward=risk_reward,
        stop_loss=stop_loss,
        entry_price=entry_price,
        position_size=position_size,
        conflict_status=conflict["status"],
        trade_quality=quality["quality"],
    )

    if signal == "HOLD":
        final_decision = "WAIT"
    elif conflict["status"] == "CONFLICT":
        final_decision = "CAUTION"
    elif not risk_gate["allowed"]:
        final_decision = "NO TRADE"
    else:
        final_decision = decision["decision"]

    return {
        "market_regime": market["regime"],
        "volume_status": volume_status,
        "trade_quality": quality,
        "conflict": conflict,
        "decision": decision,
        "position_size": position_size,
        "targets": targets,
        "risk_gate": risk_gate,
        "final_decision":final_decision,
    }
