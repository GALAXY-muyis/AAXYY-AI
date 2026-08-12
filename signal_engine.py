def generate_signal(price, moving_average):
    """
    Generate a basic trading signal from price and moving average.
    """

    if price > moving_average:
        return "BUY"

    if price < moving_average:
        return "SELL"

    return "HOLD"
