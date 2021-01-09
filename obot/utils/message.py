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

from typing import Union

from aiogram.types import Message
from orangefoxapi.types import ReleaseType


def need_args(count: int):
    def wrapped(func):
        async def wrapped_inner(*args, **kwargs):
            message = args[0]
            if len(get_args(message)) < count:
                return await message.reply(f"Not enough arguments provided! Need: {count}")

            await func(*args, **kwargs)

        return wrapped_inner

    return wrapped


def get_cmd(message: Message) -> str:
    cmd = message.text.lower().split()[0][1:].split('@')[0]
    return cmd


def get_args(message: Message) -> list:
    args = message.get_args()
    if not args:
        return []
    return args.lower().split(' ')


def get_arg(message: Message) -> str:
    args = get_args(message)
    if len(args) > 0:
        return args[0]
    return None


def get_release_type(message: Message, arg=None, arg_num: int = 0) -> Union[ReleaseType, None]:
    if not arg:
        args = get_args(message)
        if len(args) - 1 < arg_num:
            arg = ''
        else:
            arg: str = args[arg_num].lower()

    if arg in ReleaseType.stable.value:
        return ReleaseType.stable
    elif arg in ReleaseType.beta.value:
        return ReleaseType.beta

    return None
