import asyncio
import bot.main

from aiogram import types

from bot.inline_funcs.FAQ import faq_func
from bot.inline_funcs.support import support_func
from bot.keyboards.inline import menu_kb_t, settings, settings_pro
from parsers.binance_custom_parser import my_parser
from parsers.garantex_custom_parser import personal
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


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
    else:
        await msg.reply('Для использования бота необходимо подписаться.')
        return


# Стоп для оповещений
stop_event = asyncio.Event()


#  Работа с Инструкцией FAQ.py


async def faq_action(query):
    await faq_func(await query.message.edit_caption("..."))


#  Работа с Поддержкой support.py


async def support_action(query):
    await support_func(await query.message.edit_caption("..."))


#  Работа с Началом оповещений

async def bot_start_action(query):
    await query.message.edit_caption(caption="Ожидание новой сделки...")
    await query.message.answer_photo(photo=open("inner_files\\opener.png", "rb"),
                                     caption=f'<em>Оповещения включены</em>!\n',
                                     reply_markup=menu_kb_t,
                                     parse_mode="HTML")
    stop_event.clear()
    while not stop_event.is_set():
        if stop_event.is_set():
            break
        await personal.testing_message_g("RUB", 2, query.message)
        await asyncio.sleep(15)
        if stop_event.is_set():
            break
        await my_parser.testing_message("RUB", 2, query.message)
        await asyncio.sleep(15)


#  Работа с Фильтром

async def filter_action(query):
    stop_event.set()
    await query.message.edit_caption("Фильтр", reply_markup=settings)


#  Работа с Эвакуацией


async def evacuation_action(query):
    stop_event.set()
    await query.message.edit_caption("Эвакуация", reply_markup=settings)


#  Работа с Остановкой оповещений


async def bot_stop_action(query):
    stop_event.set()
    name = query.from_user.username if query.from_user.username != "None" else query.from_user.first_name
    await query.message.delete()


#  Возврат в главное меню

async def back_to_main_action(query):
    name = query.from_user.username if query.from_user.username != "None" else query.from_user.first_name
    await query.message.edit_caption(caption=f'<em>Добро пожаловать</em>, <b>{name}</b>!\n',
                                     reply_markup=menu_kb_t,
                                     parse_mode="HTML")


#  Работа с Депозитом


class Forms(StatesGroup):
    waiting_for_deposit = State()


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
    a = bot.main.database.parameter_replace(query.from_user.id, 'deposit', deposit)
    await query.message.edit_caption(f"Депозит установлен: {deposit}", reply_markup=settings)


#  Работа с Платежными методами

async def settings_payment_action(query):
    await query.message.edit_caption("Выбрана настройка 'Платежные методы'", reply_markup=settings)


#  Работа с Оповещениями

async def settings_alerts_action(query):
    await query.message.edit_caption("Выбрана настройка 'Оповещения'", reply_markup=settings)


#  Работа с Пресетами

async def settings_presets_action(query):
    await query.message.edit_caption("Выбрана настройка 'Пресеты'", reply_markup=settings)


#  Работа с Проф.Настройками

async def settings_pro_action(query):
    await query.message.edit_caption("Выбрана настройка 'Проф.Настройка'", reply_markup=settings_pro)
