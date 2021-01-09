# Copyright (C) 2017-2020 OrangeFox Recovery
# Copyright (C) 2018 - 2020 MrYacha
# Copyright (C) 2018 - 2020 Sophie
# Copyright (C) 2020 - 2021 oBOT
#
# This file is part of oBOT.
#
# oBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

import re
from string import Template

from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import Message
from orangefoxapi.types import ReleaseType

from obot import dp, api
from obot.utils.devices import release_info, get_devices_list_text, get_codenames, get_oems, nothing_matching
from obot.utils.message import get_release_type, get_arg
from obot.utils.chats import get_chat_holder


@dp.message_handler(commands='list', chat_holder=['pm'])
@dp.message_handler(commands='list', chat_holder=['official'], is_chat_admin=True)
@dp.message_handler(regexp=re.compile(r"^/(?:o(?:range)?)?fox(?:r)?(?: )?(stable|beta)?$"), chat_holder='other')
async def list_devices_cmd(message: Message, strings={}, regexp=None):
    arg = regexp.group(1) if regexp else get_arg(message)
    release_type = get_release_type(message, arg=arg) or ReleaseType.stable
    text = Template(strings['list_title']).substitute(type=strings[release_type.value])

    devices = await api.devices(supported=True, release_type=release_type)
    text += get_devices_list_text(devices)
    text += strings['list_help'] if await get_chat_holder(message) in ['pm'] else strings['other_chats_get']

    return await message.reply(text)


@dp.message_handler(regexp=re.compile(r'^[/!#](\w+)(?: )?(stable|beta)?'), chat_holder='pm')
@dp.message_handler(regexp=re.compile(r'^[/!#](\w+)(?: )?(stable|beta)?'), chat_holder='official', is_chat_admin=True)
@dp.message_handler(regexp=re.compile(r"^/(?:o(?:range)?)?fox(?:r)? (\w+)(?: )?(stable|beta)?"), chat_holder='other')
async def get_release_cmd(message: Message, strings: dict = {}, regexp=None):
    codename = regexp.group(1).lower()
    release_type = get_release_type(message, arg=regexp.group(2)) or ReleaseType.stable

    # If not found device try to search across oems
    if codename not in await get_codenames(None):
        raise SkipHandler()

    device = await api.device(codename=codename)

    if not (releases := (await api.releases(device_id=device.id, type=release_type)).data):
        text = Template(strings['release_found_for_device']).substitute(
            type=strings[release_type.value],
            device_name=device.full_name,
            url=device.url
        )
        return await message.reply(text)

    release = await api.release(id=releases[0].id)

    text, buttons = await release_info(strings, release, device=device)
    return await message.reply(text, reply_markup=buttons, disable_web_page_preview=True)


@dp.message_handler(regexp=re.compile(r'^[/!#](\w+)(?: )?(stable|beta)?'), chat_holder='pm')
@dp.message_handler(regexp=re.compile(r'^[/!#](\w+)(?: )?(stable|beta)?'), chat_holder='official', is_chat_admin=True)
@dp.message_handler(regexp=re.compile(r"^/(?:o(?:range)?)?fox(?:r)? (\w+)(?: )?(stable|beta)?"), chat_holder='other')
async def get_oem_cmd(message: Message, strings={}, regexp=None):
    oem_name = regexp.group(1).lower()

    if oem_name not in (oems := await get_oems()).keys():
        return await message.reply(await nothing_matching(strings, oem_name))

    release_type = get_release_type(message, arg=regexp.group(2)) or ReleaseType.stable

    devices = await api.devices(oem_name=oems[oem_name])

    text = Template(strings['list_oem_title']).substitute(
        oem=oems[oem_name],
        type=strings[release_type.value]
    )
    text += get_devices_list_text(devices)
    text += strings['list_help'] if await get_chat_holder(message) in ['pm'] else strings['other_chats_get']

    return await message.reply(text)
