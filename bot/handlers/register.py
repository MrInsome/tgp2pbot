from aiogram import Dispatcher

from .other import register_inline_msg_handlers
from .user import register_user_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_handlers,
        register_inline_msg_handlers,
    )
    for handler in handlers:
        handler(dp)
