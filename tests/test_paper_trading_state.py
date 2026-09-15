from paper_trading_state import PaperTradingState


def test_state_starts_with_default_values(tmp_path):
    state = PaperTradingState(
        tmp_path / "paper_trading_state.json"
    )

    result = state.load()

    assert result == {
        "balance": 1000.0,
        "position": None,
    }


def test_state_saves_and_loads_balance(tmp_path):
    state = PaperTradingState(
        tmp_path / "paper_trading_state.json"
    )

    state.save(
        balance=1050.0,
        position=None,
    )

    result = state.load()

    assert result["balance"] == 1050.0
    assert result["position"] is None


def test_state_saves_and_loads_open_position(tmp_path):
    state = PaperTradingState(
        tmp_path / "paper_trading_state.json"
    )

    position = {
        "symbol": "ETHUSDT",
        "side": "SELL",
        "entry_price": 2518.49,
        "quantity": 0.397,
        "stop_loss": 2568.86,
        "take_profit": 2367.38,
    }

    state.save(
        balance=1000.0,
        position=position,
    )

    result = state.load()

    assert result["balance"] == 1000.0
    assert result["position"] == position


def test_state_rejects_invalid_saved_data(tmp_path):
    state = PaperTradingState(
        tmp_path / "paper_trading_state.json"
    )

    state.file_path.write_text(
        "[]",
        encoding="utf-8",
    )

    try:
        state.load()
        assert False
    except ValueError:
        assert True
