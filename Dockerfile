FROM python:3.10

RUN mkdir /currency_converter_bot

WORKDIR /currency_converter_bot

RUN pip install aiogram==2.25.1

COPY . /currency_converter_bot/
