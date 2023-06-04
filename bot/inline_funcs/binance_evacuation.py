import asyncio
import logging

import aiohttp
from aiogram import types

from bot.keyboards.inline.alert import alert_inline
from parsers.binance_custom_parser.evacuation import get_p2p_data


async def evacuation_message(asset, payment, msg: types.Message):
    assets = [asset]
    banks = ['RosBankNew', 'TinkoffNew', 'RaiffeisenBank', 'QIWI', 'YandexMoneyNew', 'PostBankNew']#,
             # 'MTSBank', 'HomeCreditBank', 'RUBfiatbalance', 'AkBarsBank', 'UralsibBank', 'Mobiletopup',
             # 'Payeer', 'BCSBank', 'RenaissanceCredit', 'Advcash', 'RussianStandardBank', 'BankSaintPetersburg',
             # 'UniCreditRussia', 'OTPBankRussia', 'CreditEuropeBank', 'BinanceGiftCardRUB', 'CitibankRussia',
             # 'RaiffeisenBankAval', 'CashInPerson', 'PrivatBank']

    caption = None
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        tasks = []
        for bank in banks:
            for asset_sell in assets:
                tasks.append(get_p2p_data(session, asset_sell, bank))
        p2p_sell_results = await asyncio.gather(*tasks)

        for bank in banks:
            for p2p_sell_data, asset_sell in zip(p2p_sell_results, assets):
                if caption is not None:
                    caption += f'➖BNC ➖BNC(spot) ➖BNC\n' \
                               f'➖ {p2p_sell_data["data"][0]["advertiser"]["nickName"]} ' \
                               f'{p2p_sell_data["data"][0]["advertiser"]["monthOrderCount"]} ' \
                               f'({int(round(float(p2p_sell_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)\n' \
                               f'➖Продажа {p2p_sell_data["data"][0]["adv"]["asset"]} за {p2p_sell_data["data"][0]["adv"]["price"]} ₽\n' \
                               f'➖{bank}\n\n'
                else:
                    caption = f'➖BNC ➖BNC(spot) ➖BNC\n' \
                              f'➖ {p2p_sell_data["data"][0]["advertiser"]["nickName"]} ' \
                              f'{p2p_sell_data["data"][0]["advertiser"]["monthOrderCount"]} ' \
                              f'({int(round(float(p2p_sell_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)\n' \
                              f'➖Продажа {p2p_sell_data["data"][0]["adv"]["asset"]} за {p2p_sell_data["data"][0]["adv"]["price"]} ₽\n' \
                              f'➖{bank}\n\n'
        await msg.edit_caption(
            caption
            , parse_mode="HTML",
            reply_markup=alert_inline)
