def validate_market_data(
    price,
    moving_average,
    volume,
    average_volume,
):
    """Validate market data before analysis."""

    if price <= 0:
        return {
            "valid": False,
            "reason": "INVALID_PRICE",
        }

    if moving_average <= 0:
        return {
            "valid": False,
            "reason": "INVALID_MOVING_AVERAGE",
        }

    if volume < 0:
        return {
            "valid": False,
            "reason": "INVALID_VOLUME",
        }

    if average_volume <= 0:
        return {
            "valid": False,
            "reason": "INVALID_AVERAGE_VOLUME",
        }

    if volume == 0:
        return {
            "valid": False,
            "reason": "NO_VOLUME",
        }

    return {
        "valid": True,
        "reason": "MARKET_DATA_VALID",
    }
