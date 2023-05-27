import asyncio
import aiohttp
import requests
import fake_useragent
import pandas as pd
from time import sleep
from aiogram import Bot, Dispatcher, types
import tracemalloc


def parsing_bank(fiat) -> list:
    cookies = {
        'common_fiat': fiat,
    }
    headers = {
        'referer': 'https://p2p.binance.com/trade/all-payments/' + 'USDT' + '?fiat=' + fiat,
        'user-agent': fake_useragent.UserAgent().random,
    }
    json_data = {
        'proMerchantAds': False,
        'page': 1,
        'rows': 5,
        'payTypes': [],
        'countries': [],
        'publisherType': None,
        'asset': "USDT",
        'fiat': fiat,
        'tradeType': "buy",
    }

    response = requests.post('https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/filter-conditions',
                             cookies=cookies, headers=headers, json=json_data)

    data_json = response.json()

    banks = []

    for bank in data_json["data"]["tradeMethods"]:
        banks.append(bank["identifier"])
    return banks


bot = Bot(token='6299203082:AAEbIBJQzBcD1UglT6NzGn3wOk-XjVLjXe0')
dp = Dispatcher(bot)


async def fetch(session, url, payload):
    async with session.post(url, json=payload) as response:
        return await response.json()


async def parse_data(symbols: list, fiats: list, payTypes: list):
    df = pd.DataFrame()
    async with aiohttp.ClientSession() as session:
        for symbol in symbols:
            for idx, fiat in enumerate(fiats):
                try:
                    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
                    payload = {
                        'asset': symbol,
                        'countries': [],
                        'fiat': fiat,
                        'page': 1,
                        'payTypes': payTypes,
                        'publisherType': None,
                        'rows': 10,
                        # 'transAmount': transAmount[idx]
                    }

                    res = await fetch(session, url, {**payload, 'tradeType': 'BUY'})
                    res2 = await fetch(session, url, {**payload, 'tradeType': 'SELL'})

                    data = [{'tradeType': 'BUY', 'asset': i['adv']['asset'], 'fiatUnit': i['adv']['fiatUnit'],
                             'price': i['adv']['price'], 'minSingleTransAmount': i['adv']['minSingleTransAmount'],
                             'maxSingleTransAmount': i['adv']['maxSingleTransAmount'],
                             'tradeMethods': [x['tradeMethodName'] for x in i['adv']['tradeMethods']],
                             'advertiser': i['advertiser']['nickName'],
                             'platform': 'Binance P2P'} for i in res['data']]
                    data2 = [{'tradeType': 'SELL', 'asset': i['adv']['asset'], 'fiatUnit': i['adv']['fiatUnit'],
                              'price': i['adv']['price'], 'minSingleTransAmount': i['adv']['minSingleTransAmount'],
                              'maxSingleTransAmount': i['adv']['maxSingleTransAmount'],
                              'tradeMethods': [x['tradeMethodName'] for x in i['adv']['tradeMethods']],
                              'advertiser': i['advertiser']['nickName'],
                              'platform': 'Binance P2P'} for i in res2['data']]

                    tempDf = pd.DataFrame(data=data).sort_values(by=['price'])
                    tempDf2 = pd.DataFrame(data=data2).sort_values(by=['price'], ascending=False)
                    df = pd.concat([df, tempDf, tempDf2], axis=0)
                except Exception as e:
                    print(e)
                    continue

    return df


async def send_message(telegramId, df, fiats):
    for fiat in fiats:
        buy_df = df[(df['tradeType'] == 'BUY') & (df['fiatUnit'] == fiat)]
        sell_df = df[(df['tradeType'] == 'SELL') & (df['fiatUnit'] == fiat)]

        if not buy_df.empty and not sell_df.empty:
            min_price = buy_df.sort_values(by=['price']).iloc[0]
            max_price = sell_df.sort_values(by=['price'], ascending=False).iloc[0]

            price_diff = (float(max_price['price']) - float(min_price['price'])) / float(min_price['price']) * 100
            if price_diff > 1:
                await bot.send_message(
                    telegramId,
                    f'✅ Найдена новая сделка ✅ \n \n💵Профит: {round(price_diff, 2)} %'
                    f'\n \n🟢\n{min_price.to_string()} \n \n🔴\n{max_price.to_string()}'
                )


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    symbols = ["USDT"]  # crypto currencies
    fiats = ["RUB"]  # fiat currencies
    # transAmount = ["5000"]  # amount for each fiat currency
    payTypes = parsing_bank(fiat="RUB")[:20]  # pay types
    while True:
        df = await parse_data(symbols, fiats, payTypes)
        await send_message(message.from_user.id, df, fiats)
        await asyncio.sleep(15)


async def main():
    tracemalloc.start()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
