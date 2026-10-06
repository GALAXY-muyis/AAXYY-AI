import time
from datetime import datetime, timezone

from bitget_market_data_provider import BitgetMarketDataProvider
from bitget_market_universe import BitgetMarketUniverse
from market_scanner import MarketScanner
from paper_trade_history import PaperTradeHistory
from paper_trading_executor import PaperPosition, PaperTradingExecutor
from paper_trading_state import PaperTradingState


class PaperTradingRunner:
    def __init__(
        self,
        balance=1000.0,
        max_trades=3,
        max_consecutive_losses=3,
        max_daily_loss_percent=5.0,
    ):
        self.provider = BitgetMarketDataProvider(
            granularity="15m",
            limit=50,
        )

        self.universe = BitgetMarketUniverse(
            provider=self.provider,
        )

        self.scanner = MarketScanner(
            provider=self.provider,
            universe=self.universe,
        )

        self.history = PaperTradeHistory()

        self.state = PaperTradingState(
            balance=balance,
        )

        self.executor = PaperTradingExecutor(
            balance=balance,
            max_trades=max_trades,
            max_consecutive_losses=max_consecutive_losses,
            max_daily_loss_percent=max_daily_loss_percent,
        )

        self.restored_position = False

    def restore_state(self):
        saved_state = self.state.load()

        if not saved_state:
            return None

        self.executor.balance = saved_state.get(
            "balance",
            self.executor.balance,
        )

        position_data = saved_state.get("position")

        if position_data:
            self.executor.position = PaperPosition(
                symbol=position_data.get("symbol"),
                side=position_data.get("side"),
                entry_price=position_data.get("entry_price"),
                quantity=position_data.get("quantity"),
                stop_loss=position_data.get("stop_loss"),
                take_profit=position_data.get("take_profit"),
            )

            self.executor.position.opened_at = position_data.get(
                "opened_at"
            )

            self.executor.position.decision_snapshot = (
                position_data.get("decision_snapshot")
            )

            self.restored_position = True

            print(
                "RESTORED POSITION:"
                f" {self.executor.position.symbol}"
                f" {self.executor.position.side}"
            )

        return saved_state

    def save_state(self):
        position = self.executor.position

        position_data = None

        if position is not None:
            position_data = {
                "symbol": position.symbol,
                "side": position.side,
                "entry_price": position.entry_price,
                "quantity": position.quantity,
                "stop_loss": position.stop_loss,
                "take_profit": position.take_profit,
                "opened_at": getattr(
                    position,
                    "opened_at",
                    None,
                ),
                "decision_snapshot": getattr(
                    position,
                    "decision_snapshot",
                    None,
                ),
            }

        self.state.save(
            balance=self.executor.balance,
            position=position_data,
        )

    def open_best_paper_trade(self, opportunity):
        if opportunity is None:
            return None

        position = self.executor.open_position(
            symbol=opportunity["symbol"],
            side=opportunity["signal"],
            entry_price=opportunity["entry_price"],
            stop_loss=opportunity["stop_loss"],
            take_profit=opportunity["take_profit"],
            position_size=opportunity["position_size"],
        )

        if position is None:
            return None

        self.executor.position.opened_at = (
            datetime.now(timezone.utc).isoformat()
        )

        self.executor.position.decision_snapshot = opportunity

        self.save_state()

        print(
            "PAPER_TRADE_OPENED:"
            f" {position.symbol}"
            f" {position.side}"
            f" entry={position.entry_price}"
            f" qty={position.quantity}"
            f" sl={position.stop_loss}"
            f" tp={position.take_profit}"
        )

        return position

    def _get_historical_exit(self):
        """Check historical candles for the first SL/TP touch."""

        position = self.executor.position

        if position is None:
            return None

        opened_at = getattr(
            position,
            "opened_at",
            None,
        )

        start_time = None

        if opened_at is not None:
            try:
                normalized_time = opened_at

                if normalized_time.endswith("Z"):
                    normalized_time = (
                        normalized_time[:-1] + "+00:00"
                    )

                opened_datetime = datetime.fromisoformat(
                    normalized_time
                )

                if opened_datetime.tzinfo is None:
                    opened_datetime = opened_datetime.replace(
                        tzinfo=timezone.utc
                    )

                start_time = int(
                    opened_datetime.timestamp() * 1000
                )

                current_time = int(
                    datetime.now(timezone.utc).timestamp() * 1000
                )

                elapsed_time = current_time - start_time

                if elapsed_time < 15 * 60 * 1000:
                    return None

            except (TypeError, ValueError):
                start_time = None

        elif not self.restored_position:
            return None

        end_time = int(
            datetime.now(timezone.utc).timestamp() * 1000
        )

        candles = self.provider.get_historical_candles(
            position.symbol,
            start_time=start_time,
            end_time=end_time,
            limit=1000,
        )

        valid_candles = [
            candle
            for candle in candles
            if len(candle) >= 5
        ]

        if valid_candles:
            earliest_timestamp = int(
                valid_candles[0][0]
            )

            latest_timestamp = int(
                valid_candles[-1][0]
            )

            highest_high = max(
                float(candle[2])
                for candle in valid_candles
            )

            lowest_low = min(
                float(candle[3])
                for candle in valid_candles
            )

            earliest_datetime = datetime.fromtimestamp(
                earliest_timestamp / 1000,
                tz=timezone.utc,
            ).isoformat()

            latest_datetime = datetime.fromtimestamp(
                latest_timestamp / 1000,
                tz=timezone.utc,
            ).isoformat()

            print("HISTORICAL EXIT DIAGNOSTIC:")
            print(
                f"  symbol={position.symbol}"
            )
            print(
                f"  candle_count={len(valid_candles)}"
            )
            print(
                f"  earliest_candle={earliest_datetime}"
            )
            print(
                f"  latest_candle={latest_datetime}"
            )
            print(
                f"  highest_high={highest_high}"
            )
            print(
                f"  lowest_low={lowest_low}"
        )
