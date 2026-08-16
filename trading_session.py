from datetime import date


class TradingSession:
    """Track AAXYY AI trading activity and safety limits."""

    def __init__(self, max_trades=3, max_consecutive_losses=3):
        self.max_trades = max_trades
        self.max_consecutive_losses = max_consecutive_losses

        self.trades_today = 0
        self.consecutive_losses = 0
        self.session_date = date.today()

    def _reset_if_new_day(self):
        """Reset daily counters when a new day begins."""

        today = date.today()

        if today != self.session_date:
            self.trades_today = 0
            self.consecutive_losses = 0
            self.session_date = today

    def can_trade(self):
        """Return whether another trade is allowed."""

        self._reset_if_new_day()

        if self.trades_today >= self.max_trades:
            return False

        if self.consecutive_losses >= self.max_consecutive_losses:
            return False

        return True

    def record_trade(self, result):
        """Record a completed trade result."""

        self._reset_if_new_day()

        self.trades_today += 1

        if result.upper() == "LOSS":
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    def get_status(self):
        """Return the current trading-session status."""

        self._reset_if_new_day()

        return {
            "trades_today": self.trades_today,
            "consecutive_losses": self.consecutive_losses,
            "can_trade": self.can_trade(),
          }
