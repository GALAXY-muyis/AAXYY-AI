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
