class PaperTradeData:
    """Manage completed paper trades for performance analysis."""

    def __init__(self, trades=None):
        self.trades = list(trades or [])

    def add_trades(self, trades):
        """Add completed trades to the dataset."""

        if not isinstance(trades, list):
            raise ValueError("Trades must be a list.")

        for trade in trades:
            if not isinstance(trade, dict):
                raise ValueError("Each trade must be a dictionary.")

        self.trades.extend(trades)

    def total_trades(self):
        """Return the number of completed trades."""

        return len(self.trades)

    def symbols(self):
        """Return unique symbols represented in the dataset."""

        return sorted(
            {
                trade.get("symbol")
                for trade in self.trades
                if trade.get("symbol")
            }
        )

    def pnl_values(self):
        """Return PnL values from completed trades."""

        return [
            trade.get("pnl", 0)
            for trade in self.trades
        ]

    def winning_trades(self):
        """Return completed winning trades."""

        return [
            trade
            for trade in self.trades
            if trade.get("pnl", 0) > 0
        ]

    def losing_trades(self):
        """Return completed losing trades."""

        return [
            trade
            for trade in self.trades
            if trade.get("pnl", 0) < 0
        ]

    def summary(self):
        """Return basic dataset statistics."""

        return {
            "total_trades": self.total_trades(),
            "winning_trades": len(self.winning_trades()),
            "losing_trades": len(self.losing_trades()),
            "symbols": self.symbols(),
            "pnl_values": self.pnl_values(),
        }
