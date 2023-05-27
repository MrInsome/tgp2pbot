from aiogram import types

from bot.keyboards.inline import back_to_menu_kb_t


async def support_func(msg: types.Message):
    support_chat_id = '@hamsteroney'

    await msg.edit_caption(f'Ваши вопросы и предложения могут быть отправлены в чат поддержки: {support_chat_id}',
                           reply_markup=back_to_menu_kb_t
                           )
