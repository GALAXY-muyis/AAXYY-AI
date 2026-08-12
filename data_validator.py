def validate_price(price):
    """
    Validate a market price before AAXYY AI uses it.
    """

    if price is None:
        return False

    if not isinstance(price, (int, float)):
        return False

    if price <= 0:
        return False

    return True
