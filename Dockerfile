# Copyright (C) 2018 - 2020 MrYacha.
# Copyright (C) 2019 - 2020 Sophie.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file is part of oBot.

# Build image
FROM python:3-slim AS compile-image

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN apt-get install -y git

COPY requirements.txt .
RUN pip install --user -r requirements.txt


# Run image
FROM python:3-alpine AS run-image

RUN apk add libstdc++
RUN apk add tzdata
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

ADD . /obot
RUN rm -rf /obot/data/
WORKDIR /obot

ENV PRODUCTION=true

CMD [ "python", "-m", "obot" ]
