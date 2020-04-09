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


from .utils.api_client import available_stable_releases, all_codenames
from .utils.devices import get_devices_list_text_from_codenames, get_last_build

from obot.decorator import register
from obot.utils.config import CONFIG


def is_other_chat(func):
    async def wrapped(*args, **kwargs):
        print('test')
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


@register(cmd='start')
@is_other_chat
async def start(message):
    text = "Hi, I'm a OrangeFox Recovery official bot, here is what I can do:"
    text += "\n - /start: This message"
    text += "\n - /orangefox: List of devices with official Stable releases available"
    text += "\n - /orangefox (codename): Gets latest Stable build"
    text += "\nInstead of <code>/orangefox</code> command you can use any of this aliases:"
    text += "\n/fox, /of, /ofox, /ofoxr"
    text += '\n\nPM to me and write /start if you want see more info about me.'

    await message.reply(text)


@register(cmd='orangefox|fox|of|ofox|ofoxr')
@is_other_chat
async def orangefox_cmd(message):
    arg = message.get_args()
    if not arg:
        text = f'<b>List of devices which currently have Stable releases</b>'
        text += await get_devices_list_text_from_codenames(await available_stable_releases())
        text += "\n\nTo get latest device release write /orangefox (codename), for example: /orangefox lavender."

        return await message.reply(text)

    codename = arg.split(' ')[0].lower()
    if codename not in await all_codenames():
        return await message.reply('This device is not supported! To see a list of devices write /orangefox.')

    text, buttons = await get_last_build(codename, 'stable')

    return await message.reply(text, reply_markup=buttons)
