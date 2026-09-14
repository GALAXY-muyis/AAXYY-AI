import requests


class BitgetMarketUniverse:
    """Discover eligible Bitget USDT perpetual futures markets."""

    BASE_URL = "https://api.bitget.com"
    ENDPOINT = "/api/v2/mix/market/contracts"

    def __init__(self, max_symbols=250):
        self.max_symbols = max_symbols

    def get_symbols(self):
        """Return eligible USDT perpetual futures symbols."""

        params = {
            "productType": "USDT-FUTURES",
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

        contracts = payload.get("data", [])

        eligible = []

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

            eligible.append(symbol)

        eligible = sorted(set(eligible))

        return eligible[: self.max_symbols]
