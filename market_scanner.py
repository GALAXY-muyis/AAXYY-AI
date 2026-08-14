from market_data_validator import validate_market_data


class MarketScanner:
    """Scan multiple markets and return valid market data."""

    def __init__(self, data_provider):
        self.data_provider = data_provider

    def scan(self, symbols):
        valid_markets = []

        for symbol in symbols:
            data = self.data_provider.get_market_data(symbol)

            validation = validate_market_data(
                price=data["price"],
                moving_average=data["moving_average"],
                volume=data["volume"],
                average_volume=data["average_volume"],
            )

            if validation["valid"]:
                valid_markets.append(data)

        return valid_markets
