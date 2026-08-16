class PaperTrader:
    """Simulate AAXYY trades without sending real exchange orders."""

    def __init__(self):
        self.open_trades = []

    def open_trade(self, trade_setup):
        """Open a simulated trade."""

        if not trade_setup.get("approved", False):
            return {
                "opened": False,
                "reason": "TRADE_NOT_APPROVED",
            }

        setup = trade_setup["setup"]

        trade = {
            "signal": setup["signal"],
            "entry_price": setup["entry_price"],
            "stop_loss": setup["stop_loss"],
            "take_profit": setup["take_profit"],
            "position_size": setup["position_size"],
            "risk_reward": setup["risk_reward"],
            "status": "OPEN",
        }

        self.open_trades.append(trade)

        return {
            "opened": True,
            "trade": trade,
        }

    def get_open_trades(self):
        """Return all currently open paper trades."""

        return list(self.open_trades)
