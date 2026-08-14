class BitgetDataProvider:
    """Read-only Bitget market data provider."""

    def __init__(self):
        self.exchange_name = "Bitget"

    def get_market_data(self, symbol):
        """
        Return market data for a symbol.

        Live API connection will be added later.
        """
        raise NotImplementedError(
            "Bitget market data connection is not configured yet."
        )
