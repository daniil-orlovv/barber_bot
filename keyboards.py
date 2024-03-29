import datetime

from aiogram.types import (KeyboardButton, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import return_month


current_year = datetime.datetime.now().year

button_contacts = KeyboardButton(text='Контакты')
button_sign_up = KeyboardButton(text='Записаться')
button_cancel = KeyboardButton(text='Отменить запись')


def create_inline_kb(adjust, type, *args, **kwargs):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    label_button: list[InlineKeyboardButton] = []

    if type == 'simple':
        if kwargs:
            for name, callback_data in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=name,
                    callback_data=callback_data
                ))

    if type == 'time':
        if args:
            for time in args[1]:
                buttons.append(InlineKeyboardButton(
                            text=time,
                            callback_data=f'{time}'
                ))
            label_button.append(InlineKeyboardButton(
                        text=args[0],
                        callback_data=args[0]
            ))

    if type == 'service':

        if kwargs:
            for service_title, service_id in kwargs.items():
                buttons.append(InlineKeyboardButton(
                            text=service_title,
                            callback_data=f'{service_title}'
                ))

    if type == 'staff':

        if kwargs:
            print(kwargs)
            for staff_name, staff_id in kwargs.items():
                buttons.append(InlineKeyboardButton(
                            text=staff_name,
                            callback_data=f'{staff_id}_{staff_name}'
                ))
    print(buttons)
    kb_builder.add(*label_button, *buttons)
    kb_builder.adjust(*adjust)
    return kb_builder.as_markup(resize_keyboard=True)


def create_calendar(kwargs):
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
