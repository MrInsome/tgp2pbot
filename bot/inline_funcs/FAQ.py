from aiogram import types

from bot.keyboards.inline import back_to_menu_kb_t


async def faq_func(msg: types.Message):
    await msg.edit_caption("FAQ", reply_markup=back_to_menu_kb_t)
