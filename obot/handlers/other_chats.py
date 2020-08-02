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


from obot.utils.api_client import api
from obot.utils.devices import get_devices_list_text, release_info

from obot import dp


@dp.message_handler(commands=['start', 'help'], chat_holder='other')
async def start_cmd(message, strings={}):
    await message.reply(strings['other_chats_start'])


@dp.message_handler(commands=['orangefox', 'fox', 'of', 'ofox', 'ofoxr'], chat_holder='other')
async def orangefox_cmd(message, strings={}):
    build_type = 'stable'
    arg = message.get_args()
    if not arg:
        text = strings['list_title'].format(build_type=strings[build_type])
        text += await get_devices_list_text(
            await api.get_devices_with_releases(release_type=build_type), codename_code=True
        )
        text += strings['other_chats_get']

        return await message.reply(text)

    codename = arg.split(' ')[0].lower()
    if codename not in await api.list_devices(only_codenames=True):
        return await message.reply(strings['other_chats_404'])

    text, buttons = await release_info(codename, build_type, 'last')

    return await message.reply(text, reply_markup=buttons)
