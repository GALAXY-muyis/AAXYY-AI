import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import market_data
from market_data import get_price, get_market_data


def test_bitcoin_price_is_positive():
    price = get_price("bitcoin")
    assert price > 0


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "prices": [
                [1, 100.0],
                [2, 105.0],
                [3, 110.0],
            ],
            "total_volumes": [
                [1, 1000.0],
                [2, 1200.0],
                [3, 1500.0],
            ],
        }


def fake_get(*args, **kwargs):
    return FakeResponse()


def test_get_market_data(monkeypatch):
    monkeypatch.setattr(
        market_data.requests,
        "get",
        fake_get,
    )

    data = get_market_data("bitcoin")

    assert data["current_price"] == 110.0
    assert data["previous_price"] == 105.0
    assert data["moving_average"] == 105.0
    assert data["current_volume"] == 1500.0
    assert data["average_volume"] == 1233.3333333333333


def test_get_market_data_has_required_fields(monkeypatch):
    monkeypatch.setattr(
        market_data.requests,
        "get",
        fake_get,
    )

    data = get_market_data("bitcoin")

    required_fields = {
        "current_price",
        "previous_price",
        "moving_average",
        "current_volume",
        "average_volume",
    }

    assert required_fields.issubset(data.keys())
