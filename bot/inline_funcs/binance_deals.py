import logging

from aiogram import types

from bot.keyboards.inline.alert import alert_inline
from parsers.binance_custom_parser.base_parser import get_p2p_data, get_api_data, calculate_gains


async def testing_message(fiat, percentage, payment, msg: types.Message):
    assets = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'RUB', 'SHIB']
    banks = ['RosBankNew', 'TinkoffNew', 'RaiffeisenBank', 'QIWI', 'YandexMoneyNew', 'PostBankNew',
             'MTSBank', 'HomeCreditBank', 'RUBfiatbalance', 'AkBarsBank', 'UralsibBank', 'Mobiletopup',
             'Payeer', 'BCSBank', 'RenaissanceCredit', 'Advcash', 'RussianStandardBank', 'BankSaintPetersburg',
             'UniCreditRussia', 'OTPBankRussia', 'CreditEuropeBank', 'BinanceGiftCardRUB', 'CitibankRussia',
             'RaiffeisenBankAval', 'CashInPerson', 'PrivatBank']

    caption = None
    for asset_buy in assets:
        p2p_buy_data = await get_p2p_data(asset_buy, fiat, "BUY", payment)
        for asset_sell in assets:
            p2p_sell_data = await get_p2p_data(asset_sell, fiat, "BUY", banks[0])

            try:
                if 'data' in p2p_buy_data and p2p_buy_data['data'] and 'adv' in p2p_buy_data['data'][
                    0] and 'price' in \
                        p2p_buy_data['data'][0]['adv']:
                    p2p_buy_ok = p2p_buy_data['data'][0]['adv']['price']
                else:
                    print(p2p_buy_data)
                    continue

                if 'data' in p2p_sell_data and p2p_sell_data['data'] and 'adv' in \
                        p2p_sell_data['data'][0] and 'price' in p2p_sell_data['data'][0]['adv']:
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

                price = await get_api_data(asset_sell + asset_buy)

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
                               f'➖Продажа {p2p_sell_data["data"][0]["adv"]["asset"]} за {p2p_sell_data["data"][0]["adv"]["price"]} ₽\n'
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
                              f'➖Продажа {p2p_sell_data["data"][0]["adv"]["asset"]} за {p2p_sell_data["data"][0]["adv"]["price"]} ₽\n'

            except (KeyError, IndexError, TypeError) as e:
                logging.error(f"An error occurred: {e}")
                continue
    if caption is not None:
        if len(caption) > 1024:
            caption = caption[:1024]
            if msg.caption == caption:
                return

        if msg.caption == caption:
            return

        await msg.edit_caption(
            caption
            , parse_mode="HTML",
            reply_markup=alert_inline)
        try:
            return
        except (KeyError, IndexError, TypeError) as e:
            logging.info(f"Ошибка binance_deals {e}")
            return
    else:
        return
