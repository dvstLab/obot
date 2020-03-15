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

from operator import itemgetter

from .api_client import (
    list_devices,
    all_codenames,
    available_stable_releases,
    available_beta_releases,
    details,
    last_stable_release,
    last_beta_release
)


async def get_devices_list_text_from_codenames(codenames):
    devices_info = await list_devices()
    devices = []
    for codename in codenames:
        data = [element for element in devices_info if element['codename'] == codename]
        if not data:
            continue
        data = data[0]
        fullname = data['fullname']
        devices.append((fullname, codename))

    text = ''
    for device in sorted(devices, key=itemgetter(0)):
        text += f'\n- {device[0]} (<code>{device[1]}</code>)'

    return text


async def get_last_build(codename, build_type):
    if codename not in await all_codenames():
        return None, None
    
    if build_type == 'stable':
        if codename not in await available_stable_releases():
            return None, None
    elif build_type == 'beta':
        if codename not in await available_beta_releases():
            return None, None
    
    device_info = await details(codename)
    last_build = await last_stable_release(codename) if build_type == 'stable' else await last_beta_release(codename)

    maintained = ''
    if device_info['maintained'] == 1:
        maintained = f"\nMaintainer: {device_info['maintainer']}, Maintained"
    elif device_info['maintained'] == 2:
        maintained = f"\nMaintainer: {device_info['maintainer']}, Maintained without having device on hands"
    elif device_info['maintained'] == 3:
        maintained = f"\n⚠️ Not maintained! Previous maintainer: {device_info['maintainer']}"

    text = f"<b> Latest OrangeFox Recovery {build_type} release</b>"
    text += maintained
    text += f"\n🔺 Version: <code>{last_build['version']}</code>"
    text += f"\n👨‍🔬 Maintainer: {device_info['maintainer']}, {maintained}"
    text += f"\n📄 <code>{last_build['file_name']}</code>: {last_build['size_human']}"
    text += f"\n✅ File MD5: <code>{last_build['md5']}</code>"

    if 'notes' in last_build:
        text += "\n\n📝 <b>Build notes:</b>\n"
        text += last_build['notes']

    buttons = InlineKeyboardMarkup().add(InlineKeyboardButton(
        '⬇️ Download',
        url=last_build['url']
    ))

    if 'sf' in last_build:
        buttons.insert(
            InlineKeyboardButton(
                '☁️ Mirror',
                url=last_build['sf']['url']
            )
        )

    return text, buttons