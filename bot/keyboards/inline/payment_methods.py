from aiogram import types
from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.callback_datas import payment_callback

#  Платёжные методы TODO переместить

# TODO подумать как сделать полную клавиатуру в этой категории.

pm_buttons = ['RosBankNew', 'TinkoffNew', 'RaiffeisenBank', 'QIWI', 'YandexMoneyNew', 'PostBankNew',
              'MTSBank', 'HomeCreditBank', 'RUBfiatbalance', 'AkBarsBank', 'UralsibBank', 'Mobiletopup',
              'Payeer', 'BCSBank', 'RenaissanceCredit', 'Advcash', 'RussianStandardBank', 'BankSaintPetersburg',
              'UniCreditRussia', 'OTPBankRussia', 'CreditEuropeBank', 'BinanceGiftCardRUB', 'CitibankRussia',
              'RaiffeisenBankAval', 'CashInPerson', 'PrivatBank']

payment_methods = types.InlineKeyboardMarkup(row_width=3)

for button_name in pm_buttons:
    button = types.InlineKeyboardButton(text=button_name, callback_data=payment_callback.new(
        payment_method=button_name
    ))
    payment_methods.insert(button)

payment_methods.insert(InlineKeyboardButton("Возврат к настройкам", callback_data='settings'), )
