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

import json
from importlib import import_module

from aiocache import caches
from aiogram import Bot, Dispatcher, types
from aiogram.bot.base import TelegramAPIServer
from orangefoxapi import OrangeFoxAsyncAPI
from tinydb import TinyDB

VERSION = 'v5.0'

print("---------------------------------")
print(f"| OrangeFox Recovery bot - {VERSION} |")
print("---------------------------------")

CONFIG = json.load(open('data/config.json', "r"))

TOKEN: str = CONFIG['TOKEN']
OWNER_ID: int = CONFIG['OWNER_ID']

api_server = TelegramAPIServer.from_base(CONFIG['BOTAPI'])
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML, server=api_server)
dp = Dispatcher(bot)

print("Enabling databases...")
path: str = CONFIG['DB_PATH']

db = TinyDB(CONFIG['DB_PATH'])

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

api = OrangeFoxAsyncAPI(
    cache_class=cache
)

import_module('obot.filters')
import_module('obot.handlers')
import_module('obot.middlewares')
