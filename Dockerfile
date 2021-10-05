FROM python:3.9
FROM gorialis/discord.py

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /app/

CMD [ "python", "main.py" ]