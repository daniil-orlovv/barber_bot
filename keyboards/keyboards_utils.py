import datetime

from aiogram.types import (KeyboardButton, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from utils.utils import return_month


current_year = datetime.datetime.now().year

button_contacts = KeyboardButton(text='Контакты')
button_sign_up = KeyboardButton(text='Записаться')
button_cancel = KeyboardButton(text='Отменить запись')


def create_kb(adjust: list, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons: list[KeyboardButton] = []

    if kwargs:
        for key, value in kwargs.items():
            buttons.append(KeyboardButton(
                    text=key,
                    callback_data=value
                ))
    if args:
        for item in args:
            buttons.append(KeyboardButton(
                text=item
            ))
    kb_builder.add(*buttons)
    kb_builder.adjust(*adjust)
    return kb_builder.as_markup(resize_keyboard=True)


def create_inline_kb(method_kb, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if kwargs:
        print('kwargs: {kwargs}')

        for key, value in kwargs.items():
            print(key, value)
            if value.startswith('https'):
                buttons.append(InlineKeyboardButton(
                    text=key,
                    url=value
                ))
            else:
                buttons.append(InlineKeyboardButton(
                        text=key,
                        callback_data=str(value)
                    ))

    if args:
        for value in args:
            buttons.append(InlineKeyboardButton(
                        text=f'{value}',
                        callback_data=f'{value}'
            ))

    kb_builder.add(*buttons)
    kb_builder.adjust(*method_kb)
    return kb_builder.as_markup(resize_keyboard=True)


def create_calendar(kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons_for_months: list[list[InlineKeyboardButton]] = []
    buttons_for_days: list[list[InlineKeyboardButton]] = []

    for key, values in kwargs.items():

        buttons_months = []
        label_month = return_month(key)
        buttons_months.append(InlineKeyboardButton(
            text=label_month,
            callback_data=label_month
            ))

        buttons_days = []
        for value in values:
            buttons_days.append(InlineKeyboardButton(
                text=value,
                callback_data=f'{key}-{value}'
            ))
        buttons_for_months.append(buttons_months)
        buttons_for_days.append(buttons_days)

    for month, days in zip(buttons_for_months, buttons_for_days):
        kb_builder.row(*month, width=1)
        kb_builder.row(*days, width=7)

    return kb_builder.as_markup()
