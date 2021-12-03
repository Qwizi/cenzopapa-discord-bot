FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip  \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip
COPY . /app/