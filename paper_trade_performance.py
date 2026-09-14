class PaperTradePerformance:
    """Calculate performance statistics from completed paper trades."""

    def __init__(self, trades=None):
        self.trades = list(trades or [])

    def total_trades(self):
        return len(self.trades)

    def winning_trades(self):
        return sum(
            1
            for trade in self.trades
            if trade.get("pnl", 0) > 0
        )

    def losing_trades(self):
        return sum(
            1
            for trade in self.trades
            if trade.get("pnl", 0) < 0
        )

    def breakeven_trades(self):
        return sum(
            1
            for trade in self.trades
            if trade.get("pnl", 0) == 0
        )

    def win_rate(self):
        if not self.trades:
            return 0.0

        return (
            self.winning_trades()
            / self.total_trades()
            * 100
        )

    def total_pnl(self):
        return sum(
            trade.get("pnl", 0)
            for trade in self.trades
        )

    def average_pnl(self):
        if not self.trades:
            return 0.0

        return self.total_pnl() / self.total_trades()

    def best_trade(self):
        if not self.trades:
            return None

        return max(
            self.trades,
            key=lambda trade: trade.get("pnl", 0),
        )

    def worst_trade(self):
        if not self.trades:
            return None

        return min(
            self.trades,
            key=lambda trade: trade.get("pnl", 0),
        )

    def profit_factor(self):
        gross_profit = sum(
            trade.get("pnl", 0)
            for trade in self.trades
            if trade.get("pnl", 0) > 0
        )

        gross_loss = abs(
            sum(
                trade.get("pnl", 0)
                for trade in self.trades
                if trade.get("pnl", 0) < 0
            )
        )

        if gross_loss == 0:
            if gross_profit > 0:
                return float("inf")

            return 0.0

        return gross_profit / gross_loss

    def summary(self):
        """Return all performance statistics."""

        return {
            "total_trades": self.total_trades(),
            "winning_trades": self.winning_trades(),
            "losing_trades": self.losing_trades(),
            "breakeven_trades": self.breakeven_trades(),
            "win_rate": self.win_rate(),
            "total_pnl": self.total_pnl(),
            "average_pnl": self.average_pnl(),
            "profit_factor": self.profit_factor(),
            "best_trade": self.best_trade(),
            "worst_trade": self.worst_trade(),
      }
