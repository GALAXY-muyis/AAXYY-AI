def format_signal(signal_data):
    """
    Format an AAXYY AI signal into a clean human-readable report.
    """

    symbol = signal_data.get("symbol", "UNKNOWN")
    signal = signal_data.get("signal", "UNKNOWN")
    score = signal_data.get("score", 0)
    decision = signal_data.get("decision", "WAIT")
    confidence = signal_data.get("confidence", 0)
    entry = signal_data.get("entry_price", 0)
    stop_loss = signal_data.get("stop_loss", 0)
    take_profit = signal_data.get("take_profit", 0)
    leverage = signal_data.get("leverage", 5)
    risk_reward = signal_data.get("risk_reward", 0)

    report = (
        "AAXYY AI SIGNAL\n"
        "====================\n"
        f"Pair: {symbol}\n"
        f"Signal: {signal}\n"
        f"Decision: {decision}\n"
        f"Score: {score}/100\n"
        f"Confidence: {confidence}/100\n"
        f"Entry: {entry}\n"
        f"Stop Loss: {stop_loss}\n"
        f"Take Profit: {take_profit}\n"
        f"Risk/Reward: {risk_reward}\n"
        f"Leverage: {leverage}x\n"
        "===================="
    )

    return report
