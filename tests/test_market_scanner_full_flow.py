from market_scanner import MarketScanner


def test_scanner_analysis_and_ranking_work_together():
    scanner = MarketScanner(None)

    markets = [
        {
            "symbol": "ETH",
            "price": 102,
            "moving_average": 100,
            "volume": 1000,
            "average_volume": 1000,
            "previous_price": 100,
        },
        {
            "symbol": "BTC",
            "price": 110,
            "moving_average": 100,
            "volume": 2000,
            "average_volume": 1000,
            "previous_price": 105,
        },
    ]

    analyzed = scanner.analyze_markets(markets)

    for market in analyzed:
        market["trade_quality"] = "STRONG"
        market["risk_reward"] = 3
        market["market_regime"] = "BULLISH"
        market["conflict_status"] = "ALIGNED"

    ranked = scanner.rank_markets(analyzed)

    assert len(ranked) == 2
    assert ranked[0]["symbol"] == "BTC"
    assert ranked[1]["symbol"] == "ETH"
    assert ranked[0]["scan_score"] == 100
def test_scanner_pipeline_flow():
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
def test_scanner_run_pipeline():
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

    analyzed = scanner.analyze_markets(markets)
    result = scanner.run_pipeline(analyzed)

    assert len(result) == 1
    assert result[0]["symbol"] == "BTC"
    assert result[0]["signal"] == "BUY"
    assert "risk_gate" in result[0]
    assert "trading_guard" in result[0]
    assert "final_decision" in result[0]
    analyzed = scanner.analyze_markets(markets)

    assert analyzed[0]["signal"] == "BUY"
    assert analyzed[0]["confidence"] == 90
