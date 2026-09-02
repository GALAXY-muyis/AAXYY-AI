from market_scanner import MarketScanner


def test_rank_markets_puts_strongest_first():
    scanner = MarketScanner(None)

    markets = [
        {
            "symbol": "ETH",
            "confidence": 75,
            "trade_quality": "GOOD",
            "risk_reward": 2,
            "market_regime": "BULLISH",
            "conflict_status": "ALIGNED",
        },
        {
            "symbol": "BTC",
            "confidence": 90,
            "trade_quality": "STRONG",
            "risk_reward": 3,
            "market_regime": "BULLISH",
            "conflict_status": "ALIGNED",
        },
        {
            "symbol": "SOL",
            "confidence": 50,
            "trade_quality": "MODERATE",
            "risk_reward": 2,
            "market_regime": "BULLISH",
            "conflict_status": "ALIGNED",
        },
    ]

    result = scanner.rank_markets(markets)

    assert result[0]["symbol"] == "BTC"
    assert result[1]["symbol"] == "ETH"
    assert result[2]["symbol"] == "SOL"


def test_rank_markets_adds_scan_score():
    scanner = MarketScanner(None)

    markets = [
        {
            "symbol": "BTC",
            "confidence": 90,
            "trade_quality": "STRONG",
            "risk_reward": 3,
            "market_regime": "BULLISH",
            "conflict_status": "ALIGNED",
        }
    ]

    result = scanner.rank_markets(markets)

    assert result[0]["scan_score"] == 100
