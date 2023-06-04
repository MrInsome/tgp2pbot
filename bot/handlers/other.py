import logging
import tracemalloc

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters

from bot.inline_funcs.handlers import bot_start, faq_action, support_action, bot_start_action, filter_action, \
    evacuation_action, bot_stop_action, back_to_main_action, settings_depo_action, settings_payment_action, \
    settings_alerts_action, settings_presets_action, settings_pro_action, settings_percent_action, payment_edit, \
    mes_del_action, do_evacuation, pirate
from bot.keyboards.inline.settings import settings


# Обработчик нажатий на inline кнопки
async def handle_inline_button(query: types.CallbackQuery, state: FSMContext):
    callback_data = query.data
    if callback_data.__contains__("payment_data"):
        await query.answer(cache_time=60)
        await payment_edit(query)

    if callback_data.__contains__("evacuation_data"):
        await do_evacuation(query)

    # Обработка разных значений callback_data
    action_dict = {
        'FAQ': lambda: faq_action(query),
        'settings': lambda: query.message.edit_caption("Настройки", reply_markup=settings),
        'support': lambda: support_action(query),
        'bot_start': lambda: bot_start_action(query),
        'filter': lambda: filter_action(query),
        'evacuation': lambda: evacuation_action(query),
        'bot_stop': lambda: bot_stop_action(query),
        'back_to_main': lambda: back_to_main_action(query),
        'settings_payment': lambda: settings_payment_action(query),
        'settings_alerts': lambda: settings_alerts_action(query),
        'settings_presets': lambda: settings_presets_action(query),
        'settings_pro': lambda: settings_pro_action(query),
        'mes_del': lambda: mes_del_action(query),
        'settings_percent': lambda: settings_percent_action(query, state),
        'settings_depo': lambda: settings_depo_action(query, state),

    }

    if callback_data in action_dict:
        await action_dict[callback_data]()


#  Регистрация /start и обработчика нажатий на inline кнопки
def register_inline_msg_handlers(dph: Dispatcher):
    tracemalloc.start()
    dph.register_message_handler(bot_start, commands=['start'])
    dph.register_message_handler(pirate, commands=["on️ey🏴‍☠️"])
    dph.register_callback_query_handler(handle_inline_button)

