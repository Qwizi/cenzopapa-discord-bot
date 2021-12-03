FROM arm32v7/python
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip
COPY . /app/