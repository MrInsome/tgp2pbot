import asyncio
import json
import tracemalloc

import aiohttp
import fake_useragent
from aiogram import Bot, Dispatcher, types

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def get_p2p_data(fiat, method):
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
    }
    params = {
        "direction": method,
        "currency": f"{fiat.lower()}",
        "only_available": "true"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://garantex.io/api/v2/otc/ads?', headers=headers, params=params) as response:
            text = await response.text()
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                return 0
            return data


async def get_api_data(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://garantex.io/api/v2/trades?market={symbol.lower()}&limit=1") as response:
            data = await response.json()
            if "error" in data:
                return 0
            return data


async def calculate_gains(p2p_sell, spot_price, p2p_buy):
    return round(((((100 / float(p2p_buy)) / float(spot_price)) * float(p2p_sell)) / 100 - 1) * 100, 2)


async def main():
    tracemalloc.start()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
