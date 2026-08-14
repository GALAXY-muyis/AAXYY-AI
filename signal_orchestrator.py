from market_scanner import MarketScanner
from aaxyy_pipeline import run_aaxyy_pipeline


class SignalOrchestrator:
    """Coordinate market scanning and AAXYY signal generation."""

    def __init__(self, data_provider):
        self.scanner = MarketScanner(data_provider)

    def generate_signals(
        self,
        symbols,
        account_balance,
        risk_percent,
        risk_reward,
        stop_loss,
    ):
        markets = self.scanner.scan(symbols)

        signals = []

        for market in markets:
            result = run_aaxyy_pipeline(
                price=market["price"],
                moving_average=market["moving_average"],
                volume=market["volume"],
                average_volume=market["average_volume"],
                signal="BUY" if market["price"] > market["moving_average"]
                else "SELL",
                confidence=70,
                risk_reward=risk_reward,
                momentum=market["momentum"],
                account_balance=account_balance,
                risk_percent=risk_percent,
                entry_price=market["price"],
                stop_loss=stop_loss,
            )

            signals.append(
                {
                    "symbol": market["symbol"],
                    "analysis": result,
                }
            )

        return signals
