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

from operator import itemgetter

from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from .api_client import get_device, get_release


async def get_devices_list_text(devices, devices_filter=None):
    text = ''
    for device in devices:
        if devices_filter:
            print(device)
            if device['codename'] not in devices_filter:
                continue

        text += f"\n- {device['fullname']} (/{device['codename']})"

    return text


async def release_info(codename, build_type, version):
    if build_type == 'last':
        build_type = None

    device = await get_device(codename)
    if not device:
        return None, None

    release = await get_release(codename, version, build_type=build_type)
    if not release:
        return None, None

    maintained = ''
    if device['maintained'] == 1:
        maintained = f"Maintainer: {device['maintainer']['name']}, Maintained"
    elif device['maintained'] == 2:
        maintained = f"Maintainer: {device['maintainer']['name']}, Maintained without having device on hands"
    elif device['maintained'] == 3:
        maintained = f"⚠️ Not maintained! Previous maintainer: {device['maintainer']['name']}"

    text = f"<b>Latest OrangeFox Recovery {release['build_type']} release</b>"
    text += f"\n📱 Device: {device['fullname']} (<code>{device['codename']}</code>)"
    text += f"\n🔺 Version: <code>{release['version']}</code>"
    text += f"\n👨‍🔬 {maintained}"
    text += f"\n📄 <code>{release['file_name']}</code>: {release['size_human']}"
    text += f"\n📅 Release date: " + release['date']
    text += f"\n✅ File MD5: <code>{release['md5']}</code>"

    if 'notes' in release:
        text += "\n\n📝 <b>Build notes:</b>\n"
        text += release['notes']

    buttons = InlineKeyboardMarkup().add(InlineKeyboardButton(
        '⬇️ Download',
        url=release['url']
    ))

    if 'sf' in release:
        buttons.insert(
            InlineKeyboardButton(
                '☁️ Mirror',
                url=release['sf']['url']
            )
        )

    return text, buttons
