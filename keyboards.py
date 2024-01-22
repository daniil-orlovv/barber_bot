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


def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


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


def create_calendar_kb(adjust, month, days):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    months: list[InlineKeyboardButton] = []

    named_month = return_month(month)

    for day in days:
        buttons.append(InlineKeyboardButton(
                    text=day,
                    callback_data=day
        ))
    months.append(InlineKeyboardButton(
                text=named_month,
                callback_data=named_month
    ))

    kb_builder.add(*months, *buttons)
    kb_builder.adjust(*adjust)
    return kb_builder.as_markup(resize_keyboard=True)
