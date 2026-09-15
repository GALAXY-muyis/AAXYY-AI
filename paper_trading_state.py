import json
from pathlib import Path


class PaperTradingState:
    """Persist paper-trading state between AAXYY runs."""

    def __init__(self, file_path="paper_trading_state.json"):
        self.file_path = Path(file_path)

    def load(self):
        """Load saved paper-trading state."""

        if not self.file_path.exists():
            return {
                "balance": 1000.0,
                "position": None,
            }

        with self.file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            state = json.load(file)

        if not isinstance(state, dict):
            raise ValueError(
                "Paper trading state must be a dictionary."
            )

        if "balance" not in state:
            raise ValueError(
                "Paper trading state must contain balance."
            )

        if "position" not in state:
            raise ValueError(
                "Paper trading state must contain position."
            )

        return state

    def save(self, balance, position):
        """Save current paper-trading state."""

        state = {
            "balance": float(balance),
            "position": position,
        }

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                state,
                file,
                indent=2,
            )

        return state
