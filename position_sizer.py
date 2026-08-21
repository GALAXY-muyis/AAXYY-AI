def calculate_position_size(
    account_balance,
    risk_percent,
    entry_price,
    stop_loss,
):
    risk_amount = account_balance * (risk_percent / 100)

    risk_per_unit = abs(entry_price - stop_loss)

    if risk_per_unit <= 0:
        return 0

    position_size = risk_amount / risk_per_unit

    return position_size
