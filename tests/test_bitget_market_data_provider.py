from bitget_market_data_provider import BitgetMarketDataProvider


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "code": "00000",
            "data": self.data,
        }


def test_bitget_provider_returns_market_data(monkeypatch):
    candles = [
        ["2000", "110", "112", "108", "110", "2000", "220000"],
        ["1000", "105", "111", "104", "108", "1500", "162000"],
        ["0", "100", "106", "99", "105", "1000", "105000"],
    ]

    def fake_get(*args, **kwargs):
        return FakeResponse(candles)

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


def test_get_historical_candles_returns_chronological_order(
    monkeypatch,
):
    candles = [
        ["3000", "120", "125", "115", "122", "3000", "366000"],
        ["1000", "100", "110", "95", "105", "1000", "105000"],
        ["2000", "105", "120", "100", "115", "2000", "230000"],
    ]

    captured = {}

    def fake_get(url, params, timeout):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return FakeResponse(candles)

    monkeypatch.setattr(
        "bitget_market_data_provider.requests.get",
        fake_get,
    )

    provider = BitgetMarketDataProvider(
        granularity="15m",
        limit=50,
    )

    result = provider.get_historical_candles(
        "BTC",
        start_time=1000,
        end_time=3000,
        limit=3,
    )

    assert [int(candle[0]) for candle in result] == [
        1000,
        2000,
        3000,
    ]

    assert captured["params"]["symbol"] == "BTCUSDT"
    assert captured["params"]["productType"] == "USDT-FUTURES"
    assert captured["params"]["granularity"] == "15m"
    assert captured["params"]["limit"] == 3
    assert captured["params"]["startTime"] == 1000
    assert captured["params"]["endTime"] == 3000
    assert captured["timeout"] == 10


def test_get_historical_candles_returns_empty_list_when_no_data(
    monkeypatch,
):
    def fake_get(*args, **kwargs):
        return FakeResponse([])

    monkeypatch.setattr(
        "bitget_market_data_provider.requests.get",
        fake_get,
    )

    provider = BitgetMarketDataProvider()

    result = provider.get_historical_candles("BTC")

    assert result == []


def test_get_historical_candles_rejects_invalid_limit():
    provider = BitgetMarketDataProvider()

    try:
        provider.get_historical_candles("BTC", limit=0)
    except ValueError as error:
        assert str(error) == "Candle limit must be greater than zero."
    else:
        raise AssertionError("Expected ValueError for zero candle limit.")


def test_get_historical_candles_rejects_limit_over_1000():
    provider = BitgetMarketDataProvider()

    try:
        provider.get_historical_candles("BTC", limit=1001)
    except ValueError as error:
        assert str(error) == "Candle limit cannot be greater than 1000."
    else:
        raise AssertionError(
            "Expected ValueError for candle limit over 1000."
        )
