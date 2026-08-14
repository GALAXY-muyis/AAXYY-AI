class MarketDataProvider:
    """Base interface for AAXYY market data providers."""

    def get_market_data(self, symbol):
        raise NotImplementedError(
            "Market data provider must implement get_market_data()."
        )


class MockMarketDataProvider(MarketDataProvider):
    """Temporary provider used for development and testing."""

    def get_market_data(self, symbol):
        return {
            "symbol": symbol,
            "price": 100.0,
            "moving_average": 98.0,
            "volume": 1500.0,
            "average_volume": 1000.0,
            "momentum": 5.0,
        }
