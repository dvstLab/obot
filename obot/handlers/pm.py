# Copyright (C) 2017-2020 OrangeFox Recovery
# Copyright (C) 2018 - 2020 MrYacha
# Copyright (C) 2018 - 2020 Sophie
# Copyright (C) 2020 oBOT
#
# This file is part of oBOT.
#
# oBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from obot import VERSION, dp


@dp.message_handler(commands='start', chat_type='private')
async def pm_start(message: types.Message, strings={}):
    text = strings['pm_start_text'].format(version=VERSION)

    buttons = InlineKeyboardMarkup(row_width=2)
    buttons.insert(InlineKeyboardButton(
        strings['pm_btn_upd'],
        url='https://t.me/OrangeFoxUpdates'
    ))
    buttons.insert(InlineKeyboardButton(
        strings['pm_btn_support_chat'],
        url='https://t.me/OrangeFoxChat'
    ))
    buttons.add(InlineKeyboardButton(
        strings['pm_btn_news'],
        url='https://t.me/OrangeFoxNEWS'
    ))
    buttons.add(InlineKeyboardButton(
        strings['pm_btn_dl'],
        url='https://t.me/OrangeFoxNEWS'
    ))

    await message.reply(text, disable_web_page_preview=True, reply_markup=buttons)
