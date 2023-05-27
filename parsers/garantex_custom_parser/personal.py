import asyncio
import json
import tracemalloc
from time import sleep

import aiohttp
import fake_useragent
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


async def testing_message_g(fiat, percentage, msg: types.Message):
    p2pusdt_data = await get_p2p_data(fiat, "sell")
    p2peth_data = await get_p2p_data(fiat, "buy")

    p2pusdtok = p2pusdt_data[0]['price']
    p2pethok = p2peth_data[0]['price']

    priceeth = await get_api_data("ETHUSDT")

    resulteth = await calculate_gains(float(p2pethok), float(priceeth[0]['price']),
                                      float(p2pusdtok))

    caption = f'<b>✅ Найдена новая сделка ✅\n\n</b>'\
              f'🟢<b>{resulteth}%</b>\n'\
              f'➖GRTX ➖GRTX(spot) ➖GRTX\n'\
              f'➖{p2pusdt_data[0]["member"]} '\
              f'➖ {p2peth_data[0]["member"]}\n '\
              f'➖{p2pusdt_data[0]["currency"]} за {p2pusdt_data[0]["price"]} '\
              f'{p2pusdt_data[0]["fiat_currency"]}\n'\
              f'➖Покупка спот {priceeth[0]["market"]} за {round(float(priceeth[0]["price"]), 2)}\n'\
              f'➖Продажа {p2peth_data[0]["currency"]} за {p2peth_data[0]["price"]} ₽'

    if resulteth < percentage:
        return

    if msg.caption == caption:
        return

    try:
        await msg.edit_caption(
            caption,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton("Фильтр👁️‍🗨️", callback_data="filter"),
                InlineKeyboardButton("Эвакуация🆘", callback_data="evacuation"),
                InlineKeyboardButton("Остановить оповещения🔴", callback_data="bot_stop"),
            ))
    except Exception as ex:
        print(f'Smth went wrong\n: {ex.args}')
        return



async def main():
    tracemalloc.start()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
