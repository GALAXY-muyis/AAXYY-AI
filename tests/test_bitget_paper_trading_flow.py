from bitget_market_data_provider import BitgetMarketDataProvider
from market_scanner import MarketScanner
from paper_trading_executor import PaperTradingExecutor


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "code": "00000",
            "data": [
                ["3000", "110", "112", "108", "110", "2000", "220000"],
                ["2000", "105", "111", "104", "108", "1500", "162000"],
                ["1000", "100", "106", "99", "105", "1000", "105000"],
            ],
        }


def test_bitget_data_can_reach_paper_trading(monkeypatch):
    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "bitget_market_data_provider.requests.get",
        fake_get,
    )

    provider = BitgetMarketDataProvider(
        granularity="15m",
        limit=3,
    )

    scanner = MarketScanner(provider)

    markets = scanner.scan(["BTC"])
    analyzed = scanner.analyze_markets(markets)
    pipeline_results = scanner.run_pipeline(analyzed)

    assert len(pipeline_results) == 1

    result = pipeline_results[0]

    assert result["symbol"] == "BTCUSDT"
    assert result["signal"] == "BUY"
    assert result["confidence"] == 90
    assert result["final_decision"] == "STRONG BUY"

    executor = PaperTradingExecutor(
        starting_balance=1000
    )

    trade = executor.open_position(
        symbol=result["symbol"],
        side=result["signal"],
        entry_price=result["price"],
        quantity=result["position_size"],
        stop_loss=result["targets"]["stop_loss"],
        take_profit=result["targets"]["take_profit"],
    )

    assert trade["status"] == "OPENED"
    assert executor.position is not None
    assert executor.position.symbol == "BTCUSDT"
    assert executor.position.side == "BUY"
