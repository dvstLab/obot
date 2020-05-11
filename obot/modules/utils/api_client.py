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

import aiohttp
import ujson as json

from obot import cache

API_HOST = 'https://api.orangefox.download/v2/'
CACHE_EXPIRE = 300


async def send_request(api_method):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_HOST + api_method) as response:
            if response.status == 404:
                return 404

            text = await response.text()
            return text


async def cached_or_make_request(api_method):
    if cached := await cache.get(api_method):
        return json.loads(cached)

    data = await send_request(api_method)

    await cache.set(api_method, data)
    await cache.expire(api_method, CACHE_EXPIRE)

    if data == 404:
        return None

    return json.loads(data)


async def all_devices(only_codenames=False):
    api_method = 'device'

    if only_codenames:
        api_method += f'?only_codenames=True'

    data = await cached_or_make_request(api_method)

    return data


async def get_device(codename):
    api_method = f'device/{codename}'
    data = await cached_or_make_request(api_method)

    return data


async def get_all_oems():
    api_method = 'oem'
    data = await cached_or_make_request(api_method)

    return data


async def get_oem_devices(oem_name):
    api_method = f'oem/{oem_name}'
    data = await cached_or_make_request(api_method)

    return data


async def get_devices_with_releases(build_type=None, only_codenames=False):
    if build_type == 'any':
        build_type = None

    if not build_type:
        api_method = f'device/releases'
    else:
        api_method = f'device/releases/{build_type}'

    if only_codenames:
        api_method += f'?only_codenames=True'
    return await cached_or_make_request(api_method)


async def get_release(codename, version, build_type=None):
    if not build_type:
        api_method = f'device/{codename}/releases/{version}'
    else:
        api_method = f'device/{codename}/releases/{build_type}/{version}'
    return await cached_or_make_request(api_method)


