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

import hashlib

from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from obot.utils.api_client import api
from obot.utils.devices import get_devices_list_text, release_info

from obot.utils.strings import get_strings

from obot import dp


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    request = inline_query.query
    strings = await get_strings(inline_query.from_user.id)

    if not request:
        articles = []

        stable_devices_text = strings['inline_list_title'].format(build_type=strings['stable'])
        devices = await api.get_devices_with_releases(release_type='stable')
        stable_devices_text += await get_devices_list_text(devices, codename_code=True)
        stable_devices_text += strings['inline_get']

        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'stable').encode()).hexdigest(),
                title=strings['list_title'].format(build_type=strings['stable']),
                description=strings['inline_list_desk'].format(build_type=strings['stable']),
                input_message_content=InputTextMessageContent(stable_devices_text)
            )
        )

        beta_devices_text = strings['inline_list_title'].format(build_type=strings['beta'])
        devices = await api.get_devices_with_releases(release_type='beta')
        beta_devices_text += await get_devices_list_text(devices, codename_code=True)
        stable_devices_text += strings['inline_get']

        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'beta').encode()).hexdigest(),
                title=strings['list_title'].format(build_type=strings['beta']),
                description=strings['inline_list_desk'].format(build_type=strings['beta']),
                input_message_content=InputTextMessageContent(beta_devices_text)
            )
        )
        return await inline_query.answer(results=articles, cache_time=100)

    codename = request.split(' ')[0].lower()
    if codename not in await api.list_devices(only_codenames=True):
        return await inline_query.answer([])

    device = await api.get_device(codename)
    articles = []

    text, buttons = await release_info(codename, 'stable', 'last')
    articles.append(
        InlineQueryResultArticle(
            id=hashlib.md5((request + 'stable').encode()).hexdigest(),
            title=strings['inline_release_title'].format(
                fullname=device["fullname"],
                codename=device["codename"]
            ),
            input_message_content=InputTextMessageContent(text),
            reply_markup=buttons
        )
    )

    text, buttons = await release_info(codename, 'beta', 'last')
    if text:
        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'beta').encode()).hexdigest(),
                title=strings['inline_release_title'].format(
                    fullname=device["fullname"],
                    codename=device["codename"]
                ),
                input_message_content=InputTextMessageContent(text),
                reply_markup=buttons
            )
        )

    return await inline_query.answer(results=articles, cache_time=100)
