import time

from bitget_market_data_provider import BitgetMarketDataProvider
from bitget_market_universe import BitgetMarketUniverse
from market_scanner import MarketScanner
from paper_trading_executor import PaperTradingExecutor


class PaperTradingRunner:
    """Run AAXYY AI using real market data in paper-trading mode."""

    def __init__(
        self,
        symbols=None,
        starting_balance=1000,
        sleep_function=time.sleep,
    ):
        self.sleep_function = sleep_function

        self.provider = BitgetMarketDataProvider(
            granularity="15m",
            limit=50,
        )

        self.scanner = MarketScanner(self.provider)

        self.executor = PaperTradingExecutor(
            starting_balance=starting_balance,
        )

        if symbols is None:
            universe = BitgetMarketUniverse(
                max_symbols=250,
            )

            self.symbols = universe.get_symbols()
        else:
            self.symbols = symbols

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

        opportunities = self.scanner.scan_opportunities(
            self.symbols
        )

        opportunity = self.scanner.select_best_opportunity(
            opportunities
        )

        if opportunity is None:
            top_candidates = []

            for candidate in opportunities[:5]:
                top_candidates.append(
                    {
                        "symbol": candidate.get("symbol"),
                        "signal": candidate.get("signal"),
                        "confidence": candidate.get("confidence"),
                        "trade_quality": candidate.get(
                            "trade_quality"
                        ),
                        "risk_reward": candidate.get(
                            "risk_reward"
                        ),
                        "scan_score": candidate.get(
                            "scan_score"
                        ),
                        "valid": candidate.get("valid"),
                        "final_decision": candidate.get(
                            "final_decision"
                        ),
                    }
                )

            return {
                "status": "NO_TRADE",
                "reason": "NO_VALID_OPPORTUNITY",
                "diagnostic": {
                    "markets_scanned": len(self.symbols),
                    "opportunities_found": len(opportunities),
                    "top_candidates": top_candidates,
                },
            }

        if opportunity["final_decision"] not in (
            "STRONG BUY",
            "STRONG SELL",
        ):
            return {
                "status": "NO_TRADE",
                "reason": opportunity["final_decision"],
                "diagnostic": {
                    "markets_scanned": len(self.symbols),
                    "opportunities_found": len(opportunities),
                    "top_candidates": [
                        {
                            "symbol": opportunity.get("symbol"),
                            "signal": opportunity.get("signal"),
                            "confidence": opportunity.get(
                                "confidence"
                            ),
                            "trade_quality": opportunity.get(
                                "trade_quality"
                            ),
                            "risk_reward": opportunity.get(
                                "risk_reward"
                            ),
                            "scan_score": opportunity.get(
                                "scan_score"
                            ),
                            "valid": opportunity.get("valid"),
                            "final_decision": opportunity.get(
                                "final_decision"
                            ),
                        }
                    ],
                },
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

    def monitor_until_exit(
        self,
        max_checks=5,
        interval_seconds=60,
    ):
        """Monitor an open paper position for a limited number of checks."""

        if max_checks <= 0:
            raise ValueError("max_checks must be greater than zero.")

        if interval_seconds < 0:
            raise ValueError(
                "interval_seconds cannot be negative."
            )

        if self.executor.position is None:
            return {
                "status": "NO_POSITION",
                "reason": "NO_OPEN_POSITION",
            }

        last_status = None

        for check_number in range(max_checks):
            last_status = self.monitor_open_position()

            if last_status["status"] == "PAPER_TRADE_CLOSED":
                return last_status

            if check_number < max_checks - 1:
                self.sleep_function(interval_seconds)

        return {
            "status": "MONITORING_LIMIT_REACHED",
            "last_status": last_status,
        }
