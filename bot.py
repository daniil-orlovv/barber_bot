import os
from typing import Union

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from config import location, TIME, PHONE, ADDRESS
from keyboards import (button_contacts, button_sign_up, button_cancel,
                       url_button, create_inline_kb, current_year,
                       return_month)
from api import get_free_date, get_free_time, get_free_services, get_free_staff
from utils import check_date

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN', default='bot_token')

storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)
keyboard = ReplyKeyboardMarkup(keyboard=[[button_contacts, button_sign_up],
                                         [button_cancel]],
                               resize_keyboard=True)


class SignUpFSM(StatesGroup):
    staff = State()
    service = State()
    date = State()
    time = State()
    check_data = State()
    name = State()
    phone = State()
    email = State()
    comment = State()


data: dict[int, dict[str, Union[str, int, bool]]] = {}


sigh_up_keyboard = InlineKeyboardMarkup(inline_keyboard=[[url_button]])


# Этот хэндлер будет срабатывать на команду '/start'
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(
        text='Привет!\nЯ бот Максуда!'
             '\nДавай запишу тебя на стрижку!',
        reply_markup=keyboard
    )


@dp.message(F.text == 'Контакты')
async def command_contacts(message: Message):
    await message.answer_location(
        location.latitude,
        location.longitude
    )
    await message.answer(f'{ADDRESS}\n{TIME}\n{PHONE}')


@dp.message(StateFilter(default_state),
            F.text == 'Записаться')
async def command_sign_up(message: Message, state: FSMContext):

    free_staffs = get_free_staff()
    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, 'staff', *free_staffs)

    await message.answer(
        text='Выбери мастера:',
        reply_markup=keyboard_inline
    )
    await state.set_state(SignUpFSM.staff)


@dp.callback_query(
        lambda callback: callback.data in get_free_staff(),
        StateFilter(SignUpFSM.staff)
)
async def send_choose_service(
    callback: types.CallbackQuery,
    state: FSMContext
):

    print(f'{callback.from_user.full_name} выбрал мастера: {callback.data}')
    await state.update_data(staff=callback.data)

    adjust = (2, 2, 2)
    free_services = get_free_services()
    keyboard_services = create_inline_kb(adjust, 'service', *free_services)

    await callback.message.answer(
        text=(f"Ваш мастер: {callback.data}\n\n"
              f"Выбери услугу:"),
        reply_markup=keyboard_services
    )
    await state.set_state(SignUpFSM.service)


@dp.callback_query(
        StateFilter(SignUpFSM.service),
        lambda callback: callback.data in get_free_services()
)
async def send_choose_date(callback: types.CallbackQuery, state: FSMContext):

    print(f'{callback.from_user.full_name} выбрал услугу: {callback.data}')
    await state.update_data(service=callback.data)
    state_data = await state.get_data()
    staff = state_data['staff']

    await callback.message.answer(
        text=(f'Ваш мастер: {staff}\n'
              f'Ваша услуга: {callback.data}\n\n'
              f'Выбери дату:')
    )

    free_days = get_free_date()
    adjust = (1, 7, 7, 7, 7, 7)
    for i in range(0, len(free_days)):
        month_number = str(list(free_days.keys())[i])
        days = free_days.get(month_number)
        params = (month_number, days)
        keyboard_date = create_inline_kb(adjust, 'date', *params)

        await callback.message.answer(
            text='Выбери дату:',
            reply_markup=keyboard_date
        )
        await state.set_state(SignUpFSM.date)


@dp.callback_query(
        StateFilter(SignUpFSM.date),
        lambda callback: check_date(callback.data)
)
async def send_choose_time(callback: types.CallbackQuery, state: FSMContext):

    print(f'{callback.from_user.full_name} выбрал дату: {callback.data}')
    await state.update_data(date=callback.data)
    state_data = await state.get_data()
    staff = state_data['staff']
    service = state_data['service']
    data[callback.from_user.id] = await state.get_data()

    month, day = callback.data.split('-')
    date = f'{current_year}-{month}-{day}'
    adjust = (1, 4, 4, 4, 4, 4, 4)
    free_times = get_free_time(date)
    params = [date, free_times]
    keyboard_times = create_inline_kb(adjust, 'time', *params)

    await callback.message.answer(
        text=(f'Ваш мастер: {staff}\n'
              f'Ваша услуга {service}\n'
              f'Дата: {callback.data}\n\n'
              f'Выбери время:'),
        reply_markup=keyboard_times
    )
    await state.set_state(SignUpFSM.time)


@dp.callback_query(
        StateFilter(SignUpFSM.time),
        lambda callback: callback.data in get_free_time(
            f'{current_year}-{data[callback.from_user.id]["date"]}')
)
async def send_choise_of_user(
    callback: types.CallbackQuery,
    state: FSMContext
):

    print(f'{callback.from_user.full_name} выбрал время: {callback.data}')
    await state.update_data(time=callback.data)
    state_data = await state.get_data()
    staff = state_data['staff']
    service = state_data['service']
    date = state_data['date']
    norm_date = date.split('-')[::-1]
    print(f'Запись {callback.from_user.full_name}:\n'
          f'Мастер: {staff}\n'
          f'Услуга: {service}\n'
          f'Дата: {norm_date[0]} {return_month(norm_date[1])} {current_year}\n\n'
          f'Время: {callback.data}')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Подтвердить',
                    callback_data='accept'
                    ),
                InlineKeyboardButton(
                    text='Отменить',
                    callback_data='cancel'
                    )
            ],
            [
                InlineKeyboardButton(
                    text='Изменить',
                    callback_data='edit'
                    )
            ]
        ]
    )

    await callback.message.answer(
        text=(f'Ваш мастер: {staff}\n'
              f'Ваша услуга: {service}\n'
              f'Дата: {norm_date[0]} {return_month(norm_date[1])} {current_year}\n'
              f'Время: {callback.data}\n\n'
              f'Все верно?'),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.check_data)


@dp.callback_query(lambda callback: callback.data == 'cancel',
                   StateFilter(SignUpFSM.check_data))
async def process_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Вы отменили процесс записи.'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@dp.callback_query(lambda callback: callback.data == 'accept',
                   StateFilter(SignUpFSM.check_data))
async def process_accept(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer(
        text='Спасибо, теперь введите свое имя:')
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    data[callback.from_user.id] = await state.get_data()
    print(data[callback.from_user.id])
    await state.set_state(SignUpFSM.name)


@dp.message(StateFilter(SignUpFSM.name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text='А теперь введите ваш телефон в формате +7 777 777-77-77:')
    await state.set_state(SignUpFSM.phone)


@dp.message(StateFilter(SignUpFSM.phone))
async def process_phone_sent(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(text='Введите ваш email в формате mail@mail.ru:')
    await state.set_state(SignUpFSM.email)


@dp.message(StateFilter(SignUpFSM.email))
async def process_email_sent(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(text='Возможно, есть какие-то комментарии, укажите их:')
    await state.set_state(SignUpFSM.comment)


@dp.message(StateFilter(SignUpFSM.comment))
async def process_comment_sent(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer(text='Спасибо!')

    data[message.from_user.id] = await state.get_data()
    await state.clear()
    print(data)


@dp.message(F.text == 'Отменить запись')
async def command_cancel(message: Message, state: FSMContext):
    await message.answer(
        text='Запись отменена!\n\nВыбери дейстие:',
        reply_markup=keyboard
    )
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)
