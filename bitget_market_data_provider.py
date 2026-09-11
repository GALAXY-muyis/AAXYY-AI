import requests

from market_data_provider import MarketDataProvider


class BitgetMarketDataProvider(MarketDataProvider):
    """Read public USDT-margined futures market data from Bitget."""

    BASE_URL = "https://api.bitget.com"
    ENDPOINT = "/api/v2/mix/market/candles"

    def __init__(self, granularity="15m", limit=50):
        self.granularity = granularity
        self.limit = limit

    def get_market_data(self, symbol):
        """Return market data in the format expected by MarketScanner."""

        symbol = symbol.upper()

        if not symbol.endswith("USDT"):
            symbol = f"{symbol}USDT"

        params = {
            "symbol": symbol,
            "productType": "USDT-FUTURES",
            "granularity": self.granularity,
            "limit": self.limit,
        }

        response = requests.get(
            f"{self.BASE_URL}{self.ENDPOINT}",
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("code") != "00000":
            raise ValueError(
                f"Bitget API error: {payload.get('msg', 'Unknown error')}"
            )

        candles = payload.get("data", [])

        if len(candles) < 2:
            raise ValueError(
                f"Not enough candle data returned for {symbol}."
            )

        # Bitget candle format:
        # [timestamp, open, high, low, close, base_volume, quote_volume]
        candles = list(reversed(candles))

        closes = [float(candle[4]) for candle in candles]
        volumes = [float(candle[5]) for candle in candles]

        current_price = closes[-1]
        previous_price = closes[-2]

        moving_average = sum(closes) / len(closes)
        current_volume = volumes[-1]
        average_volume = sum(volumes) / len(volumes)

        momentum = current_price - previous_price

        return {
            "symbol": symbol,
            "price": current_price,
            "moving_average": moving_average,
            "volume": current_volume,
            "average_volume": average_volume,
            "previous_price": previous_price,
            "momentum": momentum,
      }
