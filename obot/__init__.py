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

import asyncio

from aiogram import Bot, Dispatcher, types
from aiocache import caches

from obot.utils.logger import log
from obot.utils.config import CONFIG


log.info("------------------------------")
log.info("|   OrangeFox Recovery bot   |")
log.info("------------------------------")

TOKEN = CONFIG['TOKEN']
OWNER_ID = CONFIG['OWNER_ID']

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

log.debug("Enabling cache...")
if 'REDIS' in CONFIG:
    log.debug("* Enabling redis cache")
    caches.set_config({
        'default': {
            'cache': "aiocache.RedisCache",
            'endpoint': CONFIG['REDIS']['URI'],
            'port': CONFIG['REDIS']['PORT'],
            'timeout': 1,
            'serializer': {
                'class': "aiocache.serializers.PickleSerializer"
            },
            'plugins': [
                {'class': "aiocache.plugins.HitMissRatioPlugin"},
                {'class': "aiocache.plugins.TimingPlugin"}
            ]
        }
    })
else:
    log.debug("* Enabling simple memory cache")
    caches.set_config({
        'default': {
            'cache': "aiocache.SimpleMemoryCache",
            'serializer': {
                'class': "aiocache.serializers.StringSerializer"
            }
        }
    })

cache = caches.get('default')


log.debug("Getting bot info...")
loop = asyncio.get_event_loop()
bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_ID = bot_info.id