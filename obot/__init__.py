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

import os
import asyncio
import yaml

from tinydb import TinyDB

from aiocache import caches
from aiogram import Bot, Dispatcher, types


VERSION = 'v4'


print("------------------------------")
print("|   OrangeFox Recovery bot   |")
print("------------------------------")

CONFIG = yaml.load(open('data/config.yaml', "r"), Loader=yaml.Loader)

TOKEN = CONFIG['TOKEN']
OWNER_ID = CONFIG['OWNER_ID']

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

print("Enabling databases...")
path: str = CONFIG['DB_PATH']

db = TinyDB(CONFIG['DB_PATH'])

print("Enabling cache...")
if 'REDIS' in CONFIG:
    print("* Enabling redis cache")
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
    print("* Enabling simple memory cache")
    caches.set_config({
        'default': {
            'cache': "aiocache.SimpleMemoryCache",
            'serializer': {
                'class': "aiocache.serializers.StringSerializer"
            }
        }
    })

cache = caches.get('default')

print("Getting bot info...")
loop = asyncio.get_event_loop()
bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_ID = bot_info.id
