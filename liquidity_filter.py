def check_liquidity(
    volume,
    average_volume,
    minimum_ratio=1.0,
):
    """
    Check whether a market has sufficient relative volume.

    Returns a dictionary containing the liquidity status
    and volume ratio.
    """

    if average_volume <= 0:
        return {
            "liquid": False,
            "ratio": 0.0,
            "reason": "INVALID_AVERAGE_VOLUME",
        }

    ratio = volume / average_volume

    if ratio < minimum_ratio:
        return {
            "liquid": False,
            "ratio": round(ratio, 2),
            "reason": "LOW_LIQUIDITY",
        }

    return {
        "liquid": True,
        "ratio": round(ratio, 2),
        "reason": "LIQUID_MARKET",
    }


def filter_liquid_markets(markets, minimum_ratio=1.0):
    """
    Return only markets that meet the liquidity requirement.
    """

    liquid_markets = []

    for market in markets:
        result = check_liquidity(
            volume=market["volume"],
            average_volume=market["average_volume"],
            minimum_ratio=minimum_ratio,
        )

        if result["liquid"]:
            market_copy = dict(market)
            market_copy["liquidity"] = result
            liquid_markets.append(market_copy)

    return liquid_markets
