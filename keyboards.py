import datetime

from aiogram.types import (KeyboardButton, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

LEXICON: dict[str, str] = {
    'btn_1': 'Кнопка 1'}


current_year = datetime.datetime.now().year

button_contacts = KeyboardButton(text='Контакты')
button_sign_up = KeyboardButton(text='Записаться')

times = (
    '10:00', '11:00', '15:00'
)

url_button = InlineKeyboardButton(
    text='Записаться на сеанс',
    url='https://n793568.yclients.com/company/304080/menu?o=m2024364'
)


def create_keyboards(width, *args):
    kb_builder = ReplyKeyboardBuilder()
    buttons = []
    for i in args:
        buttons.append(KeyboardButton(text=i))

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)


def return_month(value):
    months_key = {
        '1': 'Января', '2': 'Февраля', '3': 'Марта', '4': 'Апреля', '5': 'Мая',
        '6': 'Июня', '7': 'Июля', '8': 'Августа', '9': 'Сентября',
        '10': 'Октября', '11': 'Ноября', '12': 'Декабря'
    }
    return months_key.get(value)


def create_inline_kb(adjust, type, *args, **kwargs):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    label_button: list[InlineKeyboardButton] = []

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
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button))

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
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button))

    if type == 'service':

        if args:
            for service in args:
                buttons.append(InlineKeyboardButton(
                            text=service,
                            callback_data=f'{service}'
                ))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button))

    if type == 'staff':

        if args:
            for staff in args:
                buttons.append(InlineKeyboardButton(
                            text=staff,
                            callback_data=f'{staff}'
                ))

        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button))

    kb_builder.add(*label_button, *buttons)
    kb_builder.adjust(*adjust)
    return kb_builder.as_markup(resize_keyboard=True)
