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
from datetime import datetime

from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from babel.dates import format_datetime
from orangefoxapi.types import ReleaseType

from obot import dp, api
from obot.utils.devices import release_info


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery, strings: dict = {}):
    codename = inline_query.query.lower().split(' ')[0]
    if not codename:
        return await inline_query.answer([])

    if not (device := await api.device(codename=codename)):
        return await inline_query.answer([])

    # Get beta/stable releases
    releases = []
    if release := await api.releases(device_id=device.id, type=ReleaseType.stable):
        releases.append(release.data[0])
    if release := await api.releases(device_id=device.id, type=ReleaseType.beta):
        releases.append(release.data[0])

    result = []

    for release in releases:
        release = await api.release(id=release.id)
        text, buttons = await release_info(strings, release, device=device)
        result.append(
            InlineQueryResultArticle(
                id=hashlib.md5(f"{codename}_{release.type}".encode()).hexdigest(),
                title=f"{strings[release.type]}: {release.version}",
                description=format_datetime(datetime.fromtimestamp(release.date), locale=strings['babel'].language),
                input_message_content=InputTextMessageContent(text, disable_web_page_preview=True),
                reply_markup=buttons
            )
        )

    return await inline_query.answer(result)
