FROM python:3.8-alpine

RUN apk add gcc musl-dev libffi-dev openssl openssl-dev build-base
#RUN pip install cython

ADD requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

RUN apk del gcc build-base zlib

ADD obot/ /opt/obot/obot
WORKDIR /opt/obot/

ENV PRODUCTION=true

# start app
CMD [ "python3", "-m", "obot" ]