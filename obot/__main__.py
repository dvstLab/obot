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

from aiogram import executor
from importlib import import_module

from obot.utils.logger import log
from obot import dp


import_module("obot.modules.official_chats")
import_module("obot.modules.pm")


log.info("Starting bot..")

executor.start_polling(dp, skip_updates=True)