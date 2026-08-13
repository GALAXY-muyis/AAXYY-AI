def calculate_position_size(account_balance, risk_percent, entry_price, stop_loss):
    """
    Calculate position size based on account risk.

    account_balance: total account value
    risk_percent: percentage of account to risk
    entry_price: planned entry price
    stop_loss: stop-loss price
    """

    if account_balance <= 0:
        return 0

    if risk_percent <= 0:
        return 0

    if entry_price <= 0 or stop_loss <= 0:
        return 0

    risk_amount = account_balance * (risk_percent / 100)

    price_risk = abs(entry_price - stop_loss)

    if price_risk == 0:
        return 0

    position_size = risk_amount / price_risk

    return position_size
