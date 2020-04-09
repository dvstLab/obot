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

from importlib import import_module

from aiogram import executor

from obot import dp
from obot.utils.logger import log

import_module("obot.modules.official_chats")
import_module("obot.modules.pm")
import_module("obot.modules.inline")

log.info("Starting bot..")

executor.start_polling(dp, skip_updates=True)
