from market_scanner import MarketScanner


class FakeDataProvider:
    def get_market_data(self, symbol):
        markets = {
            "BTC": {
                "symbol": "BTC",
                "price": 110,
                "moving_average": 100,
                "volume": 2000,
                "average_volume": 1000,
            },
            "ETH": {
                "symbol": "ETH",
                "price": 105,
                "moving_average": 100,
                "volume": 1500,
                "average_volume": 1000,
            },
        }

        return markets[symbol]


def test_scanner_can_scan_multiple_markets():
    scanner = MarketScanner(FakeDataProvider())

    result = scanner.scan(["BTC", "ETH"])

    assert len(result) == 2
    assert result[0]["symbol"] == "BTC"
    assert result[1]["symbol"] == "ETH"
