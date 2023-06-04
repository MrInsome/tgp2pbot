from aiogram import types
from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.callback_datas import exchange_callback

exchanges_list = ["Binance (BNC)", "Gatantex (GAR)"]

payment_methods = types.InlineKeyboardMarkup(row_width=1)

for exchanges in exchanges_list:
    button = types.InlineKeyboardButton(text=exchanges, callback_data=exchange_callback.new(
        exchange=exchanges
    ))
    payment_methods.insert(button)

payment_methods.insert(InlineKeyboardButton("Возврат к настройкам", callback_data='settings'), )