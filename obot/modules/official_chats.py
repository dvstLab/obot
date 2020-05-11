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

from aiogram.utils.exceptions import MessageToDeleteNotFound

from obot import cache, bot
from obot.decorator import register
from obot.utils.config import CONFIG

from .utils.api_client import get_devices_with_releases, all_devices
from .utils.devices import get_devices_list_text, release_info
from .utils.message import get_cmd, get_args


def is_orangefox_chat(func):
    async def wrapped(*args, **kwargs):
        message = args[0]

        if message.chat.type == 'private':
            return

        chat_id = message.chat.id

        chats = CONFIG['CHATS']
        chats.append(CONFIG['STABLE_CHAT'])
        chats.append(CONFIG['BETA_CHAT'])

        if chat_id not in chats:
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
        message = args[0]
        chat_id = message.chat.id

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


@register(cmd='list')
@is_orangefox_chat
@auto_purge
async def list_devices_p(message):
    chat_id = message.chat.id
    build_type = get_chat_type(chat_id)

    arg = get_args(message)
    if arg and arg[0] == 'beta':
        build_type = 'beta'

    text = f'<b>List of devices which currently have {build_type} releases</b>'

    devices = await get_devices_with_releases(build_type=build_type)
    text += await get_devices_list_text(devices)

    text += '\n\nTo get latest device release write <code>/(codename)</code>, for example: /lavender.'\
            '\n<code>#(codename)</code> and <code>(codename)</code> are supported too.'

    return await message.reply(text)


@register(cmd='\w+', add_cmd_start_symbols='!#')
@is_orangefox_chat
@auto_purge
async def get_release(message):
    build_type = get_chat_type(message.chat.id)

    arg = get_args(message)
    codename = get_cmd(message)

    if codename not in await all_devices(only_codenames=True):
        return

    if arg and arg[0] == 'beta':
        build_type = 'beta'

    text, buttons = await release_info(codename, build_type, 'last')

    if not text:
        return

    return await message.reply(text, reply_markup=buttons)
