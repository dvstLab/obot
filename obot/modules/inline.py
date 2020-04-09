import hashlib

from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

from .utils.api_client import available_stable_releases, available_beta_releases, details, all_codenames
from .utils.devices import get_devices_list_text_from_codenames, get_last_build

from obot import dp


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    request = inline_query.query

    if not request:
        articles = []

        stable_devices_text = "<b>Devices with Stable releases available:</b>"
        stable_devices_text += await get_devices_list_text_from_codenames(await available_stable_releases())
        stable_devices_text += "\n\nWrite <code>@ofoxr_bot codename</code> to get the last release"

        articles.append(
            InlineQueryResultArticle(
                id=hashlib.md5((request + 'stable').encode()).hexdigest(),
                title='Devices with Stable releases available',
                description="This will send a list of devices which have stable releases",
                input_message_content=InputTextMessageContent(stable_devices_text)
            )
        )

        beta_devices_text = "<b>Devices with Beta releases available:</b>"
        beta_devices_text += await get_devices_list_text_from_codenames(await available_beta_releases())
        beta_devices_text += "\n\nWrite <code>@ofoxr_bot codename</code> to get the last release"

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
    if codename not in await all_codenames():
        return await inline_query.answer([])

    device = await details(codename)
    articles = []

    text, buttons = await get_last_build(codename, 'stable')
    articles.append(
        InlineQueryResultArticle(
            id=hashlib.md5((request + 'stable').encode()).hexdigest(),
            title=f'Latest Stable release for {device["fullname"]} ({device["codename"]})',
            input_message_content=InputTextMessageContent(text),
            reply_markup=buttons
        )
    )

    text, buttons = await get_last_build(codename, 'beta')
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
