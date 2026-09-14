import requests


class BitgetMarketUniverse:
    """Discover liquid Bitget USDT perpetual futures markets."""

    BASE_URL = "https://api.bitget.com"
    CONTRACTS_ENDPOINT = "/api/v2/mix/market/contracts"
    TICKERS_ENDPOINT = "/api/v3/market/tickers"

    def __init__(
        self,
        max_symbols=250,
        minimum_quote_volume=5_000_000,
    ):
        self.max_symbols = max_symbols
        self.minimum_quote_volume = minimum_quote_volume

    def get_symbols(self):
        """Return the most liquid eligible USDT perpetual markets."""

        contracts_response = requests.get(
            f"{self.BASE_URL}{self.CONTRACTS_ENDPOINT}",
            params={
                "productType": "USDT-FUTURES",
            },
            timeout=10,
        )

        contracts_response.raise_for_status()

        contracts_payload = contracts_response.json()

        if contracts_payload.get("code") != "00000":
            raise ValueError(
                "Bitget API error: "
                f"{contracts_payload.get('msg', 'Unknown error')}"
            )

        contracts = contracts_payload.get("data", [])

        eligible_symbols = set()

        for contract in contracts:
            symbol = contract.get("symbol")
            symbol_type = contract.get("symbolType")
            symbol_status = contract.get("symbolStatus")

            if not symbol:
                continue

            if symbol_type != "perpetual":
                continue

            if symbol_status != "normal":
                continue

            if not symbol.endswith("USDT"):
                continue

            eligible_symbols.add(symbol)

        if not eligible_symbols:
            raise ValueError(
                "Bitget returned no eligible USDT perpetual markets."
            )

        ticker_response = requests.get(
            f"{self.BASE_URL}{self.TICKERS_ENDPOINT}",
            params={
                "category": "USDT-FUTURES",
            },
            timeout=10,
        )

        ticker_response.raise_for_status()

        ticker_payload = ticker_response.json()

        if ticker_payload.get("code") != "00000":
            raise ValueError(
                "Bitget API error: "
                f"{ticker_payload.get('msg', 'Unknown error')}"
            )

        tickers = ticker_payload.get("data", [])

        ranked_symbols = []

        for ticker in tickers:
            symbol = ticker.get("symbol")

            if symbol not in eligible_symbols:
                continue

            try:
                quote_volume = float(
                    ticker.get("quoteVolume", 0)
                )
            except (TypeError, ValueError):
                quote_volume = 0.0

            if quote_volume < self.minimum_quote_volume:
                continue

            ranked_symbols.append(
                (symbol, quote_volume)
            )

        ranked_symbols.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            symbol
            for symbol, _ in ranked_symbols[: self.max_symbols]
        ]
