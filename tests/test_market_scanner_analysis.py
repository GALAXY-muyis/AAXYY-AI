from market_scanner import MarketScanner


def test_scanner_analysis_generates_signal_data():
    scanner = MarketScanner(None)

    markets = [
        {
            "symbol": "BTC",
            "price": 110,
            "moving_average": 100,
            "volume": 2000,
            "average_volume": 1000,
            "previous_price": 105,
        }
    ]

    result = scanner.analyze_markets(markets)

    assert len(result) == 1
    assert result[0]["symbol"] == "BTC"
    assert result[0]["signal"] == "BUY"
    assert result[0]["confidence"] == 90
    assert result[0]["momentum"] == 5
    assert result[0]["volume_status"] == "HIGH"
