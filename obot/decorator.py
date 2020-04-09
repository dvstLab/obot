# Copyright (C) 2019 The Raphielscape Company LLC.
# Copyright (C) 2018 - 2020 MrYacha
# Copyright (C) 2018 - 2020 Sophie
# Copyright (C) 2020 oAPI
# Copyright (C) 2020 oBOT
#
# This file is part of oBOT.
#
# oBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

from aiogram.dispatcher.handler import SkipHandler

from obot import BOT_USERNAME, dp
from obot.utils.logger import log


# from sentry_sdk import configure_scope


def register(*args, cmd=None, f=None, allow_edited=True, allow_kwargs=False, add_cmd_start_symbols='!', **kwargs):
    register_kwargs = {}
    if cmd:
        regex = f'\A^[/{add_cmd_start_symbols}]('
        regex += cmd

        if 'disable_args' in kwargs:
            del kwargs['disable_args']
            regex += f")($|@{BOT_USERNAME}$)"
        else:
            regex += f")(|@{BOT_USERNAME})(:? |$)"

        register_kwargs['regexp'] = regex

    log.debug(f"Registred new handler: <d><n>{str(register_kwargs)}</></>")

    register_kwargs.update(kwargs)

    def decorator(func):
        async def new_func(*def_args, **def_kwargs):
            message = def_args[0]

            if allow_kwargs is False:
                def_kwargs = dict()

            # Sentry
            # with configure_scope() as scope:
            #    scope.set_extra("update", str(message))

            await func(*def_args, **def_kwargs)
            raise SkipHandler()

        dp.register_message_handler(new_func, *args, **register_kwargs)
        if allow_edited is True:
            dp.register_edited_message_handler(new_func, *args, **register_kwargs)

    return decorator
