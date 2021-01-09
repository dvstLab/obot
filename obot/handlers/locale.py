import re
from string import Template

from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from tinydb import Query

from obot import dp
from obot.utils.strings import LANGUAGES, table

lang_cb = CallbackData('select_lang', 'lang')


@dp.message_handler(commands='lang', chat_holder='pm')
@dp.message_handler(commands='lang', chat_holder=['other', 'official'], is_chat_admin=True)
@dp.channel_post_handler(regexp=re.compile('^/lang'))
async def select_locale(message: types.Message, strings: dict = {}):
    text = Template(strings['current_locale']).substitute(
        emoji=strings['flag'],
        language=strings['babel'].language_name
    ) + strings['select_locale']

    buttons = InlineKeyboardMarkup(row_width=2)

    for lang in LANGUAGES:
        buttons.insert(InlineKeyboardButton(
            Template(strings['select_btn']).substitute(
                emoji=strings['flag'],
                language=strings['babel'].language_name
            ),
            callback_data=lang_cb.new(lang=lang)
        ))

    await message.reply(text, reply_markup=buttons)


@dp.callback_query_handler(lang_cb.filter(), chat_type='private')
@dp.callback_query_handler(lang_cb.filter(), is_chat_admin=True)
async def set_locale(query: types.CallbackQuery, callback_data: dict):
    lang = callback_data['lang']
    strings = LANGUAGES[lang]
    text = strings['lang_selected']

    chat = Query()
    chat_id = query.message.chat.id
    table.upsert({'chat_id': chat_id, 'lang': lang}, chat.chat_id == chat_id)

    await query.message.edit_text(text)
