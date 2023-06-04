from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_kb_t = InlineKeyboardMarkup(row_width=2).insert(
    InlineKeyboardButton("Инструкция", callback_data=f"FAQ")) \
    .insert(InlineKeyboardButton("Настройки", callback_data="settings")) \
    .insert(
    InlineKeyboardButton("Поддержка", callback_data="support")) \
    .insert(InlineKeyboardButton("Начать оповещения", callback_data="bot_start"))
back_to_menu_kb_t = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton("Возврат к меню", callback_data="back_to_main"),
)
