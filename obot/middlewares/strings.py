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
from aiogram.dispatcher.middlewares import BaseMiddleware

from obot.utils.strings import get_strings


class StringsMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        chat_id = message.chat.id

        strings = await get_strings(chat_id)
        data['strings'] = strings


    async def on_process_channel_post(self, message: types.Message, data: dict):
        chat_id = message.chat.id

        strings = await get_strings(chat_id)
        data['strings'] = strings
