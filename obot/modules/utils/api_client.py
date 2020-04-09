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

API_HOST = 'https://api.orangefox.tech/'
CACHE_EXPIRE = 300


async def send_request(api_method):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_HOST + api_method) as response:
            text = await response.text()
            return text


async def cached_or_make_request(api_method):
    if cached := await cache.get(api_method):
        return json.loads(cached)

    data = await send_request(api_method)

    await cache.set(api_method, data)
    await cache.expire(api_method, CACHE_EXPIRE)

    return json.loads(data)


async def all_codenames():
    api_method = 'all_codenames/'
    data = await cached_or_make_request(api_method)

    return data


async def list_devices():
    api_method = 'list_devices/'
    data = await cached_or_make_request(api_method)

    return data


async def available_releases():
    api_method = 'available_releases/'
    data = await cached_or_make_request(api_method)

    return data


async def available_stable_releases():
    api_method = 'available_stable_releases/'
    data = await cached_or_make_request(api_method)

    return data


async def available_beta_releases():
    api_method = 'available_beta_releases/'
    data = await cached_or_make_request(api_method)

    return data


async def details(codename):
    api_method = f'details/{codename}/'
    data = await cached_or_make_request(api_method)

    return data


async def last_release(codename):
    api_method = f'last_release/{codename}/'
    data = await cached_or_make_request(api_method)

    return data


async def last_stable_release(codename):
    api_method = f'last_stable_release/{codename}/'
    data = await cached_or_make_request(api_method)

    return data


async def last_beta_release(codename):
    api_method = f'last_beta_release/{codename}/'
    data = await cached_or_make_request(api_method)

    return data
