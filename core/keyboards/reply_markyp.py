from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import KeyboardBuilder, KeyboardButton, ReplyKeyboardBuilder
from core.helpers.constant import *


def main_meny():
    builder = KeyboardBuilder(KeyboardButton)
    builder.add(
        *[
            KeyboardButton(text=WEATHER),
            KeyboardButton(text=BOOK),
            KeyboardButton(text=WEB_APP),

        ]
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def weather():
    builder = ReplyKeyboardBuilder()
    builder.button(text=CURRENT_WEATHER)
    builder.button(text=WEATHER_ALARM)
    builder.button(text=TOMORROW_WEATHER)
    builder.button(text=FORECAST_10)
    builder.button(text=BACK_TO)
    builder.adjust(1, 3, )
    return builder.as_markup(resize_keyboard=True)


def weather_alarm():
    builder = ReplyKeyboardBuilder()
    builder.button(text=WEATHER_TODAY)
    builder.button(text=WEATHER_THREE_DAY)
    builder.button(text=BACK)
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def weather_ring():
    builder = ReplyKeyboardBuilder()
    builder.button(text=WEATHER_EVERY_ALARM)
    builder.button(text=WEATHER_BY_DAY)
    builder.button(text=BACK)
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def weather_by_day():
    bulder = ReplyKeyboardBuilder()
    bulder.button(text=Monday)
    bulder.button(text=Tuesday)
    bulder.button(text=Wednesday)
    bulder.button(text=Thursday)
    bulder.button(text=Friday)
    bulder.button(text=Saturday)
    bulder.button(text=Sunday)
    bulder.adjust(3, 2)
    return bulder.as_markup(resize_keyboard=True)


def weather_date():
    builder = ReplyKeyboardBuilder()
    for index in range(24):
        if index >= 10:
            builder.button(text=f'{index}:00')
            continue
        builder.button(text=f'0{index}:00')
    builder.button(text=BACK)
    builder.adjust(5, 5)
    return builder.as_markup(resize_keyboard=True)


def book():
    builder = ReplyKeyboardBuilder()
    builder.button(text=BOOK_OF_SEARCH)
    builder.button(text=BOOK_OF_SEARCH_TEXT)
    builder.adjust(1, 1)
    return builder.as_markup()
