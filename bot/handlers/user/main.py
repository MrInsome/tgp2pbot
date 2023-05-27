from aiogram import Dispatcher, types
# from aiogram.dispatcher.filters import Text

from bot.inline_funcs.handlers import process_deposit, Forms


# from bot.keyboards.reply import back_to_menu_kb, back_to_menu_kb_f
# from bot.keyboards.inline import settings
# from parsers.binance_custom_parser import personal


# async def settings_menu(msg: types.Message):
#     await msg.answer("Меню настроек", reply_markup=settings)
#     await msg.answer("_", reply_markup=back_to_menu_kb)
#
#
# async def support(msg: types.Message):
#     support_chat_id = '@hamsteroney'
#     await msg.reply(f'Ваши вопросы и предложения могут быть отправлены в чат поддержки: {support_chat_id}',
#                     reply_markup=back_to_menu_kb)
#
#
# async def opovesheniya(msg: types.Message):
#     fiat = "RUB"  # todo
#     await personal.testing_message(fiat, await msg.answer("Загружаю данные обновления..."))

# symbols = ["USDT"]
# fiats = ["RUB"]
# payTypes = new_parser.parsing_bank(fiat="RUB")[:20]
# while True:
#     df = await new_parser.parse_data(symbols, fiats, payTypes)
#     await new_parser.send_message(msg.from_user.id, df, fiats)
#     new_parser.asyncio.sleep(15)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        process_deposit,
        state=Forms.waiting_for_deposit,
        content_types=types.ContentTypes.TEXT
    )

#     dp.register_message_handler(settings_menu, Text(equals="Настройки"))
#     dp.register_message_handler(support, Text(equals="Поддержка"))
#     dp.register_message_handler(back_to_menu_kb_f, Text(equals="Возврат к меню"))
#     dp.register_message_handler(opovesheniya, Text(equals="Начать оповещения"))
