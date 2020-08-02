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
import yaml

from babel.core import Locale


LANGUAGES = {}


for filename in os.listdir('obot/languages'):
    print('Loading language file ' + filename)
    with open('obot/languages/' + filename, "r", encoding='utf8') as f:
        lang = yaml.load(f, Loader=yaml.SafeLoader)

        lang_code = filename.split('.')[0]
        lang['babel'] = Locale.parse(lang_code, sep='-')

        LANGUAGES[lang_code] = lang

print("Languages loaded: {}".format([language['babel'].display_name for language in LANGUAGES.values()]))


async def get_chat_locale(chat_id: int) -> str:
    return 'en-US'


async def get_strings(chat_id):
    locale_name = await get_chat_locale(chat_id)
    return LANGUAGES[locale_name]
