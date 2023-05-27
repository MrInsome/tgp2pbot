from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

# menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).insert(
#     KeyboardButton("Инструкция")).insert(KeyboardButton("Настройки")).insert(
#     KeyboardButton("Поддержка")).insert(KeyboardButton("Начать оповещения"))
#
# back_to_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).insert(
#     KeyboardButton("Возврат к меню"),
# )
#
#
# async def back_to_menu_kb_f(msg: types.Message):
#     await msg.answer(text="Возврат к меню...", reply_markup=menu_kb)
