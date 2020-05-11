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

import hashlib

from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from .utils.api_client import get_devices_with_releases, all_devices, get_device
from .utils.devices import get_devices_list_text, release_info

from obot import dp


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    request = inline_query.query

    if not request:
        articles = []

        stable_devices_text = "<b>Devices with Stable releases available:</b>"
        devices = await get_devices_with_releases(build_type='stable')
        stable_devices_text += await get_devices_list_text(devices)
        stable_devices_text += "\n\nWrite <code>@ofoxr_bot (codename)</code> to get the last release"

        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'stable').encode()).hexdigest(),
                title='Devices with Stable releases available',
                description="This will send a list of devices which have stable releases",
                input_message_content=InputTextMessageContent(stable_devices_text)
            )
        )

        beta_devices_text = "<b>Devices with Beta releases available:</b>"
        devices = await get_devices_with_releases(build_type='beta')
        beta_devices_text += await get_devices_list_text(devices)
        beta_devices_text += "\n\nWrite <code>@ofoxr_bot (codename)</code> to get the last release"

        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'beta').encode()).hexdigest(),
                title='Devices with Beta releases available',
                description="Same as above, but for beta releases",
                input_message_content=InputTextMessageContent(beta_devices_text)
            )
        )
        return await inline_query.answer(results=articles, cache_time=100)

    codename = request.split(' ')[0].lower()
    if codename not in await all_devices(only_codenames=True):
        return await inline_query.answer([])

    device = await get_device(codename)
    articles = []

    text, buttons = await release_info(codename, 'stable', 'last')
    articles.append(
        InlineQueryResultArticle(
            id=hashlib.md5((request + 'stable').encode()).hexdigest(),
            title=f'Latest Stable release for {device["fullname"]} ({device["codename"]})',
            input_message_content=InputTextMessageContent(text),
            reply_markup=buttons
        )
    )

    text, buttons = await release_info(codename, 'beta', 'last')
    if text:
        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'beta').encode()).hexdigest(),
                title=f'Latest Beta release for {device["fullname"]} ({device["codename"]})',
                input_message_content=InputTextMessageContent(text),
                reply_markup=buttons
            )
        )

    return await inline_query.answer(results=articles, cache_time=100)
