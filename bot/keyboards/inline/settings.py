from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

settings = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Депозит", callback_data="settings_depo"),
    InlineKeyboardButton("Платежные методы", callback_data="settings_payment"),
    InlineKeyboardButton("Оповещения", callback_data="settings_alerts"),
    InlineKeyboardButton("Пресеты", callback_data="settings_presets"),
    InlineKeyboardButton("Проф.Настройка", callback_data="settings_pro"),
    InlineKeyboardButton("Назад в меню", callback_data="back_to_main"),
)

settings_pro = InlineKeyboardMarkup().insert(
    InlineKeyboardButton("Актив", callback_data="dead_end")).insert(
    InlineKeyboardButton("Покупка", callback_data="dead_end")).insert(
    InlineKeyboardButton("Продажа", callback_data="dead_end"))

asset_names = ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'RUB', 'SHIB']

matrix = [
        [
            InlineKeyboardButton(asset_names[i], callback_data=f'button_{i}'),
            InlineKeyboardButton("✅", callback_data=f'button_{i}')
        ] + [
            InlineKeyboardButton("✅", callback_data=f'button_{i}_{j}')
            for j in range(3)
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
