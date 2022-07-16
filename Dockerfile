# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

ENV ACCESS_TOKEN=${ACCESS_TOKEN}
ENV LOGS_FOLDER=${LOGS_FOLDER}
ENV STAGE=${STAGE}
ENV HOST=${HOST}
ENV PORT=${PORT}

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE ${PORT}

ENTRYPOINT [ "python", "application.py"]
