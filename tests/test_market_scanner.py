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
                "price": 90,
                "moving_average": 100,
                "volume": 500,
                "average_volume": 1000,
            },
        }

        return markets[symbol]


def test_market_scanner_returns_valid_markets():
    scanner = MarketScanner(FakeDataProvider())

    result = scanner.scan(["BTC"])

    assert len(result) == 1
    assert result[0]["symbol"] == "BTC"


def test_market_scanner_scans_multiple_symbols():
    scanner = MarketScanner(FakeDataProvider())

    result = scanner.scan(["BTC", "ETH"])

    assert len(result) == 2
    assert result[0]["symbol"] == "BTC"
    assert result[1]["symbol"] == "ETH"
def test_selects_highest_ranked_valid_opportunity():
    scanner = MarketScanner(FakeDataProvider())

    opportunities = [
        {
            "symbol": "BTC",
            "scan_score": 95,
            "valid": False,
        },
        {
            "symbol": "ETH",
            "scan_score": 90,
            "valid": True,
        },
        {
            "symbol": "SOL",
            "scan_score": 85,
            "valid": True,
        },
    ]

    result = scanner.select_best_opportunity(opportunities)

    assert result["symbol"] == "ETH"
    assert result["valid"] is True
def test_selects_highest_ranked_valid_opportunity():
    scanner = MarketScanner(FakeDataProvider())

    opportunities = [
        {
            "symbol": "BTC",
            "scan_score": 95,
            "valid": False,
        },
        {
            "symbol": "ETH",
            "scan_score": 90,
            "valid": True,
        },
        {
            "symbol": "SOL",
            "scan_score": 85,
            "valid": True,
        },
    ]

    result = scanner.select_best_opportunity(opportunities)

    assert result["symbol"] == "ETH"
    assert result["valid"] is True
