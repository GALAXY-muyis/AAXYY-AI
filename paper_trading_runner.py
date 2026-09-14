from bitget_market_data_provider import BitgetMarketDataProvider
from market_scanner import MarketScanner
from paper_trading_executor import PaperTradingExecutor


class PaperTradingRunner:
    """Run AAXYY AI using real market data in paper-trading mode."""

    def __init__(
        self,
        symbols,
        starting_balance=1000,
    ):
        self.symbols = symbols

        self.provider = BitgetMarketDataProvider(
            granularity="15m",
            limit=50,
        )

        self.scanner = MarketScanner(self.provider)

        self.executor = PaperTradingExecutor(
            starting_balance=starting_balance,
        )

    def find_best_opportunity(self):
        """Scan markets and return the strongest valid opportunity."""

        opportunities = self.scanner.scan_opportunities(
            self.symbols
        )

        return self.scanner.select_best_opportunity(
            opportunities
        )

    def open_best_paper_trade(self):
        """Open the best valid opportunity as a paper trade."""

        opportunity = self.find_best_opportunity()

        if opportunity is None:
            return {
                "status": "NO_TRADE",
                "reason": "NO_VALID_OPPORTUNITY",
            }

        if opportunity["final_decision"] not in (
            "STRONG BUY",
            "STRONG SELL",
        ):
            return {
                "status": "NO_TRADE",
                "reason": opportunity["final_decision"],
            }

        trade = self.executor.open_position(
            symbol=opportunity["symbol"],
            side=opportunity["signal"],
            entry_price=opportunity["price"],
            quantity=opportunity["position_size"],
            stop_loss=opportunity["targets"]["stop_loss"],
            take_profit=opportunity["targets"]["take_profit"],
        )

        return {
            "status": "PAPER_TRADE_OPENED",
            "trade": trade,
            "opportunity": opportunity,
        }

    def monitor_open_position(self):
        """Check the open paper position against the latest market price."""

        if self.executor.position is None:
            return {
                "status": "NO_POSITION",
                "reason": "NO_OPEN_POSITION",
            }

        symbol = self.executor.position.symbol

        market_data = self.provider.get_market_data(symbol)

        current_price = market_data["price"]

        exit_result = self.executor.check_exit(current_price)

        if exit_result is not None:
            return {
                "status": "PAPER_TRADE_CLOSED",
                "exit": exit_result,
            }

        return {
            "status": "POSITION_OPEN",
            "symbol": symbol,
            "current_price": current_price,
            "pnl": self.executor.calculate_pnl(current_price),
        }
