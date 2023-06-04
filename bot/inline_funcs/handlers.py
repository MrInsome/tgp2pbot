import asyncio
import logging

from aiogram.types import InlineKeyboardButton

import bot.main

from aiogram import types

from bot.inline_funcs import garantex_deals, test_binance_deals
from bot.inline_funcs.binance_evacuation import evacuation_message
from bot.keyboards.inline.evacuation import evacuation_keyboard
from bot.keyboards.inline.payment_methods import pm_buttons, payment_methods
from bot.keyboards.inline.menu import menu_kb_t, back_to_menu_kb_t
from bot.keyboards.inline.alert import alert_setup
from bot.keyboards.inline.settings import settings, settings_pro
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Forms(StatesGroup):
    waiting_for_deposit = State()
    waiting_for_percent = State()


#  /start
async def bot_start(msg: types.Message):
    name = msg.from_user.username if msg.from_user.username != "None" else msg.from_user.first_name

    bot.main.database.create_user(int(msg.from_user.id), name)

    is_subscribed = bot.main.database.check_subscription(int(msg.from_user.id))

    if is_subscribed:
        await msg.answer_photo(photo=open('inner_files/opener.png', "rb"),
                               caption=f'<em>Добро пожаловать</em>, <b>{name}</b>!\n',
                               reply_markup=menu_kb_t,
                               parse_mode="HTML")
        stop_event.set()
    else:
        await msg.reply('Для использования бота необходимо подписаться.')
        return

async def pirate(msg: types.Message):
    name = msg.from_user.username if msg.from_user.username != "None" else msg.from_user.first_name

    bot.main.database.create_user(int(msg.from_user.id), name)

    await msg.answer_photo(photo=open('inner_files/opener.png', "rb"),
                           caption=f'<em>Добро пожаловать</em>, <b>{name}</b>!\n',
                           reply_markup=menu_kb_t,
                           parse_mode="HTML")
    stop_event.set()

# Стоп для оповещений
stop_event = asyncio.Event()


#  Работа с Инструкцией FAQ.py


async def faq_action(query):
    await query.message.edit_caption("FAQ", reply_markup=back_to_menu_kb_t)


#  Работа с Поддержкой support.py


async def support_action(query):
    support_chat_id = '@hamsteroney'

    await query.message.edit_caption(f'Ваши вопросы и предложения могут быть отправлены в чат поддержки: {support_chat_id}',
                           reply_markup=back_to_menu_kb_t
                           )


#  Работа с Началом оповещений

async def bot_start_action(query):
    percent_data = bot.main.database.value_parameters(query.from_user.id, 'spred_percent')
    fiat_data = bot.main.database.value_parameters(query.from_user.id, 'fiat')
    payment_data = bot.main.database.value_parameters(query.from_user.id, 'payment_methods')
    await query.message.edit_caption(caption="Ожидание новой сделки...")
    await query.message.answer_photo(photo=open('inner_files/opener.png', 'rb'),
                                     caption=f'<em>Оповещения включены</em>!\n',
                                     reply_markup=menu_kb_t,
                                     parse_mode="HTML")
    stop_event.clear()
    while not stop_event.is_set():
        if stop_event.is_set():
            break
        await test_binance_deals.testing_message(fiat_data, float(percent_data), payment_data, "", query.message)
        # await binance_deals.testing_message(fiat_data, float(percent_data), payment_data, query.message)
        await asyncio.sleep(15)
        if stop_event.is_set():
            break
        await garantex_deals.testing_message(fiat_data, float(percent_data), query.message)
        await asyncio.sleep(15)


#  Работа с Фильтром

async def filter_action(query):
    stop_event.set()
    await query.message.edit_caption("Фильтр", reply_markup=settings)


#  Работа с Эвакуацией


async def evacuation_action(query):
    stop_event.set()
    await query.message.edit_caption("Оповещения остановлены! Выберите монету для эвакуации",
                                     reply_markup=evacuation_keyboard)


async def do_evacuation(query):
    payment_data = bot.main.database.value_parameters(query.from_user.id, 'payment_methods')
    asset = query.data.split(":")[1]
    await evacuation_message(asset, payment_data, query.message)


#  Работа с Остановкой оповещений


async def bot_stop_action(query):
    if stop_event.is_set():
        await query.message.edit_caption("Оповещения уже остановлены", reply_markup=menu_kb_t)
        return
    stop_event.set()
    await query.message.delete()


async def mes_del_action(query):
    await query.message.delete()

#  Возврат в главное меню

async def back_to_main_action(query):
    name = query.from_user.username if query.from_user.username != "None" else query.from_user.first_name
    await query.message.edit_caption(caption=f'<em>Добро пожаловать</em>, <b>{name}</b>!\n',
                                     reply_markup=menu_kb_t,
                                     parse_mode="HTML")


#  Работа с Депозитом


async def settings_depo_action(query, state: FSMContext):
    await Forms.waiting_for_deposit.set()
    depo = bot.main.database.value_parameters(query.from_user.id, 'deposit')
    await query.message.edit_caption(f"Депозит установленный на данный момент: {depo}\n"
                                     f"Введите ваш Депозит:")
    await state.update_data(query_data=
                            query
                            )


async def process_deposit(message: types.Message, state: FSMContext):
    deposit = message.text
    await message.delete()
    data = await state.get_data()
    query = data.get("query_data")
    await state.finish()
    if not any(char.isdigit() for char in deposit):
        await query.message.edit_caption(f"Попробуйте ввести без букв и спец. символов", reply_markup=settings)
        return
    a = bot.main.database.parameter_replace(query.from_user.id, 'deposit', deposit)
    await query.message.edit_caption(f"Депозит установлен: {deposit}₽", reply_markup=settings)


#  Работа с Платежными методами

async def settings_payment_action(query):
    await query.message.edit_caption("Выберите платежный метод:", reply_markup=payment_methods)


async def payment_edit(query):
    method = query.data.split(":")[1]
    a = bot.main.database.parameter_replace(query.from_user.id, 'payment_methods', method)
    await query.message.edit_caption(f"Платёжный метод установлен: {method}", reply_markup=settings)


#  Работа с Оповещениями

async def settings_alerts_action(query):
    await query.message.edit_caption("Выбрана настройка 'Оповещения'", reply_markup=alert_setup)


#  Работа с Пресетами

async def settings_presets_action(query):
    await query.message.edit_caption("Ожидайте настройку 'Пресеты'"
                                     "в следующих обновлениях", reply_markup=settings)


#  Работа с Проф.Настройками

async def settings_pro_action(query):
    await query.message.edit_caption("Ожидайте настройку 'Проф.Настройка'"
                                     "в следующих обновлениях", reply_markup=settings_pro)


async def settings_percent_action(query, state: FSMContext):
    await Forms.waiting_for_percent.set()
    spred = bot.main.database.value_parameters(query.from_user.id, 'spred_percent')
    await query.message.edit_caption(f"Спред установленный на данный момент: {spred}%\n"
                                     f"Введите спред при достижении которого сделки будут обновляться:")
    await state.update_data(query_data=
                            query
                            )


async def process_percent(message: types.Message, state: FSMContext):
    spred = message.text
    await message.delete()
    data = await state.get_data()
    query = data.get("query_data")
    await state.finish()
    if not any(char.isdigit() for char in spred):
        await query.message.edit_caption(f"Попробуйте ввести без букв и спец. символов", reply_markup=alert_setup)
        return
    a = bot.main.database.parameter_replace(query.from_user.id, 'spred_percent', spred)
    await query.message.edit_caption(f"Спред установлен: {spred}%", reply_markup=alert_setup)
