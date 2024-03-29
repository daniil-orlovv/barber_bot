import os
import datetime
from typing import Union

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import location, TIME, PHONE, ADDRESS
from keyboards import (button_contacts, button_sign_up, button_cancel,
                       create_inline_kb, create_calendar)
from api import (get_free_date, get_free_time, get_free_services,
                 get_free_staff, create_session_api)
from utils import (check_date_for_staff, create_object_for_db,
                   check_free_services_for_staff, check_free_time_for_staff,
                   to_normalize_date)
from models import Base


current_year = datetime.datetime.now().year

engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5428/mydatabase")
session = Session(bind=engine)
Base.metadata.create_all(engine)

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
    accept_session = State()


data: dict[int, dict[str, Union[str, int, bool]]] = {}


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
    await state.update_data(all_staffs=free_staffs)
    adjust = (2, 2, 2)
    keyboard_inline = create_inline_kb(adjust, 'staff', **free_staffs)

    await message.answer(
        text='Выбери мастера:',
        reply_markup=keyboard_inline
    )
    await state.set_state(SignUpFSM.staff)


@dp.callback_query(
        lambda callback: callback.data.split('_')[0] in get_free_staff().values(),
        StateFilter(SignUpFSM.staff)
)
async def send_choose_service(
    callback: types.CallbackQuery,
    state: FSMContext
):
    staff_id = callback.data.split('_')[0]
    staff_name = callback.data.split('_')[1]
    print(f'{callback.from_user.full_name} выбрал мастера: {staff_name}')
    await state.update_data(staff_id=staff_id)
    await state.update_data(staff_name=staff_name)

    adjust = (2, 2, 2)
    free_services = get_free_services(staff_id)
    keyboard_services = create_inline_kb(adjust, 'service', **free_services)

    await callback.message.edit_text(
        text=(f"Ваш мастер: {staff_name}\n\n"
              f"Выбери услугу:"),
        reply_markup=keyboard_services
    )
    await state.set_state(SignUpFSM.service)


@dp.callback_query(
        StateFilter(SignUpFSM.service),
        lambda callback, state: check_free_services_for_staff(
            callback, state, get_free_services)
)
async def send_choose_date(callback: types.CallbackQuery, state: FSMContext):

    service_title = callback.data
    print(f'{callback.from_user.full_name} выбрал услугу: {service_title}')
    await state.update_data(service_title=service_title)
    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    staff_id = state_data['staff_id']

    free_days = get_free_date(staff_id)
    keyboard = create_calendar(free_days)

    await callback.message.edit_text(
        text=(f'Ваш мастер: {staff_name}\n'
              f'Ваша услуга: {service_title}\n\n'
              f'Выбери дату:'),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.date)


@dp.callback_query(
        StateFilter(SignUpFSM.date),
        lambda callback, state: check_date_for_staff(callback.data, state)
)
async def send_choosing_time(callback: types.CallbackQuery, state: FSMContext):

    print(f'{callback.from_user.full_name} выбрал дату: {callback.data}')
    await state.update_data(date=callback.data)
    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    staff_id = state_data['staff_id']
    service_title = state_data['service_title']
    data[callback.from_user.id] = await state.get_data()

    month, day = callback.data.split('-')
    date = f'{current_year}-{month}-{day}'
    norm_date = to_normalize_date(callback.data)
    adjust = (1, 4, 4, 4, 4, 4, 4)
    free_times = get_free_time(staff_id, date)
    params = [norm_date, free_times]
    keyboard_times = create_inline_kb(adjust, 'time', *params)

    await callback.message.edit_text(
        text=(f'Ваш мастер: {staff_name}\n'
              f'Ваша услуга {service_title}\n'
              f'Дата: {to_normalize_date(callback.data)}\n\n'
              f'Выбери время:'),
        reply_markup=keyboard_times
    )
    await state.set_state(SignUpFSM.time)


@dp.callback_query(
        StateFilter(SignUpFSM.time),
        lambda callback, state: check_free_time_for_staff(callback, state)
)
async def send_choise_of_user(
    callback: types.CallbackQuery,
    state: FSMContext
):

    print(f'{callback.from_user.full_name} выбрал время: {callback.data}')
    await state.update_data(time=callback.data)
    state_data = await state.get_data()
    staff_name = state_data['staff_name']
    service_title = state_data['service_title']
    date = state_data['date']
    print(f'Запись {callback.from_user.full_name}:\n'
          f'Мастер: {staff_name}\n'
          f'Услуга: {service_title}\n'
          f'Дата: {to_normalize_date(date)}\n\n'
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

    await callback.message.edit_text(
        text=(f'Ваш мастер: {staff_name}\n'
              f'Ваша услуга: {service_title}\n'
              f'Дата: {to_normalize_date(date)}\n'
              f'Время: {callback.data}\n\n'
              f'Все верно?'),
        reply_markup=keyboard
    )
    await state.set_state(SignUpFSM.check_data)


@dp.callback_query(StateFilter(SignUpFSM.check_data),
                   lambda callback: callback.data == 'cancel')
async def process_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Вы отменили процесс записи.'
    )
    await state.clear()


@dp.callback_query(StateFilter(SignUpFSM.check_data),
                   lambda callback: callback.data == 'accept')
async def process_accept(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text='Спасибо, теперь введите свое имя:')
    id_message = callback.message.message_id
    await state.update_data(id_message=id_message)
    data[callback.from_user.id] = await state.get_data()
    await state.set_state(SignUpFSM.name)


@dp.message(StateFilter(SignUpFSM.name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='А теперь введите ваш телефон в формате 79000000000:')

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.phone)


@dp.message(StateFilter(SignUpFSM.phone))
async def process_phone_sent(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='Введите ваш email в формате mail@mail.ru:')

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.email)


@dp.message(StateFilter(SignUpFSM.email))
async def process_email_sent(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    sent_message = await message.answer(
        text='Возможно, есть какие-то комментарии, укажите их:')

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    await state.set_state(SignUpFSM.comment)


@dp.message(StateFilter(SignUpFSM.comment))
async def create_session(message: Message, state: FSMContext):

    adjust = (2, 2)
    params = {'Подтвердить': 'accept',
              'Отменить': 'cancel'}
    keyboard = create_inline_kb(adjust, 'simple', **params)

    state_data = await state.get_data()
    message_id = state_data['id_message']
    await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
    await message.delete()

    await state.update_data(comment=message.text)
    sent_message = await message.answer(
        text='Спасибо!\n\n Создать запись на сеанс?',
        reply_markup=keyboard)

    sent_message_id = sent_message.message_id
    await state.update_data(id_message=sent_message_id)

    data[message.from_user.id] = await state.get_data()
    await state.set_state(SignUpFSM.accept_session)


@dp.callback_query(StateFilter(SignUpFSM.accept_session),
                   lambda callback: callback.data == 'accept')
async def accept_session(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()

    data_for_request = await state.get_data()
    await create_session_api(data_for_request)

    data_for_db = create_object_for_db(data_for_request)
    session.add(data_for_db)
    session.commit()

    await callback.answer(text='Запись создана!\n\n')
    await state.clear()


@dp.message(F.text == 'Отменить запись')
async def command_cancel(message: Message, state: FSMContext):
    await message.answer(
        text='Запись отменена!\n\nВыбери дейстие:',
        reply_markup=keyboard
    )
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)
