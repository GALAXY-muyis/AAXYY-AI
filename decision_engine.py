def make_trade_decision(
    signal,
    score,
    approved,
    conflict_status,
):
    """
    Convert AAXYY analysis into a final trading decision.
    """

    if not approved:
        return {
            "decision": "NO TRADE",
            "reason": "TRADE GUARD REJECTED THE SIGNAL",
        }

    if conflict_status == "CONFLICT":
        return {
            "decision": "CAUTION",
            "reason": "SIGNAL CONFLICT DETECTED",
        }

    if score >= 85 and signal == "BUY":
        return {
            "decision": "STRONG BUY",
            "reason": "High score with aligned BUY conditions",
        }

    if score >= 70 and signal == "BUY":
        return {
            "decision": "BUY",
            "reason": "Good score with BUY conditions",
        }

    if score >= 85 and signal == "SELL":
        return {
            "decision": "STRONG SELL",
            "reason": "High score with aligned SELL conditions",
        }

    if score >= 70 and signal == "SELL":
        return {
            "decision": "SELL",
            "reason": "Good score with SELL conditions",
        }

    return {
        "decision": "WAIT",
        "reason": "Signal strength is insufficient",
    }
