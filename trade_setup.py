from trade_targets import calculate_trade_targets
from trade_setup_validator import validate_trade_setup
from position_sizer import calculate_position_size


def build_trade_setup(
    account_balance,
    risk_percent,
    entry_price,
    stop_loss,
    signal,
    risk_reward=3.0,
):
    """
    Build and validate a complete AAXYY AI trade setup.
    """

    targets = calculate_trade_targets(
        entry_price=entry_price,
        stop_loss=stop_loss,
        risk_reward=risk_reward,
        signal=signal,
    )

    if not targets["valid"]:
        return {
            "valid": False,
            "reason": targets["reason"],
        }

    setup_validation = validate_trade_setup(
        entry_price=entry_price,
        stop_loss=stop_loss,
        take_profit=targets["take_profit"],
        signal=signal,
    )

    if not setup_validation["valid"]:
        return {
            "valid": False,
            "reason": setup_validation["reason"],
        }

    position_size = calculate_position_size(
        account_balance=account_balance,
        risk_percent=risk_percent,
        entry_price=entry_price,
        stop_loss=stop_loss,
    )

    if position_size <= 0:
        return {
            "valid": False,
            "reason": "INVALID_POSITION_SIZE",
        }

    return {
        "valid": True,
        "signal": signal,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": targets["take_profit"],
        "risk_per_unit": targets["risk_per_unit"],
        "risk_reward": targets["risk_reward"],
        "position_size": position_size,
        "risk_percent": risk_percent,
  }
