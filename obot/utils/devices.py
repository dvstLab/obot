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

from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from .api_client import api


async def get_devices_list_text(devices, codename_code=False):
    text = ''
    for device in devices:
        text += f"\n - {device['fullname']}"
        if codename_code:
            text += f" (<code>{device['codename']}</code>)"
        else:
            text += f" (/{device['codename']})"

    return text


async def release_info(codename, build_type, version):
    if build_type == 'last':
        build_type = None

    device = await api.get_device(codename)
    if not device:
        return None, None

    release = await api.get_device_release(codename, version=version, release_type=build_type)
    if not release:
        return None, None

    maintained_list = {
        1: f"<b>Maintainer:</b> {device['maintainer']['name']}, Maintained",
        2: f"<b>Maintainer:</b> {device['maintainer']['name']}, Maintained without having device on hands",
        3: f"<b>⚠️ Not maintained! Previous maintainer:</b> {device['maintainer']['name']}"
    }
    maintained = maintained_list[device['maintained']]

    text = f"<b>Latest OrangeFox {release['build_type']} release</b>"
    text += f"\n📱  <b>Device:</b> {device['fullname']} (<code>{device['codename']}</code>)"
    text += f"\n👨‍🔬  {maintained}"
    text += f"\n🔺  <b>Version:</b> <code>{release['version']}</code>"
    text += f"\n💾  <b>Size:</b> {release['size_human']}"
    text += f"\n📅  <b>Date:</b> " + release['date']

    if 'notes' in release:
        text += "\n\n📝 <b>Build notes:</b>\n"
        text += release['notes']

    buttons = InlineKeyboardMarkup().add(InlineKeyboardButton(
        '⬇️ Download',
        url=release['url']
    ))

    return text, buttons
