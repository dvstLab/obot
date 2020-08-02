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

import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from obot.utils.chats import get_chat_holder


class ChatType(BoundFilter):
    key = 'chat_type'

    def __init__(self, chat_type: typing.Union[list, str]):
        if isinstance(chat_type, str):
            chat_type = [chat_type]
        self.chat_type = chat_type

    async def check(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_type


class ChatHolder(BoundFilter):
    key = 'chat_holder'

    def __init__(self, chat_holder: typing.Union[list, str]):
        if isinstance(chat_holder, str):
            chat_holder = [chat_holder]
        self.chat_holder = chat_holder

    async def check(self, message: types.Message) -> bool:
        holder = await get_chat_holder(message)

        if holder in self.chat_holder:
            return True

        return False
