import datetime

from aiogram.types import (KeyboardButton, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from utils.utils import return_month


current_year = datetime.datetime.now().year

button_contacts = KeyboardButton(text='Контакты')
button_sign_up = KeyboardButton(text='Записаться')
button_cancel = KeyboardButton(text='Отменить запись')


def create_kb(adjust, *args, **kwargs) -> InlineKeyboardMarkup:
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


def create_inline_kb(adjust: list, *args, **kwargs) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    label_button: list[InlineKeyboardButton] = []

    if kwargs:
        for key, value in kwargs.items():
            buttons.append(InlineKeyboardButton(
                    text=key,
                    callback_data=value
                ))

    if args:
        for time in args[1]:
            buttons.append(InlineKeyboardButton(
                        text=time,
                        callback_data=time
            ))
        label_button.append(InlineKeyboardButton(
                    text=args[0],
                    callback_data=args[0]
        ))

    kb_builder.add(*label_button, *buttons)
    kb_builder.adjust(*adjust)
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
