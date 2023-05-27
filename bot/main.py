import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

import config
from bot.database.sql_base import TableUser
from bot.handlers import register_all_handlers

database = None


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_handlers(dp)


def start_bot():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    global database
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    database = TableUser("database", "profile")

    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
