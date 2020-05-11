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

from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from obot.decorator import register
from obot.version import OBOT_VERSION
from .utils.api_client import get_all_oems, get_oem_devices, get_devices_with_releases, all_devices
from .utils.devices import get_devices_list_text, release_info
from .utils.message import get_cmd, get_args


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
    text = f'Hi, I\'m a OrangeFox Recovery official bot (<code>{OBOT_VERSION}</code>), here is what I can do for you:' \
           '\n - /start: This message' \
           '\n - /list: This shows you a list of supported devices.' \
           '\n - <code>/list beta</code>: This shows you list of available devices that are in beta.' \
           '\n - <code>/(codename)</code>: Get latest stable build info and download links, for example: /lavender' \
           '\n - <code>/(codename) beta</code>: Same as above, but will I will show you a beta build.' \
           '\n - <code>/(codename) last</code>: Same as the two above, but I will show you the latest build from the ' \
           'beta or stable list.' \
           '\n - <code>/(OEM)</code>: This will show you all devices from that OEM, that have stable releases, ' \
           'for example: /Xiaomi .' \
           '\n - <code>/(OEM) beta</code>: This will show you all devices with available beta releases from that OEM.' \
           '\n' \
           '\n - Supports non-OrangeFox chats, add me in your chats and write /start to get help' \
           '\n - I support inline mode, try to type <code>@ofoxr_bot</code> in any chat where inline is <b>NOT</b> ' \
           'disabled.' \
           '\n' \
           '\nMade by @MrYacha' \
           ' | powered by <a href="api.orangefox.tech">OrangeFox API</a>' \
           ' | <a href="https://gitlab.com/OrangeFox/site/obot">Sources</a>' \
           '\nRuns on <a href="https://www.ua-hosting.company">ua-hosting.company</a>\'s servers'

    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(InlineKeyboardButton(
        '⬇️ OrangeFox Recovery Downloads website',
        url='https://t.me/OrangeFoxNEWS'
    ))
    buttons.insert(InlineKeyboardButton(
        '📝 OrangeFox Recovery NEWS',
        url='https://t.me/OrangeFoxNEWS'
    ))
    buttons.insert(InlineKeyboardButton(
        '🆕 OrangeFox Recovery Updates',
        url='https://t.me/OrangeFoxUpdates'
    ))
    buttons.insert(InlineKeyboardButton(
        '💬 OrangeFox Recovery Support chat',
        url='https://t.me/OrangeFoxChat'
    ))

    await message.reply(text, disable_web_page_preview=True, reply_markup=buttons)


@register(cmd='list')
@is_pm
async def start(message):
    build_type = 'stable'
    arg = get_args(message)
    if arg and arg[0] == 'beta':
        build_type = 'beta'
    elif arg and arg[0] == 'any':
        build_type = 'any'

    text = f'<b>List of devices which currently have {build_type} releases</b>'

    devices = await get_devices_with_releases(build_type=build_type)
    text += await get_devices_list_text(devices)

    text += "\n\nTo get latest stable release write <code>/(codename)</code>, for example: /lavender"
    if build_type != 'beta':
        text += "\nIf you want see beta devices list write <code>/list beta</code>"

    await message.reply(text)


@register(cmd='\w+', add_cmd_start_symbols='!#')
@is_pm
async def pm_get_release(message):
    build_type = 'stable'
    codename = get_cmd(message)

    if codename not in await all_devices(only_codenames=True):
        return

    arg = get_args(message)
    if arg and arg[0] == 'beta':
        build_type = 'beta'
    elif arg and arg[0] == 'last':
        build_type = 'last'

    text, buttons = await release_info(codename, build_type, 'last')

    if not text:
        return

    await message.reply(text, reply_markup=buttons)


@register(cmd='\w+', add_cmd_start_symbols='!#')
@is_pm
async def pm_get_oem(message):
    oem_name = get_cmd(message)
    if oem_name not in (name.lower() for name in await get_all_oems()):
        return

    build_type = 'stable'
    arg = get_args(message)
    if arg and arg[0] == 'beta':
        build_type = 'beta'
    elif arg and arg[0] == 'any':
        build_type = 'any'

    text = f'<b>List of devices by {oem_name} which currently have {build_type} releases</b>'

    all_devices = await get_oem_devices(oem_name)
    devices = None

    if build_type != 'any':
        devices = await get_devices_with_releases(build_type=build_type, only_codenames=True)

    text += await get_devices_list_text(all_devices, devices_filter=devices)

    text += "\n\nTo get latest stable release write <code>/(codename)</code>, for example: /lavender"
    if build_type != 'beta':
        text += "\nIf you want see beta devices list write <code>/(OEM) beta</code>, for example: /Xiaomi"
    text += "\nIf you want see list of all devices write /list"

    await message.reply(text)
