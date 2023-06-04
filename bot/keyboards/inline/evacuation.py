from aiogram import types
from aiogram.types import InlineKeyboardButton

from bot.keyboards.inline.callback_datas import evacuation_callback

evacuation_buttons = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'RUB', 'SHIB']

evacuation_keyboard = types.InlineKeyboardMarkup(row_width=3)

for ev_asset in evacuation_buttons:
    button = types.InlineKeyboardButton(text=ev_asset, callback_data=evacuation_callback.new(
        asset=ev_asset
    ))
    evacuation_keyboard.insert(button)

evacuation_keyboard.insert(InlineKeyboardButton("Отмена (удаление сообщения)", callback_data='mes_del'))
