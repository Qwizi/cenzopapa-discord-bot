FROM gorialis/discord.py

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get install ca-certificates
RUN update-ca-certificates
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip
COPY . /app/

CMD [ "python", "bot.py" ]