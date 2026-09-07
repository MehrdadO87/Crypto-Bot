import requests


BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_price():
    coin_ids = ["bitcoin","ethereum","binancecoin","solana","ripple"]
    params = {
        "ids": ",".join(coin_ids),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data

