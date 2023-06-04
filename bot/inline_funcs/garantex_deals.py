from aiogram import types

from bot.keyboards.inline.alert import alert_inline
from parsers.garantex_custom_parser.base_parser import get_api_data, get_p2p_data
from parsers.garantex_custom_parser.base_parser import calculate_gains


async def testing_message(fiat, percentage, msg: types.Message):
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

    await msg.edit_caption(caption,
                           parse_mode="HTML",
                           reply_markup=alert_inline)
