
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from market_data import get_price


def test_bitcoin_price_is_positive():
    price = get_price("bitcoin")
    assert price > 0
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from market_data import get_price, get_market_data


def test_bitcoin_price_is_positive():
    price = get_price("bitcoin")
    assert price > 0


def test_get_market_data():
    market_data = get_market_data("bitcoin")

    assert market_data["current_price"] > 0
    assert market_data["previous_price"] > 0
    assert market_data["moving_average"] > 0
    assert market_data["current_volume"] > 0
    assert market_data["average_volume"] > 0


def test_get_market_data_has_required_fields():
    market_data = get_market_data("bitcoin")

    required_fields = {
        "current_price",
        "previous_price",
        "moving_average",
        "current_volume",
        "average_volume",
    }

    assert required_fields.issubset(market_data.keys())
