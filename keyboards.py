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

    if type == 'date':
        named_month = return_month(args[0])

        if args:
            month_number, days = args
            for day in days:
                buttons.append(InlineKeyboardButton(
                    text=day,
                    callback_data=f'{month_number}-{day}'
                ))
        label_button.append(InlineKeyboardButton(
                    text=named_month,
                    callback_data=named_month
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
                            callback_data=f'{service_id}'
                ))

    if type == 'staff':

        if kwargs:
            print(kwargs)
            for staff_name, staff_id in kwargs.items():
                buttons.append(InlineKeyboardButton(
                            text=staff_name,
                            callback_data=f'{staff_id}'
                ))
    print(buttons)
    kb_builder.add(*label_button, *buttons)
    kb_builder.adjust(*adjust)
    return kb_builder.as_markup(resize_keyboard=True)
