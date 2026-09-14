from bitget_market_data_provider import BitgetMarketDataProvider
from market_scanner import MarketScanner


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


def test_bitget_provider_connects_to_market_scanner(monkeypatch):
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

    result = scanner.scan(["BTC"])

    assert len(result) == 1
    assert result[0]["symbol"] == "BTCUSDT"
    assert result[0]["price"] == 110.0
    assert result[0]["moving_average"] == 107.66666666666667
