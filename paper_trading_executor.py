"""
AAXYY AI - Paper Trading Executor

Safe paper-trading execution layer.
This module simulates trade execution without sending real orders
to an exchange.

It supports:
- Opening paper positions
- Closing paper positions
- Stop-loss and take-profit checks
- Position sizing
- Realized and unrealized PnL
- Trade history
- Account balance tracking
"""

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict


@dataclass
class PaperPosition:
    symbol: str
    side: str
    entry_price: float
    quantity: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class PaperTradingExecutor:
    """Simulates trade execution without using real exchange funds."""

    def __init__(self, starting_balance: float = 1000.0):
        if starting_balance <= 0:
            raise ValueError("Starting balance must be greater than zero.")

        self.starting_balance = float(starting_balance)
        self.balance = float(starting_balance)

        self.position: Optional[PaperPosition] = None
        self.trade_history: List[Dict] = []

        self.realized_pnl = 0.0

    def calculate_quantity(
        self,
        entry_price: float,
        stop_loss: float,
        risk_percent: float = 1.0,
    ) -> float:
        """Calculate position quantity using percentage risk."""

        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if stop_loss <= 0:
            raise ValueError("Stop-loss price must be greater than zero.")

        if risk_percent <= 0:
            raise ValueError("Risk percentage must be greater than zero.")

        risk_amount = self.balance * (risk_percent / 100)

        price_distance = abs(entry_price - stop_loss)

        if price_distance == 0:
            raise ValueError("Entry price and stop-loss cannot be equal.")

        quantity = risk_amount / price_distance

        return quantity

    def open_position(
        self,
        symbol: str,
        side: str,
        entry_price: float,
        quantity: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ) -> Dict:
        """Open a paper position."""

        side = side.upper()

        if side not in ("BUY", "SELL"):
            raise ValueError("Side must be BUY or SELL.")

        if self.position is not None:
            raise ValueError("A paper position is already open.")

        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        self.position = PaperPosition(
            symbol=symbol.upper(),
            side=side,
            entry_price=float(entry_price),
            quantity=float(quantity),
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

        return {
            "status": "OPENED",
            "symbol": self.position.symbol,
            "side": self.position.side,
            "entry_price": self.position.entry_price,
            "quantity": self.position.quantity,
            "stop_loss": self.position.stop_loss,
            "take_profit": self.position.take_profit,
        }

    def calculate_pnl(self, current_price: float) -> float:
        """Calculate unrealized PnL for the current position."""

        if self.position is None:
            return 0.0

        if current_price <= 0:
            raise ValueError("Current price must be greater than zero.")

        price_change = current_price - self.position.entry_price

        if self.position.side == "SELL":
            price_change = -price_change

        return price_change * self.position.quantity

    def close_position(
        self,
        exit_price: float,
        reason: str = "MANUAL",
    ) -> Dict:
        """Close the current paper position."""

        if self.position is None:
            raise ValueError("No open paper position.")

        if exit_price <= 0:
            raise ValueError("Exit price must be greater than zero.")

        pnl = self.calculate_pnl(exit_price)

        self.balance += pnl
        self.realized_pnl += pnl

        trade = {
            "symbol": self.position.symbol,
            "side": self.position.side,
            "entry_price": self.position.entry_price,
            "exit_price": float(exit_price),
            "quantity": self.position.quantity,
            "pnl": pnl,
            "reason": reason,
            "balance_after": self.balance,
        }

        self.trade_history.append(trade)

        self.position = None

        return trade

    def check_exit(self, current_price: float) -> Optional[Dict]:
        """Check whether stop-loss or take-profit has been reached."""

        if self.position is None:
            return None

        if current_price <= 0:
            raise ValueError("Current price must be greater than zero.")

        side = self.position.side

        stop_loss = self.position.stop_loss
        take_profit = self.position.take_profit

        if side == "BUY":
            if stop_loss is not None and current_price <= stop_loss:
                return self.close_position(
                    current_price,
                    reason="STOP_LOSS",
                )

            if take_profit is not None and current_price >= take_profit:
                return self.close_position(
                    current_price,
                    reason="TAKE_PROFIT",
                )

        elif side == "SELL":
            if stop_loss is not None and current_price >= stop_loss:
                return self.close_position(
                    current_price,
                    reason="STOP_LOSS",
                )

            if take_profit is not None and current_price <= take_profit:
                return self.close_position(
                    current_price,
                    reason="TAKE_PROFIT",
                )

        return None

    def get_status(self, current_price: Optional[float] = None) -> Dict:
        """Return the current paper-trading account status."""

        unrealized_pnl = 0.0

        if current_price is not None and self.position is not None:
            unrealized_pnl = self.calculate_pnl(current_price)

        return {
            "starting_balance": self.starting_balance,
            "balance": self.balance,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": unrealized_pnl,
            "total_pnl": self.realized_pnl + unrealized_pnl,
            "position_open": self.position is not None,
            "position": (
                asdict(self.position)
                if self.position is not None
                else None
            ),
            "total_trades": len(self.trade_history),
        }

    def get_trade_history(self) -> List[Dict]:
        """Return all completed paper trades."""

        return list(self.trade_history)
