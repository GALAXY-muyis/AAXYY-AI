
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from market_data import get_price


def test_bitcoin_price_is_positive():
    price = get_price("bitcoin")
    assert price > 0
