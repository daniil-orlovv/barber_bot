from aiogram.types import (KeyboardButton, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

LEXICON: dict[str, str] = {
    'btn_1': 'Кнопка 1'}


button_contacts = KeyboardButton(text='Контакты')
button_sign_up = KeyboardButton(text='Записаться')
digital_of_month = (
    '1', '2', '3', '4', '5', '6', '7',
    '8', '9', '10', '11', '12', '13', '14',
    '15', '16', '17', '18', '19', '20', '21',
    '22', '23', '24', '25', '26', '27', '28',
    '29', '30', '31'
)

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
        '1': 'Январь', '2': 'Февраль', '3': 'Март', '4': 'Апрель', '5': 'Май',
        '6': 'Июнь', '7': 'Июль', '8': 'Август', '9': 'Сентябрь',
        '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'
    }
    return months_key.get(value)


def create_inline_kb(adjust, type, *args, **kwargs):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    label_button: list[InlineKeyboardButton] = []

    if type == 'date':
        named_month = return_month(args[0])

        if args:
            for day in args[1]:
                buttons.append(InlineKeyboardButton(
                            text=day,
                            callback_data=f"{args[0]}_{day}"
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
                            callback_data=time
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

    kb_builder.add(*label_button, *buttons)
    kb_builder.adjust(*adjust)
    kb = kb_builder.as_markup(resize_keyboard=True)
    print(kb)
    return kb_builder.as_markup(resize_keyboard=True)
