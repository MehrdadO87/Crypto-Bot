import os
import time
import requests

COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY")


BASE_URL = "https://api.coingecko.com/api/v3"

HEADERS = {"x-cg-demo-api-key": COINGECKO_API_KEY}

CACHE_TTL = 60

cache = {}

def _get_cached(key):
    if key not in cache:
        return None

    data, timestamp = cache[key]

    if time.time() - timestamp < CACHE_TTL:
        return data

    del cache[key]
    return None


def _set_cache(key, data):
    cache[key] = (data, time.time())

def get_top_5_prices():
    cache_key = "top_5"
    cached_data = _get_cached(cache_key)

    if cached_data is not None:
        return cached_data

    coin_ids = "bitcoin,ethereum,binancecoin,solana,ripple"
    params = {
        "vs_currency": "usd",
        "ids": coin_ids,
        "price_change_percentage": "24h,7d,30d,1y"}

    try:
        response = requests.get(
            f"{BASE_URL}/coins/markets",params=params,headers=HEADERS,timeout=10)

        if response.status_code == 429:
            return {"error": "rate_limit"}

        response.raise_for_status()
        data = response.json()
        _set_cache(cache_key, data)
        return data

    except requests.exceptions.Timeout:
        return {"error": "timeout"}

    except requests.exceptions.RequestException:
        return {"error": "network"}


def search_coin(query):
    cache_key = f"search:{query.lower()}"

    cached_data = _get_cached(cache_key)

    if cached_data is not None:
        return cached_data

    params = {"query": query}
    try:
        response = requests.get(
            f"{BASE_URL}/search",params=params,headers=HEADERS,timeout=10)

        if response.status_code == 429:
            return {"error": "rate_limit"}

        response.raise_for_status()

        data = response.json()
        _set_cache(cache_key, data)
        return data

    except requests.exceptions.Timeout:
        return {"error": "timeout"}

    except requests.exceptions.RequestException:
        return {"error": "network"}


def get_coin_data(coin_id):
    cache_key = f"coin:{coin_id}"

    cached_data = _get_cached(cache_key)

    if cached_data is not None:
        return cached_data

    params = {"vs_currency": "usd","ids": coin_id,"price_change_percentage": "24h,7d,30d,1y"}
    try:
        response = requests.get(
            f"{BASE_URL}/coins/markets",params=params,headers=HEADERS,timeout=10)

        if response.status_code == 429:
            return {"error": "rate_limit"}
        
        response.raise_for_status()
        data = response.json()

        if not data:
            return None

        coin = data[0]
        _set_cache(cache_key, coin)
        return coin

    except requests.exceptions.Timeout:
        return {"error": "timeout"}

    except requests.exceptions.RequestException:
        return {"error": "network"}