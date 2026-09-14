from bitget_market_data_provider import BitgetMarketDataProvider


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "code": "00000",
            "data": [
                ["2000", "110", "112", "108", "110", "2000", "220000"],
                ["1000", "105", "111", "104", "108", "1500", "162000"],
                ["0", "100", "106", "99", "105", "1000", "105000"],
            ],
        }


def test_bitget_provider_returns_market_data(monkeypatch):
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

    result = provider.get_market_data("BTC")

    assert result["symbol"] == "BTCUSDT"
    assert result["price"] == 110.0
    assert result["previous_price"] == 108.0
    assert result["moving_average"] == 107.66666666666667
    assert result["volume"] == 2000.0
    assert result["average_volume"] == 1500.0
    assert result["momentum"] == 2.0
