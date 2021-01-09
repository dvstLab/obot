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

import difflib
from datetime import datetime
from string import Template
from typing import Union

from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from babel.dates import format_datetime
from orangefoxapi.models import Release, Device
from orangefoxapi.types import ReleaseType

from obot import api


def get_devices_list_text(devices, codename_code=False):
    text = ''
    for device in devices:
        text += f"\n - {device.full_name}"
        if codename_code:
            text += f" (<code>{device.codename}</code>)"
        else:
            text += f" (/{device.codename})"

    return text


async def get_codenames(release_type: Union[ReleaseType, None]) -> list:
    codenames = []
    for device in await api.devices(release_type=release_type):
        codenames.append(device.codename)

    return codenames


async def get_device_names() -> dict:
    data = {}
    for device in await api.devices():
        data[device.id] = f"{device.full_name} (<code>{device.codename}</code>)"

    return data


async def get_oems() -> dict:
    oems = await api.oems()

    data = {}
    for oem in oems:
        data[oem.lower()] = oem

    return data


async def nothing_matching(strings, value) -> str:
    codenames = await get_codenames(None)
    oems = await get_oems()

    text = Template(strings['nothing_is_found_text']).substitute(value=value)

    possibilities: list = codenames
    possibilities.extend(oems.keys())
    if match_codename := difflib.get_close_matches(value, codenames, n=1, cutoff=0.7):
        text += Template(strings['did_you_mean']).substitute(possible=match_codename[0])

    return text


async def release_info(strings: dict, release: Release, device: Device = None):
    if not device:
        device: Device = await api.device(id=release.device_id)

    text = Template(strings['release_text']).substitute(
        fullname=device.full_name,
        codename=device.codename,
        version=release.version,
        release_type=release.type,
        date=format_datetime(datetime.fromtimestamp(release.date), locale=strings['babel'].language),
        changelog='\n    - '.join(release.changelog)
    )

    if release.notes:
        text += Template(strings['release_notes']).substitute(url=release.url + '/buildnotes')
    if release.bugs:
        text += Template(strings['release_bugs']).substitute(url=release.url + '/bugs')

    buttons = InlineKeyboardMarkup().add(InlineKeyboardButton(
        strings['release_dl_btn'],
        url=release.url
    ))

    return text, buttons
