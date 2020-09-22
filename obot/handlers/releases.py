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

import re

from aiogram.types import Message
from aiogram.dispatcher.handler import SkipHandler

from obot import dp
from obot.utils.api_client import api
from obot.utils.devices import release_info, get_devices_list_text
from obot.utils.message import get_cmd, get_args
from obot.utils.chats import get_chat_holder
from obot.utils.purge import auto_purge


@dp.message_handler(commands='list', chat_holder=['official', 'stable', 'beta', 'pm'], is_chat_admin=True)
@auto_purge
async def list_devices_cmd(message: Message, strings={}):
    release_type = 'stable'

    chat_id = message.chat.id
    if (chat_holder := await get_chat_holder(message)) in ['stable', 'beta']:
        release_type = chat_holder

    if arg := get_args(message):
        if arg[0] == 'beta':
            release_type = 'beta'
        elif arg[0] == 'any':
            release_type = 'any'

    build_type_text = strings[release_type]

    text = strings['list_title'].format(build_type=build_type_text)

    text += await get_devices_list_text(await api.get_devices_with_releases(release_type=release_type))

    text += strings['list_help']
    if release_type != 'beta':
        text += strings['list_help_beta']

    return await message.reply(text)


@dp.message_handler(regexp=re.compile(r'[/!#]\w+'), chat_holder=['official', 'stable', 'beta', 'pm'], is_chat_admin=True)
@auto_purge
async def get_release_cmd(message: Message):
    build_type = 'stable'
    codename = get_cmd(message)

    # Device not found - let's try to get OEM
    if codename not in await api.list_devices(only_codenames=True):
        raise SkipHandler()

    chat_id = message.chat.id
    if (chat_holder := await get_chat_holder(message)) in ['stable', 'beta']:
        build_type = chat_holder

    if arg := get_args(message):
        if arg[0] == 'beta':
            build_type = 'beta'
        elif arg[0] == 'last' or arg[0] == 'any':
            build_type = 'last'

    text, buttons = await release_info(codename, build_type, 'last')

    if not text:
        return

    return await message.reply(text, reply_markup=buttons)


@dp.message_handler(regexp=re.compile(r'[/!#]\w+'), chat_holder=['official', 'stable', 'beta', 'pm'], is_chat_admin=True)
@auto_purge
async def get_oem_cmd(message: Message, strings={}):
    oem_name = get_cmd(message)

    # Get right OEM name as curent one can have wrong case.
    oem = None
    for c_oem in await api.list_oems():
        if oem_name.lower() == c_oem.lower():
            oem = c_oem
    # OEM not found - nothing to do.
    if not oem:
        return

    build_type = 'stable'
    chat_id = message.chat.id
    if (chat_holder := await get_chat_holder(message)) in ['stable', 'beta']:
        build_type = chat_holder

    if arg := get_args(message):
        if arg[0] == 'beta':
            build_type = 'beta'
        elif arg[0] == 'any':
            build_type = 'any'

    text = strings['list_oem_title'].format(
        oem_name=oem_name,
        build_type=strings[build_type]
    )

    text += await get_devices_list_text(await api.get_oem_devices_with_releases(oem, release_type=build_type))

    text += strings['list_help']
    if build_type != 'beta':
        text += strings['list_help_beta']
    text += strings['list_oem_help']

    return await message.reply(text)
