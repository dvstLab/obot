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


def get_cmd(message) -> str:
    cmd = message.text.lower().split()[0][1:].split('@')[0]
    return cmd


def get_args(message) -> list:
    args = message.get_args()
    if not args:
        return []
    return args.lower().split(' ')
