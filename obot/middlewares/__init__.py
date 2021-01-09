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

from obot import dp
from .strings import StringsMiddleware

# dp.middleware.setup(ChatMiddleware())
dp.middleware.setup(StringsMiddleware())
