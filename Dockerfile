# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV TZ="Europe/Moscow"

WORKDIR /server

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "server.py"]