import asyncio
import logging

import aiohttp
from aiogram import types

from bot.keyboards.inline.alert import alert_inline
from parsers.binance_custom_parser.test_parser import get_p2p_data, get_api_data, calculate_gains


async def testing_message(fiat, percentage, payment, filters, msg: types.Message):
    assets = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'RUB', 'SHIB']
    banks = ['RosBankNew', 'TinkoffNew', 'RaiffeisenBank', 'QIWI', 'YandexMoneyNew', 'PostBankNew']#,
             # 'MTSBank', 'HomeCreditBank', 'RUBfiatbalance', 'AkBarsBank', 'UralsibBank', 'Mobiletopup',
             # 'Payeer', 'BCSBank', 'RenaissanceCredit', 'Advcash', 'RussianStandardBank', 'BankSaintPetersburg',
             # 'UniCreditRussia', 'OTPBankRussia', 'CreditEuropeBank', 'BinanceGiftCardRUB', 'CitibankRussia',
             # 'RaiffeisenBankAval', 'CashInPerson', 'PrivatBank']

    caption = None
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100)) as session:
        tasks = []
        for asset_buy in assets:
            tasks.append(get_p2p_data(session, asset_buy, fiat, "BUY", payment))
        p2p_buy_results = await asyncio.gather(*tasks)

        tasks = []
        for bank in banks:
            for asset_sell in assets:
                tasks.append(get_p2p_data(session, asset_sell, fiat, "BUY", bank))
        p2p_sell_results = await asyncio.gather(*tasks)

        for bank in banks:
            for p2p_sell_data, asset_sell in zip(p2p_sell_results, assets):
                for p2p_buy_data, asset_buy in zip(p2p_buy_results, assets):
                    try:
                        if 'data' in p2p_buy_data and p2p_buy_data['data'] and 'adv' in p2p_buy_data['data'][
                            0] and 'price' in p2p_buy_data['data'][0]['adv']:
                            p2p_buy_ok = p2p_buy_data['data'][0]['adv']['price']
                        else:
                            print(p2p_buy_data)
                            continue

                        if 'data' in p2p_sell_data and p2p_sell_data['data'] and 'adv' in p2p_sell_data['data'][
                            0] and 'price' in p2p_sell_data['data'][0]['adv']:
                            p2p_sell_ok = p2p_sell_data['data'][0]['adv']['price']
                        else:
                            print(p2p_sell_data)
                            continue

                        # Проверка, что значения не равны None
                        if p2p_buy_ok is None or p2p_sell_ok is None:
                            continue

                        p2p_buy_ok = float(p2p_buy_ok)
                        p2p_sell_ok = float(p2p_sell_ok)

                        if asset_sell + asset_buy == 'SHIBRUB':
                            continue

                        price = await get_api_data(session, asset_sell + asset_buy)

                        if price == 0:
                            continue

                        result = await calculate_gains(p2p_sell_ok, price['price'], p2p_buy_ok)

                        if result < percentage:
                            continue
                        if caption is not None:
                            caption += f'\n🟢<b>{result}%</b>\n' \
                                       f'➖BNC ➖BNC(spot) ➖BNC\n' \
                                       f'➖{p2p_buy_data["data"][0]["advertiser"]["nickName"]} ' \
                                       f'{p2p_buy_data["data"][0]["advertiser"]["monthOrderCount"]} ' \
                                       f'({int(round(float(p2p_buy_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)' \
                                       f'➖ {p2p_sell_data["data"][0]["advertiser"]["nickName"]} ' \
                                       f'{p2p_sell_data["data"][0]["advertiser"]["monthOrderCount"]} ' \
                                       f'({int(round(float(p2p_sell_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)\n' \
                                       f'➖{p2p_buy_data["data"][0]["adv"]["asset"]} за {p2p_buy_data["data"][0]["adv"]["price"]} ' \
                                       f'{p2p_buy_data["data"][0]["adv"]["fiatUnit"]}\n' \
                                       f'➖Покупка спот {price["symbol"]} за {float(price["price"])}\n' \
                                       f'➖Продажа {p2p_sell_data["data"][0]["adv"]["asset"]} за {p2p_sell_data["data"][0]["adv"]["price"]} ₽\n' \
                                       f'➖{payment} -> {bank}\n'
                        else:
                            caption = f'<b>✅ Найдена новая сделка ✅\n\n</b>' \
                                      f'🟢<b>{result}%</b>\n' \
                                      f'➖BNC ➖BNC(spot) ➖BNC\n' \
                                      f'➖{p2p_buy_data["data"][0]["advertiser"]["nickName"]} ' \
                                      f'{p2p_buy_data["data"][0]["advertiser"]["monthOrderCount"]} ' \
                                      f'({int(round(float(p2p_buy_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)' \
                                      f'➖ {p2p_sell_data["data"][0]["advertiser"]["nickName"]} ' \
                                      f'{p2p_sell_data["data"][0]["advertiser"]["monthOrderCount"]} ' \
                                      f'({int(round(float(p2p_sell_data["data"][0]["advertiser"]["monthFinishRate"]), 2) * 100)}%)\n' \
                                      f'➖{p2p_buy_data["data"][0]["adv"]["asset"]} за {p2p_buy_data["data"][0]["adv"]["price"]} ' \
                                      f'{p2p_buy_data["data"][0]["adv"]["fiatUnit"]}\n' \
                                      f'➖Покупка спот {price["symbol"]} за {float(price["price"])}\n' \
                                      f'➖Продажа {p2p_sell_data["data"][0]["adv"]["asset"]} за {p2p_sell_data["data"][0]["adv"]["price"]} ₽\n' \
                                      f'➖{payment} -> {bank}\n'

                    except (KeyError, IndexError, TypeError) as e:
                        logging.error(f"An error occurred: {e}")
                        continue

    if caption is not None:
        if caption == msg.caption:
            return
        if len(caption) > 1024:
            caption = caption[:1024]
            await msg.edit_caption(
                caption
                , parse_mode="HTML",
                reply_markup=alert_inline)
        else:
            await msg.edit_caption(
                caption
                , parse_mode="HTML",
                reply_markup=alert_inline)
    else:
        await msg.edit_caption(f'Не найдено подходящих сделок')
