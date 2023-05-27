from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

settings = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Депозит", callback_data="settings_depo"),
    InlineKeyboardButton("Платежные методы", callback_data="settings_payment"),
    InlineKeyboardButton("Оповещения", callback_data="settings_alerts"),
    InlineKeyboardButton("Пресеты", callback_data="settings_presets"),
    InlineKeyboardButton("Проф.Настройка", callback_data="settings_pro"),
    InlineKeyboardButton("Назад в меню", callback_data="back_to_main"),
)

menu_kb_t = InlineKeyboardMarkup(row_width=2).insert(
    InlineKeyboardButton("Инструкция", callback_data=f"FAQ")) \
    .insert(InlineKeyboardButton("Настройки", callback_data="settings")) \
    .insert(
    InlineKeyboardButton("Поддержка", callback_data="support")) \
    .insert(InlineKeyboardButton("Начать оповещения", callback_data="bot_start"))

back_to_menu_kb_t = InlineKeyboardMarkup(row_width=1).insert(
    InlineKeyboardButton("Возврат к меню", callback_data="back_to_main"),
)

settings_pro = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Актив", callback_data="back_to_main")).insert(
    InlineKeyboardButton("Покупка", callback_data="back_to_main")).insert(
    InlineKeyboardButton("Продажа", callback_data="back_to_main"))

options_matrix = [
    [True, True, True, True],
    [True, False, True, True],
    [True, True, True, True],
    [True, True, True, True],
    [True, True, True, True],
    [True, True, True, True],
    [True, True, True, True],
    [True, True, True, True]
]

asset_names = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'RUB', 'SHIB', '']

matrix = [
    [
        InlineKeyboardButton(asset_names[i], callback_data=f'button_{i}'),
        InlineKeyboardButton("✅", callback_data=f'button_{i}')
    ] + [
        InlineKeyboardButton("✅", callback_data=f'button_{i}_{j}')
        for j in range(4)
    ]
    for i in range(7)
]
matrix += [[
    InlineKeyboardButton("Назад", callback_data=f'settings'),
    InlineKeyboardButton("Применить", callback_data=f'accept')
]
]

for row in matrix:
    settings_pro.row(*row)


async def update_button_state(query: types.CallbackQuery):
    data = query.data.split('_')
    row = int(data[1])
    col = int(data[2])
    current_state = options_matrix[row][col]

    options_matrix[row][col] = not current_state

    new_symbol = "✅" if options_matrix[row][col] else "❌"
    await query.message.edit_reply_markup(reply_markup=settings_pro)
    await query.answer()
