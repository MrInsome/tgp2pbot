from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

alert_setup = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Начать оповещения🟢", callback_data="bot_start"),
    InlineKeyboardButton("Остановить оповещения🔴", callback_data="bot_stop"),
    InlineKeyboardButton("Настройка оповещения📈", callback_data="settings_percent"),
    InlineKeyboardButton("Назад к настройкам↩", callback_data="settings"),
)
alert_inline = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("Фильтр👁️‍🗨️", callback_data="filter"),
            InlineKeyboardButton("Эвакуация🆘", callback_data="evacuation"),
            InlineKeyboardButton("Остановить оповещения🔴", callback_data="bot_stop"),
        )
