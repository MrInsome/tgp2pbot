from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.keyboards.reply import back_to_menu_kb
from bot.keyboards.inline import settings


async def settings_menu(msg: types.Message):
    # replacement reply keyboard
    await msg.answer("TODO", reply_markup=back_to_menu_kb) #todo
    await msg.delete()
    await msg.answer("Settings menu", reply_markup=settings)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(settings_menu, Text(equals="Settings"))