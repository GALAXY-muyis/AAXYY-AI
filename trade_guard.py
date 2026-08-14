from config import (
    MIN_CONFIDENCE,
    MAX_RISK_PERCENT,
    MAX_TRADES_PER_DAY,
    MAX_CONSECUTIVE_LOSSES,
    MAX_LEVERAGE,
    MIN_RISK_REWARD,
)


def validate_trade(
    confidence,
    risk_percent,
    leverage,
    risk_reward,
    trades_today,
    consecutive_losses,
):
    """
    Validate a proposed trade against AAXYY AI safety rules.

    Returns:
        dict containing approval status and rejection reason.
    """

    if confidence < MIN_CONFIDENCE:
        return {
            "approved": False,
            "reason": "CONFIDENCE_TOO_LOW",
        }

    if risk_percent > MAX_RISK_PERCENT:
        return {
            "approved": False,
            "reason": "RISK_TOO_HIGH",
        }

    if leverage > MAX_LEVERAGE:
        return {
            "approved": False,
            "reason": "LEVERAGE_TOO_HIGH",
        }

    if risk_reward < MIN_RISK_REWARD:
        return {
            "approved": False,
            "reason": "RISK_REWARD_TOO_LOW",
        }

    if trades_today >= MAX_TRADES_PER_DAY:
        return {
            "approved": False,
            "reason": "DAILY_TRADE_LIMIT_REACHED",
        }

    if consecutive_losses >= MAX_CONSECUTIVE_LOSSES:
        return {
            "approved": False,
            "reason": "LOSS_LIMIT_REACHED",
        }

    return {
        "approved": True,
        "reason": "TRADE_APPROVED",
  }
