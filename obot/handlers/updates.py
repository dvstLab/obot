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

import re
from asyncio import sleep
from string import Template

import aiocron
from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest, RetryAfter
from tinydb import Query

from obot import bot, dp, db, cache, api
from obot.utils.devices import get_codenames, release_info, get_device_names
from obot.utils.message import get_args, need_args
from obot.utils.strings import get_strings

db_subscribes = db.table('subscribes')


@dp.message_handler(commands='subscriptionhelp', chat_type='private')
@dp.message_handler(commands='subscriptionhelp', is_chat_admin=True)
@dp.channel_post_handler(regexp=re.compile(r'^/subscriptionhelp'))
async def subscribed_cmd(message: Message, strings={}):
    await message.reply(strings['subscriptionhelp'])


@dp.message_handler(commands='subscribed', chat_type='private')
@dp.message_handler(commands='subscribed', is_chat_admin=True)
@dp.channel_post_handler(regexp=re.compile(r'^/subscribed'))
async def subscribed_cmd(message: Message, strings={}):
    chat_id = message.chat.id
    text = strings['subscribed_title']

    query = Query()
    if not (subscribed := db_subscribes.search(query.chat_id == chat_id)):
        return await message.reply(strings['not_subscribed'])

    device_names = await get_device_names()

    for item in subscribed:
        device_id = item['device_id']
        device_name = device_names[device_id] if device_id else strings['all']
        release_type = strings[item['release_type'] or 'any']
        text += f" - {device_name} [<code>{release_type}</code>]\n"

    await message.reply(text)


@dp.message_handler(commands='subscribe', chat_type='private')
@dp.message_handler(commands='subscribe', is_chat_admin=True)
@dp.channel_post_handler(regexp=re.compile(r'^/subscribe'))
@need_args(1)
async def subscribe_cmd(message: Message, strings={}, **kwargs):
    chat_id = message.chat.id
    device_id = None

    if (codename := (args := get_args(message))[0]) in ['any', 'all']:
        codename = None

    # Get release type
    release_type = args[1] if len(args) > 1 else None
    if release_type in ['any', 'all'] or not release_type:
        release_type = None
    elif release_type not in ['stable', 'beta']:
        return await message.reply(strings['sub_wrong_branch'])

    # Get already subscribed
    query = Query()
    subscribed = db_subscribes.search(query.chat_id == chat_id)

    if any([not x['device_id'] for x in subscribed]):
        return await message.reply(strings['subscribed_all_already'])

    # Checks
    if codename:
        if codename not in await get_codenames(release_type=None):
            await message.reply(strings['sub_wrong_device'])
            return

        # Get device
        device = await api.device(codename=codename)
        device_id = device.id

        # Check
        if any([device.id in x['device_id'] for x in subscribed]):
            text = Template(strings['subscribed_device']).substitute(
                device_name=device.full_name,
                codename=device.codename
            )
            return await message.reply(text)
    else:
        # Check if there is no other subscribed devices
        if subscribed:
            return await message.reply(strings['subscribed_devices'])

    db_subscribes.upsert(
        {'chat_id': chat_id, 'device_id': device_id, 'release_type': release_type},
        (query.chat_id == chat_id) & (query.device_id == device_id)
    )

    text = Template(strings['sub_done']).substitute(
        codename=codename or 'any',
        release_type=release_type or 'all'
    )
    await message.reply(text)


@dp.message_handler(commands='unsubscribe', chat_type='private')
@dp.message_handler(commands='unsubscribe', is_chat_admin=True)
@dp.channel_post_handler(regexp=re.compile(r'^/unsubscribe'))
@need_args(1)
async def unsubscribe_cmd(message: Message, strings={}, **kwargs):
    query = Query()
    chat_id = message.chat.id

    if (codename := (args := get_args(message))[0]) in ['any', 'all']:
        codename = None
        device_id = None
    else:
        if codename not in await get_codenames(release_type=None):
            await message.reply(strings['sub_wrong_device'])
            return

        # Get device
        device = await api.device(codename=codename)
        device_id = device.id

    check = db_subscribes.remove((query.chat_id == chat_id) & (query.device_id == device_id))
    if check:
        text = Template(strings['unsub_done']).substitute(codename=codename or 'any')
        await message.reply(text)
    else:
        await message.reply(strings['unsub_err'])


@aiocron.crontab('* * * * *')
async def updates_fun():
    for item in db_subscribes.all():
        query = Query()

        chat_id = item['chat_id']
        device_id = item['device_id']
        release_type = item['release_type']

        # Just write last ID
        if not (last_known_id := item.get('last_known_id', None)):
            if not (releases := (await api.releases(device_id=device_id, type=release_type)).data):
                print(f'There is no release! {device_id=} | {release_type=}')
                return
            release = releases[0]
            db_subscribes.update(
                {'last_known_id': release.id},
                (query.chat_id == chat_id) & (query.device_id == device_id)
            )
            return

        for update in await api.updates(last_known_id, release_type=release_type, device_id=device_id):
            release_id = update.id
            if last_known_id == release_id:
                # No new updates
                continue

            if not (broadcast_num := await cache.get('broadcast_num')):
                await cache.set('broadcast_num', 0)
                await cache.expire('broadcast_num', 65)
                broadcast_num = 0
            if broadcast_num > 17:
                await sleep(65)
                await cache.set('broadcast_num', 0)
                # return  # Broadcast limit reached
            await cache.increment('broadcast_num')

            strings = await get_strings(chat_id)

            # Get full info
            device = await api.device(id=update.device_id)
            release = await api.release(id=update.id)

            text, buttons = await release_info(strings, release, device=device)

            try:
                await bot.send_message(chat_id, text, reply_markup=buttons, disable_web_page_preview=True)
            except BadRequest:
                db_subscribes.remove(query.chat_id == chat_id)
            except RetryAfter:
                # Ratelimit reached
                await cache.set('broadcast_num', 20)
                continue

            db_subscribes.update(
                {'last_known_id': update.id},
                (query.chat_id == chat_id) & (query.device_id == device_id)
            )
