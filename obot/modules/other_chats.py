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


from .utils.api_client import get_devices_with_releases, all_devices
from .utils.devices import get_devices_list_text, release_info

from obot.decorator import register
from obot.utils.config import CONFIG


def is_other_chat(func):
    async def wrapped(*args, **kwargs):
        message = args[0]

        if message.chat.type == 'private':
            return

        chat_id = message.chat.id

        fox_chats = CONFIG['CHATS']
        fox_chats.append(CONFIG['STABLE_CHAT'])
        fox_chats.append(CONFIG['BETA_CHAT'])

        if chat_id in fox_chats:
            return

        return await func(*args, **kwargs)

    return wrapped


@register(cmd='start|help')
@is_other_chat
async def start(message):
    text = 'Hi, I\'m the official OrangeFox Recovery bot, here is what I can do for non-OrangeFox chats:' \
           '\n - /start: This will start me up and show you this message.' \
           '\n - /orangefox: This will show you a list of devices with official stable releases available.' \
           '\n - <code>/orangefox (codename)</code>: This will get you the latest stable build, for example: ' \
           '"/orangefox lavender"' \
           '\nInstead of the <code>/orangefox</code> command, you can use any of this aliases:' \
           '\n/fox, /of, /ofox, /ofoxr' \
           '\nI only support stable releases, if you want to get beta releases - PM me.' \
           '\n' \
           '\nPM me and type /start if you want see more information about me.'

    await message.reply(text)


@register(cmd='orangefox|fox|of|ofox|ofoxr')
@is_other_chat
async def orangefox_cmd(message):
    build_type = 'stable'
    arg = message.get_args()
    if not arg:
        text = f'<b>List of devices which currently have stable releases</b>'
        devices = await get_devices_with_releases(build_type=build_type)
        text += await get_devices_list_text(devices)
        text += "\n\nTo get latest device release write /orangefox (codename), for example: /orangefox lavender."

        return await message.reply(text)

    codename = arg.split(' ')[0].lower()
    if codename not in await all_devices(only_codenames=True):
        return await message.reply('This device is not supported! To see a list of devices write /orangefox.')

    text, buttons = await release_info(codename, build_type, 'last')

    return await message.reply(text, reply_markup=buttons)
