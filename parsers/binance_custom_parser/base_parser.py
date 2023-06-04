import asyncio
import tracemalloc

import aiohttp
import fake_useragent


async def get_p2p_data(asset, fiat, method, payTypes=None):
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
    }
    data = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "payTypes": [payTypes],
        "publisherType": None,
        "rows": 5,
        "tradeType": method
    }

    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                                    headers=headers, json=data) as response:
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Ошибка при выполнении запроса: {e}")
        except asyncio.TimeoutError:
            print("Таймаут запроса")


async def get_api_data(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}") as response:
            data = await response.json()
            if "code" in data:
                return 0
            return data


async def calculate_gains(p2p_sell, spot_price, p2p_buy):
    p2p_sell = float(p2p_sell)
    spot_price = float(spot_price)
    p2p_buy = float(p2p_buy)
    return round(((((100 / p2p_buy) / spot_price) * p2p_sell) / 100 - 1) * 100, 2)


async def main():
    tracemalloc.start()


if __name__ == '__main__':
    asyncio.run(main())
