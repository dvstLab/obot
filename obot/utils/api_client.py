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

from orangefoxapi import OrangeFoxAPI
import ujson as json

from obot import cache

#API_HOST = 'https://api.orangefox.download/v2/'
#API_HOST = 'http://127.0.0.1:5000'
SSL = False


api = OrangeFoxAPI(
    cache=cache,
    json=json
)