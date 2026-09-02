from market_data_validator import validate_market_data


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
