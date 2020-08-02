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

from tinydb import Query

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from obot import db


db_chats = db.table('chats')


class ChatMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        chat_id = message.chat.id

        query = Query()
        if db_chats.search(query.chat_id == chat_id):
            return

        db_chats.insert({'chat_id': chat_id})
