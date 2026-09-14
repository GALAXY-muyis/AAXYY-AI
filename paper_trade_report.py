from paper_trade_history import PaperTradeHistory
from paper_trade_performance import PaperTradePerformance


class PaperTradeReport:
    """Generate a readable performance report from paper trades."""

    def __init__(self, history=None):
        self.history = history or PaperTradeHistory()

    def generate(self):
        """Generate performance statistics from saved paper trades."""

        trades = self.history.load()

        performance = PaperTradePerformance(trades)

        return performance.summary()

    def format_report(self):
        """Return a human-readable AAXYY paper-trading report."""

        report = self.generate()

        return (
            "AAXYY PAPER TRADING PERFORMANCE\n"
            "--------------------------------\n"
            f"Total Trades: {report['total_trades']}\n"
            f"Winning Trades: {report['winning_trades']}\n"
            f"Losing Trades: {report['losing_trades']}\n"
            f"Breakeven Trades: {report['breakeven_trades']}\n"
            f"Win Rate: {report['win_rate']:.2f}%\n"
            f"Total PnL: {report['total_pnl']:.2f}\n"
            f"Average PnL: {report['average_pnl']:.2f}\n"
            f"Profit Factor: {report['profit_factor']}\n"
  )
