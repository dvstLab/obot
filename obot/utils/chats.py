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

from obot import CONFIG


async def get_chat_holder(message) -> str:
    chat_id = message.chat.id

    if chat_id == message.from_user.id:
        return 'pm'

    if chat_id in CONFIG['CHATS']:
        return 'official'

    elif chat_id == CONFIG['STABLE_CHAT']:
        return 'stable'
    elif chat_id == CONFIG['BETA_CHAT']:
        return 'beta'

    return 'other'
