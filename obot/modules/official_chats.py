# Copyright (C) 2019 The Raphielscape Company LLC.
# Copyright (C) 2018 - 2020 MrYacha
# Copyright (C) 2018 - 2020 Sophie
# Copyright (C) 2020 oBOT
#
# This file is part of oBOT.
#
# oBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

from .utils.api_client import avaible_stable_releases, avaible_beta_releases
from .utils.devices import get_devices_list_text_from_codenames, get_last_build

from obot.utils.config import CONFIG
from obot.decorator import register
from obot import cache, bot


def is_orangefox_chat(func):
    async def wrapped(*args, **kwargs):
        message = args[0]

        if message.chat.type == 'private':
            return

        chat_id = message.chat.id
        if chat_id not in CONFIG['CHATS']:
            return

        return await func(*args, **kwargs)
    return wrapped


def get_chat_type(chat_id):
    chat_type = 'stable'
    if chat_id == CONFIG['BETA_CHAT']:
        chat_type = 'beta'
    
    return chat_type

def auto_purge(func):
    async def wrapped(*args, **kwargs):
        sended_msg = await func(*args, **kwargs)

        message = args[0]
        chat_id = message.chat.id
        msg_id = message.message_id

        bot_msg_key = 'last_bot_msg_' + str(chat_id)
        if d := await cache.get(bot_msg_key):
            await bot.delete_message(chat_id, d)

        user_msg_key = 'last_user_msg_' + str(chat_id)
        if d := await cache.get(user_msg_key):
            await bot.delete_message(chat_id, d)

        if 'message_id' in sended_msg:
            await cache.set(bot_msg_key, sended_msg.message_id)
        if 'message_id' in message:
            await cache.set(user_msg_key, message.message_id)

    return wrapped

@register(cmd='list')
@is_orangefox_chat
@auto_purge
async def list_devices_p(message):
    chat_id = message.chat.id
    chat_type = get_chat_type(chat_id)

    text = f'<b>List of devices which currently have {chat_type} releases</b>'

    if chat_type == 'stable':
        codenames = await avaible_stable_releases()
    else:
        codenames = await avaible_beta_releases()

    text += await get_devices_list_text_from_codenames(codenames)
    text += "\n\nTo get latest device release write /'codename', for example: /lavender"

    return await message.reply(text)


@register(regexp='^[/!#]')
@is_orangefox_chat
@auto_purge
async def get_release(message):
    btype = get_chat_type(message.chat.id)

    arg = message.get_args()
    codename = message.text.split(' ' + arg)[0][1:].lower()

    if arg and arg.split(' ')[0].lower() == 'beta':
        btype = 'beta'

    text, buttons = await get_last_build(codename, btype)
    
    if not text:
        return

    return await message.reply(text, reply_markup=buttons)