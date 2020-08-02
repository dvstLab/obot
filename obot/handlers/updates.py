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

import aiocron

from tinydb import Query

from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest, RetryAfter

from obot import bot, dp, db, cache
from obot.utils.message import get_args
from obot.utils.api_client import api
from obot.utils.strings import get_strings


db_subscribes = db.table('subscribes')


@dp.message_handler(commands='subscriptionhelp', is_chat_admin=True)
@dp.message_handler(lambda a: a.chat.type == 'private', commands='subscriptionhelp')
async def subscribed_cmd(message: Message, strings={}):
    await message.reply(strings['subscriptionhelp'])


@dp.message_handler(commands='subscribed', is_chat_admin=True)
@dp.message_handler(lambda a: a.chat.type == 'private', commands='subscribed')
@dp.channel_post_handler(regexp='[!/]subscribed')
async def subscribed_cmd(message: Message, strings={}):
    chat_id = message.chat.id
    text = strings['subscribed_title']
    query = Query()
    for item in db_subscribes.search(query.chat_id == chat_id):
        text += f"\n  - {item['codename']} (<code>{item['release_type']}</code>)"

    await message.reply(text)


@dp.message_handler(commands='subscribe', is_chat_admin=True)
@dp.message_handler(lambda a: a.chat.type == 'private', commands='subscribe')
@dp.channel_post_handler(regexp='[!/]subscribe')
async def subscribe_cmd(message: Message, strings={}):
    args = get_args(message)

    release_type = 'stable'
    chat_id = message.chat.id

    if len(args) < 1:
        await message.reply(strings['sub_not_enoff_args'])
        return
    elif len(args) > 1:
        release_type = args[1]

    if release_type not in ['stable', 'beta', 'any', 'all']:
        await message.reply(strings['sub_wrong_branch'])
        return

    codename = args[0]

    if codename not in await api.list_devices(only_codenames=True) and codename != 'any':
        await message.reply(strings['sub_wrong_device'])
        return

    query = Query()

    if codename != 'any':
        if db_subscribes.search(query.chat_id == chat_id and query.codename == 'any'):
            await message.reply(strings['sub_err'].format(codename=codename))
            return

    if db_subscribes.search(query.chat_id == chat_id and query.codename == codename):
        await message.reply(strings['sub_err'].format(codename=codename))
        return

    db_subscribes.insert({'chat_id': chat_id, 'codename': codename, 'release_type': release_type})
    await message.reply(strings['sub_done'].format(codename=codename, release_type=release_type))


@dp.message_handler(commands='unsubscribe', is_chat_admin=True)
@dp.message_handler(lambda a: a.chat.type == 'private', commands='unsubscribe')
@dp.channel_post_handler(regexp='[!/]unsubscribe')
async def unsubscribe_cmd(message: Message, strings={}):
    args = get_args(message)
    chat_id = message.chat.id

    if len(args) < 1:
        await message.reply(strings['unsub_not_enoff_args'])
        return

    codename = args[0]

    query = Query()

    check = db_subscribes.remove(query.chat_id == chat_id and query.codename == codename)
    if check:
        await message.reply(strings['unsub_done'].format(codename=codename))
    else:
        await message.reply(strings['unsub_err'])


@aiocron.crontab('* * * * *')
async def updates_fun():
    for item in db_subscribes.all():
        chat_id = item['chat_id']
        codename = item['codename']
        real_codename = codename
        release_type = item['release_type']

        if codename == 'any':
            last_release = await api.get_last_release(release_type=release_type)
            real_codename = last_release['codename']
        else:
            last_release = await api.get_device_release(codename, release_type=release_type)
        last_release_id = last_release['_id']

        if 'release_id' in item:
            release_id = item['release_id']
            if last_release_id == release_id:
                # No new updates
                continue

            # Update is detected
            if not (broadcast_num := await cache.get('broadcast_num')):
                await cache.set('broadcast_num', 0)
                await cache.expire('broadcast_num', 65)
                broadcast_num = 0
            if broadcast_num > 17:
                # Broadcast limit reached
                return

            await cache.increment('broadcast_num')

            device = await api.get_device(real_codename)

            strings = await get_strings(chat_id)
            text = strings['update_text'].format(
                fullname=device['fullname'],
                codename=device['codename'],
                version=last_release['version'],
                date=last_release['date'],
                release_type=strings[last_release['build_type']]
            )
            buttons = InlineKeyboardMarkup().add(InlineKeyboardButton(
                '⬇️ Download',
                url=last_release['url']
            ))
            try:
                if not await bot.send_message(chat_id, text, reply_markup=buttons):
                    continue
            except BadRequest:
                db_subscribes.remove(query.chat_id == chat_id)
            except RetryAfter:
                continue

        query = Query()
        db_subscribes.update(
            {'release_id': last_release_id},
            query.chat_id == chat_id and query.codename == codename
        )
