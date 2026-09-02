from market_data_validator import validate_market_data
from signal_engine import analyze_market
from signal_engine import analyze_market
from aaxyy_pipeline import run_aaxyy_pipeline

def calculate_scan_score(
    confidence,
    trade_quality,
    risk_reward,
    market_regime,
    conflict_status,
):
    """Calculate a score for a trading opportunity."""

    score = 0

    if confidence >= 90:
        score += 40
    elif confidence >= 75:
        score += 30
    elif confidence >= 50:
        score += 20

    if trade_quality == "STRONG":
        score += 30
    elif trade_quality == "GOOD":
        score += 20
    elif trade_quality == "MODERATE":
        score += 10

    if risk_reward >= 3:
        score += 20
    elif risk_reward >= 2:
        score += 10

    if market_regime in ("BULLISH", "BEARISH"):
        score += 10

    if conflict_status == "CONFLICT":
        score -= 30

    return score


class MarketScanner:
    """Scan multiple markets and return valid market data."""

    def __init__(self, data_provider):
        self.data_provider = data_provider

    def scan(self, symbols):
        valid_markets = []

        for symbol in symbols:
            data = self.data_provider.get_market_data(symbol)

            validation = validate_market_data(
                price=data["price"],
                moving_average=data["moving_average"],
                volume=data["volume"],
                average_volume=data["average_volume"],
            )

            if validation["valid"]:
                valid_markets.append(data)

        return valid_markets
    def analyze_markets(self, markets):
        """Analyze validated markets using the signal engine."""

        analyzed_markets = []
    def run_pipeline(self, markets):
        """Run analyzed markets through the AAXYY pipeline."""

        results = []

        for market in markets:
            entry_price = market["price"]

            if market["signal"] == "BUY":
                stop_loss = entry_price * 0.98
            elif market["signal"] == "SELL":
                stop_loss = entry_price * 1.02
            else:
                stop_loss = entry_price

            result = run_aaxyy_pipeline(
                price=market["price"],
                moving_average=market["moving_average"],
                volume=market["volume"],
                average_volume=market["average_volume"],
                signal=market["signal"],
                confidence=market["confidence"],
                risk_reward=3,
                momentum=market["momentum"],
                account_balance=1000,
                risk_percent=2,
                entry_price=entry_price,
                stop_loss=stop_loss,
            )

            combined = dict(market)
            combined.update(result)

            results.append(combined)

        return results
        for market in markets:
            analysis = analyze_market(
                price=market["price"],
                moving_average=market["moving_average"],
                volume=market["volume"],
                average_volume=market["average_volume"],
                previous_price=market["previous_price"],
            )

            result = dict(market)
            result.update(analysis)

            analyzed_markets.append(result)

        return analyzed_markets
    def rank_markets(self, markets):
        """Rank valid markets from strongest to weakest opportunity."""

        ranked_markets = []

        for market in markets:
            score = calculate_scan_score(
                confidence=market["confidence"],
                trade_quality=market["trade_quality"],
                risk_reward=market["risk_reward"],
                market_regime=market["market_regime"],
                conflict_status=market["conflict_status"],
            )

            result = dict(market)
            result["scan_score"] = score

            ranked_markets.append(result)

        ranked_markets.sort(
            key=lambda item: item["scan_score"],
            reverse=True,
        )

        return ranked_markets
