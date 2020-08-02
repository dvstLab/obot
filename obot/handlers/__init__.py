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

from importlib import import_module
from obot.middlewares import __setup__ as middlewares
from obot.filters import __setup__ as filters


def __setup__(dp):
    filters(dp)
    middlewares(dp)

    # ['inline', 'official_chats', 'other_chats', 'pm', 'releases']

    for module_name in ['pm', 'updates', 'releases', 'other_chats', 'inline']:
        import_module('obot.handlers.' + module_name)

