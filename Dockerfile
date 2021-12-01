FROM python:3.9-alpine

WORKDIR /app
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip install https://github.com/Qwizi/cenzopapa-sdk/archive/refs/tags/v1.0.2.tar.gz
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip
COPY . /app/

CMD [ "python", "bot.py" ]