from aiogram import Dispatcher, types

from bot.inline_funcs.handlers import process_deposit, Forms, process_percent


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(
        process_deposit,
        state=Forms.waiting_for_deposit,
        content_types=types.ContentTypes.TEXT
    )
    dp.register_message_handler(
        process_percent,
        state=Forms.waiting_for_percent,
        content_types=types.ContentTypes.TEXT
    )

