import asyncio
import logging
import time
import tracemalloc

import aiohttp
import fake_useragent

req = 0


async def get_p2p_data(session, asset, fiat, method, payTypes=""):
    global req
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
        "rows": 1,
        "tradeType": method
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


async def calculate_gains(p2p_sell, spot_price, p2p_buy):
    p2p_sell = float(p2p_sell)
    spot_price = float(spot_price)
    p2p_buy = float(p2p_buy)
    return round(((((100 / p2p_buy) / spot_price) * p2p_sell) / 100 - 1) * 100, 2)


def main():
    start_time = time.time()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    tracemalloc.start()
    fiat = "RUB"
    percentage = 0
    payment = "QIWI"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # result = loop.run_until_complete(testing_message(fiat, percentage, payment))
    # print(result)
    current, peak = tracemalloc.get_traced_memory()
    print(f"Текущее потребление памяти: {current / 10 ** 6}MB, Пиковое потребление памяти: {peak / 10 ** 6}MB")
    end_time = time.time()
    execution_time = end_time - start_time
    tracemalloc.stop()
    logging.info(f"Количество запросов: {req}")
    logging.info(f"Время выполнения запросов: {execution_time} секунд")

if __name__ == '__main__':
    main()
