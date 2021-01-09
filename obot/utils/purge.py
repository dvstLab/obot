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

from functools import wraps

from aiogram.utils.exceptions import MessageToDeleteNotFound

from obot import cache, bot
from obot.utils.chats import get_chat_holder


def auto_purge(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        message = args[0]
        chat_id = message.chat.id

        chat_holder = await get_chat_holder(message)

        if chat_holder == 'pm':
            await func(*args, **kwargs)
            return

        elif chat_holder not in ['stable', 'beta', 'official']:
            return

        bot_msg_key = 'last_bot_msg_' + str(chat_id)
        user_msg_key = 'last_user_msg_' + str(chat_id)

        sent_msg = await func(*args, **kwargs)

        if sent_msg and 'message_id' in sent_msg:
            if bot_msg := await cache.get(bot_msg_key):
                try:
                    await bot.delete_message(chat_id, bot_msg)
                except MessageToDeleteNotFound:
                    pass

            if user_msg := await cache.get(user_msg_key):
                try:
                    await bot.delete_message(chat_id, user_msg)
                except MessageToDeleteNotFound:
                    pass

            await cache.set(bot_msg_key, sent_msg.message_id)

            if 'message_id' in message:
                await cache.set(user_msg_key, message.message_id)

    return wrapped
