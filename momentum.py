def calculate_momentum(current_price, previous_price):
    """
    Calculate percentage price momentum.
    """

    if previous_price == 0:
        return 0

    momentum = ((current_price - previous_price) / previous_price) * 100

    return momentum
