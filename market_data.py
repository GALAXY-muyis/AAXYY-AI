import requests


def get_price(coin_id):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data[coin_id]["usd"]
def get_market_data(coin_id, days=1):
    """
    Get market data needed by the AAXYY signal engine.

    Returns:
    - current_price
    - previous_price
    - moving_average
    - current_volume
    - average_volume
    """

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    params = {
        "vs_currency": "usd",
        "days": days,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    prices = data.get("prices", [])
    volumes = data.get("total_volumes", [])

    if len(prices) < 2:
        raise ValueError("Not enough price data returned.")

    if not volumes:
        raise ValueError("No volume data returned.")

    price_values = [
        float(item[1])
        for item in prices
    ]

    volume_values = [
        float(item[1])
        for item in volumes
    ]

    current_price = price_values[-1]
    previous_price = price_values[-2]

    moving_average = (
        sum(price_values) / len(price_values)
    )

    current_volume = volume_values[-1]

    average_volume = (
        sum(volume_values) / len(volume_values)
    )

    return {
        "current_price": current_price,
        "previous_price": previous_price,
        "moving_average": moving_average,
        "current_volume": current_volume,
        "average_volume": average_volume,
    }

if __name__ == "__main__":
    coins = ["bitcoin", "ethereum", "solana"]

    print("AAXYY AI - MARKET DATA")
    print("----------------------")

    for coin in coins:
        try:
            price = get_price(coin)
            print(f"{coin.upper()}: ${price:,.2f}")
        except Exception as error:
            print(f"{coin.upper()}: ERROR - {error}")
