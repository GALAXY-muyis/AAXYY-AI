import pytest

from paper_trade_data import PaperTradeData


def test_empty_dataset():
    data = PaperTradeData()

    assert data.total_trades() == 0
    assert data.symbols() == []
    assert data.pnl_values() == []


def test_dataset_tracks_trades():
    trades = [
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "pnl": 20.0,
        },
        {
            "symbol": "ETHUSDT",
            "side": "SELL",
            "pnl": -10.0,
        },
    ]

    data = PaperTradeData(trades)

    assert data.total_trades() == 2
    assert data.symbols() == [
        "BTCUSDT",
        "ETHUSDT",
    ]
    assert data.pnl_values() == [
        20.0,
        -10.0,
    ]


def test_dataset_separates_winners_and_losers():
    trades = [
        {
            "symbol": "BTCUSDT",
            "pnl": 25.0,
        },
        {
            "symbol": "ETHUSDT",
            "pnl": -5.0,
        },
        {
            "symbol": "SOLUSDT",
            "pnl": 0.0,
        },
    ]

    data = PaperTradeData(trades)

    assert len(data.winning_trades()) == 1
    assert len(data.losing_trades()) == 1


def test_add_trades():
    data = PaperTradeData(
        [
            {
                "symbol": "BTCUSDT",
                "pnl": 10.0,
            }
        ]
    )

    data.add_trades(
        [
            {
                "symbol": "ETHUSDT",
                "pnl": -3.0,
            }
        ]
    )

    assert data.total_trades() == 2
    assert data.pnl_values() == [
        10.0,
        -3.0,
    ]


def test_add_trades_rejects_non_list():
    data = PaperTradeData()

    with pytest.raises(ValueError):
        data.add_trades("invalid")


def test_add_trades_rejects_invalid_trade():
    data = PaperTradeData()

    with pytest.raises(ValueError):
        data.add_trades(
            [
                {
                    "symbol": "BTCUSDT",
                    "pnl": 10.0,
                },
                "invalid",
            ]
        )


def test_summary():
    trades = [
        {
            "symbol": "BTCUSDT",
            "pnl": 15.0,
        },
        {
            "symbol": "ETHUSDT",
            "pnl": -5.0,
        },
    ]

    data = PaperTradeData(trades)

    assert data.summary() == {
        "total_trades": 2,
        "winning_trades": 1,
        "losing_trades": 1,
        "symbols": [
            "BTCUSDT",
            "ETHUSDT",
        ],
        "pnl_values": [
            15.0,
            -5.0,
        ],
          }
