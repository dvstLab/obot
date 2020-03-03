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

from obot.decorator import register

def is_pm(func):
    async def wrapped(*args, **kwargs):
        message = args[0]

        if message.chat.type == 'private':
            return await func(*args, **kwargs)

        return
    return wrapped


@register(cmd='start')
@is_pm
async def start(message):
    text = "Hi, I'm a OrangeFox Recovery official bot, here is what I can do:"
    text += "\n - /start: This message"
    text += "\n - /list: List of supported devices"
    text += "\n - /listbeta: List of avaible beta devices"
    text += "\n - /'codename': Get latest build info and download links, for example: /lavender"
    text += "\n\n Developed by Yacha"

    await message.reply(text)


@register(cmd='list')
@is_pm
async def start(message):
    text = f'<b>List of devices which currently have stable releases</b>'

    codenames = await avaible_stable_releases()
    text += await get_devices_list_text_from_codenames(codenames)

    text += "\n\nTo get latest device release write /'codename', for example: /lavender"
    text += "\nIf you want see beta devices list write /listbeta"

    await message.reply(text)


@register(cmd='listbeta')
@is_pm
async def start(message):
    text = f'<b>List of devices which currently have beta releases</b>'

    codenames = await avaible_beta_releases()
    text += await get_devices_list_text_from_codenames(codenames)

    text += "\n\nTo get latest device release write <code>/'codename' beta</code>, for example: <code>/lavender beta</code>"
    text += "\nIf you want see stable devices list write /list"

    await message.reply(text)


@register(regexp='^[/!#]')
@is_pm
async def get_release(message):
    btype = 'stable'
    arg = message.get_args()
    codename = message.text.split()[0][1:].lower()

    if arg and arg.split(' ')[0].lower() == 'beta':
        btype = 'beta'
    
    text, buttons = await get_last_build(codename, btype)
    
    if not text:
        return

    await message.reply(text, reply_markup=buttons)


