import asyncio
import logging
import time
import tracemalloc

import aiohttp
import fake_useragent

req = 0


async def get_p2p_data(session, asset, payTypes=""):
    global req
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
    }
    data = {
        "asset": asset,
        "fiat": "RUB",
        "merchantCheck": False,
        "page": 1,
        "payTypes": [payTypes],
        "publisherType": None,
        "rows": 5,
        "tradeType": "SELL"
    }

    req += 1

    try:
        async with session.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                                headers=headers, json=data) as response:
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except asyncio.TimeoutError:
        print("Таймаут запроса")


async def get_api_data(session, symbol):
    global req
    req += 1
    async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}") as response:
        data = await response.json()
        if "code" in data:
            return 0
        return data


