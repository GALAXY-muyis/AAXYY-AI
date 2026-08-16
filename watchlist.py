DEFAULT_WATCHLIST = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "XRP/USDT",
    "SUI/USDT",
    "TAO/USDT",
    "RENDER/USDT",
    "FET/USDT",
    "ONDO/USDT",
    "SEI/USDT",
    "ARB/USDT",
    "ZEC/USDT",
]


class Watchlist:
    """Manage the markets AAXYY AI is allowed to scan."""

    def __init__(self, symbols=None):
        self.symbols = list(
            symbols if symbols is not None else DEFAULT_WATCHLIST
        )

    def add(self, symbol):
        """Add a market to the watchlist."""

        if symbol not in self.symbols:
            self.symbols.append(symbol)

    def remove(self, symbol):
        """Remove a market from the watchlist."""

        if symbol in self.symbols:
            self.symbols.remove(symbol)

    def contains(self, symbol):
        """Check whether a market is on the watchlist."""

        return symbol in self.symbols

    def get_symbols(self):
        """Return the current watchlist."""

        return list(self.symbols)
