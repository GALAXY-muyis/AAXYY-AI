class PerformanceTracker:
    """Track AAXYY AI trading performance."""

    def __init__(self):
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_profit_loss = 0.0

    def record_trade(self, profit_loss):
        """Record the result of a completed trade."""

        self.total_trades += 1
        self.total_profit_loss += profit_loss

        if profit_loss > 0:
            self.winning_trades += 1
        elif profit_loss < 0:
            self.losing_trades += 1

    def get_win_rate(self):
        """Return win rate as a percentage."""

        if self.total_trades == 0:
            return 0.0

        return (
            self.winning_trades
            / self.total_trades
        ) * 100

    def get_average_profit_loss(self):
        """Return average P/L per trade."""

        if self.total_trades == 0:
            return 0.0

        return (
            self.total_profit_loss
            / self.total_trades
        )

    def get_summary(self):
        """Return complete performance summary."""

        return {
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": self.get_win_rate(),
            "total_profit_loss": self.total_profit_loss,
            "average_profit_loss": self.get_average_profit_loss(),
        }
