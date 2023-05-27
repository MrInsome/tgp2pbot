import asyncio
import tracemalloc
from asyncio import sleep

import aiohttp
import fake_useragent
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def get_p2p_data(asset, fiat, method):
    headers = {
        "User-Agent": fake_useragent.UserAgent().random,
    }
    data = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 1,
        "tradeType": method
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers,
                                json=data) as response:
            return await response.json()


async def get_api_data(symbol):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}") as response:
            data = await response.json()
            if "code" in data:
                return 0
            return data


async def calculate_gains(p2p_sell, spot_price, p2p_buy):
    return round(((((100 / float(p2p_buy)) / float(spot_price)) * float(p2p_sell)) / 100 - 1) * 100, 2)


async def testing_message(fiat, percentage, msg: types.Message):
    p2pusdt_data = await get_p2p_data("USDT", fiat, "BUY")
    p2peth_data = await get_p2p_data("ETH", fiat, "SELL")

    p2pusdtok = p2pusdt_data['data'][0]['adv']['price']
    p2pethok = p2peth_data['data'][0]['adv']['price']

    priceeth = await get_api_data("ETHUSDT")

    resulteth = await calculate_gains(p2pethok, priceeth['price'], p2pusdtok)

    if resulteth < percentage:
        return

    caption = f'<b>✅ Найдена новая сделка ✅\n\n</b>'\
              f'🟢<b>{resulteth}%</b>\n'\
              f'➖BNC ➖BNC(spot) ➖BNC\n'\
              f'➖{p2pusdt_data["data"][0]["advertiser"]["nickName"]} '\
              f'{p2pusdt_data["data"][0]["advertiser"]["monthOrderCount"]} '\
              f'({int(round(float(p2pusdt_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)'\
              f'➖ {p2peth_data["data"][0]["advertiser"]["nickName"]} '\
              f'{p2peth_data["data"][0]["advertiser"]["monthOrderCount"]} '\
              f'({int(round(float(p2peth_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)\n'\
              f'➖{p2pusdt_data["data"][0]["adv"]["asset"]} за {p2pusdt_data["data"][0]["adv"]["price"]} '\
              f'{p2pusdt_data["data"][0]["adv"]["fiatUnit"]}\n'\
              f'➖Покупка спот {priceeth["symbol"]} за {round(float(priceeth["price"]), 2)}\n'\
              f'➖Продажа {p2peth_data["data"][0]["adv"]["asset"]} за {p2peth_data["data"][0]["adv"]["price"]} ₽'

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
