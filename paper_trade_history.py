import json
from pathlib import Path


class PaperTradeHistory:
    """Persist completed AAXYY paper trades locally."""

    def __init__(self, file_path="paper_trade_history.json"):
        self.file_path = Path(file_path)

    def load(self):
        """Load saved paper trades."""

        if not self.file_path.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Paper trade history must contain a list."
            )

        return data

    def save(self, trades):
        """Save paper trades."""

        if not isinstance(trades, list):
            raise ValueError(
                "Paper trade history must be a list."
            )

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                trades,
                file,
                indent=2,
            )

    def append(self, trade):
        """Append one completed paper trade."""

        if not isinstance(trade, dict):
            raise ValueError(
                "Trade must be a dictionary."
            )

        trades = self.load()
        trades.append(trade)
        self.save(trades)

        return trade
