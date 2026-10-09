import requests

from market_data_provider import MarketDataProvider


class BitgetMarketDataProvider(MarketDataProvider):
    """Read public USDT-margined futures market data from Bitget."""

    BASE_URL = "https://api.bitget.com"
    ENDPOINT = "/api/v2/mix/market/candles"

    def __init__(self, granularity="15m", limit=50):
        self.granularity = granularity
        self.limit = limit

    def _normalize_symbol(self, symbol):
        """Normalize a symbol to its USDT futures form."""

        symbol = symbol.upper()

        if not symbol.endswith("USDT"):
            symbol = f"{symbol}USDT"

        return symbol

    def _request_candles(self, symbol, params):
        """Request a single batch of historical candles."""

        response = requests.get(
            f"{self.BASE_URL}{self.ENDPOINT}",
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("code") != "00000":
            raise ValueError(
                f"Bitget API error: "
                f"{payload.get('msg', 'Unknown error')}"
            )

        return payload.get("data", [])

    def get_market_data(self, symbol):
        """Return market data in the format expected by MarketScanner."""

        symbol = self._normalize_symbol(symbol)

        params = {
            "symbol": symbol,
            "productType": "USDT-FUTURES",
            "granularity": self.granularity,
            "limit": self.limit,
        }

        candles = self._request_candles(symbol, params)

        if len(candles) < 2:
            raise ValueError(
                f"Not enough candle data returned for {symbol}."
            )

        candles = sorted(
            candles,
            key=lambda candle: int(candle[0]),
        )

        closes = [float(candle[4]) for candle in candles]
        volumes = [float(candle[5]) for candle in candles]

        current_candle = candles[-1]

        current_price = closes[-1]
        previous_price = closes[-2]

        current_high = float(current_candle[2])
        current_low = float(current_candle[3])

        moving_average = sum(closes) / len(closes)
        current_volume = volumes[-1]
        average_volume = sum(volumes) / len(volumes)

        momentum = current_price - previous_price

        return {
            "symbol": symbol,
            "price": current_price,
            "high": current_high,
            "low": current_low,
            "moving_average": moving_average,
            "volume": current_volume,
            "average_volume": average_volume,
            "previous_price": previous_price,
            "momentum": momentum,
        }

    def get_historical_candles(
        self,
        symbol,
        start_time=None,
        end_time=None,
        limit=1000,
    ):
        """Retrieve historical candles in chronological order.

        When start_time is supplied, fetch consecutive batches backwards
        from end_time until the requested start is reached or the API
        returns no further data.
        """

        symbol = self._normalize_symbol(symbol)

        if limit <= 0:
            raise ValueError(
                "Candle limit must be greater than zero."
            )

        if limit > 1000:
            raise ValueError(
                "Candle limit cannot be greater than 1000."
            )

        params = {
            "symbol": symbol,
            "productType": "USDT-FUTURES",
            "granularity": self.granularity,
            "limit": limit,
        }

        if start_time is not None:
            start_time = int(start_time)
            params["startTime"] = start_time

        if end_time is not None:
            end_time = int(end_time)
            params["endTime"] = end_time

        all_candles = {}
        current_end_time = end_time

        while True:
            if current_end_time is not None:
                params["endTime"] = current_end_time

            batch = self._request_candles(symbol, params)

            valid_batch = [
                candle
                for candle in batch
                if len(candle) >= 5
            ]

            if not valid_batch:
                break

            for candle in valid_batch:
                timestamp = int(candle[0])

                if start_time is not None and timestamp < start_time:
                    continue

                if end_time is not None and timestamp > end_time:
                    continue

                all_candles[timestamp] = candle

            if start_time is None:
                break

            oldest_timestamp = min(
                int(candle[0])
                for candle in valid_batch
            )

            if oldest_timestamp <= start_time:
                break

            if len(valid_batch) < limit:
                break

            next_end_time = oldest_timestamp - 1

            if (
                current_end_time is not None
                and next_end_time >= current_end_time
            ):
                break

            current_end_time = next_end_time

        return [
            all_candles[timestamp]
            for timestamp in sorted(all_candles)
        ]
